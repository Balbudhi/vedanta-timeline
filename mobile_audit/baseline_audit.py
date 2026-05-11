#!/orcd/software/core/001/pkg/miniforge/24.3.0-0/bin/python

import argparse
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_PATH = SCRIPT_DIR / "baseline_results.json"
SCREENSHOT_ROOT = Path("/orcd/pool/008/eeshan/philosophy_articles/mobile_audit/screenshots")
BASE_URL = "http://127.0.0.1:8765/"
THINKER_ID = "sankara"

VIEWPORTS = {
    "iphone-14-pro": {"width": 393, "height": 852},
    "iphone-se": {"width": 375, "height": 667},
    "pixel-7": {"width": 412, "height": 915},
    "galaxy-s22": {"width": 390, "height": 844},
}


def ensure_dirs():
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    for slug in VIEWPORTS:
        (SCREENSHOT_ROOT / slug).mkdir(parents=True, exist_ok=True)


def shot_path(viewport_slug, flow_slug):
    return SCREENSHOT_ROOT / viewport_slug / f"{flow_slug}.png"


def wait_for_app(page):
    page.goto(BASE_URL, wait_until="networkidle", timeout=60000)
    page.locator(".topbar").wait_for(timeout=30000)
    page.locator(".thinker-dot").first.wait_for(timeout=30000)
    page.wait_for_timeout(800)


def save_shot(page, viewport_slug, flow_slug):
    page.screenshot(path=str(shot_path(viewport_slug, flow_slug)), full_page=False, animations="disabled")


def center_on_thinker(page, thinker_id):
    page.evaluate(
        """(id) => {
          const scroller = document.getElementById("timelineScroller");
          const dot = document.querySelector(`.thinker-dot[data-id="${id}"]`);
          if (!scroller || !dot) return;
          scroller.scrollTo({
            left: Math.max(0, dot.offsetLeft - ((scroller.clientWidth - dot.clientWidth) / 2)),
            top: Math.max(0, dot.offsetTop - ((scroller.clientHeight - dot.clientHeight) / 2)),
            behavior: "instant",
          });
        }""",
        thinker_id,
    )
    page.wait_for_timeout(500)


def scroll_timeline(page, ratio):
    page.evaluate(
        """(ratio) => {
          const scroller = document.getElementById("timelineScroller");
          if (!scroller) return;
          const maxTop = Math.max(0, scroller.scrollHeight - scroller.clientHeight);
          scroller.scrollTo({ top: Math.round(maxTop * ratio), behavior: "instant" });
        }""",
        ratio,
    )
    page.wait_for_timeout(500)


def tap_or_click(locator):
    try:
        locator.tap(timeout=10000)
    except Exception:
        locator.click(timeout=10000, force=True)


def open_thinker(page):
    center_on_thinker(page, THINKER_ID)
    tap_or_click(page.locator(f'.thinker-dot[data-id="{THINKER_ID}"] .label').first)
    page.locator('#detailPane[aria-hidden="false"]').wait_for(timeout=15000)
    page.locator("#detailContent .detail-hero").wait_for(timeout=15000)
    page.wait_for_timeout(600)


def open_article(page, slug):
    tap_or_click(page.locator("#articlesBtn"))
    page.locator('#articlesModal[aria-hidden="false"]').wait_for(timeout=15000)
    tap_or_click(page.locator(f'.article-row[data-slug="{slug}"]').first)
    page.locator('#dpPaneArticle:not([hidden])').wait_for(timeout=15000)
    page.locator("#dpArticleBody article").wait_for(timeout=20000)
    page.wait_for_timeout(900)


def expand_source_and_select(page):
    tap_or_click(page.locator('.dp-tab[data-pane="source"]'))
    page.locator('#dpPaneSource:not([hidden])').wait_for(timeout=15000)
    page.locator("#dpSourceTree").wait_for(timeout=15000)
    nested = page.locator("#dpSourceTree details.cst-group details.cst-group summary").first
    tap_or_click(nested)
    page.wait_for_timeout(600)
    leaf = page.locator("#dpSourceTree details.cst-group details.cst-group[open] .cst-leaf").first
    tap_or_click(leaf)
    page.wait_for_timeout(1200)


