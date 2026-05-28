"""
Email Sender Module
Formats and sends daily reports via email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
    
    def format_html_report(self, articles: List[Dict]) -> str:
        """Format articles into a beautiful HTML report"""
        
        html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                    color: #333;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                .header {
                    text-align: center;
                    border-bottom: 3px solid #4CAF50;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }
                .header h1 {
                    margin: 0;
                    color: #2c3e50;
                    font-size: 28px;
                }
                .header p {
                    margin: 10px 0 0 0;
                    color: #7f8c8d;
                    font-size: 14px;
                }
                .article {
                    border-left: 4px solid #4CAF50;
                    padding: 15px;
                    margin-bottom: 20px;
                    background-color: #f9f9f9;
                    border-radius: 4px;
                }
                .article h3 {
                    margin-top: 0;
                    margin-bottom: 10px;
                    color: #2c3e50;
                    font-size: 16px;
                }
                .article-meta {
                    font-size: 12px;
                    color: #7f8c8d;
                    margin-bottom: 10px;
                }
                .article-category {
                    display: inline-block;
                    background-color: #4CAF50;
                    color: white;
                    padding: 3px 8px;
                    border-radius: 3px;
                    font-size: 11px;
                    margin-right: 10px;
                }
                .article-source {
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    padding: 3px 8px;
                    border-radius: 3px;
                    font-size: 11px;
                }
                .article-description {
                    color: #555;
                    line-height: 1.6;
                    font-size: 14px;
                    margin: 10px 0;
                }
                .article-link {
                    display: inline-block;
                    margin-top: 10px;
                    color: #4CAF50;
                    text-decoration: none;
                    font-weight: 500;
                }
                .article-link:hover {
                    text-decoration: underline;
                }
                .footer {
                    text-align: center;
                    border-top: 1px solid #ecf0f1;
                    padding-top: 20px;
                    margin-top: 40px;
                    color: #7f8c8d;
                    font-size: 12px;
                }
                .count {
                    color: #4CAF50;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 AI运动教练 & AI健康助手 日报</h1>
                    <p>Daily Report | """ + datetime.now().strftime("%Y年%m月%d日 %H:%M") + """</p>
                </div>
        """
        
        # Organize articles by category
        categories = {}
        for article in articles:
            category = article.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(article)
        
        # Add articles grouped by category
        for category, items in categories.items():
            html += f'<h2 style="color: #2c3e50; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px;">📌 {category} ({len(items)})</h2>'
            
            for i, article in enumerate(items, 1):
                published_at = article.get('published_at', 'Unknown date')
                if published_at:
                    try:
                        dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                        published_at = dt.strftime("%m-%d %H:%M")
                    except:
                        pass
                
                html += f"""
                <div class="article">
                    <h3>{i}. {article.get('title', 'Untitled')}</h3>
                    <div class="article-meta">
                        <span class="article-category">{article.get('category', 'Other')}</span>
                        <span class="article-source">{article.get('source_name', 'Unknown')}</span>
                        <span style="color: #95a5a6; margin-left: 10px;">📅 {published_at}</span>
                    </div>
                    <div class="article-description">
                        {article.get('description', 'No description available')[:200]}...
                    </div>
                    <a href="{article.get('url', '#')}" class="article-link">阅读全文 →</a>
                </div>
                """
        
        html += f"""
                <div class="footer">
                    <p>📊 本期共收集 <span class="count">{len(articles)}</span> 条相关资讯</p>
                    <p>✨ 此邮件由自动化系统生成 | 下次发送时间：明天早上10:00</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_report(self, articles: List[Dict]) -> bool:
        """Send the formatted report via email"""
        
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            print("Error: Email configuration is incomplete")
            return False
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = f"🤖 AI运动教练 & AI健康助手 日报 - {datetime.now().strftime('%Y年%m月%d日')}"
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            
            # Create text and HTML versions
            text = f"AI运动教练 & AI健康助手 日报\n\n共收集 {len(articles)} 条资讯\n\n请使用支持HTML的邮件客户端查看完整报告"
            html = self.format_html_report(articles)
            
            # Attach both versions
            part1 = MIMEText(text, 'plain', 'utf-8')
            part2 = MIMEText(html, 'html', 'utf-8')
            message.attach(part1)
            message.attach(part2)
            
            # Send email
            print(f"Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                print(f"Authenticating as {self.sender_email}...")
                server.login(self.sender_email, self.sender_password)
                print(f"Sending email to {self.recipient_email}...")
                server.send_message(message)
            
            print("✅ Email sent successfully!")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Error: SMTP authentication failed. Check your email and password.")
            print("   For Gmail, use an App Password: https://support.google.com/accounts/answer/185833")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False


if __name__ == '__main__':
    # Test email sending
    sender = EmailSender()
    
    # Sample articles for testing
    sample_articles = [
        {
            'title': 'Sample Article Title',
            'description': 'This is a sample article description',
            'url': 'https://example.com',
            'category': 'AI Sports Coach',
            'source_name': 'Tech News',
            'published_at': datetime.now().isoformat()
        }
    ]
    
    sender.send_report(sample_articles)
