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
    Q = np.zeros([
        env.observation_space.n, env.action_space.n
    ])

    # 設置參數
    # 學習速率
    alpha = 0.8
    # 折扣因子
    gamma = 0.95
    # 探索機率
    epsilon = 0.1
    # 訓練的回合數
    episodes = 1000

    # 存儲每回合的總獎勵
    reward_list = []

    # 訓練 Q-learning 模型
    for i in range(episodes):
        # 初始化狀態
        state = env.reset()
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
            next_state, reward, done, _ = env.step(action)

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

<br>

2. 訓練過程中，Q 表逐漸收斂，代表代理逐漸學會在不同狀態下選擇最優行動以獲得最大回報。訓練完成後可以測試模型在環境中的表現。

<br>

## 進階範例

_使用 `Taxi-v3` 環境來進一步演示 Q-learning 的應用。這個環境非常直觀，有助於觀察強化學習模型的效果。_

<br>

1. 使用 `Taxi-v3` 環境來演示 Q-learning 的應用。

    ```python
    # 引入所需的庫
    import numpy as np
    import gym

    # 創建 Taxi 環境
    env = gym.make("Taxi-v3")

    # 初始化 Q 表
    Q = np.zeros([
        env.observation_space.n, env.action_space.n
    ])

    # 設置參數
    alpha = 0.8 
    gamma = 0.95
    epsilon = 1.0
    epsilon_decay = 0.995
    min_epsilon = 0.01
    episodes = 1000

    # 訓練 Q-learning 模型
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            if np.random.rand() < epsilon:
                # 探索
                action = env.action_space.sample()
            else:
                # 選擇最優行動
                action = np.argmax(Q[state, :])

            next_state, reward, done, _ = env.step(action)
            total_reward += reward

            Q[state, action] = Q[state, action] + alpha * (
                reward + gamma * np.max(Q[next_state, :]) - Q[state, action]
            )

            state = next_state

            if done:
                epsilon = max(min_epsilon, epsilon * epsilon_decay)

    print("訓練完成")
    ```

<br>

2. 測試訓練後的模型，可以進一步觀察 Q 表的變化。

    ```python
    import matplotlib.pyplot as plt

    reward_list = []

    for episode in range(100):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = np.argmax(Q[state, :])
            next_state, reward, done, _ = env.step(action)
            total_reward += reward
            state = next_state

        reward_list.append(total_reward)

    plt.plot(range(100), reward_list)
    plt.xlabel('測試回合')
    plt.ylabel('累積獎勵')
    plt.title('測試過程中累積獎勵的變化')
    plt.show()
    ```

<br>

___

_END_