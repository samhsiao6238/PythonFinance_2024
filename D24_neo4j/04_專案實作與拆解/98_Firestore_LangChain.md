_尚未實測_

# Firestore + LangChain

1. 參考 [官網範例](https://api.python.langchain.com/en/latest/_modules/langchain_community/chat_message_histories/firestore.html)。

2. 這段程式碼定義一個名為 `FirestoreChatMessageHistory` 的類，用於在 Google Firestore 中儲存和管理聊天記錄。

<br>

## 程式碼逐行說明

1. Imports 和類定義。

    ```python
    # 導入需要的模組和類別
    from __future__ import annotations
    # 用於記錄日誌
    import logging
    # 類型檢查
    from typing import TYPE_CHECKING, List, Optional

    from langchain_core.chat_history import BaseChatMessageHistory
    from langchain_core.messages import (
        # 基礎類
        BaseMessage,
        messages_from_dict,
        messages_to_dict,
    )

    logger = logging.getLogger(__name__)

    if TYPE_CHECKING:
        from google.cloud.firestore import Client, DocumentReference
    ```

<br>

2. Firestore 客戶端初始化：如果 `firebase-admin` 模組未安裝，會引發錯誤。它確保 Firebase 應用僅初始化一次。

    ```python
    def _get_firestore_client() -> Client:
        try:
            import firebase_admin
            from firebase_admin import firestore
        except ImportError:
            raise ImportError(
                "Could not import firebase-admin python package. "
                "Please install it with `pip install firebase-admin`."
            )

        # For multiple instances, only initialize the app once.
        try:
            firebase_admin.get_app()
        except ValueError as e:
            logger.debug("Initializing Firebase app: %s", e)
            firebase_admin.initialize_app()

        return firestore.client()
    ```

<br>

3. FirestoreChatMessageHistory 類：這是核心類的定義，它繼承自 `BaseChatMessageHistory` 並添加了對 Firestore 的支持。`__init__` 方法初始化類實例並設置必要的參數。

    ```python
    class FirestoreChatMessageHistory(BaseChatMessageHistory):
        """Chat message history backed by Google Firestore."""

        def __init__(
            self,
            collection_name: str,
            session_id: str,
            user_id: str,
            firestore_client: Optional[Client] = None,
        ):
            self.collection_name = collection_name
            self.session_id = session_id
            self.user_id = user_id
            self._document: Optional[DocumentReference] = None
            self.messages: List[BaseMessage] = []
            self.firestore_client = firestore_client or _get_firestore_client()
            self.prepare_firestore()
    ```

<br>

4. 準備工作：準備 Firestore 客戶端，並加載現有的聊天記錄。

    ```python
        def prepare_firestore(self) -> None:
            self._document = self.firestore_client.collection(
                self.collection_name
            ).document(self.session_id)
            self.load_messages()
    ```

<br>

5. 從 Firestore 加載消息。

    ```python
        def load_messages(self) -> None:
            if not self._document:
                raise ValueError("Document not initialized")
            doc = self._document.get()
            if doc.exists:
                data = doc.to_dict()
                if "messages" in data and len(data["messages"]) > 0:
                    self.messages = messages_from_dict(data["messages"])
    ```

<br>

6. 將新消息添加到列表中並更新 Firestore。

    ```python
        def add_message(self, message: BaseMessage) -> None:
            self.messages.append(message)
            self.upsert_messages()
    ```

<br>

7. 將消息列表更新到 Firestore 文件中。

    ```python
        def upsert_messages(self, new_message: Optional[BaseMessage] = None) -> None:
            if not self._document:
                raise ValueError("Document not initialized")
            self._document.set(
                {
                    "id": self.session_id,
                    "user_id": self.user_id,
                    "messages": messages_to_dict(self.messages),
                }
            )
    ```

<br>

8. 除聊天記錄，並從 Firestore 刪除相應的文件。

    ```python
        def clear(self) -> None:
            self.messages = []
            if self._document:
                self._document.delete()
    ```

<br>

## 運行

1. 安裝必要的套件

    ```bash
    pip install firebase-admin
    pip install langchain-core
    ```

<br>

2. 設置 Firebase：在 Firebase 控制台建立一個項目，並生成服務帳戶密鑰文件。這個文件需要在程式碼中初始化 Firebase 應用。

<br>

3. 建立 `secrets.toml` 文件

    ```toml
    [secrets]
    FIREBASE_KEY = "/path/to/your/serviceAccountKey.json"
    ```

<br>

4. 初始化 Firebase 應用：在程式碼的開頭載入 `secrets.toml` 並初始化 Firebase 應用。

    ```python
    import os
    import toml
    from firebase_admin import credentials, initialize_app

    secrets = toml.load("secrets.toml")
    firebase_key = secrets["secrets"]["FIREBASE_KEY"]

    cred = credentials.Certificate(firebase_key)
    initialize_app(cred)
    ```

<br>

5. 測試 FirestoreChatMessageHistory。

    ```python
    if __name__ == "__main__":
        # 初始化 FirestoreChatMessageHistory
        chat_history = FirestoreChatMessageHistory(
            collection_name="chat_history",
            session_id="session_12345",
            user_id="user_12345"
        )
        
        # 添加消息
        message = BaseMessage(content="Hello, this is a test message.")
        chat_history.add_message(message)
        
        # 加載消息
        chat_history.load_messages()
        for msg in chat_history.messages:
            print(msg.content)
        
        # 清除消息
        chat_history.clear()
    ```

<br>

___

_END_