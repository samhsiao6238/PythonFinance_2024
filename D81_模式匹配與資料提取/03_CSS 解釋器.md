# CSS 選擇器

_CSS Selectors_

![](images/img_03.png)

<br>

## 說明

1. `CSS 選擇器` 是網頁中用來應用樣式的語法，可雙向用於設計網頁樣式與資料提取，尤其在網頁爬蟲中是一種直觀的工具；與 `XPath` 相似，但語法更簡單。

<br>

2. Python 提供多個工具來使用 CSS 選擇器進行網頁元素提取，最常用的庫是 `BeautifulSoup`。

<br>

3. 面對不同的情境時選擇合適的工具，若是處理 `結構化資料` 如 `XML` 時，`XPath` 可能會提供更多靈活性的功能。

<br>

## CSS 選擇器語法與用法

1. 基本元素選擇器：直接選擇特定標籤的所有元素。

    ```css
    /* 選擇所有 `<p>` 元素 */
    p { ... }
    ```

<br>

2. 類別選擇器：選擇具有特定 class 屬性的元素。

    ```css
    /* 選擇 class 為 `description` 的元素 */
    .classname { ... }
    ```

<br>

3. ID 選擇器：選擇具有特定 id 屬性的元素。

    ```css
    /* 選擇 id 為 `main` 的元素 */
    #idname { ... }
    ```

<br>

## 屬性選擇器

1. 根據元素的屬性進行選擇。

    ```css
    /*  */
    [attribute=value] { ... }
    ```

    _範例_

    ```css
    /* 選擇所有 `type="button"` 的 `<input>` 元素 */
    input[type="button"] { ... }
    ```

<br>

## 組合選擇器

1. 後代選擇器：選擇元素的所有後代元素。

    ```css
    /* 選擇所有位於 `<div>` 中的 `<p>` 元素 */
    div p { ... }
    ```

<br>

2. 子選擇器：選擇元素的直接子元素。

    ```css
    /* 選擇所有 `<div>` 的直接子元素 `<p>` */
    div > p { ... }
    ```

<br>

3. 緊鄰兄弟選擇器：選擇緊鄰的兄弟元素。

    ```css
    /* 選擇緊接在 `<h1>` 後的第一個 `<p>` */
    h1 + p { ... }
    ```

<br>

4. 一般兄弟選擇器：選擇所有的兄弟元素。

    ```css
    /* 選擇所有在 `<h1>` 之後的 `<p>` 元素 */
    h1 ~ p { ... }
    ```

<br>

## `BeautifulSoup`

_比 `XPath` 語法更簡潔，且更適合處理 `HTML` 結構_

<br>

1. 安裝 BeautifulSoup。

    ```bash
    pip install beautifulsoup4
    ```

<br>

2. 範例：使用元素選擇器。

    ```python
    from bs4 import BeautifulSoup

    html_content = """
    <html>
      <body>
        <h1>網站標題</h1>
        <p>這是一段文字。</p>
        <p>這是另一段文字。</p>
      </body>
    </html>
    """

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 使用 `soup.select('p')`
    # 可以選擇所有的 `<p>` 標籤，並提取其文本內容
    paragraphs = soup.select('p')
    for p in paragraphs:
        print("段落內容:", p.text)
    ```

    _輸出結果_

    ```bash
    段落內容: 這是一段文字。
    段落內容: 這是另一段文字。
    ```

<br>

3. 範例：使用類別選擇器。

    ```python
    html_content = """
    <html>
      <body>
        <div class="header">
          <h1>網站標題</h1>
        </div>
        <p class="description">這是一段範例描述。</p>
        <p>這是一般段落。</p>
      </body>
    </html>
    """

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 使用 `.description` 選擇 class 為 `description` 的元素
    description = soup.select('.description')
    for d in description:
        print("描述段落:", d.text)
    ```

    _輸出結果_

    ```bash
    描述段落: 這是一段範例描述。
    ```

<br>

4. 範例：使用 ID 選擇器與屬性選擇器。

    ```python
    html_content = """
    <html>
      <body>
        <div id="main">
          <h1>網站標題</h1>
          <input type="text" name="username" value="admin">
          <input type="password" name="password" value="123456">
          <input type="submit" value="Login">
        </div>
      </body>
    </html>
    """

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 使用 `#main` 選擇 id 為 `main` 的 `<div>`
    main_div = soup.select('#main')
    print("主內容區:", main_div[0].text.strip())

    # 使用 `input[type="text"]`
    # 選擇所有 `type="text"` 的 `<input>` 元素
    text_inputs = soup.select('input[type="text"]')
    for input_tag in text_inputs:
        print("文字輸入框的值:", input_tag['value'])
    ```

    _輸出結果_

    ```bash
    主內容區: 網站標題Login
    文字輸入框的值: admin
    ```

<br>

5. 使用組合選擇器。

    ```python
    html_content = """
    <html>
      <body>
        <div class="content">
          <h1>網站標題</h1>
          <p>第一段文字</p>
          <p>第二段文字</p>
        </div>
        <div class="footer">
          <p>網站版權資訊</p>
        </div>
      </body>
    </html>
    """

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 使用後代選擇器選擇 class 為 content 的 div 中的所有段落
    # 使用 `.content p`
    # 選擇 `.content` 中所有 `<p>` 元素（後代選擇器）
    content_paragraphs = soup.select('.content p')
    for p in content_paragraphs:
        print("內容區段落:", p.text)

    # 使用子選擇器選擇 class 為 footer 的 div 中的直接子段落
    # 使用 `.footer > p`
    # 選擇 `.footer` 中的直接子元素 `<p>`（子選擇器）
    footer_paragraph = soup.select('.footer > p')
    for p in footer_paragraph:
        print("頁腳區段落:", p.text)
    ```

    _輸出結果_

    ```bash
    內容區段落: 第一段文字
    內容區段落: 第二段文字
    頁腳區段落: 網站版權資訊
    ```

<br>

## CSS 選擇器 vs XPath

_參考下表說明_

<br>

![](images/img_01.png)

<br>

___

_END_