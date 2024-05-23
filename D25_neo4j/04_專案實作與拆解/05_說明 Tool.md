# Tool

<br>

## 說明

1. 當自己構建 `代理 agent` 時，需要提供一個 `Tool 清單`，讓代理可以使用這些 Tool。

<br>

2. 可參考本專案的 Tool 清單。

    ```python
    tools = [
        Tool.from_function(
            name="General Chat",
            description="處理一般聊天對話，涵蓋所有其他工具未涵蓋的問題和請求。",
            func=llm.invoke,
            return_direct=False,
        ),。
        Tool.from_function(
            name="Vector Search Index",
            description="用於基於向量搜索的電影情節信息檢索。",
            func=kg_qa,
            return_direct=False,
        ),
        Tool.from_function(
            name="Cypher QA",
            description="用於使用 Cypher 查詢語句來回答有關電影的具體問題。",
            func=cypher_qa,
            return_direct=False,
        )
    ]
    ```

<br>

## Tool 的組成

1. name (str): `必需的`，且在一個工具列表中必須唯一、不可重複。

2. description (str): `可選的`，但建議提供且詳細說明，因為 _代理會使用描述來決定如何使用工具_。

3. args_schema (Pydantic BaseModel): `可選的`，但建議提供，可以用來提供更多的信息（例如，少量樣本）或驗證預期的參數。

<br>

## 定義工具的方式

_通過兩個例子來演示如何為函數定義工具_

<br>

1. 一個模擬的搜尋函數，總是返回字串 "LangChain"。

2. 一個乘法函數，將兩個數字相乘。

_這兩個範例展示了如何處理單一輸入和多個輸入的情況。大多數代理僅處理需要單一輸入的函數，因此了解如何處理這些函數非常重要。雖然定義這些自訂工具的方式大體相同，但仍存在一些差異。_

<br>

## 使用 @tool 裝飾器

1. 使用 `@tool` 裝飾器是定義自訂工具的最簡單方式。裝飾器預設使用函數名作為工具名，也可通過傳遞字串作為第一個參數來自訂工具名。

2. 裝飾器將使用函數的文檔字串作為 `工具的描述`，因此必須提供文檔字串。

3. 程式碼。

    ```python
    from langchain.pydantic_v1 import BaseModel, Field
    from langchain.tools import BaseTool, StructuredTool, tool

    @tool
    def search(query: str) -> str:
        """在線查找內容。"""
        return "LangChain"

    # Output: search
    print('1. search.name：', search.name)
    # Output: search(query: str) -> str 
    print('2. search.description：', search.description)
    # Output: {'query': {'title': 'Query', 'type': 'string'}}
    print('3. search.args：', search.args)

    @tool
    def multiply(a: int, b: int) -> int:
        """將兩個數字相乘。"""
        return a * b
    print('\n')
    print('1. multiply.name：', multiply.name)
    print('2. multiply.description：', multiply.description)
    print('3. multiply.args：', multiply.args)
    ```

<br>

## 自訂工具名稱和 JSON 參數

1. 可以通過將參數傳遞給 tool 裝飾器來自訂工具名稱和 JSON 參數。

2. 程式碼。

    ```python
    class SearchInput(BaseModel):
        query: str = Field(description="應該是一個搜尋查詢")

    @tool("search-tool", args_schema=SearchInput, return_direct=True)
    def search(query: str) -> str:
        """在線查找內容。"""
        return "LangChain"

    print('search.name：', search.name)
    print('search.description：', search.description)
    print('search.args：', search.args)
    print('search.return_direct：', search.return_direct)
    ```

<br>

## 繼承 BaseTool 類

1. 可以通過繼承 `BaseTool 類` 來顯示自定義工具，這樣可以最大限度地控制工具定義，但需要更多的工作。

