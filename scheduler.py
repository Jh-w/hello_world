"""
Scheduler Module
Runs the news collection and email sending at scheduled times
"""

import os
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from news_collector import NewsCollector
from email_sender import EmailSender

load_dotenv()

class ReportScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.email_hour = int(os.getenv('EMAIL_HOUR', 10))
        self.email_minute = int(os.getenv('EMAIL_MINUTE', 0))
        self.collector = NewsCollector()
        self.sender = EmailSender()
    
    def job_daily_report(self):
        """Job to collect news and send daily report"""
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting daily report job...")
        print(f"{'='*60}")
        
        try:
            # Collect news
            print("\n📰 Collecting news articles...")
            articles = self.collector.collect_all()
            
            if not articles:
                print("⚠️  No articles collected")
                return
            
            print(f"✅ Collected {len(articles)} articles")
            
            # Send email
            print("\n📧 Sending email report...")
            success = self.sender.send_report(articles)
            
            if success:
                print("✅ Daily report completed successfully!")
            else:
                print("❌ Failed to send email")
            
        except Exception as e:
            print(f"❌ Error in daily report job: {e}")
        
        print(f"{'='*60}\n")
    
    def start(self):
        """Start the scheduler"""
        # Schedule the job to run daily at specified time
        self.scheduler.add_job(
            self.job_daily_report,
            CronTrigger(hour=self.email_hour, minute=self.email_minute),
            id='daily_report',
            name='Daily AI Report',
            replace_existing=True
        )
        
        self.scheduler.start()
        print(f"✅ Scheduler started!")
        print(f"📅 Daily report scheduled for {self.email_hour:02d}:{self.email_minute:02d}")
        print(f"📬 Reports will be sent to: {self.sender.recipient_email}")
        
        # Keep the scheduler running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⛔ Scheduler stopped by user")
            self.scheduler.shutdown()
    
    def run_once(self):
        """Run the job once immediately (useful for testing)"""
        print("🚀 Running report job once...")
        self.job_daily_report()


if __name__ == '__main__':
    scheduler = ReportScheduler()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'once':
        # Test run: python scheduler.py once
        scheduler.run_once()
    else:
        # Normal run: python scheduler.py
        scheduler.start()
