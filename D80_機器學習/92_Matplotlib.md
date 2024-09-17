# `Matplotlib` 

_Python 視覺化工具，以下是常見的圖形類型_

<br>

## 折線圖（Line Plot）

1. 折線圖常用於顯示數據隨時間或順序變化的趨勢。

    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    # 模擬數據
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # 繪製折線圖
    plt.plot(x, y)
    plt.title('Line Plot')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.show()
    ```

    ![](images/img_167.png)

<br>

## 散點圖（Scatter Plot）

1. 散點圖展示數據點的分佈，通常用來觀察變數之間的關係。

    ```python
    # 模擬數據
    x = np.random.rand(50)
    y = np.random.rand(50)

    # 繪製散點圖
    plt.scatter(x, y)
    plt.title('Scatter Plot')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.show()
    ```

    ![](images/img_168.png)

<br>

## 柱狀圖（Bar Plot）

1. 柱狀圖用於比較不同類別的數據。

    ```python
    # 模擬數據
    categories = ['A', 'B', 'C', 'D']
    values = [10, 15, 7, 10]

    # 繪製柱狀圖
    plt.bar(categories, values)
    plt.title('Bar Plot')
    plt.ylabel('Values')
    plt.show()
    ```

    ![](images/img_169.png)

<br>

## 直方圖（Histogram）

1. 直方圖用於顯示數據分佈的頻率，可以用來觀察數據的分佈模式。

    ```python
    # 模擬數據
    data = np.random.randn(1000)

    # 繪製直方圖
    plt.hist(data, bins=30)
    plt.title('Histogram')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()
    ```

    ![](images/img_170.png)

<br>

## 餅圖（Pie Chart）

1. 餅圖用於顯示各類別佔總數的比例。

    ```python
    # 模擬數據
    labels = ['A', 'B', 'C', 'D']
    sizes = [20, 30, 25, 25]

    # 繪製餅圖
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Pie Chart')
    plt.show()
    ```

    ![](images/img_171.png)

<br>

## 箱線圖（Box Plot）

1. 箱線圖顯示數據的分佈情況，包括中位數和四分位數範圍。

    ```python
    # 模擬數據
    data = [np.random.normal(0, std, 100) for std in range(1, 4)]

    # 繪製箱線圖
    plt.boxplot(data)
    plt.title('Box Plot')
    plt.show()
    ```

    ![](images/img_172.png)

<br>

## 熱圖（Heatmap）

1. 熱圖用來顯示矩陣形式的數據，並通過顏色來表示數值的大小。

    ```python
    import seaborn as sns

    # 模擬數據
    data = np.random.rand(10, 10)

    # 繪製熱圖
    sns.heatmap(data, annot=True, cmap='coolwarm')
    plt.title('Heatmap')
    plt.show()
    ```

    ![](images/img_173.png)

<br>

## 面積圖（Area Plot）

1. 面積圖展示累積數據的變化。

    ```python
    # 模擬數據
    x = np.arange(1, 6)
    y1 = np.array([3, 6, 9, 12, 15])
    y2 = np.array([2, 4, 6, 8, 10])

    # 繪製面積圖
    plt.fill_between(x, y1, label='y1', alpha=0.5)
    plt.fill_between(x, y2, label='y2', alpha=0.5)
    plt.title('Area Plot')
    plt.legend()
    plt.show()
    ```

    ![](images/img_174.png)

<br>

## 堆積柱狀圖（Stacked Bar Plot）

1. 堆積柱狀圖顯示不同類別在總數中的構成。

    ```python
    # 模擬數據
    labels = ['A', 'B', 'C']
    x1 = [3, 2, 5]
    x2 = [4, 7, 1]

    # 繪製堆積柱狀圖
    plt.bar(labels, x1, label='X1')
    plt.bar(labels, x2, bottom=x1, label='X2')
    plt.title('Stacked Bar Plot')
    plt.legend()
    plt.show()
    ```

    ![](images/img_175.png)

<br>

## 極區圖（Polar Plot）

1. 極區圖用於展示數據的角度和半徑。

    ```python
    # 模擬數據
    theta = np.linspace(0, 2*np.pi, 100)
    r = np.abs(np.sin(theta))

    # 繪製極區圖
    plt.polar(theta, r)
    plt.title('Polar Plot')
    plt.show()
    ```

    ![](images/img_176.png)

<br>

## 雷達圖（Radar Chart）

1. 雷達圖主要用於顯示多個變量的表現，它通常應用於比較不同類別的多個維度。

    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    from math import pi

    # 模擬數據
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [4, 3, 2, 5, 4]

    # 計算角度
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    values += values[:1]  # 閉合圖形
    angles += angles[:1]

    # 繪製雷達圖
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticklabels([])

    # 設定軸標籤
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    plt.title('Radar Chart')
    plt.show()
    ```

    ![](images/img_177.png)

<br>

## 3D 分佈圖（3D Plot）

