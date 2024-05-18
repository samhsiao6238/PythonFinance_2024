# 範例一

_這第一個範例將用詳細拆解的方式來指引_

## 使用虛擬環境並建立專案資料夾

建立虛擬環境。
```bash
cd ~/Documents/PythonVenv && python -m venv envStllm
```

查詢路徑
```bash
cd envStllm && cd bin && pwd
```

將路徑複製下來
```bash
/Users/samhsiao/Documents/PythonVenv/envStllm/bin
```

編輯環境參數
```bash
# 使用 Nano
nano ~/.zshrc
# 或使用 VSCode
code ~/.zshrc
```

加入
```bash
source /Users/samhsiao/Documents/PythonVenv/envStllm/bin/activate
```

退出（control+O）、儲存（control+X）並啟動
```bash
source ~/.zshrc
```

建立專案資料夾
```bash
cd ~/Desktop && mkdir exStllm && cd exStllm
```

建立主腳本並啟動 VSCode
```bash
touch app.py && code .
```



```bash
# 這是一個 Streamlit 應用，所以會使用 Streamlit
import streamlit as st
# 會使用到 OpenAI 官方的套件
from openai import OpenAI