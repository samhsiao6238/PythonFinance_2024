# Meta Llama

_依據官網的 [Running Meta Llama on Mac](https://llama.meta.com/docs/llama-everywhere/running-meta-llama-on-mac/) 說明，節錄其中 `Python` 腳本部分。_

<br>

## 範例

1. 官方提供的 Python 範例。

    ```python
    import requests
    import json

    url = "http://localhost:11434/api/chat"

    def llama3(prompt):
        data = {
            "model": "llama3",
            "messages": [
                {
                    "role": "user",
                    "content": prompt

                }
            ],
            "stream": False,
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()["message"]["content"]

    response = llama3("誰建立了中華民國？")
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