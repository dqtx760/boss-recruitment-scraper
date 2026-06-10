---
name: boss-recruitment-scraper
description: |
  Scrape ALL job listings from a company on BOSS直聘 (zhipin.com) and save to CSV.
  Outputs: 岗位名称, 职位描述, 薪资待遇 — matching the standard recruitment data format.
  
  Use this skill when the user:
  - Asks to "scrape jobs from BOSS直聘 for company X"
  - Says "帮我抓取XX公司的招聘岗位" or "拉一下XX的招聘数据"
  - Mentions "BOSS直聘 scrape", "智聘爬取", or company recruitment data extraction
  - Wants to batch-download all job postings from a specific company
  - Is an HR professional needing competitor recruitment analysis
  - Shares a company name and asks for their complete job listings with salaries
  
  Also use when the user references "boss-scraper", "recruitment scraper", or any variant
  of "grab all jobs from BOSS直聘". Even if they just say a company name followed by
  "招聘岗位" or "招什么人", check if they want a full scrape.
---

# BOSS Recruitment Scraper

Scrape complete job listings from any company on BOSS直聘. Takes a company name,
outputs a CSV with job titles, full descriptions, and salary info.

## Prerequisites

Before scraping, verify these dependencies are ready:

1. **CDP Proxy** - Chrome remote debugging must be accessible at `http://localhost:3456`
2. **BOSS直聘 Login** - The user's Chrome must be logged into zhipin.com
3. **Python 3** with `requests` library

Check CDP status:
```bash
curl -s http://localhost:3456/targets | head -1
```

If CDP is not running, start it:
```bash
bash ~/.claude/skills/web-access/scripts/check-deps.sh
```

If user is not logged into BOSS直聘, guide them to:
1. Open Chrome and go to https://www.zhipin.com
2. Log in via WeChat scan or phone verification
3. Confirm login by checking the page shows their profile (not a login screen)

## Scraping Workflow

### Step 1: Get the CDP target ID

Find an available browser tab, or create a new one:

```bash
curl -s "http://localhost:3456/new?url=https://www.zhipin.com"
```

Save the `targetId` from the response — use it for all subsequent CDP calls.

### Step 2: Discover the company's brand ID

Search for the company on BOSS直聘 and extract its brand ID:

```bash
# Navigate to search
curl -s "http://localhost:3456/navigate?target=<TARGET_ID>&url=https://www.zhipin.com/web/geek/job?query=<URL_ENCODED_COMPANY_NAME>&city=100010000"

# Wait for load, then extract brand ID
python -c "
import requests, json, time, urllib.parse
time.sleep(4)
company = '<COMPANY_NAME>'
js = '''
(function() {
    var links = document.querySelectorAll('a[href*=\"gongsi\"]');
    var results = [];
    links.forEach(function(a) {
        var m = a.href.match(/gongsi\\/([^.]+)\\.html/);
        if (m) results.push({id: m[1], name: a.textContent.trim().substring(0, 30)});
    });
    return JSON.stringify(results.slice(0, 5));
})()
'''
r = requests.post('http://localhost:3456/eval?target=<TARGET_ID>', data=js.encode(), timeout=10)
print(json.loads(r.text).get('value',''))
"
```

From the results, pick the matching brand ID (the hash string like `07b072ef03f6aac71XN629m-E1M~`).

### Step 3: Run the scraper

Use the bundled Python script with the discovered brand ID:

```bash
python <SKILL_DIR>/scripts/boss_scraper.py "<COMPANY_NAME>" <BRAND_ID> <TARGET_ID> [max_pages]
```

The script will:
1. Navigate to company jobs page: `https://www.zhipin.com/gongsi/job/<BRAND_ID>.html`
2. Go through each page (default: all pages until no new jobs)
3. Click each job card to load its full description
4. Extract: job name, full description, salary
5. Save incremental CSV to the desktop

**Parameters:**
- `COMPANY_NAME` - The company name (used for CSV filename)
- `BRAND_ID` - The brand ID hash from BOSS直聘 (e.g., `07b072ef03f6aac71XN629m-E1M~`)
- `TARGET_ID` - CDP browser target ID
- `max_pages` - Optional, max pages to scrape (default: 20)

### Step 4: Deliver the result

The CSV is saved to: `C:\Users\<USER>\Desktop\<COMPANY_NAME>_BOSS招聘.csv`

Format:
| 岗位名称 | 职位描述 | 薪资待遇 |
|---------|---------|---------|
| 大模型预训练研究员 | 1、聚焦机器人具身操纵场景... | 25-40K·15薪 |

Each job description includes: responsibilities, requirements, and bonus qualifications.

## Troubleshooting

**"No jobs found" or "Permission denied"**
- Check the CSV isn't open in Excel (close it first)
- Verify the brand ID is correct for the target company

**"Login required" / redirect to login page**
- Have the user log into BOSS直聘 in their Chrome first
- Re-run check-deps.sh and try again

**Extraction returns empty descriptions**
- Increase sleep time between clicks (edit `SLEEP_MS` in the scraper script)
- Check if BOSS直聘 has changed its page structure

**Company has multiple brand IDs**
- Some large companies have separate brand IDs for different divisions
- Run once per brand ID, or let the user choose the right one

## Known Company Brand IDs (Jun 2026)

For reference — these may expire:
- 智元机器人: `07b072ef03f6aac71XN629m-E1M~`
- 优必选: `57ec97d3367153eb1X173960GVY~`

## Performance

~30s per page. Companies with 100+ jobs typically complete in 3-5 minutes.

## Critical Implementation Notes

When using CDP eval with async JavaScript, ALWAYS add `&awaitPromise=true` to the URL:
```
/eval?target=ID          -> returns immediately (sync only)
/eval?target=ID&awaitPromise=true  -> waits for async to resolve
```

The BOSS直聘 company job listing page (`gongsi/job/`) does NOT use the CSS `active` class
on job cards. Use JavaScript `card.click()` rather than relying on `querySelector('.active')`.

If a page returns empty/parse error, retry once after 2s — transient page load issues are common.

## Files

- `scripts/boss_scraper.py` - Main scraper (v2: JS-based click+extract, auto-retry)
- `scripts/extract_page.js` - JS: click all job cards on a page, return JSON with {n,d,s}
- `scripts/extract_info.js` - JS: extract single active card's info (fallback/legacy)
- `scripts/count_cards.js` - JS: count `li.job-card-box` on current page
- `references/setup.md` - First-time setup guide for new users
