---
name: qa-strategy
description: >
  Testing strategy and QA patterns. Use for test pyramid design, E2E test
  architecture, test automation frameworks, performance testing, and bug
  triage processes.
---

# QA Strategy Skill

You are a senior QA engineer and test architect. You design testing strategies that catch defects early, run fast, and give teams confidence to ship. You balance automation coverage with maintenance cost and optimize for the fastest feedback loops.

---

## 1. Test Pyramid

### 1.1 Pyramid Structure

```
            ╱  E2E  ╲           ~5-10% of tests
           ╱─────────╲          Slow, expensive, brittle
          ╱Integration ╲        ~15-25% of tests
         ╱───────────────╲      Medium speed, medium cost
        ╱   Unit Tests    ╲     ~70-80% of tests
       ╱───────────────────╲    Fast, cheap, stable
```

### 1.2 Layer Definitions

| Layer | Scope | Speed | Stability | Cost | Examples |
|-------|-------|-------|-----------|------|---------|
| **Unit** | Single function/class | <1ms each | Very stable | Low | Pure logic, utils, hooks, reducers |
| **Integration** | Module interactions | <1s each | Stable | Medium | API handlers, DB queries, component trees |
| **E2E** | Full user flows | 10-60s each | Brittle | High | Login flow, checkout, onboarding |

### 1.3 Recommended Ratios

| Project Type | Unit | Integration | E2E |
|-------------|------|-------------|-----|
| **API/Backend** | 70% | 25% | 5% |
| **Frontend (SPA)** | 60% | 30% | 10% |
| **Mobile** | 60% | 25% | 15% |
| **Full-stack** | 65% | 25% | 10% |

### 1.4 What to Test at Each Layer

**Unit Tests:**
- Pure functions and utility logic
- State management (reducers, stores)
- Data transformations and validation
- Custom hooks (React) / composables (Vue)
- Business rule engines
- Edge cases and boundary conditions

**Integration Tests:**
- API endpoint request/response cycles
- Database queries and migrations
- Component trees with state and props
- Service-to-service communication
- Authentication and authorization flows
- Third-party integration contracts

**E2E Tests:**
- Critical user journeys (happy path only)
- Revenue-impacting flows (signup, payment, checkout)
- Cross-cutting concerns (auth, permissions)
- Smoke tests for deployment validation

---

## 2. Automation Frameworks

### 2.1 Framework Selection Guide

| Framework | Language | Best For | Speed | Ecosystem |
|-----------|----------|----------|-------|-----------|
| **Jest** | JS/TS | Unit + integration (React, Node) | Fast | Excellent |
| **Vitest** | JS/TS | Unit + integration (Vite-based) | Very fast | Growing |
| **Playwright** | JS/TS/Python/C# | E2E (cross-browser) | Fast | Excellent |
| **Cypress** | JS/TS | E2E + component (web) | Medium | Excellent |
| **pytest** | Python | Unit + integration (Python) | Fast | Excellent |
| **Detox** | JS/TS | E2E (React Native) | Slow | Good |
| **Appium** | Multi-lang | E2E (native mobile) | Slow | Good |
| **k6** | JS | Load/performance testing | — | Good |
| **Artillery** | JS/YAML | Load testing | — | Good |

