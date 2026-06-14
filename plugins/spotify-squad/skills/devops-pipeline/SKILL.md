---
name: devops-pipeline
description: >
  CI/CD pipeline and infrastructure patterns. Use for GitHub Actions workflows,
  Docker configurations, Kubernetes manifests, Terraform modules, monitoring
  setup, and deployment strategies.
---

# DevOps Pipeline Skill

You are a senior DevOps/platform engineer. You design and implement reliable CI/CD pipelines, infrastructure-as-code, monitoring systems, and deployment strategies that enable teams to ship fast and safe.

---

## 1. CI/CD Pipeline Patterns

### 1.1 Pipeline Stages

Every pipeline should follow this progression:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Build   │───▶│   Test   │───▶│   Lint   │───▶│ Security │───▶│  Deploy  │
│          │    │          │    │  & Fmt   │    │   Scan   │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │
              ┌──────┴──────┐
              │   Unit  │ Int │
              │   Tests │ Tests│
              └─────────┴─────┘
```

| Stage | Purpose | Max Duration | Failure Action |
|-------|---------|-------------|----------------|
| **Build** | Compile, install deps, generate artifacts | 3 min | Block merge |
| **Lint & Format** | Code style, static analysis | 2 min | Block merge |
| **Unit Tests** | Fast, isolated tests | 3 min | Block merge |
| **Integration Tests** | Service interactions, DB tests | 5 min | Block merge |
| **Security Scan** | Dependency audit, SAST, secrets scan | 3 min | Block merge (P0), warn (P1+) |
| **Build Artifact** | Docker image, binary, bundle | 5 min | Block deploy |
| **Deploy Staging** | Deploy to staging environment | 5 min | Block prod deploy |
| **E2E Tests** | Full system tests on staging | 10 min | Block prod deploy |
| **Deploy Production** | Progressive rollout | 10 min | Auto-rollback on failure |

### 1.2 Pipeline Principles

1. **Fast feedback.** Fail fast — run cheapest checks first.
2. **Deterministic.** Same commit = same result. Pin all dependencies.
3. **Isolated.** Tests don't depend on external state or each other.
4. **Cached.** Cache dependencies, Docker layers, and build artifacts aggressively.
5. **Observable.** Pipeline metrics: duration, success rate, flake rate.

---

## 2. GitHub Actions Best Practices

### 2.1 Workflow Structure
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read
  packages: write
  pull-requests: write

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check
      - run: npx tsc --noEmit

  test:
    name: Tests
    runs-on: ubuntu-latest
    timeout-minutes: 10
    needs: [lint]
    strategy:
      matrix:
        shard: [1, 2, 3]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --shard=${{ matrix.shard }}/3
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: test-results-${{ matrix.shard }}
          path: coverage/

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - uses: github/codeql-action/analyze@v3

  build:
    name: Build & Push Image
    runs-on: ubuntu-latest
    timeout-minutes: 10
    needs: [test, security]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy Staging
    runs-on: ubuntu-latest
    timeout-minutes: 10
    needs: [build]
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to staging
        run: |
          # Deploy using your method (kubectl, helm, etc.)
          echo "Deploying ${{ needs.build.outputs.image-tag }} to staging"

  deploy-production:
    name: Deploy Production
    runs-on: ubuntu-latest
    timeout-minutes: 10
    needs: [deploy-staging]
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          echo "Deploying to production with canary strategy"
```

### 2.2 GitHub Actions Best Practices

| Practice | Why |
|----------|-----|
| Pin action versions (`@v4`, not `@main`) | Prevents supply-chain attacks |
| Use `concurrency` to cancel stale runs | Saves CI minutes |
| Set `timeout-minutes` on every job | Prevents runaway jobs |
| Use `permissions` with least privilege | Security hardening |
| Cache dependencies (`actions/cache` or built-in) | Speed |
| Use matrix strategies for parallelism | Faster test suites |
| Use `environment` for deployment approvals | Controlled rollouts |
| Store secrets in GitHub Secrets, not env vars | Security |
| Use `if: failure()` for artifact upload | Debugging |
| Use reusable workflows for shared patterns | DRY pipelines |

---

## 3. Docker

### 3.1 Multi-Stage Build
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

# Security: non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 appuser

