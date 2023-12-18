from celery import Celery

app = Celery(
    "task",
    # 只包含 tasks.py 裡面的程式, 才會成功執行
    include=["tasks"],
    # 連線到 rabbitmq,
    # pyamqp://user:password@rabbitmq_ip:5672/
    # 本書的帳號密碼都是 worker
    broker="pyamqp://worker:worker@127.0.0.1:5672/",
)