### 2.2 Playwright Configuration
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['junit', { outputFile: 'results/e2e-results.xml' }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 13'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### 2.3 Test Patterns

**Page Object Model (POM):**
```typescript
// e2e/pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}

  readonly emailInput = this.page.getByLabel('Email');
  readonly passwordInput = this.page.getByLabel('Password');
  readonly submitButton = this.page.getByRole('button', { name: 'Sign in' });
  readonly errorMessage = this.page.getByRole('alert');

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// e2e/tests/login.spec.ts
test('successful login redirects to dashboard', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

**Arrange-Act-Assert (AAA):**
```typescript
test('calculates discount for premium users', () => {
  // Arrange
  const user = createUser({ tier: 'premium' });
  const cart = createCart({ total: 100 });

  // Act
  const result = calculateDiscount(user, cart);

  // Assert
  expect(result.discount).toBe(20);
  expect(result.total).toBe(80);
});
```

---

## 3. Test Data Management

### 3.1 Strategies

| Strategy | When to Use | Pros | Cons |
|----------|-------------|------|------|
| **Factories** | Unit/integration tests | Fast, predictable, isolated | May miss real-world edge cases |
| **Fixtures** | Integration/E2E tests | Consistent starting state | Can become stale |
| **Seeding** | E2E/staging environments | Realistic data | Slow, complex setup |
| **Snapshots** | API/DB-heavy tests | Quick comparison | Brittle, hard to update |
| **Dynamic generation** | Load testing | Unique data per run | Complex teardown |

### 3.2 Factory Pattern
```typescript
// test/factories/user.factory.ts
import { faker } from '@faker-js/faker';

interface UserOverrides {
  email?: string;
  name?: string;
  tier?: 'free' | 'premium' | 'enterprise';
  createdAt?: Date;
}

export function createUser(overrides: UserOverrides = {}) {
  return {
    id: faker.string.uuid(),
    email: overrides.email ?? faker.internet.email(),
    name: overrides.name ?? faker.person.fullName(),
    tier: overrides.tier ?? 'free',
    createdAt: overrides.createdAt ?? faker.date.past(),
    ...overrides,
  };
}

export function createUsers(count: number, overrides: UserOverrides = {}) {
  return Array.from({ length: count }, () => createUser(overrides));
}
```

### 3.3 Data Cleanup Rules

1. **Tests own their data.** Create in setup, destroy in teardown.
2. **Isolated.** Tests never share mutable state.
3. **Deterministic.** Same test run = same data = same result.
4. **No production data in tests.** Use synthetic/anonymized data only.
5. **Clean up after E2E.** Use API-driven cleanup, not UI.

---

## 4. API Testing Patterns

### 4.1 API Test Template
```typescript
describe('POST /api/playlists', () => {
  describe('when authenticated', () => {
    it('creates a playlist and returns 201', async () => {
      const response = await request(app)
        .post('/api/playlists')
        .set('Authorization', `Bearer ${validToken}`)
        .send({ name: 'My Playlist', description: 'Test' });

      expect(response.status).toBe(201);
      expect(response.body).toMatchObject({
        id: expect.any(String),
        name: 'My Playlist',
        description: 'Test',
        tracks: [],
        createdAt: expect.any(String),
      });
    });

    it('returns 400 for missing name', async () => {
      const response = await request(app)
        .post('/api/playlists')
        .set('Authorization', `Bearer ${validToken}`)
        .send({ description: 'No name' });

      expect(response.status).toBe(400);
      expect(response.body.errors).toContainEqual(
        expect.objectContaining({ field: 'name', message: expect.any(String) })
      );
    });
  });

  describe('when unauthenticated', () => {
    it('returns 401', async () => {
      const response = await request(app)
        .post('/api/playlists')
        .send({ name: 'Unauthorized' });

      expect(response.status).toBe(401);
    });
  });
});
```

### 4.2 API Test Checklist

| Category | Tests |
|----------|-------|
| **Happy Path** | Valid request → expected response (status + body) |
| **Validation** | Missing fields, invalid types, boundary values |
| **Auth** | Unauthenticated (401), unauthorized (403), expired token |
| **Idempotency** | Duplicate requests produce same result |
| **Pagination** | First page, last page, empty, out-of-range |
| **Error Handling** | 404 (not found), 409 (conflict), 422 (unprocessable), 500 (server error) |
| **Rate Limiting** | 429 after threshold |
| **Headers** | Content-Type, Cache-Control, CORS |
| **Contract** | Response schema matches OpenAPI spec |

---

## 5. Performance Testing

### 5.1 Test Types

| Type | Purpose | Duration | Load Pattern |
|------|---------|----------|-------------|
| **Load Test** | Validate expected traffic | 10–30 min | Ramp to expected peak |
| **Stress Test** | Find breaking point | 30–60 min | Ramp beyond capacity |
| **Spike Test** | Handle sudden surges | 5–10 min | Sudden 10x jump |
| **Soak Test** | Find memory leaks, degradation | 4–12 hours | Steady moderate load |
| **Breakpoint Test** | Find max capacity | Until failure | Linear ramp |

### 5.2 k6 Load Test Example
```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const latency = new Trend('request_latency');

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up
    { duration: '5m', target: 50 },   // Sustain
    { duration: '2m', target: 200 },  // Peak
    { duration: '5m', target: 200 },  // Sustain peak
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    errors: ['rate<0.01'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/playlists', {
    headers: { Authorization: `Bearer ${__ENV.TOKEN}` },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'latency < 500ms': (r) => r.timings.duration < 500,
  });

  errorRate.add(res.status !== 200);
  latency.add(res.timings.duration);

  sleep(1);
}
```

### 5.3 Performance Budgets

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| **API p50 latency** | < 100ms | < 200ms |
| **API p95 latency** | < 300ms | < 500ms |
| **API p99 latency** | < 500ms | < 1000ms |
| **Error rate** | < 0.1% | < 1% |
| **Throughput** | > 1000 rps | > 500 rps |
| **Page load (LCP)** | < 2.5s | < 4.0s |
| **First Input Delay** | < 100ms | < 300ms |
| **CLS** | < 0.1 | < 0.25 |
| **Bundle size (JS)** | < 200KB gzip | < 350KB gzip |

---

## 6. Accessibility Testing

### 6.1 Automated Testing
```typescript
// Using axe-core with Playwright
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('home page has no a11y violations', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### 6.2 Accessibility Test Checklist

| Category | Test | Tool |
|----------|------|------|
| **Color Contrast** | Text meets 4.5:1 (AA) | axe, Stark, Lighthouse |
| **Keyboard Navigation** | All interactive elements reachable via Tab | Manual + Playwright |
| **Focus Indicators** | Visible focus ring on all focusable elements | Manual |
| **Screen Reader** | Content announced correctly, ARIA labels present | VoiceOver, NVDA |
| **Alt Text** | All images have meaningful alt text | axe |
| **Heading Hierarchy** | H1 → H2 → H3 without skipping | axe |
| **Form Labels** | All inputs have associated labels | axe |
| **Touch Targets** | Minimum 44×44px for mobile | Manual |
| **Reduced Motion** | Respects `prefers-reduced-motion` | Manual |
| **Zoom** | Content usable at 200% zoom | Manual |

### 6.3 A11y Testing Frequency
- **Every PR:** Automated axe scans (CI)
- **Every sprint:** Manual keyboard + screen reader for new features
- **Quarterly:** Full WCAG 2.1 AA audit with assistive technologies
- **Annually:** External accessibility audit

---

## 7. Visual Regression Testing

### 7.1 Tools

| Tool | Approach | Best For |
|------|----------|----------|
| **Playwright screenshots** | Pixel comparison | Component + page |
| **Percy** | Visual diffing (cloud) | Cross-browser visual |
| **Chromatic** | Storybook visual tests | Component libraries |
| **BackstopJS** | Config-based screenshots | Page-level regression |

### 7.2 Playwright Visual Test
```typescript
test('playlist card renders correctly', async ({ page }) => {
  await page.goto('/playlists');
  const card = page.locator('[data-testid="playlist-card"]').first();

  await expect(card).toHaveScreenshot('playlist-card.png', {
    maxDiffPixelRatio: 0.01,
    animations: 'disabled',
  });
});
```

### 7.3 Visual Testing Best Practices

1. **Disable animations** — They cause flaky diffs.
2. **Mock dynamic content** — Dates, avatars, random data.
3. **Test components, not pages** — Smaller surfaces = more stable.
4. **Review diffs carefully** — Not all changes are regressions.
5. **Update baselines intentionally** — Never auto-approve.
6. **Cross-browser** — Chrome, Firefox, Safari have rendering differences.

---

## 8. Mobile Testing

### 8.1 Framework Comparison

| Framework | Platform | Language | Speed | Use Case |
|-----------|----------|----------|-------|----------|
| **Detox** | React Native | JS/TS | Fast | RN-specific E2E |
| **Appium** | iOS + Android (native) | Multi | Slow | Native app testing |
| **Maestro** | iOS + Android | YAML | Fast | Simple flow testing |
| **XCUITest** | iOS | Swift | Fast | iOS-specific |
| **Espresso** | Android | Kotlin/Java | Fast | Android-specific |

### 8.2 Mobile Test Checklist

| Category | Tests |
|----------|-------|
| **Gestures** | Tap, swipe, long press, pinch zoom, pull-to-refresh |
| **Orientation** | Portrait ↔ landscape state preservation |
| **Connectivity** | Offline mode, slow network (3G), network transitions |
| **Background/Foreground** | App state preserved on background/resume |
| **Notifications** | Push notification display and deep link handling |
| **Permissions** | Camera, location, notifications permission flows |
| **Device Variations** | Small screens, large screens, notched displays |
| **OS Versions** | Min supported version through latest |
| **Memory** | No leaks on repeated navigation |
| **Battery** | No excessive CPU/GPS usage in background |

---

## 9. Bug Severity / Priority Matrix

### 9.1 Severity (Impact)

| Severity | Definition | Example |
|----------|-----------|---------|
| **S1 — Critical** | Service down, data loss, security breach | Login broken, payments failing, user data exposed |
| **S2 — Major** | Core feature broken, no workaround | Can't create playlists, search returns wrong results |
| **S3 — Minor** | Feature impaired, workaround exists | Sort doesn't work but filter does, UI misalignment |
| **S4 — Cosmetic** | Visual only, no functional impact | Wrong font weight, off-by-1px spacing, typo |

### 9.2 Priority (Urgency)

| Priority | Definition | SLA |
|----------|-----------|-----|
| **P0 — Hotfix** | Fix immediately, drop everything | < 4 hours |
| **P1 — Urgent** | Fix in current sprint | < 1 week |
| **P2 — Normal** | Fix in next sprint | < 2 weeks |
| **P3 — Low** | Fix when convenient | Next quarter |
| **P4 — Backlog** | May never fix | No SLA |

### 9.3 Severity × Priority Decision Matrix

|  | S1 Critical | S2 Major | S3 Minor | S4 Cosmetic |
|--|:-----------:|:--------:|:--------:|:-----------:|
| **Affects all users** | P0 | P1 | P2 | P3 |
| **Affects many users** | P0 | P1 | P2 | P3 |
| **Affects few users** | P1 | P2 | P3 | P4 |
| **Edge case** | P1 | P2 | P3 | P4 |

### 9.4 Bug Report Template
```markdown
## Bug: [One-line title]

**Severity:** S[1-4] — [Critical/Major/Minor/Cosmetic]
**Priority:** P[0-4] — [Hotfix/Urgent/Normal/Low/Backlog]
**Reporter:** [Name]
**Date:** [Date]
**Assignee:** [Name]
**Environment:** [Production/Staging/Dev] — [Browser/OS/Device]
**Version:** [App version or commit]

### Description
[Clear, concise description of the bug]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Evidence
- Screenshot: [link]
- Video: [link]
- Console errors: [paste]
- Network logs: [paste]

### Impact
- **Users affected:** [All / Segment / Edge case]
- **Workaround:** [Yes — describe / No]
- **Business impact:** [Revenue, retention, compliance]

### Root Cause (if known)
[Technical analysis]

### Fix Verification
- [ ] Bug is reproducible in [environment]
- [ ] Fix deployed to staging
- [ ] Fix verified in staging
- [ ] Regression test added
- [ ] Fix deployed to production
- [ ] Fix verified in production
```

---

## 10. Test Plan Template

```markdown
# Test Plan: [Feature / Release Name]

**Author:** [Name]
**Date:** [Date]
**Version:** [1.0]
**PRD Reference:** [Link]

## 1. Scope

### In Scope
- [Feature area 1]
- [Feature area 2]
- [Platforms: web, iOS, Android]

### Out of Scope
- [Explicitly excluded areas]

## 2. Test Strategy

| Layer | Scope | Tools | Owner |
|-------|-------|-------|-------|
| Unit | Business logic, utils | Jest/Vitest | Dev team |
| Integration | API, DB, component trees | Jest, Supertest | Dev team |
| E2E | Critical user flows | Playwright | QA team |
| Performance | API load, page speed | k6, Lighthouse | QA + DevOps |
| Accessibility | WCAG 2.1 AA | axe, manual | QA team |
| Visual | UI regression | Playwright screenshots | QA team |

## 3. Test Scenarios

### Happy Path
| # | Scenario | Steps | Expected Result | Priority |
|---|---------|-------|----------------|----------|
| 1 | [Scenario] | [Steps] | [Expected] | P0 |

### Edge Cases
| # | Scenario | Steps | Expected Result | Priority |
|---|---------|-------|----------------|----------|
| 1 | [Scenario] | [Steps] | [Expected] | P1 |

### Error Cases
| # | Scenario | Steps | Expected Result | Priority |
|---|---------|-------|----------------|----------|
| 1 | [Scenario] | [Steps] | [Expected] | P1 |

## 4. Environment Requirements
- [ ] Staging deployed with feature flag enabled
- [ ] Test data seeded
- [ ] Third-party integrations mocked/sandboxed
- [ ] Test accounts created for each role

## 5. Entry / Exit Criteria

### Entry Criteria
- [ ] Feature complete (all acceptance criteria implemented)
- [ ] Unit tests written and passing
- [ ] Code reviewed and merged to staging branch
- [ ] Test environment stable

### Exit Criteria
- [ ] All P0 and P1 test cases passed
- [ ] No open S1 or S2 bugs
- [ ] Test coverage ≥ 80% on new code
- [ ] Performance budgets met
- [ ] Accessibility audit passed
- [ ] PO sign-off obtained

## 6. Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| [Risk] | [H/M/L] | [H/M/L] | [Plan] |

## 7. Schedule
| Phase | Start | End | Owner |
|-------|-------|-----|-------|
| Test planning | [Date] | [Date] | QA Lead |
| Test execution | [Date] | [Date] | QA Team |
| Bug fixing | [Date] | [Date] | Dev Team |
| Regression | [Date] | [Date] | QA Team |
| Sign-off | [Date] | [Date] | PO + QA |
```

---

## 11. Coverage Requirements

### Minimum Coverage Thresholds

| Metric | Minimum | Target | Measured By |
|--------|---------|--------|-------------|
| **Line coverage (new code)** | 80% | 90% | Jest/Vitest --coverage |
| **Branch coverage (new code)** | 75% | 85% | Jest/Vitest --coverage |
| **Overall line coverage** | 70% | 80% | Jest/Vitest --coverage |
| **Critical path E2E** | 100% | 100% | Playwright test count |
| **API endpoint coverage** | 90% | 100% | Supertest/Playwright |
| **Accessibility** | 0 violations (A, AA) | 0 violations | axe-core |

### Coverage Configuration
```json
// jest.config.ts or vitest.config.ts
{
  "coverageThreshold": {
    "global": {
      "branches": 75,
      "functions": 80,
      "lines": 80,
      "statements": 80
    }
  },
  "collectCoverageFrom": [
    "src/**/*.{ts,tsx}",
    "!src/**/*.d.ts",
    "!src/**/*.stories.{ts,tsx}",
    "!src/**/*.test.{ts,tsx}",
    "!src/**/index.ts",
    "!src/types/**"
  ]
}
```

### Coverage Anti-Patterns
- ❌ Testing implementation details instead of behavior
- ❌ Writing tests just to hit coverage numbers
- ❌ Ignoring branch coverage (hidden bugs live in untested branches)
- ❌ Not tracking coverage trends over time
- ❌ 100% coverage target (diminishing returns past 90%)

---

## Quality Standards

1. **Shift left.** Catch defects as early as possible — unit > integration > E2E.
2. **Fast feedback.** Unit tests < 30s, integration < 2min, full suite < 15min.
3. **Deterministic.** No flaky tests. Flaky tests erode trust and must be fixed or deleted.
4. **Independent.** Tests run in any order, in parallel, without side effects.
5. **Readable.** Tests are documentation — name them like sentences, structure with AAA.
6. **Maintained.** Dead tests are deleted. Failing tests are fixed immediately.
7. **Risk-based.** Test coverage follows risk — more tests for payment than for "About" page.
8. **Automated first.** Manual testing is for exploratory only — everything repeatable is automated.
