import { expect, type Locator, type Page } from '@playwright/test';

export class CartPage {
  readonly itemNames: Locator;

  constructor(private readonly page: Page) {
    this.itemNames = page.getByTestId('cart-list').getByTestId('inventory-item-name');
  }

  async expectItems(names: string[]) {
    await expect(this.itemNames).toHaveText(names, { useInnerText: true });
  }

  async checkout() {
    await this.page.getByTestId('checkout').click();
    await expect(this.page).toHaveURL(/\/checkout-step-one\.html$/);
  }
}
