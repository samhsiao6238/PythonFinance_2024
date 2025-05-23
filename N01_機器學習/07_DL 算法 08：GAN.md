# GAN

_Generative Adversarial Network，GAN 是一種深度學習模型，用於生成逼真的數據；核心概念是通過一個 `生成器（Generator）` 和一個 `辨別器（Discriminator）` 之間的對抗性訓練，使生成器能夠建立難以區分於真實數據的假數據。_

<br>

## GAN 的應用領域

1. 圖像生成和風格轉換：生成逼真的圖像或將一種圖像風格轉換為另一種風格，如將素描轉換為油畫風格。

<br>

2. 圖像超分辨率：提高圖像的解析度，使低分辨率圖像變得清晰。

<br>

3. 文本到圖像合成：根據描述性的文本生成對應的圖像。

<br>

4. 數據增強：在醫學影像、語音數據等領域，用於生成更多樣本來增強數據集。

<br>

5. 虛擬石徑和遊戲開發：建立虛擬環境中逼真的物體或場景。

<br>

6. 音頻生成：生成音樂、語音等音頻數據，用於音樂創作和語音合成。

<br>

## GAN 的基本概念

1. GAN 由兩個相互競爭的神經網絡組成，分別是 `生成器` 和 `辨別器`，這兩個網絡彼此競爭，生成器試圖生成與真實數據相似的數據，而辨別器試圖區分生成的數據和真實數據。

<br>

2. 在 GAN 中，生成器模型從隨機噪聲中生成假數據，例如在此範例中，生成器接收一個潛在向量 𝑧 並將其轉換為類似於 MNIST 手寫數字的圖像數據；而辨別器模型則用來區分真實數據和生成器生成的假數據，辨別器通過輸出一個機率來判斷輸入數據是真實的還是生成的，其目標是最大化正確區分真實數據和假數據的機率。

<br>

## 說明

1. 以下使用 `PyTorch` 和 `MNIST 資料集` 來實作訓練一個簡單的 GAN，並生成類似手寫數字的圖像。

<br>

