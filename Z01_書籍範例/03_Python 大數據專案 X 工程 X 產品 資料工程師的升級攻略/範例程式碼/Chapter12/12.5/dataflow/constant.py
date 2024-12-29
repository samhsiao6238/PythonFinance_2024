import datetime

DEFAULT_ARGS = {
    "owner": "FinMind",
    "retries": 1,
    "retry_delay": datetime.timedelta(
        minutes=1
    ),
    "start_date": datetime.datetime(
        2022, 1, 1
    ),
    "execution_timeout": datetime.timedelta(
        minutes=60
    ),
    "max_active_tasks": 10
}
MAX_ACTIVE_RUNS = 1
