import re

from playwright.sync_api import Page, expect


def test_dashboard_presents_quality_metrics(page: Page, base_url: str) -> None:
    page.goto(base_url)

    expect(page).to_have_title("Data QA Lab")
    expect(page.get_by_test_id("api-status")).to_have_text(
        "API y PostgreSQL conectados"
    )
    expect(page.get_by_test_id("total-transactions")).to_have_text(
        re.compile(r"4[.\s]?825")
    )
    expect(page.get_by_test_id("inconsistent-transactions")).to_have_text("200")
    expect(page.get_by_test_id("inconsistency-rate")).to_have_text("4.15%")
    expect(page.get_by_test_id("without-items")).to_have_text("100")
    expect(page.get_by_test_id("transactions-body").locator("tr")).to_have_count(20)


def test_inconsistent_filter_updates_visible_rows(page: Page, base_url: str) -> None:
    page.goto(base_url)

    page.get_by_label("Sólo inconsistentes").check()
    rows = page.get_by_test_id("transactions-body").locator("tr")
    expect(rows).to_have_count(20)
    expect(rows.locator(".badge-error")).to_have_count(20)
    expect(rows.locator(".badge-ok")).to_have_count(0)
