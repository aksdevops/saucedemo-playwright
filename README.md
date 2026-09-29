# SauceDemo checkout test (Playwright)

Automated E2E test for the SauceDemo checkout, made for the Tentwenty SQA assessment (Task C).

Flow: login → add 2 products → cart → checkout → check subtotal, tax (8%) and total → finish → check success message and empty cart.
There is also one small negative test: checkout is blocked when First Name is empty.

## Run it

Needs Node.js 20+.

```bash
npm install
npx playwright install chromium
npm test              # headless
npm run test:headed   # see the browser
npm run report        # open the HTML report
```

It also runs in GitHub Actions on every push (`.github/workflows/playwright.yml`).

Optional env vars: `BASE_URL`, `SAUCE_USERNAME`, `SAUCE_PASSWORD`. The defaults are the public demo values shown on the SauceDemo login page.

## Notes

- Locators use SauceDemo's `data-test` attributes (`getByTestId`, set up in `playwright.config.ts`). No CSS classes or XPath.
- Products are found by name, not position, so changing the sort order doesn't break the test.
- No fixed waits. The test only uses Playwright's built-in waiting and `expect()`.
- Prices are read from the page and the totals are calculated, so the test checks the maths instead of fixed numbers.
- Each test runs in a fresh browser context and logs in by itself.

## Limitations

- It runs against a public demo site, so if the site is down or changes, the test fails.
- Login goes through the UI every time. That's fine for 2 tests, but for more tests I'd save the login state once.
- The 8% tax is what I saw in the app, not a written requirement.
- Only Chromium + standard_user. The bugs I found (see my report) aren't asserted here yet.
