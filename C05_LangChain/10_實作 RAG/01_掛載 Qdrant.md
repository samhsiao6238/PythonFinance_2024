# 準備工作

## 建立虛擬環境

_略_

## 安裝 poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

```bash
poetry --version
```

3. Poetry 需要在專案資料夾中管理依賴，因此先建立一個新專案

```bash
cd ~/Desktop
poetry new exLangChain0301
cd exLangChain0301
```

4. 修改

```bash
code pyproject.toml
```

5. 將版本改如下。

```bash
requires-python = ">=3.9,<4"
```

6. 安裝 LangChain

```bash
poetry add langchain langchain-qdrant qdrant-client pypdf
```

## 啟動

```bash
open -a Docker
```

查看
```bash
docker info
```

## 掛載

1. 掛載。

```bash
sudo docker pull qdrant/qdrant
```

2. 啟動。

```bash
sudo docker run -p 6333:6333 qdrant/qdrant
```

