import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { DashboardPage } from '../pages/dashboard.page';
import { TradePage } from '../pages/trade.page';
import { TEST_USERS, TEST_DATA } from '../fixtures/test-data';

test.describe('Gold Trading', () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;
  let tradePage: TradePage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
    tradePage = new TradePage(page);
    
    // Login before each test
    await loginPage.goto();
    await loginPage.login(TEST_USERS.existing.email, TEST_USERS.existing.password);
    await expect(page).toHaveURL('/dashboard');
  });

  test('should display current gold price on dashboard', async ({ page }) => {
    const goldPrice = await dashboardPage.getGoldPrice();
    expect(goldPrice).toBeGreaterThan(0);
  });

  test('should navigate to trade page', async ({ page }) => {
    await dashboardPage.buyGoldButton.click();
    await expect(page).toHaveURL('/trade');
    
    // Verify trade page elements
    await expect(tradePage.goldAmountInput).toBeVisible();
    await expect(tradePage.orderTypeSelect).toBeVisible();
    await expect(tradePage.confirmButton).toBeVisible();
  });

  test('should calculate total price for gold purchase', async ({ page }) => {
    await tradePage.goto();
    await tradePage.selectOrderType('buy');
    await tradePage.enterGoldAmount(TEST_DATA.goldTrades.small.amount);
    
    const totalPrice = await tradePage.getTotalPrice();
    expect(totalPrice).toBeGreaterThan(0);
    expect(totalPrice).toBeGreaterThanOrEqual(TEST_DATA.goldTrades.small.expectedPriceRange.min);
    expect(totalPrice).toBeLessThanOrEqual(TEST_DATA.goldTrades.small.expectedPriceRange.max);
  });

  test('should show error for invalid gold amount', async ({ page }) => {
    await tradePage.goto();
    await tradePage.selectOrderType('buy');
    await tradePage.enterGoldAmount(-1); // Invalid negative amount
    
    // Check for validation error
    const errorMessage = page.locator('[data-testid="error"], .text-red-600');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText('amount');
  });

  test('should execute buy gold order successfully', async ({ page }) => {
    await tradePage.goto();
    await tradePage.selectOrderType('buy');
    await tradePage.enterGoldAmount(TEST_DATA.goldTrades.small.amount);
    await tradePage.confirmTrade();
    
    // Wait for success message
    await expect(tradePage.successMessage).toBeVisible();
    await expect(tradePage.successMessage).toContainText('successfully');
    
    // Verify balance updated
    await dashboardPage.goto();
    const balance = await dashboardPage.getBalance();
    expect(balance).toBeLessThan(0); // Balance should decrease after purchase
  });

  test('should execute sell gold order successfully', async ({ page }) => {
    await tradePage.goto();
    await tradePage.selectOrderType('sell');
    await tradePage.enterGoldAmount(TEST_DATA.goldTrades.small.amount);
    await tradePage.confirmTrade();
    
    // Wait for success message
    await expect(tradePage.successMessage).toBeVisible();
    await expect(tradePage.successMessage).toContainText('successfully');
    
    // Verify balance updated
    await dashboardPage.goto();
    const balance = await dashboardPage.getBalance();
    expect(balance).toBeGreaterThan(0); // Balance should increase after selling
  });

  test('should display transaction history', async ({ page }) => {
    // Go to transaction history
    await dashboardPage.transactionHistoryLink.click();
    
    // Verify transactions are displayed
    const transactionTable = page.locator('[data-testid="transaction-table"], .transaction-history');
    await expect(transactionTable).toBeVisible();
    
    // Check for transaction rows
    const transactionRows = page.locator('[data-testid="transaction-row"], tr[data-transaction-id]');
    const rowCount = await transactionRows.count();
    expect(rowCount).toBeGreaterThan(0);
  });

  test('should filter transactions by type', async ({ page }) => {
    // Go to transaction history
    await dashboardPage.transactionHistoryLink.click();
    
    // Filter by buy transactions
    const buyFilter = page.locator('button:has-text("Buy"), [data-testid="filter-buy"]');
    await buyFilter.click();
    
    // Verify only buy transactions are shown
    const transactionRows = page.locator('[data-testid="transaction-row"], tr[data-transaction-id]');
    for (let i = 0; i < await transactionRows.count(); i++) {
      const row = transactionRows.nth(i);
      await expect(row).toContainText('Buy');
    }
  });
});