def topbar_metrics(page):
    return page.evaluate(
        """() => {
          const bar = document.querySelector(".topbar");
          if (!bar) return null;
          const r = bar.getBoundingClientRect();
          return { top: r.top, bottom: r.bottom, height: r.height, innerHeight: window.innerHeight };
        }"""
    )


def popover_metrics(page, selector):
    return page.evaluate(
        """(selector) => {
          const pop = document.querySelector(selector);
          if (!pop) return null;
          const r = pop.getBoundingClientRect();
          const topEl = document.elementFromPoint(window.innerWidth / 2, Math.max(0, window.innerHeight - 20));
          return {
            box: { top: r.top, left: r.left, right: r.right, bottom: r.bottom, width: r.width, height: r.height },
            topElementClass: topEl ? topEl.className : "",
            topElementText: topEl ? (topEl.textContent || "").slice(0, 80) : "",
          };
        }""",
        selector,
    )


def article_metrics(page):
    return page.evaluate(
        """() => ({
          inlineCitations: document.querySelectorAll("#dpArticleBody a.cite-link").length,
          superscripts: document.querySelectorAll("#dpArticleBody sup.cite-fn").length,
          listCount: document.querySelectorAll("#dpArticleBody ul, #dpArticleBody ol").length,
          tableCount: document.querySelectorAll("#dpArticleBody table").length
        })"""
    )


