---
name: frontend-patterns
description: >
  Frontend development patterns and best practices. Use for component architecture, state management, CSS patterns, accessibility, performance optimization, and design system integration.
---

# Frontend Patterns

## 1. Component Architecture
- **Atomic Design**: Organize components into Atoms, Molecules, Organisms, Templates, and Pages.
- **Compound Components**: Use context to share implicit state between parent and child components (e.g., `<Select>`, `<Select.Option>`).
- **Render Props**: Share code between React components using a prop whose value is a function.
- **Custom Hooks**: Extract stateful logic from a component so it can be tested independently and reused.

## 2. State Management
- **Local State**: Use `useState` or `useReducer` for state that is isolated to a single component or small subtree.
- **Global State**: Use context API, Redux, Zustand, or Jotai for application-wide state.
- **Server State**: Use React Query, SWR, or Apollo Client to manage asynchronous data fetching, caching, synchronization, and error handling.
- **Form State**: Use libraries like React Hook Form or Formik for complex forms.

## 3. CSS Patterns
- **Utility-first CSS**: Tailwind CSS conventions for rapid styling and consistency.
- **CSS Modules**: Scope CSS locally by default to avoid class name collisions.
- **Styled-components**: Write actual CSS in JavaScript, leveraging tagged template literals.

## 4. Performance Optimization
- **Code Splitting**: Use `React.lazy` and Suspense to lazy load components.
- **Memoization**: Use `React.memo`, `useMemo`, and `useCallback` to prevent unnecessary re-renders.
- **Virtual Scrolling**: Render only the visible items in a long list to save memory and processing time.

## 5. Accessibility (A11y)
- **WCAG 2.1 Checklist**: Follow guidelines for contrast, text resizing, and keyboard navigability.
- **ARIA Patterns**: Use ARIA attributes appropriately to enhance semantics for screen readers.
- **Focus Management**: Ensure logical tab order and visible focus states.

## 6. Testing
- **Component Testing**: Use React Testing Library to test components from the user's perspective.
- **Visual Regression**: Compare screenshots of components to detect unintended visual changes (e.g., Chromatic, Percy).
- **E2E Testing**: Automate browser actions to test critical user flows (e.g., Playwright, Cypress).

## 7. Design System Integration
- **Token Consumption**: Map design tokens (colors, typography, spacing) to CSS variables or a theme provider.
- **Component Composition**: Build complex UIs by composing simpler, reusable design system components.

## 8. SEO
- **Meta Tags**: Use next/head or react-helmet for dynamic meta tags.
- **Structured Data**: Inject JSON-LD to help search engines understand page content.
- **SSR/SSG**: Leverage Next.js or Remix for server-side rendering or static site generation.
