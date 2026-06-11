# BOSS Recruitment Scraper

一键抓取 BOSS直聘上任意公司的全部招聘岗位，输出标准 CSV（岗位名称 / 职位描述 / 薪资待遇）。

## 这是什么

一个 Claude Code Skill，让 AI 自动操控 Chrome 浏览器，从 BOSS直聘逐页提取指定公司的所有在招岗位。

输入公司名 → 自动搜索 → 发现公司页面 → 逐条点击展开详情 → 提取完整岗位描述 → 保存到桌面 CSV。

## 安装

1. 将整个文件夹复制到 `~/.claude/skills/boss-recruitment-scraper/`
2. 确保 Python 3 已安装：`pip install requests`
3. Chrome 需启用 Remote Debugging：地址栏输入 `chrome://inspect/#remote-debugging`，勾选"Allow remote debugging"
4. Chrome 中先登录 BOSS直聘（zhipin.com）

## 使用

在 Claude Code 中直接说：

```
帮我抓取智元机器人的BOSS直聘招聘岗位
```

或：

```
拉一下优必选的所有招聘数据
```

AI 会自动完成：
- 🔍 搜索公司，发现 Brand ID
- 📄 逐页翻页（最多 20 页）
- 👆 逐条点击岗位卡片展开详情
- 📝 提取：岗位名称 + 完整职位描述（含职责/要求/加分项）+ 薪资
- 💾 增量保存到桌面 CSV

## 输出格式

`~/Desktop/<公司名>_BOSS招聘.csv`

| 岗位名称 | 职位描述 | 薪资待遇 | 工作地址 |
|---------|---------|---------|---------|
| 大模型预训练研究员 | 聚焦机器人具身操纵场景，负责VLA相关算法... | 25-40K·15薪 | 上海浦东新区漕河泾康桥商务绿洲E2 |
| C++软件开发工程师 | 开发自研机器人操作系统，建设开发者平台... | 25-35K·15薪 | 上海浦东新区张江数采中心 |

## 依赖

- **Chrome**（需开启 Remote Debugging，端口 9223）
- **CDP Proxy**（由 `web-access` skill 自动启动）
- **Python 3** + `requests` 库
- **BOSS直聘账号**（免费注册，需在 Chrome 中保持登录态）

## 文件结构

```
├── SKILL.md                    # Skill 定义（触发规则 + 完整工作流）
├── README.md                   # 本文件
├── scripts/
│   ├── boss_scraper.py         # 主抓取脚本
│   ├── extract_page.js         # JS：逐条点击并提取整页数据
│   ├── extract_info.js         # JS：提取单个活跃卡片信息
│   └── count_cards.js          # JS：统计页面岗位卡片数
└── references/
    └── setup.md                # 详细首次配置指南
```

## 已验证公司

| 公司 | 抓取岗位数 | 耗时 |
|------|-----------|------|
| 智元机器人 | 185 | ~8 分钟 |
| 优必选 | 58 | ~2.5 分钟 |
| 宇树科技 | 290+ | ~10 分钟 |

## 注意事项

- 需要 Chrome 保持 BOSS直聘登录态
- 抓取过程中请勿操作 Chrome 中的 BOSS直聘页面
- CSV 保存时请关闭 Excel 避免文件锁定
- BOSS直聘页面结构可能变化，如遇问题请提 Issue

## License

MIT