1. 3D 分佈圖適合用於顯示三維數據的分佈情況，例如用於觀察數據點在三維空間中的分佈。

    ```python
    from mpl_toolkits.mplot3d import Axes3D

    # 模擬數據
    x = np.random.randn(100)
    y = np.random.randn(100)
    z = np.random.randn(100)

    # 繪製 3D 散點圖
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)

    # 設定標籤
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title('3D Scatter Plot')
    plt.show()
    ```

    ![](images/img_178.png)

<br>

## 3D 曲面圖（3D Surface Plot）

1. 3D 曲面圖常用於顯示函數的三維曲面，適合於觀察變數之間的複雜關係。

    ```python
    from mpl_toolkits.mplot3d import Axes3D

    # 模擬數據
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2))

    # 繪製 3D 曲面圖
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='viridis')

    # 設定標籤
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title('3D Surface Plot')
    plt.show()
    ```

    ![](images/img_179.png)

<br>

## 帕累托圖（Pareto Chart）

1. 帕累托圖展示數據值的排序以及累積百分比，通常用於分析主要因素。

    ```python
    from matplotlib.ticker import PercentFormatter

    # 模擬數據
    values = [10, 20, 15, 35, 40]
    categories = ['A', 'B', 'C', 'D', 'E']

    # 繪製帕累托圖
    fig, ax = plt.subplots()
    ax.bar(categories, values)

    # 累積百分比
    cumsum = np.cumsum(values)
    ax2 = ax.twinx()
    ax2.plot(categories, cumsum, color='red', marker='D', ms=7)
    ax2.yaxis.set_major_formatter(PercentFormatter(cumsum[-1]))

    plt.title('Pareto Chart')
    plt.show()
    ```

    ![](images/img_180.png)

<br>

## 瀑布圖（Waterfall Chart）

1. 瀑布圖展示某些變量的累積效果，常用於財務分析。

    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    # 模擬數據
    categories = ['Start', 'Increase 1', 'Increase 2', 'Decrease 1', 'Final']
    values = [1000, 300, 200, -400, 1100]

    # 計算累計效果
    y = np.zeros(len(values))
    y[1:] = np.cumsum(values[:-1])

    # 定義每個條形圖的顏色，根據正負值不同顯示不同顏色
    colors = ['green' if val >= 0 else 'red' for val in values]

    # 繪製條形圖
    plt.bar(categories, values, bottom=y, color=colors)

    # 添加標題和標籤
    plt.title('Waterfall Chart')
    plt.ylabel('Values')

    # 顯示圖形
    plt.show()
    ```

    ![](images/img_181.png)

<br>

## 等高線圖（Contour Plot）

1. 等高線圖用於表示三維數據的二維投影，其中等高線代表數據中相同值的點。

    ```python
    # 模擬數據
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2))

    # 繪製等高線圖
    plt.contour(x, y, z, cmap='coolwarm')
    plt.title('Contour Plot')
    plt.show()
    ```

    ![](images/img_182.png)

<br>

2. 這種圖形在地形圖、氣象數據中非常有用，比如想分析一片地區的山脈，使用等高線圖可以直觀地看到不同區域的高度分佈。

    ```python
    import numpy as np
    import matplotlib.pyplot as plt

    # 模擬數據：x 和 y 為平面坐標，z 表示高度（例如地形的高度）
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)

    # z 為高度，這裡模擬一個圓形波浪的高度分佈
    z = np.sin(np.sqrt(x**2 + y**2))

    # 繪製填充的等高線圖
    plt.contourf(x, y, z, cmap='coolwarm')

    # 添加等高線
    contours = plt.contour(x, y, z, colors='black')
    # 添加等高線標籤
    plt.clabel(contours, inline=True, fontsize=8) 

    # 添加標題
    plt.title('Filled Contour Plot with Labels')

    # 顯示圖表，顯示顏色條，對應不同的高度數值
    plt.colorbar()
    plt.show()
    ```

    ![](images/img_183.png)

<br>

3. 等高線圖可以與 3D 圖相結合，使用 Matplotlib 中的 Axes3D 模塊來實現 3D 視角的效果，這樣可以在同一個圖中既展示 2D 等高線圖，又展示 3D 的數據分佈；在前面的範例中，使用了 `Axes3D` 繪圖，適用於基本的 3D 曲面圖顯示，主要目的是展示數據的三維結構，而不考慮等高線或其他細節，而這個同時包含高解析度數據、3D 曲面圖、2D 等高線圖，展示曲面和等高線的情況下，該腳本提供了更多的視覺細節和交互性。

    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # 模擬數據
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2))

    # 創建 3D 圖
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # 繪製 3D 曲面圖
    ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none', alpha=0.8)

    # 在底部繪製 2D 等高線圖
    ax.contour(x, y, z, zdir='z', offset=-1, cmap='coolwarm')

    # 設定視角
    ax.view_init(45, 240)

    # 標籤與標題
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Contour Plot with Surface')

    # 顯示圖表
    plt.show()
    ```

    ![](images/img_184.png)

<br>

___

_未完_