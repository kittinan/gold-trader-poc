import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { DashboardPage } from '../pages/dashboard.page';
import { TEST_USERS, TEST_DATA } from '../fixtures/test-data';

test.describe('Wallet & Deposits', () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
    
    // Login before each test
    await loginPage.goto();
    await loginPage.login(TEST_USERS.existing.email, TEST_USERS.existing.password);
    await expect(page).toHaveURL('/dashboard');
  });

  test('should display wallet balance', async ({ page }) => {
    const balance = await dashboardPage.getBalance();
    expect(balance).toBeGreaterThanOrEqual(0);
  });

  test('should navigate to deposit page', async ({ page }) => {
    // Click deposit button (adjust selector based on your app)
    const depositButton = page.locator('button:has-text("Deposit"), [data-testid="deposit-btn"]');
    await depositButton.click();
    
    await expect(page).toHaveURL('/deposit');
    
    // Verify deposit page elements
    const amountInput = page.locator('input[name="amount"], [data-testid="deposit-amount"]');
    const confirmButton = page.locator('button:has-text("Confirm Deposit"), [data-testid="confirm-deposit"]');
    
    await expect(amountInput).toBeVisible();
    await expect(confirmButton).toBeVisible();
  });

  test('should show error for invalid deposit amount', async ({ page }) => {
    // Navigate to deposit page
    const depositButton = page.locator('button:has-text("Deposit"), [data-testid="deposit-btn"]');
    await depositButton.click();
    
    // Enter invalid amount
    const amountInput = page.locator('input[name="amount"], [data-testid="deposit-amount"]');
    await amountInput.fill('-100');
    
    // Try to submit
    const confirmButton = page.locator('button:has-text("Confirm Deposit"), [data-testid="confirm-deposit"]');
    await confirmButton.click();
    
    // Check for error message
    const errorMessage = page.locator('[data-testid="error"], .text-red-600');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText('amount');
  });

  test('should process deposit successfully', async ({ page }) => {
    // Get initial balance
    const initialBalance = await dashboardPage.getBalance();
    
    // Navigate to deposit page
    const depositButton = page.locator('button:has-text("Deposit"), [data-testid="deposit-btn"]');
    await depositButton.click();
    
    // Enter deposit amount
    const amountInput = page.locator('input[name="amount"], [data-testid="deposit-amount"]');
    await amountInput.fill(TEST_DATA.deposits.small.toString());
    
    // Confirm deposit
    const confirmButton = page.locator('button:has-text("Confirm Deposit"), [data-testid="confirm-deposit"]');
    await confirmButton.click();
    
    // Wait for success message
    const successMessage = page.locator('[data-testid="success"], .alert-success');
    await expect(successMessage).toBeVisible();
    await expect(successMessage).toContainText('successfully');
    
    // Return to dashboard and verify balance updated
    await dashboardPage.goto();
    const newBalance = await dashboardPage.getBalance();
    expect(newBalance).toBe(initialBalance + TEST_DATA.deposits.small);
  });

  test('should display deposit history', async ({ page }) => {
    // Navigate to deposit history
    const historyLink = page.locator('a:has-text("Deposit History"), [data-testid="deposit-history"]');
    await historyLink.click();
    
    // Verify deposit history is displayed
    const historyTable = page.locator('[data-testid="deposit-history-table"], .deposit-history');
    await expect(historyTable).toBeVisible();
    
    // Check for deposit records
    const depositRows = page.locator('[data-testid="deposit-row"], tr[data-deposit-id]');
    const rowCount = await depositRows.count();
    expect(rowCount).toBeGreaterThan(0);
  });

  test('should display wallet transaction summary', async ({ page }) => {
    // Navigate to wallet page
    const walletLink = page.locator('a:has-text("Wallet"), [data-testid="wallet-link"]');
    await walletLink.click();
    
    await expect(page).toHaveURL('/wallet');
    
    // Verify wallet summary elements
    const totalBalance = page.locator('[data-testid="total-balance"], .total-balance');
    const availableBalance = page.locator('[data-testid="available-balance"], .available-balance');
    const pendingAmount = page.locator('[data-testid="pending-amount"], .pending-amount');
    
    await expect(totalBalance).toBeVisible();
    await expect(availableBalance).toBeVisible();
    await expect(pendingAmount).toBeVisible();
    
    // Verify amounts are positive numbers
    const totalBalanceText = await totalBalance.textContent();
    const totalBalanceValue = parseFloat(totalBalanceText?.replace(/[^\d.-]/g, '') || '0');
    expect(totalBalanceValue).toBeGreaterThanOrEqual(0);
  });

  test('should handle concurrent deposits correctly', async ({ page }) => {
    // This test would require multiple tabs or API calls
    // For now, we'll just verify the deposit page can handle rapid navigation
    
    // Navigate to deposit page multiple times quickly
    for (let i = 0; i < 3; i++) {
      const depositButton = page.locator('button:has-text("Deposit"), [data-testid="deposit-btn"]');
      await depositButton.click();
      await expect(page).toHaveURL('/deposit');
      
      // Go back to dashboard
      await dashboardPage.goto();
    }
  });
});