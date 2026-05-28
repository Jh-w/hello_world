# 📖 详细安装指南

## 目录
1. [使用GitHub Actions（推荐）](#使用github-actions推荐)
2. [本地安装](#本地安装)
3. [云服务部署](#云服务部署)

---

## 使用GitHub Actions（推荐）

GitHub Actions是最简单的部署方式，无需维护服务器。

### 第一步：准备Gmail

1. **启用Gmail的两步验证**（如果未启用）
   - 访问 https://myaccount.google.com/security
   - 点击"启用两步验证"
   - 按照步骤完成设置

2. **生成应用密码**
   - 再次访问 https://myaccount.google.com/security
   - 在"应用密码"中选择"邮件"和"Windows电脑"
   - Google会生成16位密码，**复制保存**（格式: `xxxx xxxx xxxx xxxx`）

### 第二步：获取NewsAPI密钥（可选）

如果想获取更多新闻源：

1. 访问 https://newsapi.org
2. 点击"Get API Key"
3. 注册账号
4. 复制你的API密钥

### 第三步：配置GitHub Secrets

1. 进入你的GitHub仓库：`https://github.com/Jh-w/hello_world`
2. 点击 **Settings（设置）** → **Secrets and variables（密钥和变量）** → **Actions**
3. 点击 **New repository secret（新建仓库密钥）**

创建以下密钥（大小写敏感）：

| 密钥名称 | 值 | 示例 |
|---------|-----|-------|
| `SENDER_EMAIL` | 你的Gmail地址 | `your-email@gmail.com` |
| `SENDER_PASSWORD` | Gmail应用密码 | `abcd efgh ijkl mnop` |
| `RECIPIENT_EMAIL` | 接收邮件的地址 | `your-email@gmail.com` |
| `NEWS_API_KEY` | NewsAPI密钥（可选） | `1a2b3c4d5e6f7g8h` |

#### 创建密钥步骤截图说明：
```
1. 点击 "New repository secret" 按钮
2. Name: SENDER_EMAIL
3. Secret: your-email@gmail.com
4. 点击 "Add secret"
5. 重复添加其他密钥...
```

### 第四步：验证工作流

1. 点击仓库中的 **Actions** 标签
2. 看到 **Daily AI Report** 工作流
3. 点击 **Run workflow** → **Run workflow** 来手动测试

检查运行日志：
- 点击最新的工作流运行
- 查看 **send-report** job的日志
- 查找 "✅ Email sent successfully!" 消息

### 第五步：修改发送时间（可选）

编辑 `.github/workflows/daily-report.yml` 文件：

```yaml
on:
  schedule:
    # 现在是每天 02:00 UTC（中国时间 10:00）
    # 想改为其他时间？修改下面的cron表达式
    - cron: '0 2 * * *'
```

**常见时间配置**：
- 中国上午10点：`0 2 * * *`（UTC+8）
- 中国晚上20点：`12 * * *`（UTC+8）
- 美国东部上午10点：`0 14 * * *`（EST/UTC-5）
- 欧洲中部上午10点：`0 8 * * *`（CET/UTC+1）

使用 [Cron表达式生成器](https://crontab.guru/) 来生成你需要的时间。

---

## 本地安装

想在自己的电脑上运行？跟随这些步骤。

### 系统要求
- Python 3.8+
- pip（Python包管理器）
- 互联网连接

### 第一步：克隆仓库

```bash
git clone https://github.com/Jh-w/hello_world.git
cd hello_world
```

### 第二步：创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 第三步：安装依赖

```bash
pip install -r requirements.txt
```

### 第四步：配置环境变量

```bash
# 复制模板文件
cp .env.example .env

# 编辑.env文件，填入你的配置
# 使用你喜欢的编辑器打开 .env
```

.env文件内容示例：
```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
RECIPIENT_EMAIL=your-email@gmail.com
NEWS_API_KEY=your_newsapi_key_here
EMAIL_HOUR=10
EMAIL_MINUTE=0
RESULTS_PER_QUERY=15
```

### 第五步：测试

#### 测试新闻收集：
```bash
python news_collector.py
```

你应该看到类似的输出：
```
Collecting news from Google News...
Collecting news from RSS feeds...

Collected 30 articles:

1. AI Sports Coach Helps Athletes Improve Performance
   Category: AI Sports Coach
   Source: Tech News
   URL: https://...
```

#### 测试邮件发送：
```bash
python email_sender.py
```

#### 一次性运行完整流程：
```bash
python scheduler.py once
```

你应该收到一封邮件！

### 第六步：设置定时运行（可选）

#### Windows - 使用任务计划程序

1. 按 `Win + R`，输入 `taskschd.msc`，按Enter
2. 点击 "Create Task"
3. 设置名称：`AI Report Daily`
4. 在 "Triggers" 标签页，创建新触发器，设置时间
5. 在 "Actions" 标签页，设置脚本路径

#### macOS/Linux - 使用cron

```bash
# 编辑crontab
crontab -e

# 添加这一行（每天上午10点运行）
0 10 * * * cd /path/to/hello_world && python scheduler.py once >> scheduler.log 2>&1
```

或使用systemd定时器（Linux）：

```bash
# 创建 /etc/systemd/system/ai-report.timer
# 创建 /etc/systemd/system/ai-report.service
# 启用: systemctl enable ai-report.timer
```

#### 持续运行方式

如果要让程序一直在后台运行（推荐用systemd或supervisor）：

```bash
# 使用 nohup（简单方式）
nohup python scheduler.py > scheduler.log 2>&1 &

# 或使用 screen（可断开连接）
screen -S ai_report
python scheduler.py
# 按 Ctrl+A 然后 D 来断开而保持运行
```

---

## 云服务部署

### 选项1：使用Heroku（已停止免费服务）

Heroku已停止免费计划。建议使用其他选项。

### 选项2：使用AWS Lambda

AWS Lambda可以免费运行（在限额内）。

1. 创建Lambda函数
2. 上传代码作为zip文件
3. 配置环境变量
4. 使用CloudWatch Events设置定时触发

### 选项3：使用腾讯云函数SCF

1. 访问 https://console.cloud.tencent.com/scf
2. 创建函数
3. 选择Python 3.9运行时
4. 上传代码
5. 配置触发器为定时触发（cron表达式）
6. 配置环境变量

### 选项4：使用阿里云函数计算

1. 访问 https://www.aliyun.com/product/fc
2. 创建函数
3. 选择Python运行时
4. 配置定时触发器
5. 部署

### 选项5：使用VPS（推荐）

购买便宜的VPS（如Linode、DigitalOcean、腾讯云轻量级服务器等）：

```bash
# SSH连接到VPS
ssh root@your-vps-ip

# 安装Python
apt update && apt install python3 python3-pip

# 克隆项目并安装依赖
git clone https://github.com/Jh-w/hello_world.git
cd hello_world
pip install -r requirements.txt

# 配置.env
nano .env

# 设置cron定时
crontab -e
# 添加: 0 10 * * * cd /root/hello_world && python scheduler.py once

# 或使用supervisor保持运行
apt install supervisor
# 配置supervisor...
```

---

## 故障排查

### 问题：邮件无法发送

**症状**：看到错误 `SMTPAuthenticationError`

**解决**：
1. ✅ 确认使用的是 **Gmail应用密码**，不是Gmail账户密码
2. ✅ 确认没有在密码中复制空格（应该是 `xxxxxxxxxxxx`）
3. ✅ 确认Gmail账户启用了两步验证
4. ✅ 尝试允许"不安全的应用访问"（不推荐）

### 问题：无法连接到Gmail服务器

**症状**：看到错误 `Connection refused` 或 `Timeout`

**解决**：
1. ✅ 检查网络连接
2. ✅ 检查防火墙是否阻止端口587
3. ✅ 尝试使用VPN

### 问题：没有收集到任何新闻

**症状**：邮件收到，但没有任何新闻内容

**解决**：
1. ✅ 检查搜索关键词是否正确
2. ✅ 运行 `python news_collector.py` 手动测试
3. ✅ 检查网络连接
4. ✅ 如使用NewsAPI，检查API密钥是否正确

### 问题：GitHub Actions运行失败

**症状**：在Actions日志中看到错误

**解决**：
1. ✅ 点击Failed job查看详细日志
2. ✅ 检查所有Secrets是否正确配置
3. ✅ 查找具体错误信息并搜索解决方案
4. ✅ 尝试手动运行 `Run workflow`

---

## 下一步

安装完成后，你可以：

- 📝 修改 `news_collector.py` 中的关键词
- 🎨 自定义 `email_sender.py` 中的邮件模板
- 🌐 添加更多RSS源
- 🔔 集成其他通知方式（微信、钉钉等）

祝你使用愉快！有问题欢迎提Issue 🎉
