import { mkdir } from "node:fs/promises"
import path from "node:path"

import { expect, type Page, test } from "@playwright/test"

const snapshotsDir = path.join(
  process.cwd(),
  "test-results",
  "component-snapshots",
)

test.use({ viewport: { width: 1280, height: 900 } })

const captureSnapshot = async (
  testId: string,
  filename: string,
  page: Page,
) => {
  const locator = page.getByTestId(testId)
  await expect(locator).toBeVisible()
  await locator.scrollIntoViewIfNeeded()
  await locator.screenshot({ path: path.join(snapshotsDir, filename) })
}

test("users table component snapshots", async ({ page }) => {
  await mkdir(snapshotsDir, { recursive: true })
  await page.goto("/component-snapshots-users-table")
  await page.waitForLoadState("networkidle")
  await page.evaluate(() => document.fonts.ready)

  await captureSnapshot("users-table-default", "users-table-default.png", page)
  await captureSnapshot("users-table-empty", "users-table-empty.png", page)
  await captureSnapshot(
    "users-table-paginated",
    "users-table-paginated.png",
    page,
  )
})