# Copy only what's needed
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```

### 3.2 Docker Best Practices

| Practice | Details |
|----------|---------|
| Use multi-stage builds | Reduce image size 50–90% |
| Pin base image versions | `node:20.11-alpine`, not `node:latest` |
| Run as non-root user | Security: `USER appuser` |
| Use `.dockerignore` | Exclude `node_modules`, `.git`, `*.md`, tests |
| Add HEALTHCHECK | Enable orchestrator health monitoring |
| Use COPY, not ADD | ADD has auto-extraction magic — explicit is better |
| Order layers by change frequency | Static deps first, code last — maximize cache |
| Scan images | `docker scout`, `trivy`, or `snyk container test` |
| Use `--no-cache` in CI | Ensure reproducible builds |

### 3.3 Docker Compose (Development)
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      target: builder
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:pass@db:5432/appdb
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: appdb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d appdb"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

---

## 4. Kubernetes

### 4.1 Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: app
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: app
        version: v1
    spec:
      serviceAccountName: app-sa
      containers:
        - name: app
          image: ghcr.io/org/app:sha-abc123
          ports:
            - containerPort: 3000
              name: http
          env:
            - name: NODE_ENV
              value: production
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
          startupProbe:
            httpGet:
              path: /health
              port: http
            failureThreshold: 30
            periodSeconds: 10
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: app
```

### 4.2 Service & Ingress
```yaml
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: app
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app
                port:
                  number: 80
```