2. 程式碼。

    ```python
    # 引入 PyTorch 庫
    import torch
    # 引入神經網絡模塊
    import torch.nn as nn
    # 引入優化器模塊
    import torch.optim as optim
    # 引入數據集和數據變換模塊
    from torchvision import datasets, transforms
    # 引入用於圖像儲存的工具
    from torchvision.utils import save_image
    import matplotlib.pyplot as plt
    import numpy as np

    # 設定設備為 GPU 或 CPU
    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )


    # 定義生成器模型
    class Generator(nn.Module):
        def __init__(self, latent_dim):
            # 繼承父類的初始化方法
            super(Generator, self).__init__()
            self.model = nn.Sequential(
                # 全連接層：將潛在空間中的點映射到一個更大的空間
                nn.Linear(latent_dim, 128),
                nn.ReLU(True),
                # 全連接層：進一步映射到圖像尺寸
                nn.Linear(128, 784),
                # 使用 Tanh 激活函數將輸出值範圍限制在 [-1, 1]
                nn.Tanh(),
            )

        def forward(self, z):
            # 前向傳播計算生成器的輸出
            return self.model(z)


    # 定義辨別器模型
    class Discriminator(nn.Module):
        def __init__(self):
            # 繼承父類的初始化方法
            super(Discriminator, self).__init__()
            self.model = nn.Sequential(
                # 全連接層：將圖像數據壓縮到一個小空間
                nn.Linear(784, 128),
                nn.LeakyReLU(0.2, inplace=True),
                # 全連接層：進一步壓縮到單一的真實性標誌
                nn.Linear(128, 1),
                # 使用 Sigmoid 激活函數將輸出值範圍限制在 [0, 1]
                nn.Sigmoid(),
            )

        def forward(self, img):
            # 前向傳播計算辨別器的輸出
            return self.model(img)


    # 設定超參數
    # 潛在空間的維度大小
    latent_dim = 100
    # 學習率
    lr = 0.0002
    # 批次大小
    batch_size = 64
    # 訓練的回合數
    epochs = 100

    # 載入 MNIST 數據集
    transform = transforms.Compose(
        [
            # 將圖像轉換為張量
            transforms.ToTensor(),
            # 將圖像的像素值標準化到 [-1, 1]
            transforms.Normalize([0.5], [0.5]),
        ]
    )

    # 建立數據集和數據加載器
    dataset = datasets.MNIST(
        root="./data",
        train=True,
        transform=transform,
        download=True
    )
    dataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )

    # 初始化生成器和辨別器
    generator = Generator(latent_dim).to(device)
    discriminator = Discriminator().to(device)

    # 定義損失函數（二元交叉熵損失）
    adversarial_loss = nn.BCELoss()

    # 定義生成器和辨別器的優化器
    optimizer_G = optim.Adam(
        generator.parameters(), lr=lr
    )
    optimizer_D = optim.Adam(
        discriminator.parameters(), lr=lr
    )

    # 訓練 GAN
    for epoch in range(epochs):
        for i, (imgs, _) in enumerate(dataloader):
            # 將真實圖像標籤設置為 1，假圖像標籤設置為 0
            real_labels = torch.ones(imgs.size(0), 1).to(device)
            fake_labels = torch.zeros(imgs.size(0), 1).to(device)

            # 轉換真實圖像張量的形狀
            real_imgs = imgs.view(imgs.size(0), -1).to(device)

            # ------------------
            # 訓練辨別器
            # ------------------
            optimizer_D.zero_grad()  # 梯度清零

            # 辨別真實圖像
            real_loss = adversarial_loss(
                discriminator(real_imgs),
                real_labels
            )

            # 隨機生成潛在向量並生成假圖像
            z = torch.randn(imgs.size(0), latent_dim).to(device)
            fake_imgs = generator(z)

            # 辨別假圖像
            fake_loss = adversarial_loss(
                discriminator(fake_imgs.detach()),
                fake_labels
            )

            # 計算辨別器的總損失
            d_loss = real_loss + fake_loss
            # 反向傳播
            d_loss.backward()
            # 更新辨別器權重
            optimizer_D.step()

            # -----------------
            # 訓練生成器
            # -----------------
            # 梯度清零
            optimizer_G.zero_grad()

            # 生成假圖像並計算生成器的損失
            g_loss = adversarial_loss(
                discriminator(fake_imgs),
                real_labels
            )
            # 反向傳播
            g_loss.backward()
            # 更新生成器權重
            optimizer_G.step()

            # 每 100 次批次顯示訓練進度
            if i % 100 == 0:
                print(
                    f"Epoch [{epoch}/{epochs}]"
                    f" Batch {i}/{len(dataloader)}"
                    f" Loss D: {d_loss.item():.4f},"
                    f" loss G: {g_loss.item():.4f}"
                )

        # 每個 epoch 儲存一些生成的圖像
        if epoch % 10 == 0:
            save_image(
                fake_imgs.view(
                    fake_imgs.size(0), 1, 28, 28
                ),
                f"images/{epoch}.png",
                normalize=True,
            )

    # 訓練結束後，可視化生成的圖像
    # 隨機生成 64 個潛在向量
    z = torch.randn(64, latent_dim).to(device)
    # 生成假圖像
    gen_imgs = generator(z)

    # 將生成的圖像可視化
    plt.figure(figsize=(8, 8))
    for i in range(64):
        plt.subplot(8, 8, i + 1)
        plt.imshow(
            gen_imgs[i].view(28, 28).cpu().detach().numpy(),
            cmap="gray"
        )
        plt.axis("off")
    plt.show()
    ```

<br>

2. 運行中會輸出訓練過程，`Loss D` 是辨別器的損失，`Loss G` 是生成器的損失，這些損失函數用於指導模型訓練，使得辨別器能夠更好地區分真實數據和生成數據，而生成器則努力生成越來越逼真的數據以欺騙辨別器。

    ![](images/img_43.png)

<br>

3. 以下這張圖片就是 GAN 模型初步生成的手寫數字圖像，以結果來說仍然模糊，這表示生成器還沒有完全學會生成清晰的手寫數字。

    ![](images/img_44.png)

<br>

4. 以訓練數據來說，訓練結果屬於中等偏好，`生成器損失` 較高代表生成器仍在學習如何更好地欺騙辨別器，但 `辨別器損失` 表示其能夠有效地區分真實和生成數據，所以 GAN 的訓練尚未達到理想狀態，但也沒有出現明顯的模式崩潰或者一方主導的情況；以上狀況可透過調整模型的超參數來繼續訓練，如學習率、批次大小，或者進一步調整生成器和辨別器的架構以改善訓練效果。

<br>

## 代碼說明

1. 使用 `torchvision` 載入 MNIST 數據集並進行標準化處理，將圖像像素值標準化到 `[-1, 1]` 範圍內，這有助於訓練的穩定性。

<br>

2. 定義生成器（`Generator`）是將隨機生成的潛在向量轉換為假圖像的模型。

<br>

3. 定義辨別器（`Discriminator`）是區分真實圖像和生成的假圖像的模型。

<br>

4. 損失函數使用二元交叉熵損失函數來評估辨別器和生成器的性能。

<br>

5. 優化器使用 Adam 優化器來更新生成器和辨別器的權重。

<br>

6. 在訓練迭代中，首先更新辨別器，然後更新生成器。對於辨別器，計算辨別真實圖像和假圖像的損失，並進行梯度更新。對於生成器，生成假圖像並計算辨別器對假圖像的損失，目的是騙過辨別器，使其認為假圖像為真實。

<br>

___

_END_