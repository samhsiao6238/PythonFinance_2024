# Neo4j

<br>

_這裡僅作簡單介紹，關於 Neo4j 的深入介紹可參考本章節各專案內的詳細說明。_

<br>

## 相關網址

1. [官網](https://neo4j.com/)。

<br>

## 簡介

1. Neo4j 是一款高性能的 _圖形資料庫管理系統_，專為處理複雜的 `關聯數據` 而設計。這個資料庫使用圖形理論中的 `節點（nodes）`、`關係（relationships，也稱「邊」）`、`屬性（properties）` 和 `標籤（labels）` 來儲存和呈現數據，使得它能夠有效地表達豐富的聯繫和關聯性。

<br>

2. Neo4j 的數據模型直觀、靈活且可互動，適合用於社交網絡、推薦系統、欺詐檢測、網絡安全等領域，這些領域中往往需要分析和處理大量的關係數據。它支持 `ACID事務特性`，保證數據的一致性和可靠性。

<br>

3. Neo4j 提供了強大的查詢語言 `Cypher`，它是一種聲明式的圖形查詢語言，使得執行複雜的圖形查詢變得直觀和高效。`Cypher` 的語法類似於 SQL，但是專門為圖形數據設計，能夠直接表達節點間的關聯和路徑。

<br>

## 元件說明

1. 節點 Nodes：節點是圖形資料庫中代表了實體的基本元素，如人、物件、類別等，每個節點可以包含多個屬性，用來儲存有關該實體的信息。

2. 關係 Relationships：關係用於連接兩個節點來表示節點之間的各種關聯，如 `朋友`、`擁有` 或 `工作於` 之類的特徵；關係是 `有方向性的`，描述從一個節點指向另一個節點的特徵；關係也可以有屬性，例如關係的 `權重`；關係也被稱為 `邊（edges）`，特別是在描述從一個節點到另一個節點的連接時。

3. 屬性 Properties：屬性是儲存在節點或關係上的 `鍵值對`，例如一個表示人的節點可能有一個名字和年齡的屬性。

4. 標籤 Labels：標籤是用來分類節點的 `標記`，可用於將節點分類成不同的類型，一個節點可以有多個標籤，例如，可以將 `員工` 和 `人類` 這兩個標籤同時賦予一個節點時，代表這個節點實體是一個人類，同時也是一名員工。

___

_END_