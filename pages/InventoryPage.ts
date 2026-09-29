import { expect, type Locator, type Page } from '@playwright/test';

export class InventoryPage {
  readonly cartBadge: Locator;

  constructor(private readonly page: Page) {
    this.cartBadge = page.getByTestId('shopping-cart-badge');
  }

  /** Product card located by its visible name (not by list position). */
  private card(productName: string): Locator {
    return this.page
      .getByTestId('inventory-item')
      .filter({ has: this.page.getByTestId('inventory-item-name').getByText(productName, { exact: true }) });
  }

  /** Reads the price shown on the product card, e.g. "$29.99" -> 29.99. */
  async priceOf(productName: string): Promise<number> {
    const text = await this.card(productName).getByTestId('inventory-item-price').innerText();
    return Number(text.replace('$', ''));
  }

  async addToCart(productName: string) {
    const card = this.card(productName);
    await card.getByRole('button', { name: 'Add to cart' }).click();
    // The button toggles to "Remove" once the item is in the cart.
    await expect(card.getByRole('button', { name: 'Remove' })).toBeVisible();
  }

  async openCart() {
    await this.page.getByTestId('shopping-cart-link').click();
    await expect(this.page).toHaveURL(/\/cart\.html$/);
  }
}
