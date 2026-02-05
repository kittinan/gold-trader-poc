# Phase 2: Frontend & E2E Testing Plan

## 📋 Overview

เป้าหมาย: เพิ่มระบบทดสอบที่ครอบคลุมสำหรับ Frontend และ Integration Tests

---

## Task A: Frontend Unit Tests (คุณฐาน)

### A.1 Setup Testing Environment
```bash
# Install testing dependencies
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @vitest/coverage-v8 msw
```

### A.2 Configuration Files
- `vitest.config.ts` - Vitest configuration
- `src/test/setup.ts` - Test setup file
- `src/test/mocks/` - MSW handlers for API mocking

### A.3 Test Structure
```
frontend/src/
├── test/
│   ├── setup.ts
│   ├── mocks/
│   │   ├── handlers.ts
│   │   └── server.ts
│   └── utils.tsx (test utilities)
├── components/
│   └── __tests__/
│       ├── Button.test.tsx
│       ├── GoldPriceCard.test.tsx
│       └── ...
├── hooks/
│   └── __tests__/
│       ├── useAuth.test.ts
│       └── useGoldPrice.test.ts
├── pages/
│   └── __tests__/
│       ├── Login.test.tsx
│       ├── Dashboard.test.tsx
│       └── Trade.test.tsx
└── services/
    └── __tests__/
        └── api.test.ts
```

### A.4 Test Categories
1. **Component Tests** - UI rendering, user interactions
2. **Hook Tests** - Custom hooks functionality
3. **Page Tests** - Full page rendering with routing
4. **Service Tests** - API service functions

### A.5 Scripts to Add
```json
{
  "test": "vitest",
  "test:ui": "vitest --ui",
  "test:coverage": "vitest run --coverage"
}
```

---

## Task B: Integration/E2E Tests (คุณละเอียด)

### B.1 Setup Playwright
```bash
npm init playwright@latest
```

### B.2 Configuration
- `playwright.config.ts` - Playwright configuration
- `e2e/` - E2E test directory

### B.3 Test Structure
```
e2e/
├── fixtures/
│   └── test-data.ts
├── pages/
│   ├── login.page.ts
│   ├── dashboard.page.ts
│   └── trade.page.ts
├── tests/
│   ├── auth.spec.ts
│   ├── gold-trading.spec.ts
│   ├── deposit.spec.ts
│   └── portfolio.spec.ts
└── playwright.config.ts
```

### B.4 E2E Test Scenarios
1. **Authentication Flow**
   - User registration
   - User login
   - User logout
   - Token refresh

2. **Gold Trading Flow**
   - View gold prices
   - Buy gold
   - Sell gold
   - View transaction history

3. **Wallet Flow**
   - View balance
   - Deposit funds
   - View deposit history

4. **Portfolio Flow**
   - View holdings
   - Calculate profit/loss

---

## GitHub Actions Updates

### CI Workflow Updates
```yaml
# Add to .github/workflows/ci.yml

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run test:coverage
      
  e2e-test:
    runs-on: ubuntu-latest
    needs: [test, frontend-test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npx playwright install --with-deps
      - run: cd e2e && npx playwright test
```

---

## Timeline

| Phase | Task | Owner | Duration |
|-------|------|-------|----------|
| 1 | Frontend test setup | คุณฐาน | 30 min |
| 2 | Component tests | คุณฐาน | 1-2 hours |
| 3 | Hook & Service tests | คุณฐาน | 1 hour |
| 4 | E2E setup | คุณละเอียด | 30 min |
| 5 | Auth E2E tests | คุณละเอียด | 1 hour |
| 6 | Trading E2E tests | คุณละเอียด | 1-2 hours |
| 7 | CI integration | Both | 30 min |

---

## Success Criteria

- [ ] Frontend test coverage > 70%
- [ ] All E2E critical flows passing
- [ ] GitHub Actions green for all test jobs
- [ ] Tests run in < 5 minutes

---

*Created: 5 Feb 2026*
