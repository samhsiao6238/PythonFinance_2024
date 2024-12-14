# Stocks

_以下說明 Stocks 的各種屬性_

<br>

## 訂閱行情

_通過 `subscribe` 函數可以輕鬆實現行情訂閱，僅需傳入目標合約（Contract）。_

<br>

1. 調用 `subscribe` 函數。

    ```python
    api.quote.subscribe(
        contract: shioaji.contracts.Contract,
        # 訂閱的行情類型，逐筆成交或五檔價量
        # `tick`（逐筆成交）、`bidask`（五檔價量）
        quote_type: shioaji.constant.QuoteType=<QuoteType.Tick: 'tick'>,
        # 是否訂閱盤中零股資訊
        intraday_odd: bool=False,
        # 行情數據格式版本，`v0`（舊版）、`v1`（新版）
        version: shioaji.constant.QuoteVersion=<QuoteVersion.v0: 'v0'>,
    )
    ```

<br>

2. 訂閱普通股票 `逐筆成交(Tick)`

    ```python
    api.quote.subscribe(
        api.Contracts.Stocks["2330"], 
        quote_type=sj.constant.QuoteType.Tick,
        version=sj.constant.QuoteVersion.v1
    )
    ```

    _輸出_

    ```bash
    Response Code: 200 | Event Code: 16 | Info: TIC/v1/STK/*/TSE/2330 | Event: Subscribe or Unsubscribe ok
    Exchange.TSE 
    Tick(
        code='2330', 
        datetime=datetime.datetime(2021, 7, 2, 13, 16, 35, 92970), 
        open=Decimal('590'), 
        avg_price=Decimal('589.05'), 
        close=Decimal('590'), 
        high=Decimal('593'), 
        low=Decimal('587'), 
        amount=Decimal('590000'), 
        total_amount=Decimal('8540101000'), 
        volume=1, 
        total_volume=14498, 
        tick_type=1, 
        chg_type=4, 
        price_chg=Decimal('-3'), 
        pct_chg=Decimal('-0.505902'), 
        bid_side_total_vol=6638, 
        ask_side_total_vol=7860
    )
    ```

<br>

3. 訂閱盤中零股逐筆成交。

    ```python
    api.quote.subscribe(
        api.Contracts.Stocks["2330"], 
        quote_type=sj.constant.QuoteType.Tick,
        version=sj.constant.QuoteVersion.v1,
        intraday_odd=True
    )
    ```

    _輸出_

    ```bash
    Response Code: 200 | Event Code: 16 | Info: TIC/v1/ODD/*/TSE/2330 | Event: Subscribe or Unsubscribe ok
    Exchange.TSE 
    Tick(
        code='2330', 
        datetime=datetime.datetime(2021, 7, 2, 13, 16, 55, 544646), 
        open=Decimal('591'), 
        avg_price=Decimal('590.24415'), 
        close=Decimal('590'), 
        high=Decimal('591'), 
        low=Decimal('589'), 
        amount=Decimal('276120'), 
        total_amount=Decimal('204995925'), 
        volume=468, 
        total_volume=347307
    )
    ```

<br>

4. BidAsk，訂閱普通股票五檔價量。

    ```python
    api.quote.subscribe(
        api.Contracts.Stocks["2330"], 
        quote_type=sj.constant.QuoteType.BidAsk,
        version=sj.constant.QuoteVersion.v1
    )
    ```

    _輸出_

    ```bash
    Response Code: 200 | Event Code: 16 | Info: QUO/v1/STK/*/TSE/2330 | Event: Subscribe or Unsubscribe ok
    Exchange.TSE 
    BidAsk(
        code='2330', 
        datetime=datetime.datetime(2021, 7, 1, 9, 9, 54, 36828), 
        bid_price=[Decimal('593'), Decimal('592'), Decimal('591')], 
        bid_volume=[248, 180, 258], 
        ask_price=[Decimal('594'), Decimal('595'), Decimal('596')], 
        ask_volume=[1457, 531, 506]
    )
    ```

<br>

