# Container vs. Docker

_本節將介紹在 VSCode 中使用 devcontainer，所以先介紹一下它與 Docker 的關係 。_

<br>

## 說明

1. 在 VSCode 中，`Devcontainer` 是一種 `開發環境配置方法`，而 `Docker` 是一個廣泛使用的 `容器化平台`，兩者關係密切但卻是 `不同的工具`。

2. Devcontainer 和 Docker 是不同的工具，但 Devcontainer 依賴 Docker 來建立和管理開發環境的容器，故可將 Devcontainer 看作是 Docker 功能的一個特定應用，旨在改善和簡化開發流程，特別是在多人協作和需要快速建立開發環境的場景中，透過使用 Devcontainer，開發者可以輕鬆地在任何機器上複製完整的開發環境，有效提高開發效率和專案的可移植性。 

<br>

## Docker

1. Docker 是一個開源的容器化平台，允許開發者將應用程式及其依賴項打包到一個輕量級、可移植的容器中，這個容器可以在任何支援 Docker 的機器上運行，從而解決了 `在我機器上可以運行，但是在你機器上不行` 的問題。

2. Docker 容器提供了一致的運作環境，使得應用程式的部署和測試更加簡單可靠。

<br>

## Devcontainer

1. Devcontainer 在名稱上是 `Development Container` 的縮寫，具體上是 VSCode 中的功能，功能名稱為 `Remote - Containers`。

2. Devcontainer 讓開發者可以使用一個定義好的 Docker 容器作為開發環境，其設定檔路徑與命名為 `.devcontainer/devcontainer.json`，開發者透過設定檔案可指定所需的基礎映像、安裝的工具、連接埠轉送、掛載的磁碟區等設定，這使得任何擁有 Docker 和 VSCode 的使用者都能快速設定並進入一個一致的開發環境，無論其本機作業系統如何。

<br>

## 兩者的關係

1. 在基礎原理上，Docker 是底層的容器化平台，提供容器運作的能力；Devcontainer 則是 VSCode 的擴充功能，利用 Docker 創造一個可重複、一致的開發環境。

2. 在使用情境上，Docker 可以用於開發、測試、部署多數類型的應用；而 Devcontainer 主要用於提供一個統一的開發環境，使得多人協作和專案設定變得簡單。

3. 在使用者操作上，使用 Devcontainer 時，開發者通常不需要直接操作 Docker 命令，所有的容器管理都透過 VSCode 的介面和 Devcontainer 的設定檔來完成。

<br>

___

_以上為基礎介紹_