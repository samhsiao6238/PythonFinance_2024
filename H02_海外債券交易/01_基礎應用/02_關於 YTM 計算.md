# YTM

<br>

## 說明

1. 建立試算表。

    ```python
    import pandas as pd

    # 建立 Excel 試算表數據
    data = {
        "參數": ["結算日", "到期日", "票面利率", "市場價格", "票面價值", "年付息次數", "計算基準", "YTM 計算"],
        "數值": ["2045/08/23", "2046/02/23", 0.0465, 93.46, 100, 2, 0, "=YIELD(A2, A3, A4, A5, A6, A7, A8)"]
    }

    # 建立 DataFrame
    df = pd.DataFrame(data)

    # 定義 Excel 檔案名稱
    file_path = "data/債券YTM試算.xlsx"

    # 儲存 Excel
    df.to_excel(file_path, index=False)

    file_path
    ```

    ![](images/img_42.png)

<br>

___

_END_