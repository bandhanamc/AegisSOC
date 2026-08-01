from apscheduler.schedulers.background import BackgroundScheduler

from app.services.mitre_update_service import update_mitre



scheduler = BackgroundScheduler()



def start_scheduler():


    scheduler.add_job(

        update_mitre,

        trigger="interval",

        days=2,

        id="mitre_auto_update",

        replace_existing=True

    )


    scheduler.start()


    print(
        "MITRE scheduler started"
    )