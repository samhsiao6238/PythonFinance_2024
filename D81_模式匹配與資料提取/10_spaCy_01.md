# spaCy

_自然語言處理 (NLP) 與命名實體識別 (NER)_

<br>

## 介紹

1. spaCy 是一個功能強大的開源 Python 庫，專為處理 `自然語言處理（NLP）` 任務而設計，與其他 NLP 庫不同，spaCy 是針對高效處理 `大型語料庫` 和實時應用而開發的。

<br>

2. spaCy 具備 `詞性標註（POS tagging）`、`命名實體識別（NER）`、`依存句法分析（Dependency Parsing）`等多種高級功能。

<br>

3. spaCy 以 Cython 編寫，能夠在大規模的語料庫中進行快速分析，內置多種語言的預訓練模型，可以直接使用而無需重新訓練，支持多種語言處理任務，並可以與其他 NLP 庫如 TensorFlow 和 PyTorch 無縫集成。

<br>

## 核心功能

1. 詞性標註（POS tagging）：識別詞彙在句子中的詞性，例如名詞、動詞。

<br>

2. 依存句法分析（Dependency Parsing）：分析詞與詞之間的語法關係。

<br>

3. 命名實體識別（NER）：識別文本中的命名實體，如人名、地名、組織名稱等。

<br>

4. 斷詞與分句（Tokenization and Sentence Segmentation）：將文本分割為詞彙或句子。

<br>

## 命名實體識別

_Named Entity Recognition，NER_

<br>

1. `命名實體識別` 是 NLP 領域的一項關鍵技術，旨在自動從文本中識別特定類型的詞或短語，這些詞通常代表現實世界中的具體對象，如人名、地名、組織名稱、時間、日期、貨幣等。

<br>

2. NER 的目標是從文本中提取出特定的命名實體並給予標籤，常見的實體類型有 `PERSON（人名）`、`GPE（Geopolitical Entity，地理政治實體）`、`ORG（組織名稱，Organization）`、`DATE（日期）`、`MONEY（貨幣數額）`。

<br>

## spaCy NER 的運作方式

1. spaCy 內部的 NER 模型通過預先訓練來識別這些命名實體類型，當文本輸入 spaCy 模型時，模型會自動掃描文本並識別出這些命名實體，並為其打上適當的標籤。

<br>

2. 這些實體類型（標籤）根據 spaCy 預訓練模型的能力進行分配，這表示不需要重新訓練模型，便可立即使用。

<br>

## 代碼範例

_使用 spaCy 進行命名實體識別_

<br>

1. 以下範例使用 spaCy 來進行命名實體識別，展示加載 spaCy 的預訓練模型，並識別文本中的命名實體。

    ```python
    import spacy

    # 加載 spaCy 的預訓練英文模型
    nlp = spacy.load("en_core_web_sm")

    # 要分析的文本
    text = "Apple is looking at buying a startup in New York for $1 billion."

    # 使用模型處理文本
    doc = nlp(text)

    # 識別並輸出出實體名稱及其類型
    for ent in doc.ents:
        print(ent.text, ent.label_)
    ```

    _輸出結果_

    ```
    Apple ORG
    New York GPE
    $1 billion MONEY
    ```

<br>

2. 在這個範例中，`Apple` 被識別為一個 `ORG（組織）`，`New York` 被識別為 `GPE（地理政治實體）`，`$1 billion` 被識別為 `MONEY（貨幣數額）`。

<br>

## NER 的實體類型標籤

_常用 spaCy NER 標籤的_

<br>

1. PERSON：人名，表示一個具體的人。

2. ORG：組織名稱，代表公司、政府機構等。

3. GPE：地理政治實體，表示國家、城市等。

4. MONEY：貨幣數額，表示金額。

5. DATE：日期，表示具體的時間或日期。

6. TIME：時間。

7. MONEY：貨幣。

8. QUANTITY：數量。

<br>

## spaCy 模型種類

_使用 spaCy 時需要先加載其預訓練模型_

<br>

1. `en_core_web_sm`：小型英文模型，體積小且速度快，適合初學和普通應用。

2. `en_core_web_md`：中型英文模型，提供更準確的語言處理能力。=

3. `en_core_web_lg`：大型英文模型，提供更詳細和準確的語言分析。

<br>

## 加載模型

1. 可以使用以下命令來安裝模型。

    ```bash
    python -m spacy download en_core_web_sm
    ```

<br>

2. 然後在代碼中使用以下方式加載。

    ```python
    import spacy
    nlp = spacy.load("en_core_web_sm")
    ```

<br>

3. NER 技術在實際應用中具有廣泛用途，如文本摘要與信息提取，可自動從新聞、文章中提取重要人物、地點、組織等信息；或用於問答系統或聊天機器人，能識別出問題中的關鍵實體，進行精確回答；NER 是一個泛用的名稱，不僅僅指 spaCy，它是 NLP 中的一項技術，任何 NLP 工具或框架如 spaCy、Hugging Face、Stanford NLP、BERT 等，都可以實現 NER，用來識別文本中的實體如人名、地名、組織等。

<br>

___

_END_