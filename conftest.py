import os

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage

# Public demo credentials shown on the SauceDemo login page. Can be overridden with env vars.
USERNAME = os.getenv("SAUCE_USERNAME", "standard_user")
PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")


@pytest.fixture(scope="session", autouse=True)
def use_data_test_attribute(playwright):
    # SauceDemo puts data-test="..." on its elements, so get_by_test_id() uses that.
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    login = LoginPage(page)
    login.open()
    login.login(USERNAME, PASSWORD)
    login.expect_logged_in()
    return page
