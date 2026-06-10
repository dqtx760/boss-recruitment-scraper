# BOSS Recruitment Scraper - Setup Guide

## For First-Time Users (HR friends)

### What You Need

1. **A computer** (Windows/Mac) with Chrome browser installed
2. **A BOSS直聘 account** (free, register at zhipin.com)
3. **Python 3** installed (check: open terminal, type `python --version`)
4. **Claude Code** with the `web-access` skill enabled

### One-Time Setup (5 minutes)

#### 1. Install Python dependencies

Open terminal (PowerShell on Windows, Terminal on Mac) and run:

```bash
pip install requests
```

#### 2. Log into BOSS直聘 in Chrome

- Open Chrome, go to https://www.zhipin.com
- Click "登录/注册" (top right)
- Scan the QR code with WeChat or use phone verification
- Confirm you see the job search page with your profile

#### 3. Enable Chrome Remote Debugging

- In Chrome address bar, type: `chrome://inspect/#remote-debugging`
- Check the box: "Allow remote debugging for this browser instance"
- Restart Chrome if needed

### Each Time You Scrape

#### 1. Start CDP Proxy

In Claude Code, just say: "I want to scrape company X from BOSS直聘"

Claude will automatically handle the CDP proxy setup.

Or manually:
```bash
bash ~/.claude/skills/web-access/scripts/check-deps.sh
```

#### 2. Tell Claude the Company Name

Simply say: "帮我抓取XX公司的BOSS直聘招聘岗位"

Example: "帮我抓取宇树科技的BOSS直聘招聘岗位"

#### 3. Wait and Get Your CSV

The scraper will:
- Search for the company on BOSS直聘 (~5 seconds)
- Scroll through all job pages (~1-2 minutes per page)
- Save a CSV file to your desktop

Output file: `~/Desktop/<公司名>_BOSS招聘.csv`

### CSV Format

| 岗位名称 | 职位描述 | 薪资待遇 |
|---------|---------|---------|

Each row contains:
- **岗位名称**: Job title
- **职位描述**: Complete job description (responsibilities + requirements + bonus qualifications)
- **薪资待遇**: Salary (e.g., "25-40K·15薪")

### Troubleshooting

**"I get a login error"**
- Open Chrome and go to zhipin.com to verify you're still logged in
- Try logging out and logging back in
- Restart Chrome

**"It says 'no brand ID found'"**
- The company name might be slightly different on BOSS直聘
- Try searching the company manually on zhipin.com first to see the exact name
- Use the exact name shown on BOSS直聘

**"CSV file is empty or has wrong data"**
- Close any open Excel windows that might have the CSV file locked
- Re-run the scrape

**"CDP proxy not running"**
- Make sure Chrome remote debugging is enabled
- Restart Chrome
- Re-run: `bash ~/.claude/skills/web-access/scripts/check-deps.sh`

### Privacy & Legal Note

This tool uses YOUR logged-in BOSS直聘 account to access publicly posted job listings.
It does not bypass any paywalls or access private data.
Use responsibly and respect BOSS直聘's rate limits.
For personal/HR research use only.
