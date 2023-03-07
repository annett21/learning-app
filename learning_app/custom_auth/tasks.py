from config.celery import app

@app.task
def ping():
    print("pong")
