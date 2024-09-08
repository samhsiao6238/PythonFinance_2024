# XPath

_XML Path Language_

<br>

## 說明

1. `XPath` 是一種語言，用來在 `XML` 和 `HTML` 文件中搜尋和導航節點，它使用 `路徑語法` 來選擇節點，並可根據不同的條件來篩選所需的元素。

<br>

2. `XPath` 最常應用於 `XML` 文件中，但也常用於 `HTML` 文件解析，如與網頁爬蟲和自動化測試工具結合。

<br>

## XPath 節點類型

1. 元素節點（Element Nodes）。

<br>

2. 屬性節點（Attribute Nodes）。

<br>

3. 文本節點（Text Nodes）。

<br>

4. 命名空間節點（Namespace Nodes）。

<br>

5. 處理指令（Processing Instructions）。

<br>

6. 註解節點（Comment Nodes）。

<br>

7. 文件節點（Document Nodes）。

<br>

## XPath 基本語法

1. `/`：從根節點選擇。

<br>

2. `//`：選擇文件中的節點，而不論它們位於何處。

<br>

3. `.`：當前節點。

<br>

4. `..`：父節點。

<br>

5. `@`：選擇屬性。

<br>

## 常用 XPath 選擇器

1. 選擇所有特定元素。

    ```xpath
    //標籤名稱
    ```

    _選擇所有 `<div>` 元素_

    ```xpath
    //div
    ```

<br>

2. 選擇具有特定屬性的元素。

    ```xpath
    //tag_name[@attribute='value']
    ```

    _選擇 `id` 為 `main` 的 `<div>` 元素_

    ```xpath
    //div[@id='main']
    ```

<br>

3. 選擇文本節點。

    ```xpath
    //tag_name/text()
    ```

    _選擇所有 `<p>` 標籤中的文本_

    ```xpath
    //p/text()
    ```

<br>

4. 選擇具有特定子節點的元素。

    ```xpath
    //tag_name[tag_child]
    ```

    _選擇所有包含 `<span>` 子元素的 `<div>`_

    ```xpath
    //div[span]
    ```

<br>

## XPath 操作符

1. `|`：選擇多個節點；以下 XPath 會選擇文件中所有的 `<div>` 和 `<span>` 元素。

    ```xpath
    //div | //span
    ```

<br>

2. `*`：匹配所有元素或屬性；以下 XPath 會選擇所有 `class` 為 `content` 的元素，不論標籤類型。

    ```xpath
    //*[@class='content']
    ```

<br>

3. `contains()` 部分匹配；以下 XPath 會選擇 `class` 中包含 `header` 的所有 `<div>` 元素。

    ```xpath
    //div[contains(@class, 'header')]
    ```

<br>

## 範例

_XPath 經常和 Python 的 `lxml` 或 `BeautifulSoup` 套件一起使用來解析 HTML/XML 文件_

<br>

1. 程式碼。

    ```python
    from lxml import html

    # 模擬的 HTML 文件
    html_content = """
    <html>
      <body>
        <div id="main">
          <h1>網站標題</h1>
          <p class="description">這是一個範例網站。</p>
          <ul>
            <li>第一項</li>
            <li>第二項</li>
            <li>第三項</li>
          </ul>
        </div>
      </body>
    </html>
    """

    # 解析 HTML 文件
    tree = html.fromstring(html_content)

    # 使用 XPath 選擇元素
    # 選擇 <h1> 標籤中的文。
    title = tree.xpath('//h1/text()')
    # 選擇 <p class="description"> 中的文本本
    paragraph = tree.xpath('//p[@class="description"]/text()')
    # 選擇所有 <li> 中的文本
    list_items = tree.xpath('//ul/li/text()')

    # 結果
    # 網站標題
    print("標題:", title[0])
    # 這是一個範例網站
    print("段落:", paragraph[0])
    # ['第一項', '第二項', '第三項']
    print("列表項目:", list_items)
    ```

<br>

## XPath 條件篩選

1.  `>`、`<`、`=`、`!=`：比較

<br>

2. `position()` 選擇特定位置的元素；這個 XPath 會選擇 `<li>` 中的第二個元素。

    ```xpath
    //li[position()=2]
    ```

<br>

3. `last()`：選擇最後一個元素；這個 XPath 會選擇列表中的最後一個 `<li>` 元素。

    ```xpath
    //li[last()]
    ```

<br>

## 使用 BeautifulSoup 與 lxml 結合 XPath

1. 範例。

    ```python
    from bs4 import BeautifulSoup
    from lxml import etree

    # 模擬的 HTML 文件
    html_content = """
    <html>
      <body>
        <div id="main">
          <h1>網站標題</h1>
          <p class="description">這是一個範例網站。</p>
        </div>
      </body>
    </html>
    """

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 將 BeautifulSoup 轉換成 lxml 可讀格式
    dom = etree.HTML(str(soup))

    # 使用 XPath 搜尋節點
    title = dom.xpath('//h1/text()')
    description = dom.xpath('//p[@class="description"]/text()')

    # 結果
    print("標題:", title[0])
    print("描述:", description[0])
    ```

<br>

___

_END_