5. 訂閱盤中零股五檔價量。

    ```python
    api.quote.subscribe(
        api.Contracts.Stocks["2330"], 
        quote_type=sj.constant.QuoteType.BidAsk,
        version=sj.constant.QuoteVersion.v1,
        intraday_odd=True
    )
    ```

    _輸出_

    ```bash
    Response Code: 200 | Event Code: 16 | Info: QUO/v1/ODD/*/TSE/2330 | Event: Subscribe or Unsubscribe ok
    Exchange.TSE 
    BidAsk(
        code='2330', 
        datetime=datetime.datetime(2021, 7, 2, 13, 17, 45, 743299), 
        bid_price=[Decimal('589'), Decimal('588')], 
        bid_volume=[59391, 224490], 
        ask_price=[Decimal('590'), Decimal('591')], 
        ask_volume=[26355, 9680]
    )
    ```

<br>

## Quote (綜合行情)

1. 訂閱綜合行情。

    ```python
    api.quote.subscribe(
        api.Contracts.Stocks["2330"], 
        quote_type=sj.constant.QuoteType.Quote,
        version=sj.constant.QuoteVersion.v1
    )
    ```

    _輸出_

    ```bash
    Response Code: 200 | Event Code: 16 | Info: QUO/v2/STK/*/TSE/2330 | Event: Subscribe or Unsubscribe ok
    Exchange.TSE 
    Quote(
        code='2330', 
        datetime=datetime.datetime(2022, 7, 1, 10, 43, 15, 430329), 
        open=Decimal('471.5'), 
        avg_price=Decimal('467.91'), 
        close=Decimal('461'), 
        high=Decimal('474'), 
        low=Decimal('461'), 
        amount=Decimal('461000'), 
        total_amount=Decimal('11834476000'), 
        volume=1, 
        total_volume=25292
    )
    ```

<br>

## 訂閱數據屬性

1. Tick

   - `code`: 商品代碼
   - `datetime`: 時間
   - `open`: 開盤價
   - `avg_price`: 均價
   - `close`: 成交價
   - `high`: 最高價
   - `low`: 最低價
   - `amount`: 成交額 (NTD)
   - `total_amount`: 總成交額 (NTD)
   - `volume`: 成交量
   - `tick_type`: 內外盤別（1: 外盤, 2: 內盤）
   - `chg_type`: 漲跌註記
   - `price_chg`: 漲跌價
   - `pct_chg`: 漲跌幅

<br>

2. BidAsk

   - `code`: 商品代碼
   - `datetime`: 時間
   - `bid_price`: 委買價列表
   - `bid_volume`: 委買量列表
   - `ask_price`: 委賣價列表
   - `ask_volume`: 委賣量列表

<br>

3. Quote

   - 包含 Tick 和 BidAsk 所有屬性，以及：
   - `closing_oddlot_shares`: 盤後零股成交股數
   - `fixed_trade_vol`: 定盤成交量

<br>

## 訂閱回調 (Callback)

1. 設定 Tick 回調，使用 Pythonic 裝飾器方式。

    ```python
    from shioaji import TickSTKv1, Exchange

    @api.on_tick_stk_v1()
    def tick_callback(exchange: Exchange, tick: TickSTKv1):
        print(f"Exchange: {exchange}, Tick: {tick}")
    ```

<br>

2. 傳統設定方式。

    ```python
    def tick_callback(exchange: Exchange, tick: TickSTKv1):
        print(f"Exchange: {exchange}, Tick: {tick}")
    api.quote.set_on_tick_stk_v1_callback(tick_callback)
    ```

<br>

3. 設定 BidAsk 回調。

    ```python
    @api.on_bidask_stk_v1()
    def bidask_callback(exchange: Exchange, bidask: BidAskSTKv1):
        print(f"Exchange: {exchange}, BidAsk: {bidask}")
    ```

<br>

4. 設定 Quote 回調。

    ```python
    @api.on_quote_stk_v1()
    def quote_callback(exchange: Exchange, quote: QuoteSTKv1):
        print(f"Exchange: {exchange}, Quote: {quote}")
    ```

<br>

_END_
