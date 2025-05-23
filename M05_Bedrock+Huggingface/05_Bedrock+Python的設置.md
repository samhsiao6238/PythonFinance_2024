# 專案環境設置

_在本地進行開發的前置作業_

<br>

## 設置 .env

1. 編輯 .env 文件，根據 `AccessKeys` 文件的內容填入，區域可填入 `us-east-1`。

    ```json
    AWS_ACCESS_KEY_ID=<依據下載的文件填寫>
    AWS_SECRET_ACCESS_KEY=<依據下載的文件填寫>
    AWS_REGION=us-east-1
    ```

<br>

## 檢查 Bedrock 設置

_測試 AWS Bedrock 是否完成設置_

<br>

1. 程式碼。

    ```python
    import os
    import boto3
    from botocore.exceptions import ClientError
    from dotenv import load_dotenv
    import json

    # 環境變數
    load_dotenv()

    def check_model_access():
        # 取得密鑰
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region_name = os.getenv("AWS_REGION")

        # 確認取得變數
        if not all([
            aws_access_key_id,
            aws_secret_access_key,
            region_name
        ]):
            print("錯誤：環境變數中並未設置 AWS 憑證或區域。")
            return

        # 建立 AWS Bedrock 客戶端實體
        client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        
        # 指定要使用的模型 ID
        model_id = "anthropic.claude-v2"  

        try:
            # 調用模型
            body = json.dumps({
                # 這是對話指定的格式
                "prompt": "\n\nHuman: 請簡短一句話介紹自己。\n\nAssistant:",
                "max_tokens_to_sample": 100
            })
            response = client.invoke_model(
                modelId=model_id,
                body=body.encode('utf-8'),
                contentType='application/json',
                accept='application/json'
            )
            response_body = json.loads(response['body'].read())
            print("成功：存取模型已經被允許。")
            print("響應內容：", response_body.get('completion', 'No completion in response'))
        except ClientError as e:
            if e.response["Error"]["Code"] == "AccessDeniedException":
                print(f"Access Denied: {e.response['Error']['Message']}")
            else:
                print(f"Error: {e.response['Error']['Message']}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    if __name__ == "__main__":
        check_model_access()
    ```

    _結果_

    ![](images/img_43.png)

<br>

2. 假如對話格式錯誤，會顯示 `Malformed input request`。

    ![](images/img_44.png)

<br>

## 檢查可用模型

1. 可透過指令查詢 `指定區域內` 所有可用 `基礎模型`，_不限於使用者可用_ 。

    ```bash
    aws bedrock list-foundation-models --region us-east-1
    ```

    ![](images/img_45.png)

<br>

2. 透過程式碼也可以完成相同任務。

    ```python
    import os
    import boto3
    from botocore.exceptions import ClientError
    from dotenv import load_dotenv

    # 環境變數
    load_dotenv()

    def list_available_models():
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region_name = os.getenv("AWS_REGION")

        if not all([aws_access_key_id, aws_secret_access_key, region_name]):
            print("錯誤：環境變數中並未設置 AWS 憑證或是區域。")
            return

        # 建立 AWS Bedrock 客户端物件
        client = boto3.client(
            "bedrock",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

        try:
            # 列出所有基礎模型
            response = client.list_foundation_models()
            models = response.get('modelSummaries', [])
            if models:
                print("Available models:")
                for model in models:
                    print(f"Model ID: {model['modelId']}, Name: {model['modelName']}")
            else:
                print("No models available.")
        except ClientError as e:
            print(f"ClientError: {e.response['Error']['Message']}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    if __name__ == "__main__":
        list_available_models()
    ```

<br>

3. 優化查詢輸出。

    ```python
    import os
    import boto3
    from botocore.exceptions import ClientError
    from dotenv import load_dotenv

    # 加载环境变量
    load_dotenv()

    def list_advanced_models():
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region_name = os.getenv("AWS_REGION")

        if not all([aws_access_key_id, aws_secret_access_key, region_name]):
            print("错误：环境变量中未设置 AWS 凭证或区域。")
            return

        # 建立 AWS Bedrock 客户端实例
        client = boto3.client(
            "bedrock",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

        try:
            # 列出所有基础模型
            response = client.list_foundation_models()
            models = response.get('modelSummaries', [])
            if models:
                print("Available advanced models:")
                for model in models:
                    model_id = model['modelId']
                    model_name = model['modelName']
                    provider_name = model['providerName']
                    input_modalities = ", ".join(model.get('inputModalities', []))
                    output_modalities = ", ".join(model.get('outputModalities', []))
                    customizations_supported = ", ".join(model.get('customizationsSupported', []))
                    inference_types_supported = ", ".join(model.get('inferenceTypesSupported', []))
                    response_streaming_supported = model.get('responseStreamingSupported', False)
                    model_lifecycle_status = model['modelLifecycle']['status']

                    print(f"Model ID: {model_id}")
                    print(f"Name: {model_name}")
                    print(f"Provider: {provider_name}")
                    print(f"Input Modalities: {input_modalities}")
                    print(f"Output Modalities: {output_modalities}")
                    print(f"Customizations Supported: {customizations_supported}")
                    print(f"Inference Types Supported: {inference_types_supported}")
                    print(f"Response Streaming Supported: {response_streaming_supported}")
                    print(f"Model Lifecycle Status: {model_lifecycle_status}")
                    print("-" * 60)
            else:
                print("No models available.")
        except ClientError as e:
            print(f"ClientError: {e.response['Error']['Message']}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    if __name__ == "__main__":
        list_advanced_models()
    ```

