import re

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/")

    def login(self, username: str, password: str):
        self.page.get_by_test_id("username").fill(username)
        self.page.get_by_test_id("password").fill(password)
        self.page.get_by_test_id("login-button").click()

    def expect_logged_in(self):
        expect(self.page).to_have_url(re.compile(r"/inventory\.html$"))
        expect(self.page.get_by_test_id("title")).to_have_text("Products")
