# 拓展前一個範例

_重寫前一個範例，用於儲存和管理用戶活動日誌（Activity Logs），而不是聊天記錄。_

<br>

## 範例：Firestore Activity Log Management

1. `from __future__ import annotations` 是 Python 3.7 引入的一個功能，並在 Python 3.9 中變成正式功能，這個語句主要用於在函數或方法的類型註釋中延遲類型檢查，從而允許在類中使用尚未定義的類型。

<br>

2. 程式碼

    ```python
    """Firestore 活動日誌管理。"""
    from __future__ import annotations

    import logging
    from typing import TYPE_CHECKING, List, Optional

    from langchain_core.activity_log import BaseActivityLog
    from langchain_core.logs import (
        BaseLog,
        logs_from_dict,
        logs_to_dict,
    )

    logger = logging.getLogger(__name__)

    if TYPE_CHECKING:
        from google.cloud.firestore import Client, DocumentReference


    def _get_firestore_client() -> Client:
        try:
            import firebase_admin
            from firebase_admin import firestore
        except ImportError:
            raise ImportError(
                "無法導入 firebase-admin python 套件。"
                "請使用`pip install firebase-admin` 安裝它。"
            )

        # 對於多個實例，僅初始化應用程式一次
        try:
            firebase_admin.get_app()
        except ValueError as e:
            logger.debug("Initializing Firebase app: %s", e)
            firebase_admin.initialize_app()

        return firestore.client()


    class FirestoreActivityLog(BaseActivityLog):
        """由 Google Firestore 支援的活動日誌管理"""

        def __init__(
            self,
            collection_name: str,
            session_id: str,
            user_id: str,
            firestore_client: Optional[Client] = None,
        ):
            """
            初始化 FirestoreActivityLog 類別的新實例。

            :param collection_name：要使用的集合的名稱。
            :param session_id：活動的會話 ID。
            :param user_id：活動的使用者 ID。
            """
            self.collection_name = collection_name
            self.session_id = session_id
            self.user_id = user_id
            self._document: Optional[DocumentReference] = None
            self.logs: List[BaseLog] = []
            self.firestore_client = firestore_client or _get_firestore_client()
            self.prepare_firestore()

        def prepare_firestore(self) -> None:
            """Prepare the Firestore client.

            Use this function to make sure your database is ready.
            """
            self._document = self.firestore_client.collection(
                self.collection_name
            ).document(self.session_id)
            self.load_logs()

        def load_logs(self) -> None:
            """Retrieve the logs from Firestore"""
            if not self._document:
                raise ValueError("Document not initialized")
            doc = self._document.get()
            if doc.exists:
                data = doc.to_dict()
                if "logs" in data and len(data["logs"]) > 0:
                    self.logs = logs_from_dict(data["logs"])

        def add_log(self, log: BaseLog) -> None:
            self.logs.append(log)
            self.upsert_logs()

        def upsert_logs(self, new_log: Optional[BaseLog] = None) -> None:
            """Update the Firestore document."""
            if not self._document:
                raise ValueError("Document not initialized")
            self._document.set(
                {
                    "id": self.session_id,
                    "user_id": self.user_id,
                    "logs": logs_to_dict(self.logs),
                }
            )

        def clear(self) -> None:
            """Clear session logs from this memory and Firestore."""
            self.logs = []
            if self._document:
                self._document.delete()


    # 測試範例
    if __name__ == "__main__":
        # 初始化 FirestoreActivityLog
        activity_log = FirestoreActivityLog(
            collection_name="activity_logs",
            session_id="session_12345",
            user_id="user_12345"
        )

        # 添加活動記錄
        log = BaseLog(content="User logged in.")
        activity_log.add_log(log)

        # 加載活動記錄
        activity_log.load_logs()
        for log in activity_log.logs:
            print(log.content)

        # 清除活動記錄
        activity_log.clear()
    ```

<br>

## 操作與代碼說明

1. 安裝必要的套件。

    ```bash
    pip install firebase-admin
    pip install langchain-core
    ```

<br>

2. 導入需要的模組和類別。

    ```python
    from __future__ import annotations

    import logging
    # 用於類型檢查
    from typing import TYPE_CHECKING, List, Optional
    # 自定義的基礎類別
    from langchain_core.activity_log import BaseActivityLog
    from langchain_core.logs import (
        # 用於記錄日誌
        BaseLog,
        logs_from_dict,
        logs_to_dict,
    )
    ```

