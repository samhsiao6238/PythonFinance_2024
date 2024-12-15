# Pydantic 模型

<br>

## 說明

1. `Pydantic 模型` 是由 `Pydantic 庫` 提供的一種強類型 `數據驗證` 和 `數據解析`方法。 

<br>

2. `Pydantic` 是 `Python` 中的一個數據驗證和設置管理工具，用於處理和驗證來自多種數據源的數據。它的主要功能是通過 Python 的 `型別提示（type hints）` 定義數據結構，並對數據進行自動檢查和轉換，以確保數據的完整性和有效性。

<br>

3. `Pydantic` 模型通過使用 Python `類型提示` 和 `類型注解` 提供了一個簡潔而強大的方法來處理和驗證數據，是數據密集型應用程序中的一個極其有用的工具。 

<br>

## Pydantic 模型的功能與特點

1. 數據驗證：Pydantic 模型可以自動檢查和驗證數據，確保數據符合預期的格式和類型。例如，可以檢查字串是否符合特定的正則表達式，數字是否在特定範圍內等。

<br>

2. 數據轉換：Pydantic 模型可以自動將輸入數據轉換為合適的 Python 類型。例如，將字串轉換為日期類型，或將數字字串轉換為整數。

<br>

3. 數據解析：Pydantic 模型支持從字典、JSON 等數據格式中解析數據，並將其轉換為 Python 對象。

<br>

4. 錯誤報告：當數據驗證失敗時，Pydantic 會提供詳細的錯誤訊息，幫助開發者快速定位和修復問題。

<br>

5. 預設值和選填欄位：可以為模型欄位設置預設值，並定義哪些欄位是可選的，哪些欄位是必填的。

<br>

6. 數據嵌套：Pydantic 支持嵌套模型，允許模型的欄位本身是另一個 Pydantic 模型。

<br>

## Pydantic 模型的用途

1. API 數據驗證：在 Web API 開發中，Pydantic 模型可以用來驗證和解析用戶提交的請求數據，確保 API 接收到的是有效的數據。

<br>

2. 配置管理：用於處理應用程序的配置數據，確保配置數據符合預期格式並且沒有錯誤。

<br>

3. 資料庫對象：在 ORM（對象關係映射）中，Pydantic 模型可以用來定義資料庫表結構和驗證資料庫記錄。

<br>

4. 數據轉換和處理：適用於各種數據處理任務，包括將數據從一種格式轉換為另一種格式。

<br>

## 範例

1. 以下是一個簡單的 Pydantic 模型範例，用於定義和驗證用戶數據。

    ```python
    from pydantic import BaseModel, Field, EmailStr
    from datetime import date
    from typing import List, Optional

    class User(BaseModel):
        username: str
        email: EmailStr
        birthdate: Optional[date]
        interests: List[str] = []

    # 建立 User 對象
    user_data = {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "birthdate": "1990-01-01",
        "interests": ["coding", "music"]
    }

    user = User(user_data)
    print(user)
    ```

<br>

2. 在以上範例中，`User` 是一個 Pydantic 模型，它包含了 `username`、`email`、`birthdate` 和 `interests` 等欄位。當建立 `User` 對象時，Pydantic 會自動驗證並轉換輸入數據。

<br>

___

_END_