# yfinance

<br>

1. 安裝 `yfinance` 套件。

    ```bash
    pip install yfinance
    ```

<br>

2. 更新套件。

    ```bash
    pip install yfinance --upgrade --no-cache-dir
    ```

<br>

3. 查看版本：可能出現警告，參考講義 SSL 部分的說明。

    ```python
    import yfinance as yf 
    print(yf.__version__)
    ```

<br>

## 基本用法

1. 導入庫

    ```python
    import yfinance as yf
    ```

<br>

2. 獲取單一個股資料

    ```python
    stock = yf.Ticker("AAPL")
    stock_info = stock.info
    price_available = 'regularMarketPrice' in stock_info
    yf_version, price_available, list(stock_info.keys())[:10]
    ```

<br>

3. 獲取多個股 `AAPL`、`MSFT`、`GOOGL` 即時價格

    ```python
    stocks = yf.Tickers("AAPL MSFT GOOGL")
    prices = {stock.ticker: stock.info['regularMarketPrice'] for stock in stocks.tickers}
    ```

<br>

4. 下載個股資料 Ticker


    ```python
    # 初始化
    nvda = yf.Ticker("NVDA")
    # 下載
    end_date = datetime(date.today().year,date.today().month,date.today().day)
    start_date = end_date - timedelta(365)
    stock_data = nvda.history(start=start_date,end=end_date)
    ```

<br>

5. 下載報表等資訊 Ticker：包含 `balance_sheet`、`dividends`、`earnings`等。

    ```python
    print(nvda.earnings_dates)
    ```

<br>

6. 批次下載股價資訊： NVDA、MSFT、AAPL。

    ```python
    tickers = ['NVDA','MSFT','AAPL']
    stocks = yf.Tickers(tickers)
    prices = stocks.history(start='2019-01-01',end='2023-10-12',interval='1wk')
    ```

<br>

7. 選擇權數據：Nvidia (NVDA)

    ```python
    nvda_option_chain = nvda.option_chain()
    nvda_put_options = nvda_option_chain.puts
    nvda_call_options = nvda_option_chain.calls
    ```

<br>

---

_END_