<br>

## 檢查指定模型權限 

1. 檢查使用者對指定模型如 `anthropic.claude-v2` 的訪問權限：。

    ```bash
    aws bedrock get-foundation-model --model-identifier anthropic.claude-v2 --region us-east-1
    ```

    _結果_

    ```json
    {
        "modelDetails": {
            "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2",
            "modelId": "anthropic.claude-v2",
            "modelName": "Claude",
            "providerName": "Anthropic",
            "inputModalities": [
                "TEXT"
            ],
            "outputModalities": [
                "TEXT"
            ],
            "responseStreamingSupported": true,
            "customizationsSupported": [],
            "inferenceTypesSupported": [
                "ON_DEMAND"
            ],
            "modelLifecycle": {
                "status": "ACTIVE"
            }
        }
    }
    ```

<br>

2. 透過程式碼檢查。

    ```python
    import os
    import boto3
    from botocore.exceptions import ClientError
    from dotenv import load_dotenv
    import json

    # 環境變數
    load_dotenv()

    def check_model_access():
        # 取得密鑰
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region_name = os.getenv("AWS_REGION")

        # 確認取得變數
        if not all([
            aws_access_key_id,
            aws_secret_access_key,
            region_name
        ]):
            print("錯誤：環境變數中並未設置 AWS 憑證或區域。")
            return

        # 建立 AWS Bedrock 客戶端實體
        client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        
            # 指定要使用的模型 ID
            # model_id = "anthropic.claude-v2"
            model_id = "amazon.titan-tg1-large"

            try:
                # 調用模型
                body = json.dumps({
                    # 這是對話指定的格式
                    "prompt": "\n\nHuman: 請簡短一句話介紹自己。\n\nAssistant:",
                    "max_tokens_to_sample": 100
                })
                response = client.invoke_model(
                    modelId=model_id,
                    body=body.encode('utf-8'),
                    contentType='application/json',
                    accept='application/json'
                )
                response_body = json.loads(response['body'].read())
                print("成功：存取模型已經被允許。")
                print("響應內容：", response_body.get('completion', 'No completion in response'))
            except ClientError as e:
                if e.response["Error"]["Code"] == "AccessDeniedException":
                    print(f"Access Denied: {e.response['Error']['Message']}")
                else:
                    print(f"Error: {e.response['Error']['Message']}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        if __name__ == "__main__":
            check_model_access()
    ```

<br>

2. 可用時會顯示。

    ![](images/img_49.png)

<br>

3. 不可用時會顯示。

    ![](images/img_50.png)

<br>

## 製作 Shell Script 腳本

_簡介如何製作查看可用模型的殼層腳本_

<br>

1. 建立腳本：在桌面建立腳本 `check_accessible_models.sh`。

    ```bash
    cd ~/Desktop && touch check_accessible_models.sh && echo '#!/bin/bash

    # 取得所有模型
    all_models=$(aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[].modelId" --output text)

    # 建立文件用來儲存查詢結果
    accessible_models_file="accessible_models.txt"
    > $accessible_models_file

    # 檢查每個模型訪問權限
    echo "Checking accessible models for the current user..."
    for model_id in $all_models; do
        echo "Checking model: $model_id"
        access_check=$(aws bedrock get-foundation-model --model-identifier $model_id --region us-east-1 2>&1)
        if [[ $access_check != *"AccessDenied"* ]]; then
            echo "Accessible model: $model_id"
            echo $model_id >> $accessible_models_file
        else
            echo "Access denied for model: $model_id"
        fi
    done

    echo "Accessible models have been saved to $accessible_models_file"' > check_accessible_models.sh
    ```

<br>

2. 檢查是否確實建立。

    ```bash
    ls check_accessible_models.sh
    ```

<br>

3. 查看腳本內容。

    ```bash
    cat check_accessible_models.sh
    ```

<br>

4. 賦予腳本權限。

    ```bash
    chmod +x check_accessible_models.sh
    ```

<br>

5. 運行腳本。

    ```bash
    ./check_accessible_models.sh
    ```

<br>

6. 查看腳本輸出的文件 `accessible_models.txt`。

    ```bash
    cat accessible_models.txt
    ```

<br>

___

_END_