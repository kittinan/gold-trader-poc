import { type Page } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  readonly welcomeMessage;
  readonly balanceDisplay;
  readonly goldPriceCard;
  readonly buyGoldButton;
  readonly sellGoldButton;
  readonly transactionHistoryLink;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.locator('h1, [data-testid="welcome-message"]');
    this.balanceDisplay = page.locator('[data-testid="balance"], .balance');
    this.goldPriceCard = page.locator('[data-testid="gold-price-card"], .gold-price');
    this.buyGoldButton = page.locator('button:has-text("Buy Gold"), [data-testid="buy-gold-btn"]');
    this.sellGoldButton = page.locator('button:has-text("Sell Gold"), [data-testid="sell-gold-btn"]');
    this.transactionHistoryLink = page.locator('a:has-text("Transaction History"), [data-testid="transaction-history"]');
  }

  async goto() {
    await this.page.goto('/dashboard');
  }

  async getBalance() {
    const balanceText = await this.balanceDisplay.textContent();
    return balanceText ? parseFloat(balanceText.replace(/[^\d.-]/g, '')) : 0;
  }

  async getGoldPrice() {
    const priceText = await this.goldPriceCard.textContent();
    return priceText ? parseFloat(priceText.replace(/[^\d.-]/g, '')) : 0;
  }
}