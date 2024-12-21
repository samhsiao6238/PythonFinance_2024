# 使用規範 

_相關規定可參考 [官方說明](https://sinotrade.github.io/tutor/limit/)_

<br>

## API 流量限制

_過去 30 天透過 API的交易量_

<br>

1. 股票 (Stock)：`0` 每日流量限制 500MB，`1 - 1E` 每日流量限制 2GB，`> 1E` 每日流量限制 10GB。

<br>

2. 期貨 (Future)：`0` 每日流量限制 500MB；`1 - TXF 1000 張 / MXF 4000 張` 每日流量限制 2GB；`> TXF 1000 張 / MXF 4000 張` 每日流量限制 10GB。

<br>

3. 查詢流量狀態。

    ```python
    api.usage()
    ```

    _輸出_

    ```bash
    UsageStatus(
        # 當前連線數
        connections=1, 
        # 已用流量
        bytes=41343260, 
        # 每日流量上限
        limit_bytes=2147483648, 
        # 每日剩餘流量
        remaining_bytes=2106140388
    )
    ```

<br>

## 查詢次數限制

1. 數據相關 (Data)：包括：`credit_enquire`, `short_stock_sources`, `snapshots`, `ticks`, `kbars`；總次數限制為 `5 秒內不得超過 50 次查詢`；交易時間限制為 `ticks` 每次交易時段不得超過 10 次，`kbars` 每次交易時段不得超過 270 次。

<br>

2. 資產相關 (Portfolio)：包括：`list_profit_loss_detail`, `account_balance`, `list_settlements`, `list_profit_loss`, `list_positions`, `margin`；總次數限制：5 秒內不得超過 25 次查詢。

<br>

3. 委託相關 (Order)：包括：`place_order`, `update_status`, `update_qty`, `update_price`, `cancel_order`；總次數限制為 `10 秒內不得超過 500 次查詢`。

<br>

4. 訂閱相關 (Subscribe)：最大訂閱數量：`api.subscribe()` 不得超過 200 次。

<br>

## 連線與登入限制

1. 連線 (Connect)：同一個 SinoPac Securities person_id 最多只能同時建立 5 個連線；每次執行 `api.login()` 都會建立一個連線。

<br>

2. 登入 (Login)：每天最多登入 1000 次。

<br>

## 警告與後果

1. 流量超限：如果流量超過限制，市場數據（如 `ticks`, `snapshots`, `kbars`）的查詢將返回空值，但其他功能不受影響。

<br>

2. 次數超限：如果使用次數超過限制，服務將暫停 1 分鐘；如果同一天內多次超限，公司將暫時停用該 IP 和 ID 的使用權限。

<br>

3. 服務暫停：如果 ID 被停用，請聯繫 Shioaji 管理員恢復使用權限。

<br>

___

_END_