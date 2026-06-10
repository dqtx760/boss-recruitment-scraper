#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS直聘 公司岗位批量抓取工具 v2
用法:
  python boss_scraper.py <公司名> <brand_id> <target_id> [max_pages]
  python boss_scraper.py <公司名> --auto <target_id> [max_pages]

输出: CSV 到桌面: 岗位名称, 职位描述, 薪资待遇
"""
import requests, json, time, csv, sys, os, urllib.parse

CDP = "http://localhost:3456"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
PAGE_JS = os.path.join(SKILL_DIR, "extract_page.js")


def nav(target, url):
    requests.get(CDP + "/navigate", params={"target": target, "url": url}, timeout=15)


def ev(target, code, timeout=12, await_promise=False):
    url = CDP + "/eval?target=" + target
    if await_promise:
        url += "&awaitPromise=true"
    r = requests.post(url, data=code.encode(), timeout=timeout)
    try:
        return json.loads(r.text).get("value", "")
    except:
        return ""


def discover_brand_id(target, company_name):
    """Search BOSS直聘 for company and extract brand ID"""
    encoded = urllib.parse.quote(company_name)
    nav(target, f"https://www.zhipin.com/web/geek/job?query={encoded}&city=100010000")
    time.sleep(4)

    js = """
    (function() {
        var links = document.querySelectorAll('a[href*="gongsi"]');
        var results = [], seen = new Set();
        links.forEach(function(a) {
            var m = a.href.match(/gongsi\\/([^.]+)\\.html/);
            if (m && !seen.has(m[1])) {
                seen.add(m[1]);
                results.push({id: m[1], name: a.textContent.trim().substring(0, 50)});
            }
        });
        return JSON.stringify(results);
    })()
    """
    result = ev(target, js, 10)
    try:
        candidates = json.loads(result)
        for c in candidates:
            if company_name in c.get("name", ""):
                return c["id"]
        if candidates:
            return candidates[0]["id"]
    except:
        pass
    return None


def scrape_company(target, company_name, brand_id, max_pages=20):
    """Main scraping loop - uses JS-based click+extract for reliability"""
    BASE = f"https://www.zhipin.com/gongsi/job/{brand_id}.html"
    out = os.path.expanduser(f"~/Desktop/{company_name}_BOSS招聘.csv")

    with open(PAGE_JS, "r", encoding="utf-8") as f:
        page_js = f.read()

    all_jobs = []
    seen = set()

    for pg in range(1, max_pages + 1):
        nav(target, BASE + "?page=" + str(pg))
        time.sleep(4)

        print(f"Page {pg}: extracting...", flush=True, end=" ")
        raw = ev(target, page_js, timeout=180, await_promise=True)
        try:
            job_list = json.loads(raw)
        except:
            print("parse error, retrying once...", flush=True, end=" ")
            time.sleep(2)
            raw = ev(target, page_js, timeout=180, await_promise=True)
            try:
                job_list = json.loads(raw)
            except:
                print("still failed, skipping page")
                continue

        new = 0
        for j in job_list:
            name = j.get("n", "").strip()
            desc = j.get("d", "").strip()
            sal = j.get("s", "").strip()
            if name and len(name) < 120:
                key = name[:50]
                if key not in seen:
                    seen.add(key)
                    all_jobs.append([name, desc, sal])
                    new += 1

        print(f"{len(job_list)} found, {new} new, total {len(all_jobs)}", flush=True)

        # Save after each page
        with open(out, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["岗位名称", "职位描述", "薪资待遇"])
            w.writerows(all_jobs)

        if pg > 2 and new == 0:
            break

    return all_jobs


def main():
    if len(sys.argv) < 2:
        print("用法: python boss_scraper.py <公司名> <brand_id> <target_id> [max_pages]")
        print("      python boss_scraper.py <公司名> --auto <target_id> [max_pages]")
        sys.exit(1)

    company = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == "--auto":
        target = sys.argv[3]
        max_p = int(sys.argv[4]) if len(sys.argv) > 4 else 20
        print(f"[DISCOVER] Searching brand ID for: {company}")
        brand_id = discover_brand_id(target, company)
        if not brand_id:
            print("[ERROR] Could not find brand ID.")
            sys.exit(1)
        print(f"[FOUND] Brand ID: {brand_id}")
    else:
        brand_id = sys.argv[2]
        target = sys.argv[3]
        max_p = int(sys.argv[4]) if len(sys.argv) > 4 else 20

    print(f"[START] {company} (brand: {brand_id})")
    t0 = time.time()
    jobs = scrape_company(target, company, brand_id, max_p)
    elapsed = time.time() - t0

    out = os.path.expanduser(f"~/Desktop/{company}_BOSS招聘.csv")
    print(f"\n[DONE] {len(jobs)} jobs in {elapsed:.0f}s -> {out}")


if __name__ == "__main__":
    main()
