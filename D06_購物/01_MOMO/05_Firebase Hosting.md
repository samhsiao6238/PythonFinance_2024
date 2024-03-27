# Firebase Hosting

_建立網頁應用程式_

<br>

## 步驟說明

1. 點擊齒輪，進入 `專案設定`。

    ![](images/img_39.png)

<br>

2. 點擊 `右方` 紅框標註的 `網頁應用` 圖標以建立網頁應用程式。

    ![](images/img_40.png)

<br>

3. 註冊應用程式，自訂一個應用的名稱，這裡示範命名為 `MyWeb 2024`，可勾選名稱下方的 `託管功能`，勾選後會在後續步驟進行託管的說明而已，所以沒勾選也沒關係，之後都會透過 `CLI` 工具進行部署，接著點擊 `註冊應用程式`。

    ![](images/img_41.png)

<br>

4. 在這個步驟中，主要是說明如何安裝並建立網頁應用，參考即可，然後點擊 `下一步`。

    ![](images/img_42.png)

<br>

5. 說明前一個步驟中的指令，這是用於安裝 `firebase` 客戶端 Javascript 庫，安裝後可進行 Firebase 應用程式開發，讓前端應用直接與 Firebase 服務進行互動。

    ```bash
    npm install firebase
    ```

<br>

6. 說明前步驟所顯示的語法區塊，這是要在網頁文本中寫入的語法，這裡若未做記錄，之後還是可以查詢，不用擔心。

    ```javascript
    // Import the functions you need from the SDKs you need
    import { initializeApp } from "firebase/app";
    // TODO: Add SDKs for Firebase products that you want to use
    // https://firebase.google.com/docs/web/setup#available-libraries

    // Your web app's Firebase configuration
    const firebaseConfig = {
    apiKey: "AIzaSyA7PXB6PKTBU6qEwQXebp47qLcb7Mxit5w",
    authDomain: "fir-2024-6e360.firebaseapp.com",
    databaseURL: "https://fir-2024-6e360-default-rtdb.firebaseio.com",
    projectId: "fir-2024-6e360",
    storageBucket: "fir-2024-6e360.appspot.com",
    messagingSenderId: "1024135627355",
    appId: "1:1024135627355:web:35cbd5ab47ecd31ddd757e"
    };

    // Initialize Firebase
    const app = initializeApp(firebaseConfig);
    ```

<br>

7. 接下來指引安裝開發工具。

    ![](images/img_43.png)

<br>

8. 第一步是安裝 `Firebase CLI`，這是一個命令行工具，用以管理與部署 Firebase 的項目，與前面安裝不同的是使用了全局部署參數 `-g`，如此便可在任何地方調用指令。

    ```bash
    npm install -g firebase-tools
    ```

<br>

9. 然後依據以下指令逐步進行部署。

    ![](images/img_44.png)

<br>

10. 主要會使用到這三個指令。

    ```bash
    # 登入
    firebase login
    # 初始化
    firebase init
    # 部署
    firebase deploy
    ```

<br>

11. 完成後會新增一個網頁應用，並顯示相關訊息。

    ![](images/img_45.png)

<br>

12. 如果日後要查詢這些內容，可以在這個頁面複製這個區塊。

    ![](images/img_46.png)

___

<br>

## 編輯腳本

1. 開啟 VSCode 並建立一個 `index.html` 檔案。

<br>

2. 直接貼上以下的文本內容，這裡暫時不說明腳本具體的製作過程，之後會再說明。
   
    ```html
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Firebase Data Display</title>
        <!-- Bootstrap CSS -->
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <!-- Firebase App (the core Firebase SDK) is always required and must be listed first -->
        <script src="https://www.gstatic.com/firebasejs/8.0.0/firebase-app.js"></script>
        <!-- Add Firebase database -->
        <script src="https://www.gstatic.com/firebasejs/8.0.0/firebase-database.js"></script>
    </head>

    <body>
        <div class="container mt-5">
            <h2>Firebase 資料庫</h2>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Price</th>
                        </tr>
                    </thead>
                    <tbody id="dataList"></tbody>
                </table>
            </div>
        </div>

        <script>
            // 初始化 Firebase，要使用自己的資料
            var firebaseConfig = {
                apiKey: "AIzaSyA7PXB6PKTBU6qEwQXebp47qLcb7Mxit5w",
                authDomain: "fir-2024-6e360.firebaseapp.com",
                databaseURL: "https://fir-2024-6e360-default-rtdb.firebaseio.com",
                projectId: "fir-2024-6e360",
                storageBucket: "fir-2024-6e360.appspot.com",
                messagingSenderId: "1024135627355",
                appId: "1:1024135627355:web:35cbd5ab47ecd31ddd757e"
            };
            firebase.initializeApp(firebaseConfig);

            // 建立資料庫參考物件
            var database = firebase.database();

            // 讀取資料庫資料
            var ref = database.ref('momo');
            ref.on('value', function (snapshot) {
                var data = snapshot.val();
                var list = document.getElementById('dataList');
                list.innerHTML = ''; // 清除資料
                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        var item = data[key];
                        for (var product in item) {
                            if (item.hasOwnProperty(product)) {
                                var price = Object.values(item[product].price)[0]; // 取得第一個價格
                                var row = `<tr><td>${product}</td><td>${price}</td></tr>`;
                                list.innerHTML += row;
                            }
                        }
                    }
                }
            });
        </script>

        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.5/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>

    </html>
    ```

<br>

3. 點擊右鍵，透過插件 `Open With Live Server` 進行即時瀏覽。

    ![](images/img_47.png)

<br>

3. 網頁展示如下，顯示了之前步驟上傳到 Firebase 資料庫的內容。

    ![](images/img_48.png)

<br>

4. 從瀏覽器可知這是在本地進行瀏覽，確認無誤後，將接著進行站台的部署。

    ![](images/img_49.png)

<br>

_以上完成在本地瀏覽，接下來將進行網站部署到 Firebase 進行託管。_

___

_END_