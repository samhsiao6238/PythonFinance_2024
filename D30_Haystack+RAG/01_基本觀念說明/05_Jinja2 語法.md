# `Jinja2` 循環語法

_`Jinja2` 提供了循環語法的功能可遍歷數據集合並動態生成對應的內容_

<br>

## 說明

1. `Jinja2` 是一個廣泛使用的 `Python` 模板引擎，它允許在模板中使用 `控制結構`，如 `循環` 和`條件` 語句，用來動態生成 HTML 或其他文本格式的內容。

<br>

2. 之所以說 `循環（Loop）` 所表達的是一種 `控制結構`，允許在程式中重複執行一段代碼，直到滿足某個條件或處理完某些數據。

<br>

## `Jinja2` 中的循環語法

1. 在 `Jinja2` 模板語法中，循環通常是用來遍歷數據，並為每個元素生成對應的模板內容。這種功能特別適合於生成動態網頁內容或處理多個相似的數據項。

    ```jinja2
    {% for item in items %}
        {{ item }}
    {% endfor %}
    ```

<br>

2. 在語法中，透過 `{% for item in items %}` 啟動了一個 `for-in` 循環，其中 `items` 是一個數據集合的變數名稱，`{{ item }}` 是 `Jinja2` 的變量語法，用來輸出當前元素的值， `{% endfor %}` 則是結束循環的語句。

<br>

## 範例

1. 假設有一個 `items` 列表。

    ```python
    items = ["apple", "banana", "cherry"]
    ```

<br>

2. 在 `Jinja2` 模板中使用循環來生成一段 HTML 列表。

    ```jinja2
    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
    ```

<br>

3. 渲染後的結果。

    ```html
    <ul>
        <li>apple</li>
        <li>banana</li>
        <li>cherry</li>
    </ul>
    ```

<br>

## `Jinja2` 循環中的其他功能

1. 循環索引：`loop.index` 或 `loop.index0` 可以分別獲取 `從 1 開始` 和 `從 0 開始` 的當前迭代索引，特別注意的是預設索引是從 `1` 開始。

    ```jinja2
    {% for item in items %}
        {{ loop.index }}: {{ item }}
    {% endfor %}
    ```

<br>

2. 循環控制：`break` 和 `continue` 語句可以用來控制循環的執行流，下面這個範例中， `banana` 會被跳過，不會被輸出。

    ```jinja2
    {% for item in items %}
        {% if item == "banana" %}
            {% continue %}
        {% endif %}
        {{ item }}
    {% endfor %}
    ```

<br>

3. 循環狀態：`loop.first` 和 `loop.last` 可以用來檢查當前迭代是否是第一次或最後一次。

    ```jinja2
    {% for item in items %}
        {% if loop.first %}
            <strong>{{ item }}</strong>
        {% else %}
            {{ item }}
        {% endif %}
    {% endfor %}
    ```

<br>

4. 迭代反轉：`reverse` 關鍵字可以用來反轉數據集合的迭代順序。

    ```jinja2
    {% for item in items | reverse %}
        {{ item }}
    {% endfor %}
    ```

<br>

___

_END_