#!/usr/bin/env python3
"""Pass-2 screenshot harness — captures the new search-popover, the
theme toggle, and the timeline in both light + dark across desktop +
iphone-se + iphone-13 + ipad-mini."""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "screenshots" / "2026-05-19-pass2"

URL = "http://127.0.0.1:8765/"

VIEWPORTS = {
    "desktop":    {"width": 1440, "height": 900,  "isMobile": False},
    "iphone-se":  {"width": 375,  "height": 667,  "isMobile": True},
    "iphone-13":  {"width": 390,  "height": 844,  "isMobile": True},
    "ipad-mini":  {"width": 768,  "height": 1024, "isMobile": True},
}


def shot(page, vp_slug, theme_slug, label):
    p = OUT / vp_slug / theme_slug
    p.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(p / f"{label}.png"), full_page=False, animations="disabled")


def errors_collector():
    errs = []
    return errs


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
            page.wait_for_timeout(180)
        else:
            page.evaluate("document.documentElement.removeAttribute('data-theme')")
            page.wait_for_timeout(180)

        shot(page, vp_slug, theme, "timeline")

        # Open search popover
        page.click("#searchBtn")
        page.wait_for_timeout(220)
        shot(page, vp_slug, theme, "search-popover-empty")
        page.fill("#searchPopInput", "atman")
        page.wait_for_timeout(220)
        shot(page, vp_slug, theme, "search-popover-atman")
        page.keyboard.press("Escape")
        page.wait_for_timeout(120)

        # Open a thinker detail
        try:
            page.click(".thinker-dot[data-id='sankara']", timeout=4000)
        except Exception:
            page.click(".thinker-dot", timeout=4000)
        page.wait_for_timeout(500)
        shot(page, vp_slug, theme, "detail-pane")
        # Close detail
        try:
            page.click("#closeDetail", timeout=2000)
        except Exception:
            pass
        page.wait_for_timeout(200)

    ctx.close()
    return errs


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        all_errs = {}
        for slug, vp in VIEWPORTS.items():
            print(f"[{slug}] running…", flush=True)
            errs = run_viewport(browser, slug, vp)
            all_errs[slug] = errs
            if errs:
                print(f"  {len(errs)} error(s):")
                for kind, msg in errs[:5]:
                    print(f"    {kind}: {msg[:240]}")
            else:
                print(f"  no errors")
        browser.close()


if __name__ == "__main__":
    main()
