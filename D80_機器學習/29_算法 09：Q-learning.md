以下是修改後的講義和代碼，修正了代碼的錯誤並提供了更明確的講解。

# Q-learning

_`Q-learning` 是一種 `無模型` 的強化學習算法，用於在給定環境中學習最佳策略，通過反覆試探和環境互動找到一個策略，使得在每個狀態下選擇行動時獲得的累積獎勵最大化。_

<br>

## 說明

1. `Q-learning` 通過學習 Q 值函數來實現決策，這個 `Q 值` 表示在給定狀態下採取某一行動後，能夠得到的最大累積回報。

<br>

2. Q-learning 適用於不同的強化學習場景，如遊戲 AI、機器人導航等，它在計算上相對簡單，適合離散的狀態和行動空間。

<br>

## 範例

1. 以下使用 `OpenAI Gym` 庫中的 `Taxi-v3` 環境來實現 Q-learning。這個環境的目標是讓出租車接到乘客並將其送至目的地，具有離散的狀態和行動空間。

    ```python
    # 引入所需的庫
    import numpy as np
    import gym
    import matplotlib.pyplot as plt

    # 設定支持中文的字體，避免顯示錯誤
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    # 用來正常顯示負號
    plt.rcParams['axes.unicode_minus'] = False

    # 創建 Taxi 環境
    env = gym.make("Taxi-v3")

    # 初始化 Q 表
    Q = np.zeros([env.observation_space.n, env.action_space.n])

    # 設置參數
    alpha = 0.8  # 學習速率
    gamma = 0.95  # 折扣因子
    epsilon = 0.1  # 探索機率
    episodes = 1000  # 訓練的回合數

    # 存儲每回合的總獎勵
    reward_list = []

    # 訓練 Q-learning 模型
    for i in range(episodes):
        # 初始化狀態
        state = env.reset()

        # 如果 state 是 tuple，取第一個元素
        if isinstance(state, tuple):
            state = state[0]
        
        total_reward = 0
        done = False

        while not done:
            # 探索或利用
            if np.random.rand() < epsilon:
                # 隨機選擇行動（探索）
                action = env.action_space.sample()
            else:
                # 選擇 Q 表中最優的行動（利用）
                action = np.argmax(Q[state, :])

            # 執行行動並獲得結果
            result = env.step(action)

            # 處理返回的結果
            if len(result) == 5:
                next_state, reward, done, truncated, info = result
            else:
                next_state, reward, done, info = result[:4]
                truncated = False

            # 如果 next_state 是 tuple，取第一個元素
            if isinstance(next_state, tuple):
                next_state = next_state[0]

            # 更新 Q 表
            Q[state, action] = Q[state, action] + alpha * (
                reward + gamma * np.max(Q[next_state, :]) - Q[state, action]
            )

            # 累加回合獎勵
            total_reward += reward

            # 轉移到下一狀態
            state = next_state

        reward_list.append(total_reward)

    # 訓練完成後，顯示 Q 表
    print("Q 表：")
    print(Q)

    # 可視化回合的獎勵變化
    plt.plot(range(episodes), reward_list)
    plt.xlabel('訓練回合')
    plt.ylabel('累積獎勵')
    plt.title('Q-learning 累積獎勵隨訓練回合的變化')
    plt.show()
    ```

2. 輸出 Q 表。

![](images/img_137.png)

3. 累積獎勵，訓練過程中，Q 表逐漸收斂，代表代理逐漸學會在不同狀態下選擇最優行動以獲得最大回報，訓練完成後可以測試模型在環境中的表現。

![](images/img_138.png)

<br>

<br>

## 測試訓練後的模型

1. 測試模型表現。

    ```python
    # 測試訓練後的模型
    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = np.argmax(Q[state, :])
        state, reward, done, truncated, info = env.step(action)
        total_reward += reward

    print(f"Total reward: {total_reward}")
    ```

    此代碼將使用訓練好的 Q 表來執行策略，並打印出獲得的總獎勵。

2. 如果您希望觀察代理如何在環境中執行策略，可以使用以下代碼渲染環境。

    ```python
    import time

    state = env.reset()
    done = False
    env.render()

    while not done:
        action = np.argmax(Q[state, :])
        state, reward, done, truncated, info = env.step(action)
        env.render()
        time.sleep(1)

    env.close()
    ```

這樣你可以在屏幕上看到代理在 `Taxi-v3` 環境中行動的過程。

這些修正和補充將幫助你更好地理解和測試 Q-learning 在 `Taxi-v3` 環境中的應用。如果仍有問題，请确保已正确安装所需的库，并检查所使用的 Python 版本与 Gym 版本的兼容性。