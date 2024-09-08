### CSS 選擇器簡介

CSS 選擇器（CSS Selectors）是網頁設計中用來選擇和應用樣式的語法，**CSS 選擇器** 不僅可以用來設計網頁樣式，也常用於資料提取。尤其在網頁爬蟲中，CSS 選擇器是一種直觀且強大的工具，與 XPath 相似，但語法更簡單，特別適合初學者。

Python 提供了多個工具來使用 CSS 選擇器進行資料提取，最常用的庫是 **BeautifulSoup**，它支援使用 CSS 選擇器來快速選擇網頁中的元素。

---

### CSS 選擇器語法與用法

#### 1. **基本選擇器**
- **元素選擇器**：直接選擇特定標籤的所有元素。
  ```css
  p { ... }
  ```
  範例：選擇所有 `<p>` 元素。

- **類別選擇器**：選擇具有特定 class 屬性的元素。
  ```css
  .classname { ... }
  ```
  範例：選擇 class 為 `description` 的元素。

- **ID 選擇器**：選擇具有特定 id 屬性的元素。
  ```css
  #idname { ... }
  ```
  範例：選擇 id 為 `main` 的元素。

#### 2. **屬性選擇器**
- 根據元素的屬性進行選擇。
  ```css
  [attribute=value] { ... }
  ```
  範例：選擇所有 `type="button"` 的 `<input>` 元素。
  ```css
  input[type="button"] { ... }
  ```

#### 3. **組合選擇器**
- **後代選擇器**：選擇元素的所有後代元素。
  ```css
  div p { ... }
  ```
  範例：選擇所有位於 `<div>` 中的 `<p>` 元素。

- **子選擇器**：選擇元素的直接子元素。
  ```css
  div > p { ... }
  ```
  範例：選擇所有 `<div>` 的直接子元素 `<p>`。

- **兄弟選擇器**：
  - **緊鄰兄弟選擇器**：選擇緊鄰的兄弟元素。
    ```css
    h1 + p { ... }
    ```
    範例：選擇緊接在 `<h1>` 後的第一個 `<p>`。
  
  - **一般兄弟選擇器**：選擇所有的兄弟元素。
    ```css
    h1 ~ p { ... }
    ```
    範例：選擇所有在 `<h1>` 之後的 `<p>` 元素。

---

### Python 中使用 CSS 選擇器進行資料提取

**BeautifulSoup** 支援使用 CSS 選擇器來提取網頁中的元素，與 XPath 相比，CSS 選擇器語法更簡潔，且更適合處理 HTML 結構。接下來，我們將展示如何使用 `BeautifulSoup` 結合 CSS 選擇器來解析 HTML。

#### 安裝 BeautifulSoup
```bash
pip install beautifulsoup4
```

---

### Python 範例程式碼

#### 1. **使用元素選擇器**
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

# 使用元素選擇器選擇所有 <p> 標籤
paragraphs = soup.select('p')
for p in paragraphs:
    print("段落內容:", p.text)
```

**輸出結果：**
```
段落內容: 這是一段文字。
段落內容: 這是另一段文字。
```

**解析**：
- 使用 `soup.select('p')` 可以選擇所有的 `<p>` 標籤，並提取其文本內容。

---

#### 2. **使用類別選擇器**
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

# 使用類別選擇器選擇 class 為 description 的段落
description = soup.select('.description')
for d in description:
    print("描述段落:", d.text)
```

**輸出結果：**
```
描述段落: 這是一段範例描述。
```

**解析**：
- 使用 `.description` 選擇 class 為 `description` 的元素。

---

#### 3. **使用 ID 選擇器與屬性選擇器**
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

# 使用 ID 選擇器選擇 id 為 main 的 div
main_div = soup.select('#main')
print("主內容區:", main_div[0].text.strip())

# 使用屬性選擇器選擇所有 type 為 text 的 input 元素
text_inputs = soup.select('input[type="text"]')
for input_tag in text_inputs:
    print("文字輸入框的值:", input_tag['value'])
```

**輸出結果：**
```
主內容區: 網站標題Login
文字輸入框的值: admin
```

**解析**：
- 使用 `#main` 選擇 id 為 `main` 的 `<div>`。
- 使用 `input[type="text"]` 選擇所有 `type="text"` 的 `<input>` 元素。

---

#### 4. **使用組合選擇器**
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
content_paragraphs = soup.select('.content p')
for p in content_paragraphs:
    print("內容區段落:", p.text)

# 使用子選擇器選擇 class 為 footer 的 div 中的直接子段落
footer_paragraph = soup.select('.footer > p')
for p in footer_paragraph:
    print("頁腳區段落:", p.text)
```

**輸出結果：**
```
內容區段落: 第一段文字
內容區段落: 第二段文字
頁腳區段落: 網站版權資訊
```

**解析**：
- 使用 `.content p` 選擇 `.content` 中所有 `<p>` 元素（後代選擇器）。
- 使用 `.footer > p` 選擇 `.footer` 中的直接子元素 `<p>`（子選擇器）。

---

### CSS 選擇器與 XPath 的比較

![](images/img_01.png)

### 總結

CSS 選擇器是網頁設計中用來應用樣式的基礎，但在資料提取中也非常實用，特別是在網頁爬蟲中，結合 **BeautifulSoup** 可以輕鬆地從 HTML 文件中提取所需的資料。CSS 選擇器語法簡潔，適合初學者，但在處理結構化資料（如 XML）時，**XPath** 可能會提供更多的靈活性和強大功能。

每種選擇工具都有其適合的場景，根據任務需求選擇合適的工具是關鍵。