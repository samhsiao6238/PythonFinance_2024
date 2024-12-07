# Meta Llama

_依據官網的 [Running Meta Llama on Mac](https://llama.meta.com/docs/llama-everywhere/running-meta-llama-on-mac/) 說明，節錄其中 `Python` 腳本部分。_

<br>

## 範例

1. 官方提供的 Python 範例，通過 HTTP POST 請求向本地伺服器上的 API 發送一個問題，並取得 AI 模型生成的回答。

    ```python
    # 用於發送 HTTP 請求
    import requests
    # 用於處理 JSON 格式的數據
    import json

    # 定義 API 端點的 URL
    url = "http://localhost:11434/api/chat"

    # 構建要發送給 API 的請求數據，這裡是 JSON 格式
    def llama3(prompt):
        data = {
            # 指定使用的模型為 "llama3"
            "model": "llama3",
            "messages": [
                {
                    # 定義角色為用戶
                    "role": "user",
                    # 用戶的輸入內容 prompt
                    "content": prompt

                }
            ],
            # 不使用流式傳輸，直接取得完整回應
            "stream": False,
        }
        # 設置 HTTP 請求的標頭，表明數據格式為 JSON
        headers = {
            "Content-Type": "application/json"
        }
        # 發送 POST 請求到指定的 URL，攜帶標頭和 JSON 數據
        response = requests.post(
            url, 
            headers=headers, 
            json=data
        )
        # 從回應中提取生成的文本內容並返回
        return response.json()["message"]["content"]
    
    # 呼叫函數 llama3
    response = llama3("誰建立了中華民國？")
    # 輸出模型生成的回答
    print(response)
    ```

<br>

2. 結果。

    ```txt
    A crucial question in Chinese history!

    The Republic of China (ROC), also known as the Chinese Republic or commonly referred to as Taiwan, was established on January 1, 1912, by the Qing-dynasty General Yuan Shikai. However, the ROC that exists today, officially known as the Republic of China on Taiwan, has a different history.

    After the fall of the Qing dynasty in 1911, Sun Yat-sen, a Chinese revolutionary and founder of the Kuomintang (KMT) party, became the first provisional president of the new republic. He played a key role in the Xinhai Revolution, which overthrew the Qing dynasty.

    Sun Yat-sen's presidency was short-lived, as he died on March 13, 1916. Chiang Kai-shek, also known as Jiang Jieshi, took over as the leader of the KMT and eventually became the president of the ROC in 1928.

    In 1949, after the Chinese Civil War, the Communist Party of China (CPC) defeated the Nationalist Party (KMT), led by Chiang Kai-shek. The CPC established the People's Republic of China (PRC) on October 1, 1949, and the KMT retreated to Taiwan.

    The ROC that exists today is a separate entity from the mainland Chinese government, with its own president, government, and international relations. It was officially known as the Republic of China until 1949 and has been known as the Republic of China (Taiwan) or simply Taiwan since then.
    ```

<br>

___

_END_