def run_viewport(browser, viewport_slug, viewport):
    ctx = browser.new_context(
        viewport=viewport,
        screen=viewport,
        is_mobile=True,
        has_touch=True,
        device_scale_factor=3,
        locale="en-US",
    )
    page = ctx.new_page()
    payload = {"flows": {}, "notes": []}

    def capture(flow_slug, fn):
        record = {"screenshot": str(shot_path(viewport_slug, flow_slug))}
        try:
            print(f"[{viewport_slug}] {flow_slug}")
            fn(record)
            record.setdefault("status", "ok")
        except Exception as exc:
            record["status"] = "failed"
            record["error"] = str(exc)
            payload["notes"].append(f"{flow_slug}: {exc}")
        save_shot(page, viewport_slug, flow_slug)
        payload["flows"][flow_slug] = record

    capture("timeline_initial", lambda rec: wait_for_app(page))
    capture("timeline_mid", lambda rec: (wait_for_app(page), scroll_timeline(page, 0.5)))
    capture("timeline_bottom", lambda rec: (wait_for_app(page), scroll_timeline(page, 1.0)))

    def topbar_filter(rec):
        wait_for_app(page)
        rec["metrics"] = {"before": topbar_metrics(page)}
        tap_or_click(page.locator("#filterBtn"))
        page.locator('#filterDrawer[aria-hidden="false"]').wait_for(timeout=15000)
        rec["metrics"]["after"] = topbar_metrics(page)

    capture("topbar_filter", topbar_filter)

    def topbar_search(rec):
        wait_for_app(page)
        count = page.locator('.topbar input[type="search"], .topbar [role="searchbox"], .topbar .search').count()
        rec["metrics"] = {"topbarSearchControls": count}
        rec["status"] = "missing" if count == 0 else "ok"
        if count == 0:
            payload["notes"].append("topbar_search: no search control exists inside `.topbar`.")

    capture("topbar_search", topbar_search)

    def topbar_network(rec):
        wait_for_app(page)
        rec["metrics"] = {"before": topbar_metrics(page)}
        tap_or_click(page.locator('.view-toggle-btn[data-view="network"]'))
        page.locator("body.view-network").wait_for(timeout=15000)
        rec["metrics"]["after"] = topbar_metrics(page)

    capture("topbar_network_toggle", topbar_network)

    capture("thinker_sankara", lambda rec: (wait_for_app(page), open_thinker(page)))

    def glossary_flow(rec):
        wait_for_app(page)
        open_thinker(page)
        term = page.locator('#detailContent .term').filter(has_text="brahman").first
        tap_or_click(term)
        page.locator(".glossary-popover").wait_for(timeout=15000)
        rec["metrics"] = popover_metrics(page, ".glossary-popover")

    capture("glossary_popover", glossary_flow)

    def citation_flow(rec):
        wait_for_app(page)
        open_thinker(page)
        tap_or_click(page.locator("#detailContent a.cite-link").first)
        page.locator(".citation-popover").wait_for(timeout=15000)
        rec["metrics"] = popover_metrics(page, ".citation-popover")

    capture("citation_popover", citation_flow)

    capture("article_hegel_intro", lambda rec: (wait_for_app(page), open_article(page, "hegel"), rec.update({"metrics": article_metrics(page)})))

    def hegel_blockquote(rec):
        wait_for_app(page)
        open_article(page, "hegel")
        quote = page.locator("#dpArticleBody blockquote").first
        quote.wait_for(timeout=15000)
        quote.scroll_into_view_if_needed(timeout=15000)
        page.wait_for_timeout(500)

    capture("article_hegel_blockquote", hegel_blockquote)

    def ramanuja_table(rec):
        wait_for_app(page)
        open_article(page, "ramanuja")
        table = page.locator("#dpArticleBody table").first
        table.wait_for(timeout=15000)
        table.scroll_into_view_if_needed(timeout=15000)
        page.wait_for_timeout(500)
        rec["metrics"] = popover_metrics(page, "#dpArticleBody table")

    capture("article_ramanuja_table", ramanuja_table)

    def primitive_lists(rec):
        wait_for_app(page)
        open_article(page, "primitive-graph")
        metrics = article_metrics(page)
        rec["metrics"] = metrics
        if metrics["listCount"] == 0:
            rec["status"] = "missing"
            payload["notes"].append("article_long_lists: `primitive-graph` list markdown did not become semantic `ul/ol` nodes.")
            fallback = page.get_by_text("1. It gives", exact=False).first
            fallback.wait_for(timeout=15000)
            fallback.scroll_into_view_if_needed(timeout=15000)
            page.wait_for_timeout(500)
            return
        lst = page.locator("#dpArticleBody ul, #dpArticleBody ol").first
        lst.scroll_into_view_if_needed(timeout=15000)
        page.wait_for_timeout(500)

    capture("article_long_lists", primitive_lists)

    def article_footnotes(rec):
        wait_for_app(page)
        open_article(page, "hegel")
        metrics = article_metrics(page)
        rec["metrics"] = metrics
        if metrics["superscripts"] == 0:
            rec["status"] = "missing"
            payload["notes"].append(f"article_footnotes: `hegel` has {metrics['inlineCitations']} inline cite links and no `sup.cite-fn` nodes.")
            cite = page.locator("#dpArticleBody a.cite-link").first
            cite.wait_for(timeout=15000)
            cite.scroll_into_view_if_needed(timeout=15000)
            page.wait_for_timeout(500)
            return
        sup = page.locator("#dpArticleBody sup.cite-fn").first
        sup.scroll_into_view_if_needed(timeout=15000)
        page.wait_for_timeout(500)

    capture("article_footnotes", article_footnotes)

    def source_flow(rec):
        wait_for_app(page)
        open_thinker(page)
        expand_source_and_select(page)

    capture("source_tab", source_flow)

    def network_flow(rec):
        wait_for_app(page)
        tap_or_click(page.locator('.view-toggle-btn[data-view="network"]'))
        page.locator("body.view-network").wait_for(timeout=15000)
        tap_or_click(page.locator("#networkLegendToggle"))
        page.wait_for_timeout(500)

    capture("network_view", network_flow)

    page.close()
    ctx.close()
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--viewport", action="append", choices=sorted(VIEWPORTS.keys()))
    args = parser.parse_args()

    ensure_dirs()
    selected = args.viewport or list(VIEWPORTS.keys())
    results = {"base_url": BASE_URL, "generated_at_epoch": time.time(), "results": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for viewport_slug in selected:
            results["results"][viewport_slug] = run_viewport(browser, viewport_slug, VIEWPORTS[viewport_slug])
        browser.close()
    RESULTS_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()
