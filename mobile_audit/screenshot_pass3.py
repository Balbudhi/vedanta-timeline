#!/usr/bin/env python3
"""Pass-3 screenshot harness — verifies the merged glossary popover
(search input inside the popover, not a separate popover) and the new
small-circle Theme + About icon buttons.

The previous pass2 harness exercised `#searchBtn` and `#searchPopInput`;
both selectors have been removed. The summon button is now `#glossaryBtn`,
and the search input is `.gp-search-input` inside `.glossary-popover`."""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "screenshots" / "2026-05-19-pass3"

URL = "http://127.0.0.1:8765/"

VIEWPORTS = {
    "desktop":    {"width": 1440, "height": 900, "isMobile": False},
    "iphone-se":  {"width": 375,  "height": 667, "isMobile": True},
}


def shot(page, vp_slug, theme_slug, label):
    p = OUT / vp_slug / theme_slug
    p.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(p / f"{label}.png"), full_page=False, animations="disabled")


def run_viewport(browser, vp_slug, vp):
    ctx = browser.new_context(
        viewport={"width": vp["width"], "height": vp["height"]},
        is_mobile=vp["isMobile"],
        has_touch=vp["isMobile"],
        device_scale_factor=2 if vp["isMobile"] else 1,
    )
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(("pageerror", str(e))))
    page.on("console", lambda msg: errs.append((msg.type, msg.text)) if msg.type == "error" else None)

    page.goto(URL, wait_until="networkidle", timeout=60000)
    page.locator(".topbar").wait_for(timeout=15000)
    page.locator(".thinker-dot").first.wait_for(timeout=15000)
    page.wait_for_timeout(700)

    for theme in ("light", "dark"):
        if theme == "dark":
            page.evaluate("document.documentElement.setAttribute('data-theme', 'dark')")
        else:
            page.evaluate("document.documentElement.removeAttribute('data-theme')")
        page.wait_for_timeout(200)

        shot(page, vp_slug, theme, "01_timeline")

        # Summon the glossary popover empty (search-focused).
        page.click("#glossaryBtn")
        page.wait_for_timeout(250)
        # Confirm: popover present, search input present, no separate .search-popover.
        assert page.locator(".glossary-popover").count() == 1, "glossary popover not present"
        assert page.locator(".glossary-popover .gp-search-input").count() == 1, "search input missing inside popover"
        assert page.locator(".search-popover").count() == 0, "stale standalone .search-popover element exists"
        shot(page, vp_slug, theme, "02_popover_summoned_empty")

        # Type a query; verify results render inside the popover body.
        page.fill(".glossary-popover .gp-search-input", "atman")
        page.wait_for_timeout(220)
        assert page.locator(".glossary-popover .gp-result").count() > 0, "no results for atman"
        shot(page, vp_slug, theme, "03_popover_search_atman")

        # Click first result -> term view inside the same popover.
        page.locator(".glossary-popover .gp-result").first.click()
        page.wait_for_timeout(220)
        assert page.locator(".glossary-popover").count() == 1, "popover closed instead of swapping content"
        assert page.locator(".glossary-popover .gp-term").count() == 1, "term view not rendered after click"
        shot(page, vp_slug, theme, "04_popover_term_after_search")

        # Close popover.
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)

        # Click an inline Sanskrit term directly (opens glossary popover with that term).
        # Use the first thinker dot, then look for a [data-term] in the detail pane.
        try:
            page.locator(".thinker-dot").first.click()
            page.wait_for_timeout(400)
            term_el = page.locator("[data-term]").first
            if term_el.count() > 0:
                term_el.click()
                page.wait_for_timeout(220)
                assert page.locator(".glossary-popover").count() == 1
                assert page.locator(".glossary-popover .gp-search-input").count() == 1, \
                    "term-click popover missing search input"
                shot(page, vp_slug, theme, "05_popover_term_click")
                page.keyboard.press("Escape")
                page.wait_for_timeout(150)
            page.click("#closeDetail")
            page.wait_for_timeout(150)
        except Exception as e:
            errs.append(("flow", f"term-click flow: {e}"))

        shot(page, vp_slug, theme, "06_topbar_buttons")

    ctx.close()
    return errs


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        all_errs = {}
        for slug, vp in VIEWPORTS.items():
            print(f"[{slug}] running...", flush=True)
            try:
                errs = run_viewport(browser, slug, vp)
            except Exception as e:
                print(f"  HARNESS FAILURE: {e}")
                errs = [("harness", str(e))]
            all_errs[slug] = errs
            if errs:
                print(f"  {len(errs)} error(s):")
                for kind, msg in errs[:6]:
                    print(f"    {kind}: {msg[:240]}")
            else:
                print("  ok")
        browser.close()
    any_err = any(all_errs.values())
    sys.exit(1 if any_err else 0)


if __name__ == "__main__":
    main()
