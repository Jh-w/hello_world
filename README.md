# 🤖 AI运动教练 & AI健康助手 日报系统

一个自动化的日报系统，每天早上10点收集关于"AI运动教练"和"AI健康助手"相关的全球新闻、资讯和文献，并发送到你的邮箱。

## ✨ 功能特性

- 📰 **多源数据收集**：Google News、NewsAPI、RSS订阅源
- 📧 **自动邮件发送**：精美的HTML格式，每天早上10点���送
- 🏷️ **智能分类**：按类别组织内容（AI运动教练/AI健康助手）
- 🌍 **多语言支持**：支持中英文资讯
- ⚙️ **灵活配置**：易于自定义搜索关键词和发送时间
- 🤖 **自动化部署**：使用GitHub Actions自动运行

## 🚀 快速开始

### 1. 配置环境变量

复制 `.env.example` 为 `.env`，并填入你的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# Gmail配置
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password  # 使用应用密码，不是Gmail密码
RECIPIENT_EMAIL=your_email@gmail.com

# NewsAPI密钥 (可选，从 https://newsapi.org 获取免费密钥)
NEWS_API_KEY=your_newsapi_key

# 发送时间（24小时格式）
EMAIL_HOUR=10
EMAIL_MINUTE=0

# 每个查询的结果数量
RESULTS_PER_QUERY=15
```

### 2. 配置Gmail App Password

如果使用Gmail，需要生成应用密码而不是用账户密码：

1. 访问 [Google Account Security](https://myaccount.google.com/security)
2. 启用两步验证（如果未启用）
3. 生成应用密码：https://support.google.com/accounts/answer/185833
4. 使用生成的密码作为 `SENDER_PASSWORD`

### 3. 本地测试

#### 安装依赖：
```bash
pip install -r requirements.txt
```

#### 测试收集新闻：
```bash
python news_collector.py
```

#### 测试发送邮件：
```bash
python email_sender.py
```

#### 一次性运行完整流程：
```bash
python scheduler.py once
```

### 4. 使用GitHub Actions自动运行

GitHub Actions会自动在每天早上10点（UTC+8）运行。

#### 配置Secrets：

1. 进入仓库 → Settings → Secrets and variables → Actions
2. 添加以下Secrets：
   - `SENDER_EMAIL`: 你的邮箱地址
   - `SENDER_PASSWORD`: Gmail应用密码
   - `RECIPIENT_EMAIL`: 接收邮件的地址
   - `NEWS_API_KEY`: NewsAPI密钥（可选）

3. 配置workflow文件 `.github/workflows/daily-report.yml` 中的时间（可选）

#### 手动触发：

在GitHub仓库的Actions标签页，点击"Daily AI Report"→"Run workflow"

### 5. 本地持续运行

如果要在本地计算机上持续运行：

```bash
python scheduler.py
```

这会在后台运行，每天在指定时间执行任务。

## 📁 项目结构

```
.
├── news_collector.py        # 新闻收集模块
├── email_sender.py          # 邮件发送模块
├── scheduler.py             # 定时任务调度器
├── requirements.txt         # Python依赖
├── .env.example            # 环境变量模板
├── .github/
│   └── workflows/
│       └── daily-report.yml # GitHub Actions工作流
└── README.md               # 本文件
```

## 🔧 自定义配置

### 修改搜索关键词

编辑 `news_collector.py` 中的 `keywords` 字典：

```python
self.keywords = {
    'AI Sports Coach': [
        'AI sports coach',
        'artificial intelligence fitness trainer',
        # 添加更多关键词...
    ],
    'AI Health Assistant': [
        'AI health assistant',
        'artificial intelligence healthcare',
        # 添加更多关键词...
    ]
}
```

### 修改发送时间

编辑 `.env` 文件中的时间配置：
- `EMAIL_HOUR`: 小时（0-23）
- `EMAIL_MINUTE`: 分钟（0-59）

或编辑 `.github/workflows/daily-report.yml` 中的cron表达式。

### 修改邮件模板

编辑 `email_sender.py` 中的 `format_html_report()` 方法来自定义邮件样式。

### 添加更多RSS源

编辑 `news_collector.py` 中的 `rss_feeds` 列表：

```python
self.rss_feeds = [
    'https://your-rss-feed-url',
    # 添加更多...
]
```

## 📊 数据来源

### Google News（推荐 - 无需API密钥）
- 实时新闻
- 覆盖全球

### NewsAPI（需要免费API密钥）
- 从300多个新闻源获取
- 访问 https://newsapi.org 获取免费密钥

### RSS订阅源
- Reuters、Bloomberg、TechCrunch等技术媒体
- Nature等学术出版社

## ⚠️ 注意事项

1. **API限制**：
   - Google News：无限制
   - NewsAPI Free：500请求/天
   - 请合理控制请求频率

2. **邮件限制**：
   - Gmail Free：每天最多发送100封邮件
   - 使用App Password而不是账户密码

3. **GitHub Actions**：
   - 免费账户：每月2000分钟
   - 定时任务可能晚5-10分钟执行

4. **数据更新**：
   - 每天早上10点收集过去24小时的新闻
   - 可根据需要调整搜索时间范围

## 🐛 故障排查

### 邮件无法发送
- ✅ 检查 `SENDER_EMAIL` 和 `SENDER_PASSWORD`
- ✅ 确认使用的是Gmail App Password而不是账户密码
- ✅ 检查网络连接

### 没有收集到任何新闻
- ✅ 检查搜索关键词是否正确
- ✅ 验证API密钥（如使用NewsAPI）
- ✅ 尝试手动运行 `python news_collector.py` 调试

### GitHub Actions运行失败
- ✅ 检查Secrets配置
- ✅ 查看Actions日志找出具体错误
- ✅ 确保所有必需的环境变量都已设置

## 📚 相关文档

- [NewsAPI官网](https://newsapi.org)
- [Google账户安全](https://myaccount.google.com/security)
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [APScheduler文档](https://apscheduler.readthedocs.io/)

## 📝 许可证

MIT License

## 💡 未来改进方向

- [ ] 支持微信/钉钉通知
- [ ] 添加内容分析和摘要生成
- [ ] 支持自定义邮件模板
- [ ] 添加邮件订阅管理
- [ ] 支持数据库存储历史记录
- [ ] 添加Web界面管理系统
- [ ] 支持多语言摘要

## 📧 反馈与支持

如有问题或建议，欢迎提Issue或发起Pull Request！

---

**最后更新**：2024年

祝你使用愉快！ 🎉
