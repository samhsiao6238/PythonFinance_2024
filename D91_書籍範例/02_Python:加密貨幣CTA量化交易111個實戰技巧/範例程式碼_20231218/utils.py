import lineTool
from config import line_token


def line_print(msg):
    print(msg)
    try:
        lineTool.lineNotify(line_token, msg)
    except Exception as e:
        print(f"line notify 失效：{e}")
