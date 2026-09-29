# SauceDemo checkout test (Playwright + Python)

Automated E2E test for the SauceDemo checkout, made for the Tentwenty SQA assessment (Task C).

Flow: login → add 2 products → cart → checkout → check subtotal, tax (8%) and total → finish → check success message and empty cart.
There is also one small negative test: checkout is blocked when First Name is empty.

## Run it

Needs Python 3.10+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
pytest -v                # headless
pytest -v --headed       # see the browser
```

It also runs in GitHub Actions on every push (`.github/workflows/playwright.yml`).
Every run records a video of each test. To watch it: open the run in the **Actions** tab, scroll to **Artifacts**, download **test-videos** and open the `.webm` files.

Optional env vars: `SAUCE_USERNAME`, `SAUCE_PASSWORD`. The defaults are the public demo values shown on the SauceDemo login page.

## Structure

```
conftest.py          fixtures: data-test attribute + logged_in_page
pages/               small page objects (login, inventory, cart, checkout)
tests/               test_checkout.py
pytest.ini           base URL, browser, video for every test, trace/screenshot on failure
```

## Notes

- Locators use SauceDemo's `data-test` attributes (`get_by_test_id`). No CSS classes or XPath.
- Products are found by name, not position, so changing the sort order doesn't break the test.
- No fixed waits. Only Playwright's built-in waiting and `expect()`.
- Prices are read from the page and the totals are calculated, so the test checks the maths instead of fixed numbers.
- Each test gets a fresh browser context and logs in by itself.

## Limitations

- It runs against a public demo site, so if the site is down or changes, the test fails.
- Login goes through the UI every time. Fine for 2 tests; for more I'd save the login state once.
- The 8% tax is what I saw in the app, not a written requirement.
- Only Chromium + standard_user. The bugs I found (see my report) aren't asserted here yet.
