import shioaji as sj

print(sj.__version__)

# 初始化 Shioaji API
def init_Shioaji(simulation=True):
    try:
        # 預設模擬環境，可顯式設置為正式環境
        api = sj.Shioaji(simulation=simulation)
        print("Shioaji API 初始化成功。")
        return api
    except Exception as e:
        print(f"Shioaji API 初始化失敗：{e}")
        return None

# 載入環境變數
def load_env_variables():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.environ["API_KEY"]
    secret_key = os.environ["SECRET_KEY"]
    if not api_key or not secret_key:
        raise ValueError(
            "API_KEY 或 SECRET_KEY 環境變數缺失，"
            "請檢查 .env 文件。"
        )
    return api_key, secret_key

# 檢查登入狀態
def check_login_status(api):
    try:
        accounts = api.list_accounts()
        if accounts:
            return True
        return False
    except AttributeError:
        return False
    except Exception as e:
        print(f"檢查登入狀態時發生錯誤：{e}")
        return False

# 登入帳號並檢查是否已登入
def login_Shioaji(
    api=None,
    api_key=None, 
    secret_key=None, 
    simulation=True
):
    try:
        # 確保 API 已初始化
        if api is None:
            print("API 尚未初始化，正在初始化 Shioaji API...")
            api = init_Shioaji(simulation=simulation)
            if api is None:
                print("API 初始化失敗，無法登入。")
                return None

        # 如果未傳入 API Key 或 Secret Key，則嘗試載入環境變數
        if not api_key or not secret_key:
            print("API Key 或 Secret Key 尚未提供，正在嘗試載入環境變數...")
            try:
                api_key, secret_key = load_env_variables()
                print("成功載入環境變數。")
            except Exception as e:
                print(f"載入環境變數失敗，請確認 .env 文件是否存在且正確：{e}")
                return None

        # 調用自訂函數檢查是否已登入
        if check_login_status(api):
            print("已登入，無需重新登入。")
            return api

        # 如果尚未登入，執行登入
        print("尚未登入，嘗試登入中...")
        try:
            accounts = api.login(
                api_key=api_key, 
                secret_key=secret_key
            )
            print("登入成功，帳號資訊：", accounts)
            return api
        except Exception as e:
            print(f"登入失敗，請檢查憑據或網絡狀態：{e}")
            return None

    except Exception as e:
        print(f"Shioaji API 初始化或登入過程中發生錯誤：{e}")
        return None

# 檢查簽署狀態
def check_unsigned_accounts(api):
    # 取得全部帳號
    accounts = api.list_accounts()
    if accounts:
        print(f"已登入，共有 {len(accounts)} 個帳戶。")
    else:
        print("未登入。")
        # 若未登入則直接返回
        return
    # 檢查未簽署的帳號
    unsigned_accounts = [
        account 
        for account in accounts 
        if not getattr(account, 'signed', False)
    ]

    if unsigned_accounts:
        print("未完成簽署的帳號:")
        for account in unsigned_accounts:
            print(
                f"person_id='{account.person_id}' "
                f"broker_id='{account.broker_id}' "
                f"account_id='{account.account_id}' "
                f"username='{account.username}'"
            )

        # 嘗試執行其他方式
        for account in unsigned_accounts:
            print(
                f"請手動簽署帳號 {account.account_id} "
                "或檢查 API 文件。"
            )
    else:
        print("所有帳號已完成簽署。")

# 登出全部連線
def logout_all_connections(api, reset_api=True):
    try:
        # 檢查是否已登入
        if not check_login_status(api):
            print("未偵測到登入帳戶，無需登出。")
            # 返回原始 API 實例以繼續操作
            return api

        print("已登入，正在執行登出操作...")
        try:
            # 執行登出操作
            api.logout()
            print("登出成功，所有連線已釋放。")
        except Exception as e:
            print(f"登出失敗：{e}")
            # 如果登出失敗，返回原始 API 實例
            return api

        # 根據參數選擇是否重置 API 實例
        if reset_api:
            print("正在重置 API 實例...")
            # 重新初始化 API
            api = sj.Shioaji()
            print("API 實例已重置，並準備重新使用。")
        else:
            print("選擇不重置 API 實例，登出後保留原始 API。")
        # 返回重置後的或原始的 API
        return api

    except Exception as e:
        print(f"登出過程中發生錯誤：{e}")
        return None

def check_contracts_status(api):
    try:
        print(f"商品檔狀態：{api.Contracts.status}")
    except AttributeError:
        print("商品檔尚未初始化。")

def manual_subscribe_trade(api):
    try:
        api.subscribe_trade()
        print("已手動訂閱成交回報")
    except Exception as e:
        print(f"手動訂閱成交回報時發生錯誤：{e}")

def activate_ca(api):
    import os
    try:
        # 這裡使用 `get` 方法處理環境變數
        ca_path = os.environ.get("CA_CERT_PATH")
        ca_passwd = os.environ.get("CA_PASSWORD")

        # 檢查是否取得到必要的憑證資訊
        if not ca_path or not ca_passwd:
            print(
                "未找到 CA 憑證資訊，"
                "請檢查環境變數是否正確設置。"
            )
            return False

        # 啟用 CA
        api.activate_ca(
            ca_path=ca_path,
            ca_passwd=ca_passwd
        )
        print("CA 啟用成功")
        return True
    except Exception as e:
        print(f"CA 啟用失敗：{e}")
        return False