2. 程式碼。

    ```python
    from typing import Optional, Type

    from langchain.callbacks.manager import (
        AsyncCallbackManagerForToolRun,
        CallbackManagerForToolRun,
    )


    class SearchInput(BaseModel):
        query: str = Field(description="應該是一個搜尋查詢")


    class CalculatorInput(BaseModel):
        a: int = Field(description="第一個數字")
        b: int = Field(description="第二個數字")


    class CustomSearchTool(BaseTool):
        name = "custom_search"
        description = "當你需要回答關於當前事件的問題時很有用"
        args_schema: Type[BaseModel] = SearchInput

        def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
        ) -> str:
            """使用這個工具。"""
            return "LangChain"

        async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
        ) -> str:
            """異步使用這個工具。"""
            raise NotImplementedError("custom_search 不支持異步")


    class CustomCalculatorTool(BaseTool):
        name = "Calculator"
        description = "當你需要回答數學問題時很有用"
        args_schema: Type[BaseModel] = CalculatorInput
        return_direct: bool = True

        def _run(
            self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
        ) -> str:
            """使用這個工具。"""
            return a * b

        async def _arun(
            self,
            a: int,
            b: int,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        ) -> str:
            """異步使用這個工具。"""
            raise NotImplementedError("Calculator 不支持異步")


    search = CustomSearchTool()
    print('search.name', search.name)
    print('search.description', search.description)
    print('search.args', search.args)
    print('\n')

    multiply = CustomCalculatorTool()
    print('multiply.name', multiply.name)
    print('multiply.description', multiply.description)
    print('multiply.args', multiply.args)
    print('multiply.return_direct', multiply.return_direct)
    ```

<br>

## 使用 StructuredTool 類

1. 可以使用 `StructuredTool 類`，這個方式介於前兩者之間，比 `繼承 BaseTool 類` 更方便，但比僅僅 `使用裝飾器` 更多的功能。

2. 程式碼。

    ```python
    def search_function(query: str):
        return "LangChain"

    search = StructuredTool.from_function(
        func=search_function,
        name="Search",
        description="當你需要回答關於當前事件的問題時很有用",
    )

    print(search.name)
    print(search.description)
    print(search.args)
    ```

<br>

## 定義自訂 args_schema

1. 可以定義自訂的 `args_schema` 以提供更多關於輸入的信息。

2. 程式碼。

    ```python
    class CalculatorInput(BaseModel):
        a: int = Field(description="第一個數字")
        b: int = Field(description="第二個數字")

    def multiply(a: int, b: int) -> int:
        """將兩個數字相乘。"""
        return a * b

    calculator = StructuredTool.from_function(
        func=multiply,
        name="Calculator",
        description="數字相乘",
        args_schema=CalculatorInput,
        return_direct=True,
    )

    print(calculator.name)  # Output: Calculator
    print(calculator.description)  # Output: Calculator(a: int, b: int) -> int - 數字相乘
    print(calculator.args)  # Output: {'a': {'title': 'A', 'description': '第一個數字', 'type': 'integer'}, 'b': {'title': 'B', 'description': '第二個數字', 'type': 'integer'}}
    ```

<br>

## 工具的例外處理

1. 當工具在執行過程中遇到錯誤且未捕捉例外時，程序將崩潰並停止執行。

    ```python
    from langchain_core.tools import ToolException
    from langchain.tools import StructuredTool

    def search_tool1(query: str) -> str:
        # 模擬正常的查詢邏輯
        if query == "error":
            raise ToolException("搜索工具1不可用。")
        return "搜尋結果"

    # 定義一個沒有 handle_tool_error 的工具
    search = StructuredTool.from_function(
        func=search_tool1,
        name="Search_tool1",
        description="一個查詢工具"
    )

    # 嘗試運行工具，將引發未處理的異常
    search.run("error")

    # 這行代碼永遠不會被執行，因為程序在前面已經崩潰
    print("程序仍然在運行。")
    ```
    _結果_
    ```bash
    ToolException: 搜索工具1不可用。
    ```

<br>

2. 透過手動進行例外捕捉。

    ```python
    from langchain_core.tools import ToolException
    from langchain.tools import StructuredTool

    def search_tool1(query: str) -> str:
        # 模擬正常的查詢邏輯
        if query == "error":
            raise ToolException("搜索工具1不可用。")
        return "搜尋結果"

    # 定義一個沒有 handle_tool_error 的工具
    search = StructuredTool.from_function(
        func=search_tool1,
        name="Search_tool1",
        description="一個查詢工具"
    )

    # 手動進行例外捕捉
    try:
        search.run("error")
    except ToolException as e:
        print(e)

    # 進行了例外捕捉，所以程序不會崩潰
    print("程序仍然在運行。")
    ```
    _結果_
    ```bash
    搜索工具1不可用。
    程序仍然在運行。
    ```

<br>

