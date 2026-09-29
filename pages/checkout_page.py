import re

from playwright.sync_api import Page, expect


def money(text: str) -> float:
    """'Item total: $39.98' -> 39.98"""
    return float(re.sub(r"[^0-9.]", "", text))


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        # The real attribute names are camelCase (firstName), not first-name.
        self.page.get_by_test_id("firstName").fill(first_name)
        self.page.get_by_test_id("lastName").fill(last_name)
        self.page.get_by_test_id("postalCode").fill(postal_code)
        self.page.get_by_test_id("continue").click()
        expect(self.page).to_have_url(re.compile(r"/checkout-step-two\.html$"))

    def summary(self) -> dict:
        return {
            "items": self.page.get_by_test_id("cart-list").get_by_test_id("inventory-item-name").all_inner_texts(),
            "subtotal": money(self.page.get_by_test_id("subtotal-label").inner_text()),
            "tax": money(self.page.get_by_test_id("tax-label").inner_text()),
            "total": money(self.page.get_by_test_id("total-label").inner_text()),
        }

    def finish(self):
        self.page.get_by_test_id("finish").click()
        expect(self.page).to_have_url(re.compile(r"/checkout-complete\.html$"))
