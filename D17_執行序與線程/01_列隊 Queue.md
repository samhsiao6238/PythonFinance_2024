# 隊列（Queue）

`隊列（Queue）` 也稱 `佇列`，在 `多執行緒（Multiple Threading）` 編程中常用於線程間的資料傳遞，以下是一個使用標準函式庫 `queue.Queue` 在多個執行緒間安全地傳遞訊息的範例。在這個例子中，建立一個生產者-消費者模型，其中生產者線程生成數據，並將其放入隊列中；消費者線程從隊列中取出數據並處理。

這種模式的好處包括：

- **線程安全性**： `Queue` 自動處理所有的鎖定，確保資料在任何時候只被一個線程所使用。
- **解耦生產者和消費者**：生產者只需將數據放入隊列，而不需要關心誰將消費這些數據；同樣，消費者只從隊列取數據，無需關心數據是如何產生的 。
- **平衡工作負載**：如果生產者產生數據的速度比消費者處理快，佇列會累積數據，反之則會等待，這自然地平衡了工作負載。

### 範例腳本

```python
import threading
import queue
import time

# 建立一個列隊實例
data_queue = queue.Queue()


# 定義生產者函數
def producer(queue, data):
    for item in data:
        print(f"生產者產生資料：{item}")
        # 將資料放入隊列
        queue.put(item)
        time.sleep(1)


# 定義消費者函數
def consumer(queue):
    while True:
        # 從佇列中取出數據
        item = queue.get()
        print(f"消費者處理資料：{item}")
        # 表示之前入隊的任務已經完成
        queue.task_done()
        if item == "結束":
            break
        time.sleep(2)


# 建立生產者和消費者線程
producer_thread = threading.Thread(
    target=producer,
    args=(data_queue, ["蘋果", "香蕉", "橘子", "結束"])
)
consumer_thread = threading.Thread(
    target=consumer,
    args=(data_queue,)
)

# 啟動執行緒
producer_thread.start()
consumer_thread.start()

# 等待所有任務完成
data_queue.join()
print("所有資料處理完成。")
```

在這個例子中，生產者線程產生了三種不同的水果名稱作為數據，並透過隊列傳遞給消費者線程。消費者執行緒逐一從隊列中取出資料並「處理」它們。最後一個數據「結束」用於告訴消費者沒有更多的數據需要處理，可以結束循環。

使用 `queue.Queue`在這裡的主要好處是它提供了一個線程安全的方式來交換訊息，避免了在生產者和消費者之間共享使用 `低階鎖` 的複雜性。這使得編寫多執行緒程式更加簡單、安全。

___

_END_