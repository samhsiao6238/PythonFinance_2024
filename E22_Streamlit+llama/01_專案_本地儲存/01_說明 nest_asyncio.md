# 說明 `nest_asyncio`

<br>

1. `nest_asyncio.apply()` 是一個用於解決嵌套事件循環問題的函數，特別是在 Jupyter Notebook 或其他需要嵌套事件循環的環境中非常有用。

<br>

2. 在 Python 中，異步編程使用事件循環來調度和執行異步任務。通常，一個應用程序只能有一個事件循環。但是，有些環境，如 Jupyter Notebook，可能會嵌套事件循環，這會導致錯誤，例如「RuntimeError: This event loop is already running」。

<br>

3. `nest_asyncio` 是一個 Python 庫，用於允許嵌套事件循環。通過使用 `nest_asyncio.apply()`，可以 `補丁` 當前的事件循環，允許它在已經運行的事件循環內再次運行。

<br>

## 主要用途

1. 在 Jupyter Notebook 中，同時運行異步程式碼和同步程式碼時，可能會遇到事件循環相關的問題。使用 `nest_asyncio.apply()` 可以解決這些問題，使得異步程式碼能夠正常運行。

<br>

2. 當需要在已運行的事件循環中再次運行一個新的事件循環時，這是非常有用的。

<br>

3. 使用範例

    ```python
    import nest_asyncio
    import asyncio

    # 應用 nest_asyncio 來允許嵌套事件循環
    nest_asyncio.apply()

    async def main():
        print("Hello")
        await asyncio.sleep(1)
        print("World")

    # 運行異步函數
    asyncio.run(main())
    ```

<br>

4. 在上述範例中，`nest_asyncio.apply()` 被調用，以確保即使在嵌套的環境中，事件循環也能正常運行。

<br>

## 在範例中的應用

1. 在腳本中，使用 `nest_asyncio.apply()` 可以確保即使在 Streamlit 這樣的環境中，事件循環也能夠正常嵌套和運行。

    ```python
    import nest_asyncio
    import streamlit as st

    nest_asyncio.apply()

    st.title("UBER 10-K Chatbot")
    # ... 其他程式碼 ...
    ```

<br>

___

_END_