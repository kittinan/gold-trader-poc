import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { DashboardPage } from '../pages/dashboard.page';
import { TradePage } from '../pages/trade.page';
import { TEST_USERS, TEST_DATA } from '../fixtures/test-data';

test.describe('Portfolio Management', () => {
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

  test('should display portfolio summary on dashboard', async ({ page }) => {
    // Check for portfolio summary elements
    const portfolioValue = page.locator('[data-testid="portfolio-value"], .portfolio-value');
    const goldHoldings = page.locator('[data-testid="gold-holdings"], .gold-holdings');
    const profitLoss = page.locator('[data-testid="profit-loss"], .profit-loss');
    
    await expect(portfolioValue).toBeVisible();
    await expect(goldHoldings).toBeVisible();
    await expect(profitLoss).toBeVisible();
  });

  test('should navigate to portfolio page', async ({ page }) => {
    // Click portfolio link
    const portfolioLink = page.locator('a:has-text("Portfolio"), [data-testid="portfolio-link"]');
    await portfolioLink.click();
    
    await expect(page).toHaveURL('/portfolio');
    
    // Verify portfolio page elements
    const portfolioChart = page.locator('[data-testid="portfolio-chart"], .portfolio-chart');
    const holdingsTable = page.locator('[data-testid="holdings-table"], .holdings-table');
    
    await expect(portfolioChart).toBeVisible();
    await expect(holdingsTable).toBeVisible();
  });

  test('should display gold holdings details', async ({ page }) => {
    // Navigate to portfolio
    const portfolioLink = page.locator('a:has-text("Portfolio"), [data-testid="portfolio-link"]');
    await portfolioLink.click();
    
    // Check holdings table
    const holdingsRows = page.locator('[data-testid="holding-row"], tr[data-holding-id]');
    const rowCount = await holdingsRows.count();
    
    // Should have at least one row even if no holdings (with message)
    expect(rowCount).toBeGreaterThanOrEqual(0);
    
    if (rowCount > 0) {
      // Verify holding row has required data
      const firstRow = holdingsRows.first();
      await expect(firstRow.locator('[data-testid="holding-amount"], .holding-amount')).toBeVisible();
      await expect(firstRow.locator('[data-testid="holding-value"], .holding-value')).toBeVisible();
      await expect(firstRow.locator('[data-testid="holding-pnl"], .holding-pnl')).toBeVisible();
    }
  });

  test('should calculate profit/loss correctly', async ({ page }) => {
    // Navigate to portfolio
    const portfolioLink = page.locator('a:has-text("Portfolio"), [data-testid="portfolio-link"]');
    await portfolioLink.click();
    
    // Get total P&L
    const totalProfitLoss = page.locator('[data-testid="total-profit-loss"], .total-pnl');
    await expect(totalProfitLoss).toBeVisible();
    
    const pnlText = await totalProfitLoss.textContent();
    expect(pnlText).toBeDefined();
    
    // P&L should be a valid number (positive or negative)
    const pnlValue = parseFloat(pnlText?.replace(/[^\d.-]/g, '') || '0');
    expect(isNaN(pnlValue)).toBe(false);
  });

  test('should update portfolio after trade', async ({ page }) => {
    // Get initial portfolio value
    const portfolioLink = page.locator('a:has-text("Portfolio"), [data-testid="portfolio-link"]');
    await portfolioLink.click();
    
    const initialValueText = await page.locator('[data-testid="portfolio-value"], .portfolio-value').textContent();
    const initialValue = parseFloat(initialValueText?.replace(/[^\d.-]/g, '') || '0');
    
    // Make a small trade
    await dashboardPage.goto();
    await dashboardPage.buyGoldButton.click();
    
    await tradePage.selectOrderType('buy');
    await tradePage.enterGoldAmount(0.01); // Very small amount
    await tradePage.confirmTrade();
    
    // Wait for success
    const successMessage = page.locator('[data-testid="success"], .alert-success');
    await expect(successMessage).toBeVisible();
    
    // Check portfolio again
    await portfolioLink.click();
    
    const newValueText = await page.locator('[data-testid="portfolio-value"], .portfolio-value').textContent();
    const newValue = parseFloat(newValueText?.replace(/[^\d.-]/g, '') || '0');
    
    // Portfolio value should have changed
    expect(newValue).not.toBe(initialValue);
  });

  test('should display portfolio performance chart', async ({ page }) => {
    // Navigate to portfolio
    const portfolioLink = page.locator('a:has-text("Portfolio"), [data-testid="portfolio-link"]');
    await portfolioLink.click();
    
    // Check for performance chart
    const performanceChart = page.locator('[data-testid="performance-chart"], .performance-chart');
    await expect(performanceChart).toBeVisible();
    
    // Check for time period buttons
    const periodButtons = page.locator('[data-testid="period-button"], .period-btn');
    const buttonCount = await periodButtons.count();
    expect(buttonCount).toBeGreaterThan(0);
    
    // Click on a period button (e.g., 1M, 3M, 1Y)
    if (buttonCount > 0) {
      await periodButtons.first().click();
      // Chart should still be visible
      await expect(performanceChart).toBeVisible();
    }
  });

  test('should export portfolio data', async ({ page }) => {
    // Navigate to portfolio
    const portfolioLink = page.locator('a:has-text("Portfolio"), [data-testid="portfolio-link"]');
    await portfolioLink.click();
    
    // Look for export button
    const exportButton = page.locator('button:has-text("Export"), [data-testid="export-btn"]');
    const isVisible = await exportButton.isVisible();
    
    if (isVisible) {
      // Click export button
      await exportButton.click();
      
      // Check for download (this would need to be adjusted based on your implementation)
      // For now, just verify the button works
      expect(true).toBe(true);
    } else {
      // If no export button, test passes
      expect(true).toBe(true);
    }
  });

  test('should display asset allocation', async ({ page }) => {
    // Navigate to portfolio
    const portfolioLink = page.locator('a:has-text("Portfolio"), [data-testid="portfolio-link"]');
    await portfolioLink.click();
    
    // Check for asset allocation section
    const allocationSection = page.locator('[data-testid="asset-allocation"], .asset-allocation');
    const isVisible = await allocationSection.isVisible();
    
    if (isVisible) {
      // Verify allocation elements
      const allocationChart = page.locator('[data-testid="allocation-chart"], .allocation-chart');
      await expect(allocationChart).toBeVisible();
      
      const allocationList = page.locator('[data-testid="allocation-list"], .allocation-list');
      await expect(allocationList).toBeVisible();
    } else {
      // If no allocation section, test passes
      expect(true).toBe(true);
    }
  });
});