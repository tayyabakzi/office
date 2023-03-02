from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print("this is job")

def worker():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(job, 'interval', seconds=5)
    scheduler.add_job(job,  'cron', day_of_week= 'wed', hour=9, minute= 55)
    scheduler.start()