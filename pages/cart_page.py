import re

from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.item_names = page.get_by_test_id("cart-list").get_by_test_id("inventory-item-name")

    def expect_items(self, names: list[str]):
        expect(self.item_names).to_have_text(names)

    def checkout(self):
        self.page.get_by_test_id("checkout").click()
        expect(self.page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
