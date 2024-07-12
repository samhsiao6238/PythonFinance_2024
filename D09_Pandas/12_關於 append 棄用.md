# append 棄用

<br>

## 差異

1. 程式碼。

    ```python
    # 新版：調用 pd 模組的 concat 方法
    trade = pd.concat(
        [trade, new_trade_df],
        ignore_index=True
    )

    # 舊版：調用 pd 物件的 append 方法，新版中要改為 _append
    trade = trade._append(
        new_trade,
        ignore_index=True
    )
    ```

<br>

## 新版

_改用 concat，語法略微不同_

<br>

1. 程式碼。

    ```python
    import pandas as pd

    # 建立一個空的 DataFrame
    trade = pd.DataFrame(
        columns=[
            '股票代號', '交易類型',
            '買入時間', '買入價格',
            '賣出時間', '賣出價格',
            '單位'
        ]
    )

    # 建立一個 Series 物件
    new_trade = pd.Series(
        {
            '股票代號': '2330', '交易類型': 'Buy',
            '買入時間': '2023-01-01', '買入價格': 100,
            '賣出時間': '2023- 01-02', '賣出價格': 110,
            '單位': 1
        }
    )

    # 將 Series 轉換為 DataFrame 並進行轉置，使其成為一r ow
    new_trade_df = new_trade.to_frame().T

    # 使用 concat 方法將新的 DataFrame 物件新增至原有 DataFrame 中
    trade = pd.concat(
        [trade, new_trade_df],
        ignore_index=True
    )

    # 列印
    print(trade)
    ```

<br>

## 舊版

_在新版的 Pandas 要使用 append 的時候要改用_

<br>

1. 範例程式碼。

    ```python
    import pandas as pd

    # 建立一個空的 DataFrame
    trade = pd.DataFrame(
        columns=[
            '股票代號', '交易類型',
            '買入時間', '買入價格',
            '賣出時間', '賣出價格',
            '單位'
        ]
    )

    # 建立一個 Series 物件
    new_trade = pd.Series(
        {
            '股票代號': '2330', '交易類型': 'Buy',
            '買入時間': '2023-01-01', '買入價格': 100,
            '賣出時間': '2023- 01-02', '賣出價格': 110,
            '單位': 1
        }
    )

    # 使用 append 方法將新的 Series 物件新增至 DataFrame 中
    trade = trade._append(
        new_trade,
        ignore_index=True
    )

    # 列印
    print(trade)
    ```

<br>

---

_END_