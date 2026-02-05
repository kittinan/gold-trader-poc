import { type Page } from '@playwright/test';

export class TradePage {
  readonly page: Page;
  readonly goldAmountInput;
  readonly orderTypeSelect;
  readonly totalPriceDisplay;
  readonly confirmButton;
  readonly successMessage;

  constructor(page: Page) {
    this.page = page;
    this.goldAmountInput = page.locator('input[name="amount"], [data-testid="gold-amount"]');
    this.orderTypeSelect = page.locator('select[name="order-type"], [data-testid="order-type"]');
    this.totalPriceDisplay = page.locator('[data-testid="total-price"], .total-price');
    this.confirmButton = page.locator('button:has-text("Confirm"), [data-testid="confirm-trade"]');
    this.successMessage = page.locator('[data-testid="success-message"], .alert-success');
  }

  async goto() {
    await this.page.goto('/trade');
  }

  async selectOrderType(type: 'buy' | 'sell') {
    await this.orderTypeSelect.selectOption({ label: type === 'buy' ? 'Buy' : 'Sell' });
  }

  async enterGoldAmount(amount: number) {
    await this.goldAmountInput.fill(amount.toString());
  }

  async confirmTrade() {
    await this.confirmButton.click();
  }

  async getTotalPrice() {
    const priceText = await this.totalPriceDisplay.textContent();
    return priceText ? parseFloat(priceText.replace(/[^\d.-]/g, '')) : 0;
  }

  async isTradeSuccessful() {
    return await this.successMessage.isVisible();
  }
}