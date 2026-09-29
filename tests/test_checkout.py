import re

import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
TAX_RATE = 0.08  # seen during exploratory testing, e.g. $49.99 -> $4.00 tax


def test_buy_two_products_and_totals_are_correct(logged_in_page: Page):
    page = logged_in_page
    inventory = InventoryPage(page)
    cart = CartPage(page)
    checkout = CheckoutPage(page)

    # Read prices from the page instead of hard-coding them.
    prices = []
    for name in PRODUCTS:
        prices.append(inventory.price_of(name))
        inventory.add_to_cart(name)
    expect(inventory.cart_badge).to_have_text(str(len(PRODUCTS)))

    inventory.open_cart()
    cart.expect_items(PRODUCTS)
    cart.checkout()

    checkout.fill_customer_info("Akshay", "Tester", "10001")

    summary = checkout.summary()
    expected_subtotal = round(sum(prices), 2)
    assert summary["items"] == PRODUCTS
    assert summary["subtotal"] == pytest.approx(expected_subtotal, abs=0.001)
    assert summary["tax"] == pytest.approx(round(expected_subtotal * TAX_RATE, 2), abs=0.001)
    assert summary["total"] == pytest.approx(summary["subtotal"] + summary["tax"], abs=0.001)

    checkout.finish()
    expect(page.get_by_test_id("complete-header")).to_have_text("Thank you for your order!")
    # Cart should be empty after the order.
    expect(inventory.cart_badge).to_have_count(0)


def test_checkout_blocks_empty_first_name(logged_in_page: Page):
    page = logged_in_page
    inventory = InventoryPage(page)
    inventory.add_to_cart(PRODUCTS[0])
    inventory.open_cart()
    CartPage(page).checkout()

    page.get_by_test_id("continue").click()
    expect(page.get_by_test_id("error")).to_contain_text("First Name is required")
    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
