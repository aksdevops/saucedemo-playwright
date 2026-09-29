import { expect, type Page } from '@playwright/test';

export interface Customer {
  firstName: string;
  lastName: string;
  postalCode: string;
}

/** Parses "Item total: $45.98" / "Tax: $3.68" / "Total: $49.66" into a number. */
const money = (text: string) => Number(text.replace(/[^0-9.]/g, ''));

export class CheckoutPage {
  constructor(private readonly page: Page) {}

  async fillCustomerInfo(c: Customer) {
    // Note: the real attribute values are camelCase (firstName), not kebab-case.
    await this.page.getByTestId('firstName').fill(c.firstName);
    await this.page.getByTestId('lastName').fill(c.lastName);
    await this.page.getByTestId('postalCode').fill(c.postalCode);
    await this.page.getByTestId('continue').click();
    await expect(this.page).toHaveURL(/\/checkout-step-two\.html$/);
  }

  async summary() {
    return {
      items: await this.page.getByTestId('cart-list').getByTestId('inventory-item-name').allInnerTexts(),
      subtotal: money(await this.page.getByTestId('subtotal-label').innerText()),
      tax: money(await this.page.getByTestId('tax-label').innerText()),
      total: money(await this.page.getByTestId('total-label').innerText()),
    };
  }

  async finish() {
    await this.page.getByTestId('finish').click();
    await expect(this.page).toHaveURL(/\/checkout-complete\.html$/);
  }
}