<br>

3. Firestore 客戶端初始化。

    ```python
    # 初始化 Firebase 客戶端
    def _get_firestore_client() -> Client:
        try:
            import firebase_admin
            from firebase_admin import firestore
        # 如果 `firebase-admin` 模組未安裝，會引發錯誤
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

4. FirestoreActivityLog 類：用於管理活動記錄的類，繼承自 `BaseActivityLog`。

   - `__init__` 初始化類實例並設置必要的參數。
   - `prepare_firestore()` 準備 Firestore 客戶端並加載現有的活動記錄。
   - `load_logs()` 從 Firestore 加載活動記錄。
   - `add_log()` 將新活動記錄添加到列表中並更新 Firestore。
   - `upsert_logs()` 將活動記錄列表更新到 Firestore 文件中。
   - `clear()` 清除活動記錄，並從 Firestore 刪除相應的文件。

<br>


## 設置 Firebase

_在 Firebase 控制台創建一個項目，並生成服務帳戶密鑰文件。_

<br>

## 敏感資訊

1. 創建 secrets.toml 文件

   ```toml
   [secrets]
   FIREBASE_KEY = "/path/to/your/serviceAccountKey.json"
   ```

<br>

## 完整範例

1. 程式碼。

    ```python
    """Firestore Activity Log Management."""
    from __future__ import annotations

    import logging
    from typing import TYPE_CHECKING, List, Optional

    from langchain_core.activity_log import BaseActivityLog
    from langchain_core.logs import (
        BaseLog,
        logs_from_dict,
        logs_to_dict,
    )

    logger = logging.getLogger(__name__)

    if TYPE_CHECKING:
        from google.cloud.firestore import Client, DocumentReference


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


    class FirestoreActivityLog(BaseActivityLog):
        """Activity log management backed by Google Firestore."""

        def __init__(
            self,
            collection_name: str,
            session_id: str,
            user_id: str,
            firestore_client: Optional[Client] = None,
        ):
            """
            Initialize a new instance of the FirestoreActivityLog class.

            :param collection_name: The name of the collection to use.
            :param session_id: The session ID for the activity.
            :param user_id: The user ID for the activity.
            """
            self.collection_name = collection_name
            self.session_id = session_id
            self.user_id = user_id
            self._document: Optional[DocumentReference] = None
            self.logs: List[BaseLog] = []
            self.firestore_client = firestore_client or _get_firestore_client()
            self.prepare_firestore()

        def prepare_firestore(self) -> None:
            """Prepare the Firestore client.

            Use this function to make sure your database is ready.
            """
            self._document = self.firestore_client.collection(
                self.collection_name
            ).document(self.session_id)
            self.load_logs()

        def load_logs(self) -> None:
            """Retrieve the logs from Firestore"""
            if not self._document:
                raise ValueError("Document not initialized")
            doc = self._document.get()
            if doc.exists:
                data = doc.to_dict()
                if "logs" in data and len(data["logs"]) > 0:
                    self.logs = logs_from_dict(data["logs"])

        def add_log(self, log: BaseLog) -> None:
            self.logs.append(log)
            self.upsert_logs()

        def upsert_logs(self, new_log: Optional[BaseLog] = None) -> None:
            """Update the Firestore document."""
            if not self._document:
                raise ValueError("Document not initialized")
            self._document.set(
                {
                    "id": self.session_id,
                    "user_id": self.user_id,
                    "logs": logs_to_dict(self.logs),
                }
            )

        def clear(self) -> None:
            """Clear session logs from this memory and Firestore."""
            self.logs = []
            if self._document:
                self._document.delete()


    # 測試範例
    if __name__ == "__main__":
        # 初始化 FirestoreActivityLog
        activity_log = FirestoreActivityLog(
            collection_name="activity_logs",
            session_id="session_12345",
            user_id="user_12345"
        )

        # 添加活動記錄
        log = BaseLog(content="User logged in.")
        activity_log.add_log(log)

        # 加載活動記錄
        activity_log.load_logs()
        for log in activity_log.logs:
            print(log.content)

        # 清除活動記錄
        activity_log.clear()
    ```

<br>

___

_END_
