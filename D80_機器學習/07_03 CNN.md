# CNN

_Convolutional Neural Network 卷積神經網絡_

<br>

## 說明

1. 以下範例使用 `CIFAR-10` 數據集來訓練 CNN 模型，進行彩色圖片的分類任務。

<br>

2. `CIFAR-10` 是一個常用的圖像數據集，包括 10 個類別（如飛機、汽車、鳥、貓等）。

    ```python
    import numpy as np
    import matplotlib.pyplot as plt
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
    from tensorflow.keras.utils import to_categorical
    from tensorflow.keras.datasets import cifar10
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

    # 設定支持中文的字體，避免顯示錯誤
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    # 用來正常顯示負號
    plt.rcParams['axes.unicode_minus'] = False

    # 加載 CIFAR-10 數據集
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()

    # 將影像數據轉換為浮點數並進行歸一化，縮放到 0-1 範圍
    X_train = X_train.astype('float32') / 255
    X_test = X_test.astype('float32') / 255

    # 將類別標籤進行 One-hot 編碼，轉換為二進位矩陣
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)

    # 建立 CNN 模型
    model = Sequential()

    # 第一個卷積層，32 個 3x3 卷積核，ReLU 激活函數
    model.add(
        Conv2D(32, (3, 3), 
        activation='relu', 
        input_shape=(32, 32, 3))
    )

    # 第一個池化層，2x2 大小
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # 第二個卷積層，64 個 3x3 卷積核，ReLU 激活函數
    model.add(Conv2D(64, (3, 3), activation='relu'))

    # 第二個池化層，2x2 大小
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # 展平層，將 2D 影像數據展平為 1D 向量
    model.add(Flatten())

    # 全連接層（密集層），64 個神經元，ReLU 激活函數
    model.add(Dense(64, activation='relu'))

    # 輸出層，10 個神經元，Softmax 激活函數，對應 10 個類別
    model.add(Dense(10, activation='softmax'))

    # 編譯模型，使用 Adam 優化器和類別交叉熵損失函數
    model.compile(
        loss='categorical_crossentropy', 
        optimizer='adam', 
        metrics=['accuracy']
    )

    # 訓練模型，進行 20 次迭代（epochs），每批處理 64 個樣本
    history = model.fit(
        X_train, y_train, 
        epochs=20, 
        batch_size=64, 
        verbose=1, 
        validation_data=(X_test, y_test)
    )

    # 使用測試集進行預測
    y_pred = model.predict(X_test)

    # 將預測結果轉為類別索引
    y_pred_classes = np.argmax(y_pred, axis=1)
    # 將真實標籤轉為類別索引
    y_true = np.argmax(y_test, axis=1)

    # 建立圖形框架，設定大小
    plt.figure(figsize=(12, 5))

    # 可視化準確率（Accuracy）
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='訓練準確率')
    plt.plot(history.history['val_accuracy'], label='驗證準確率')
    plt.title('模型準確率')
    plt.xlabel('迭代次數')
    plt.ylabel('準確率')
    plt.legend()

    # 可視化損失值（Loss）
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='訓練損失')
    plt.plot(history.history['val_loss'], label='驗證損失')
    plt.title('模型損失值')
    plt.xlabel('迭代次數')
    plt.ylabel('損失值')
    plt.legend()

    # 自動調整子圖參數，使圖像填充整個圖形區域
    plt.tight_layout()
    plt.show()

    # 生成混淆矩陣，並進行可視化
    cm = confusion_matrix(y_true, y_pred_classes)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.title('混淆矩陣')
    plt.show()

    # 使用測試集評估模型性能，輸出準確率
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f'測試集上的準確率：{test_acc:.2f}')
    ```

<br>

2. 結果。

    ![](images/img_17.png)

<br>

3. 混淆矩陣。

    ![](images/img_18.png)

<br>

4. 準確率。

    ![](images/img_19.png)

<br>

## 模型說明

1. 加載 CIFAR-10 數據集後，將影像數據轉換為浮點數並歸一化，將數據縮放到 0 到 1 之間，以提高模型的訓練效率，並將類別標籤進行 One-hot 編碼，因為使用的是多類別分類問題。

<br>

2. 先使用 Keras 的 `Sequential` 模型構建一個 CNN。接著使用 `Conv2D` 層進行卷積操作，提取影像的空間特徵。

<br>

3. 添加池化層（`MaxPooling2D`）來進行下采樣，減少特徵圖的尺寸並保留重要特徵。

<br>

4. 使用 `Flatten` 層將 2D 圖像展平為 1D 向量，然後添加全連接層（`Dense`）來進行分類。

<br>

5. 最後的輸出層使用 10 個神經元（對應 10 個類別）和 Softmax 激活函數，用於輸出類別機率。

<br>

6. 編譯模型時使用 `categorical_crossentropy` 損失函數，這是多類別分類問題的標準損失函數。使用 `adam` 優化器來優化模型。

<br>

___

_END_