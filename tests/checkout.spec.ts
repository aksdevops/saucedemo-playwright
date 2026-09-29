import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { InventoryPage } from '../pages/InventoryPage';
import { CartPage } from '../pages/CartPage';
import { CheckoutPage } from '../pages/CheckoutPage';

// Public demo credentials published on the SauceDemo login page. Overridable via env.
const USERNAME = process.env.SAUCE_USERNAME ?? 'standard_user';
const PASSWORD = process.env.SAUCE_PASSWORD ?? 'secret_sauce';

const PRODUCTS = ['Sauce Labs Backpack', 'Sauce Labs Bike Light'];
const TAX_RATE = 0.08; // Observed during exploratory testing (e.g. $49.99 -> $4.00 tax).

const round2 = (n: number) => Math.round(n * 100) / 100;

test.describe('Checkout - standard_user', () => {
  test.beforeEach(async ({ page }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.login(USERNAME, PASSWORD);
    await login.expectLoggedIn();
  });

  test('user can buy two products and totals are correct', async ({ page }) => {
    const inventory = new InventoryPage(page);
    const cart = new CartPage(page);
    const checkout = new CheckoutPage(page);

    // Prices are read from the UI, not hard-coded, so the test survives price changes.
    const prices: number[] = [];
    for (const name of PRODUCTS) {
      prices.push(await inventory.priceOf(name));
      await inventory.addToCart(name);
    }
    await expect(inventory.cartBadge).toHaveText(String(PRODUCTS.length));

    await inventory.openCart();
    await cart.expectItems(PRODUCTS);
    await cart.checkout();

    await checkout.fillCustomerInfo({ firstName: 'Akshay', lastName: 'Tester', postalCode: '10001' });

    const summary = await checkout.summary();
    const expectedSubtotal = round2(prices.reduce((a, b) => a + b, 0));
    expect(summary.items).toEqual(PRODUCTS);
    expect(summary.subtotal).toBeCloseTo(expectedSubtotal, 2);
    expect(summary.tax).toBeCloseTo(round2(expectedSubtotal * TAX_RATE), 2);
    expect(summary.total).toBeCloseTo(round2(summary.subtotal + summary.tax), 2);

    await checkout.finish();
    await expect(page.getByTestId('complete-header')).toHaveText('Thank you for your order!');
    // Cart must be emptied after a successful order.
    await expect(inventory.cartBadge).toHaveCount(0);
  });

  test('checkout step one blocks an empty first name', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.addToCart(PRODUCTS[0]);
    await inventory.openCart();
    await new CartPage(page).checkout();

    await page.getByTestId('continue').click();
    await expect(page.getByTestId('error')).toContainText('First Name is required');
    await expect(page).toHaveURL(/\/checkout-step-one\.html$/);
  });
});
