# Firebase Part II

_以下合併以上的腳本，將查詢結果上傳到雲端資料庫。_

<br>

## 步驟說明

1. 建立專案

```python
# Firebase
import firebase_admin
from firebase_admin import credentials
# 這個 db 是給 realtime 使用，注意 firestore 的相關物件命名不要重複到庫名 db
from firebase_admin import db


# 金鑰
CredFile = 'fir-2024-6e360-firebase-adminsdk-16wwf-d2983e1f68.json'
# 資料庫網址
StorageBucket = 'https://fir-2024-6e360-default-rtdb.firebaseio.com/'

# 初始化：database，並檢查 Firebase app 是否已經初始化
if not firebase_admin._apps:
    cred = credentials.Certificate(CredFile)
    firebase_admin.initialize_app(cred, {
        'storageBucket': StorageBucket, # 這兩個是不同的服務
        'databaseURL': StorageBucket    # 但在這個範例是一樣的
    })
# 最上層節點
refData = db.reference('momo').child(_keyword)
# 自訂函數：寫入 Firebase
def writeToFirebaseDB(_ref, _key, _value):
  try:
    _ref.update({_key: _value})
  except:
    # 實際上發生錯誤時應該中止或跳出程序
    print('發生錯誤')
```

2. 建立時間戳

```python
# 取得時間
# 時區
tz = dateutil.tz.gettz('Asia/Taipei')
# 時間字串
_info_time = datetime.datetime.now(tz).strftime("%Y%m%d%H%M%S")
```

3. 上傳

```python
_datas = {}
#
for i in range(_count):
    _i = str(i+1)
    #
    # xpath_name = f"/html/body/div[@id='BodyBase']/div[@class='bt_2_layout searchbox searchListArea selectedtop']/div[@class='searchPrdListArea bookList']/div[@id='columnType']/ul/li[{_i}]/a[@class='goodsUrl']/div[@class='prdInfoWrap']/h3[@class='prdName']"
    # xpath_info = f"/html/body/div[@id='BodyBase']/div[@class='bt_2_layout searchbox searchListArea selectedtop']/div[@class='searchPrdListArea bookList']/div[@id='columnType']/ul/li[{_i}]/a[@class='goodsUrl']/div[@class='prdInfoWrap']/p[@class='sloganTitle']"
    # xpath_price = f"/html/body/div[@id='BodyBase']/div[@class='bt_2_layout searchbox searchListArea selectedtop']/div[@class='searchPrdListArea bookList']/div[@id='columnType']/ul/li[{_i}]/a[@class='goodsUrl']/div[@class='prdInfoWrap']/p[@class='money']/span[@class='price']/b"
    #
    xpath_name = f"/html/body/div[@id='BodyBase']/div[@class='bt_2_layout searchbox searchListArea selectedtop']/div[@class='searchPrdListArea bookList']/div[@id='columnType']/ul[@class='clearfix']/li[{_i}]/a[@class='goodsUrl']/div[@class='prdInfoWrap']/div[@class='prdNameTitle']/h3[@class='prdName']"
    xpath_info = f"/html/body/div[@id='BodyBase']/div[@class='bt_2_layout searchbox searchListArea selectedtop']/div[@class='searchPrdListArea bookList']/div[@id='columnType']/ul[@class='clearfix']/li[{_i}]/a[@class='goodsUrl']/div[@class='prdInfoWrap']/p[@class='sloganTitle']"
    xpath_price = f"/html/body/div[@id='BodyBase']/div[@class='bt_2_layout searchbox searchListArea selectedtop']/div[@class='searchPrdListArea bookList']/div[@id='columnType']/ul[@class='clearfix']/li[{_i}]/a[@class='goodsUrl']/div[@class='prdInfoWrap']/p[@class='money']/span[@class='price']/b"

    #
    # _name = chrome.find_element_by_xpath(xpath_name)
    # _info = chrome.find_element_by_xpath(xpath_info)
    # _price = chrome.find_element_by_xpath(xpath_price)
    _name = chrome.find_element(By.XPATH, xpath_name)
    _info = chrome.find_element(By.XPATH, xpath_info)
    _price = chrome.find_element(By.XPATH, xpath_price)
    # 處理字串
    _string = _name.text
    # 找到 括號 在第幾個字元
    _index = _string.find('】') + 1
    # 產品名稱從下一個字元開始擷取
    _string = _string[_index:]
    # 刪除字串所有的空白字元
    _string = _string.replace(" ", "")
    _string = _string.replace("/", "-")
    _string = _string.replace(".", "。")
    # 輸出看一下
    print(_string)
    print(_info.text)
    print(_price.text)
    print()
    # 下面就是要寫入 firebase 的部分
    #
    _node_product = refData.child(_string).child('price')
    #
    _str_price = _price.text
    writeToFirebaseDB(_node_product, _info_time, _str_price)
```

3. 關閉

```python
chrome.quit()
```