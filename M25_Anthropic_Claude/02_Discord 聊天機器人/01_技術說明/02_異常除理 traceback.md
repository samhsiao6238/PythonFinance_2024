# Python 內建庫 traceback


## 說明

1. Python 的 `traceback` 模組允許取得異常，並提供格式化異常堆疊跟踪訊息的工具，便於調試和日誌記錄，理解錯誤發生的位置和原因。


2. 簡單範例。

```python
# 引入模組
import traceback

# 定義一個會引發異常的函數
def faulty_function():
    # 這會引發 ZeroDivisionError
    return 1 / 0

try:
    faulty_function()
except Exception as e:
    # 捕獲並輸出完整的異常堆疊跟踪訊息
    print("捕獲到異常：")
    traceback.print_exc()

    # 或者，將異常堆疊跟踪訊息作為字串取得
    error_details = traceback.format_exc()
    print("異常詳情：")
    print(error_details)
```