3. 設置 handle_tool_error 為 True，自動進行例外捕捉：使程序不會崩潰，並返回異常訊息。。

    ```python
    from langchain_core.tools import ToolException
    from langchain.tools import StructuredTool

    def search_tool1(query: str) -> str:
        # 模擬正常的查詢邏輯
        if query == "error":
            raise ToolException("搜索工具1不可用。")
        return "搜尋結果"

    search_with_error_handling = StructuredTool.from_function(
        func=search_tool1,
        name="Search_tool1",
        description="一個查詢工具",
        # 設置為 True
        handle_tool_error=True,
    )

    # 測試正常查詢情況
    result = search_with_error_handling.run("test")
    print(result)  # Output: '搜尋結果'

    # 測試引發錯誤的情況
    result = search_with_error_handling.run("error")
    # 預設的例外捕捉
    print(result)  # Output: '搜索工具1不可用。'
    # 進行了例外捕捉，所以程序不會崩潰
    print("進行了例外捕捉，所以程序不會崩潰。")
    ```
    _結果_
    ```bash
    搜尋結果
    搜索工具1不可用。
    程序仍然在運行。
    ```

<br>

4. 設置 handle_tool_error 為字串：當引發異常時，代理返回設置的錯誤訊息字串，而不是異常本身的訊息。。

    ```python
    from langchain_core.tools import ToolException
    from langchain.tools import StructuredTool

    def search_tool1(query: str) -> str:
        # 模擬正常的查詢邏輯
        if query == "error":
            raise ToolException("搜索工具1不可用。")
        return "搜尋結果"

    search_with_string_error_handling = StructuredTool.from_function(
        func=search_tool1,
        name="Search_tool1",
        description="一個壞工具",
        handle_tool_error="工具執行過程中發生錯誤，請嘗試使用其他工具。",
    )

    result = search_with_string_error_handling.run("error")
    print(result)
    ```
    _結果_
    ```bash
    工具執行過程中發生錯誤，請嘗試使用其他工具。
    ```

<br>

5. 設置 handle_tool_error 為字串時，代理捕捉到異常後返回該字串作為錯誤訊息，而設置為 True 時則會返回異常本身的訊息。

    ```python
    from langchain_core.tools import ToolException
    from langchain.tools import StructuredTool

    def search_tool1(query: str) -> str:
        # 模擬正常的查詢邏輯
        if query == "error":
            raise ToolException("搜索工具1不可用。")
        return "搜尋結果"

    search_with_string_error_handling = StructuredTool.from_function(
        func=search_tool1,
        name="Search_tool1",
        description="一個查詢工具",
        # 錯誤發生將返回字串
        # handle_tool_error="工具執行過程中發生錯誤，請嘗試使用其他工具。",
        # 錯誤發生將返回錯誤本身
        handle_tool_error=True,
    )

    # 測試正常查詢情況
    result = search_with_string_error_handling.run("test")
    print(result)

    # 測試引發錯誤的情況
    result = search_with_string_error_handling.run("error")
    print(result)
    ```

    _結果_
    ```bash
    搜尋結果
    搜索工具1不可用。
    ```

<br>

## 異步處理

1. 展示了如何實現和測試異步工具的異常處理邏輯

2. 程式碼。

    ```python
    import asyncio
    from langchain_core.tools import ToolException
    from langchain.tools import BaseTool
    from typing import Optional, Type
    from pydantic import BaseModel, Field

    class SearchInput(BaseModel):
        query: str = Field(description="要查詢的字符串")

    class AsyncSearchTool(BaseTool):
        name = "async_search"
        description = "異步查詢工具"
        args_schema: Type[BaseModel] = SearchInput

        def _run(
            self, query: str, run_manager: Optional = None
        ) -> str:
            # 同步版本的查詢邏輯
            if query == "error":
                raise ToolException("同步查詢工具不可用。")
            return "同步查詢結果"

        async def _arun(
            self, query: str, run_manager: Optional = None
        ) -> str:
            # 異步版本的查詢邏輯
            await asyncio.sleep(1)  # 模擬異步操作
            if query == "error":
                raise ToolException("異步查詢工具不可用。")
            return "異步查詢結果"

    # 定義一個異步工具
    async_search_tool = AsyncSearchTool()

    # 測試異步查詢工具
    async def test_async_tool():
        try:
            result = await async_search_tool._arun("test")
            print(result)  # Output: '異步查詢結果'
        except ToolException as e:
            print(f"捕捉到異常: {e}")

        try:
            result = await async_search_tool._arun("error")
            print(result)
        except ToolException as e:
            print(f"捕捉到異常: {e}")  # Output: '捕捉到異常: 異步查詢工具不可用。'

    # 執行測試異步工具的函數
    asyncio.run(test_async_tool())
    ```

    _結果_
    ```bash
    異步查詢結果
    捕捉到異常: 異步查詢工具不可用。
    ```

<br>
