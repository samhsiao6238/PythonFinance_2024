# Neo4j

_參考 [網路文章](https://hackmd.io/@kna8421/rkhaNE01Y)_

<br>

## 簡介

1. Neo4j 是一款圖形數據庫管理系統，專為處理複雜的圖形結構而設計，它以圖形方式存儲和查詢數據，與傳統的關聯數據庫有很大的不同。

<br>

2. 在 Neo4j 中，數據模型主要由 `節點（nodes）`、`關係（relationships）`、`屬性（properties）` 和 `標籤（labels）` 四個元素所組成。

<br>

3. Neo4j 使用 Cypher 查詢語言，並將所有數據以圖的形式直接儲存，每個節點和關係都可以有多個屬性，由於數據以圖的形式儲存，因此對於複雜的關聯查詢特別高效，同時也支持 ACID 事務，確保數據的一致性和完整性。

<br>

## 應用實例

1. 找查企業關係。

    ```bash
    MATCH i= ()-[:'控股']->(:公司 {名字:'某某股份有限公司'}) with p
    MATCH j= (:公司 {名字:'某某股份有限公司'})-[:'控股']->()-[:'控股']->()
    RETURE i,j
    ```

<br>

2. 文獻回顧。
    
    ```bash
    # 作者發表的文章數量
    MATCH (r:研究人員)-[w:作者]->() 
    RETURN r.Name, Count (w) as 文章數量
    ```

<br>

3. 社群網站。

    ```bash
    # 朋友圈關係圖
    MATCH f=(:朋友圈 {name:"Peter"})-[*..6]-()
    RETURN f

    # 直接認識的朋友
    MATCH f=(:朋友圈 {name:'Peter'})-[:認識]->()
    RETURN f

    # Peter 的朋友和朋友的朋友
    MATCH f=(Peter:朋友圈 {name:'Peter'})->[*..2]->()
    RETURN f
    ```

<br>

## 資料庫名詞

1. **GDB**：圖形資料庫，Graph database。

<br>

2. **ACID**：資料庫系統的四個特色。
   
   - 原子性：atomicity，或稱不可分割性。
   - 一致性：consistency。
   - 隔離性：isolation，又稱獨立性。
   - 持久性：durability。

<br>

3. **SQL**：關聯式資料庫。

<br>

4. **NoSQL**：非關聯式資料庫。

<br>

5. **CQL**：Cypher Query Language，專為圖形數據庫設計，常用於Neo4j這類圖形數據庫。