### 4.3 Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
```

---

## 5. Infrastructure as Code (Terraform)

### 5.1 Module Structure
```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── production/
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── database/
│   ├── compute/
│   ├── monitoring/
│   └── cdn/
└── README.md
```

### 5.2 State Management Best Practices

| Practice | Details |
|----------|---------|
| Remote state (S3 + DynamoDB) | Never local state in production |
| State locking | Prevent concurrent modifications |
| Separate state per environment | Blast radius isolation |
| State encryption | Encrypt at rest (S3 SSE) |
| `terraform plan` in CI | Review changes before apply |
| No manual `terraform apply` | Always through CI/CD pipeline |

### 5.3 Backend Configuration
```hcl
terraform {
  required_version = ">= 1.7"

  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "app/staging/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

---

## 6. Monitoring

### 6.1 Golden Signals (Google SRE)

| Signal | Definition | Metric Examples |
|--------|-----------|----------------|
| **Latency** | Time to serve a request | p50, p95, p99 response time |
| **Traffic** | Demand on the system | Requests per second, concurrent users |
| **Errors** | Rate of failed requests | HTTP 5xx rate, error log rate |
| **Saturation** | How full the system is | CPU %, memory %, disk I/O, queue depth |

### 6.2 SLI / SLO / SLA

| Term | Definition | Example |
|------|-----------|---------|
| **SLI** (Indicator) | Measurable metric of service behavior | Request latency, error rate |
| **SLO** (Objective) | Target value for an SLI | 99.9% of requests < 200ms |
| **SLA** (Agreement) | Business commitment with consequences | 99.9% uptime or credits issued |

**Error Budget:**
```
Error Budget = 1 - SLO
Example: SLO = 99.9% → Error Budget = 0.1% → ~43 min downtime/month
```

### 6.3 Alerting Rules

| Severity | Response Time | Notification | Example |
|----------|-------------|-------------|---------|
| **P0 — Critical** | < 15 min | PagerDuty + Slack #incidents | Service down, data loss |
| **P1 — High** | < 1 hour | PagerDuty + Slack | Error rate >5%, latency >2s p99 |
| **P2 — Medium** | < 4 hours | Slack | Error rate >1%, degraded performance |
| **P3 — Low** | Next business day | Slack / Ticket | Warning thresholds, disk space |

**Alert Best Practices:**
1. Alert on symptoms (user impact), not causes (CPU usage)
2. Every alert must be actionable — if you can't act on it, delete it
3. Include runbook link in every alert
4. Use multi-window, multi-burn-rate alerting for SLOs
5. Review and prune alerts quarterly — alert fatigue kills

### 6.4 Prometheus Alert Example
```yaml
groups:
  - name: app-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate ({{ $value | humanizePercentage }})"
          description: "Error rate is above 5% for the last 5 minutes."
          runbook_url: "https://wiki.example.com/runbooks/high-error-rate"

      - alert: HighLatencyP99
        expr: |
          histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
          > 2
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "P99 latency above 2s"
          runbook_url: "https://wiki.example.com/runbooks/high-latency"
```

---

## 7. Deployment Strategies

### 7.1 Strategy Comparison

| Strategy | Risk | Rollback Speed | Cost | Complexity | Use Case |
|----------|------|---------------|------|-----------|----------|
| **Rolling Update** | Medium | Medium (redeploy) | Low | Low | Standard deployments |
| **Blue/Green** | Low | Instant (DNS/LB switch) | High (2x infra) | Medium | Critical services |
| **Canary** | Low | Fast (route traffic back) | Medium | High | High-traffic services |
| **Feature Flags** | Lowest | Instant (toggle) | Low | Medium | Granular control |
| **A/B Testing** | Low | Instant (toggle) | Medium | High | Data-driven releases |

### 7.2 Blue/Green Deployment
```
                    ┌─────────────┐
                    │   Load      │
                    │  Balancer   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────┴─────┐          ┌─────┴─────┐
        │  Blue     │          │  Green    │
        │  (v1.0)   │          │  (v1.1)   │
        │  ACTIVE   │          │  STANDBY  │
        └───────────┘          └───────────┘

1. Deploy v1.1 to Green (standby)
2. Run smoke tests on Green
3. Switch LB to Green
4. Green becomes ACTIVE, Blue becomes STANDBY
5. If issues: switch back to Blue instantly
```

### 7.3 Canary Deployment
```
Phase 1: 1% traffic → canary (monitor 15 min)
Phase 2: 5% traffic → canary (monitor 15 min)
Phase 3: 25% traffic → canary (monitor 30 min)
Phase 4: 50% traffic → canary (monitor 30 min)
Phase 5: 100% traffic → full rollout

Auto-rollback triggers:
- Error rate increase > 1% above baseline
- P99 latency increase > 50% above baseline
- Any P0 alert fires
```

### 7.4 Feature Flags
```typescript
// Feature flag structure
interface FeatureFlag {
  key: string;
  enabled: boolean;
  rolloutPercentage: number;  // 0-100
  targetSegments: string[];   // user segments
  killSwitch: boolean;        // emergency off
}

// Usage pattern
if (featureFlags.isEnabled('new-playlist-ui', { userId, segment })) {
  return <NewPlaylistUI />;
}
return <LegacyPlaylistUI />;
```

**Feature Flag Lifecycle:**
1. **Create** — Flag off, code deployed behind flag
2. **Test** — Enable for internal/beta users
3. **Rollout** — Progressive % increase
4. **GA** — 100%, flag becomes default
5. **Cleanup** — Remove flag and legacy code (CRITICAL — don't skip!)

---

## 8. Secrets Management

### Principles

| Principle | Details |
|-----------|---------|
| Never commit secrets | Use `.gitignore`, pre-commit hooks, git-secrets |
| Rotate regularly | 90-day rotation for service credentials |
| Least privilege | Secrets scoped to specific services/environments |
| Audit access | Log every secret access |
| Encrypt at rest and in transit | Always |

### Tools Hierarchy
1. **Cloud-native:** AWS Secrets Manager, GCP Secret Manager, Azure Key Vault
2. **Self-hosted:** HashiCorp Vault
3. **CI/CD:** GitHub Secrets, environment-scoped
4. **Development:** `.env.local` (gitignored), `direnv`

### Pre-commit Secret Scanning
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

---

## 9. Runbook Templates

### Incident Runbook
```markdown
# Runbook: [Incident Type]

**Last Updated:** [Date]
**Owner:** [Team/Person]
**Alert:** [Alert name that triggers this runbook]

## Symptoms
- [Observable symptom 1]
- [Observable symptom 2]
- [Dashboard link]

## Impact
- **User Impact:** [What users experience]
- **Business Impact:** [Revenue, SLA implications]
- **Blast Radius:** [Affected services/regions]

## Diagnosis

### Step 1: Verify the issue
```bash
# Check service health
curl -s https://app.example.com/health | jq .

# Check pod status
kubectl get pods -l app=app -n production

# Check recent deployments
kubectl rollout history deployment/app -n production
```

### Step 2: Check logs
```bash
# Application logs
kubectl logs -l app=app -n production --tail=100 --since=5m

# Filter for errors
kubectl logs -l app=app -n production --tail=500 | grep -i error
```

### Step 3: Check metrics
- [Grafana dashboard link]
- Look at: error rate, latency, CPU, memory, connections

## Resolution

### Option A: Rollback deployment
```bash
kubectl rollout undo deployment/app -n production
kubectl rollout status deployment/app -n production
```

### Option B: Scale up
```bash
kubectl scale deployment/app -n production --replicas=10
```

### Option C: [Specific fix]
[Steps]

## Post-Incident
- [ ] Incident timeline documented
- [ ] Root cause identified
- [ ] Fix deployed and verified
- [ ] Post-mortem scheduled (within 48 hours)
- [ ] Action items created with owners

## Escalation
| Level | Contact | When |
|-------|---------|------|
| L1 | On-call engineer | First response |
| L2 | Tech Lead | Unresolved after 30 min |
| L3 | VP Engineering | Customer-facing outage >1 hour |
```

---

## Quality Standards

1. **Pipeline as code.** All CI/CD config lives in the repo — no ClickOps.
2. **Immutable artifacts.** Build once, deploy everywhere. Same image dev → staging → prod.
3. **Zero-downtime deploys.** Rolling updates or blue/green — never take the service down.
4. **Infrastructure as code.** All infra managed via Terraform/Pulumi — no manual changes.
5. **Observable by default.** Every service ships with health checks, metrics, logs, and traces.
6. **Automate everything.** If you do it twice, automate it. If you do it once, document it.
7. **Blast radius control.** Feature flags, canary deploys, circuit breakers — limit impact.
8. **Security-first.** Scan images, audit dependencies, rotate secrets, least-privilege access.
