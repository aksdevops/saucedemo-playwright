import re

from playwright.sync_api import Locator, Page, expect


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")

    def _card(self, product_name: str) -> Locator:
        # Find the product card by its name, not by its position in the list.
        name = self.page.get_by_test_id("inventory-item-name").get_by_text(product_name, exact=True)
        return self.page.get_by_test_id("inventory-item").filter(has=name)

    def price_of(self, product_name: str) -> float:
        text = self._card(product_name).get_by_test_id("inventory-item-price").inner_text()
        return float(text.replace("$", ""))

    def add_to_cart(self, product_name: str):
        card = self._card(product_name)
        card.get_by_role("button", name="Add to cart").click()
        # Button changes to "Remove" once the item is in the cart.
        expect(card.get_by_role("button", name="Remove")).to_be_visible()

    def open_cart(self):
        self.page.get_by_test_id("shopping-cart-link").click()
        expect(self.page).to_have_url(re.compile(r"/cart\.html$"))
