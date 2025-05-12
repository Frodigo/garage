const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

test.describe('Link Accessibility Tests', () => {
  let linksToTest;

  test.beforeAll(() => {
    const linksPath = path.join(__dirname, '..', 'links-to-test.json');
    linksToTest = JSON.parse(fs.readFileSync(linksPath, 'utf8'));
  });

  test('should render page header, not 404 error', async ({ page }) => {
    for (const link of linksToTest) {
      console.log(`Testing link: ${link}`);

      await page.goto(link);
      await page.waitForLoadState('domcontentloaded');

      const pageHeader = page.locator('.page-header');
      await expect(pageHeader).toBeVisible();
    }
  });
});
