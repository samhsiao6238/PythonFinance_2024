# git

_`git` 是一個開源的分布式版本控制系統工具，廣泛用於程式碼的管理，允許開發者在本地機器上工作並維護完整的項目歷史記錄，獨立於中央服務器。_

<br>

## `git` 可執行操作

1. `init`：初始化新的版本控制倉庫。

    ```bash
    git init
    ```

<br>

2. `clone`：複製遠端庫至本地，其中 `URL` 部分在建立倉庫後可在倉庫中查看官方指引。

    ```bash
    git clone https://github.com/<帳號名稱>/<倉庫名稱>.git
    ```

<br>

3. `add` 及 `commit`：添加與提交更改到本地倉庫。

    ```bash
    git add .
    git commit -m "說明提交資訊"
    ```

<br>

4. `push` 和 `pull`：推送變更到遠程倉庫、從遠端倉庫拉取變更。

    ```bash
    git push origin main
    git pull origin main
    ```

<br>

5. `branch`：建立分支，創建一個名為 new-branch 的新分支，這個新分支將會從你當前所在的分支基點開始分叉。執行這個命令後，new-branch 將包含當前分支的所有提交。

    ```bash
    git branch new-branch
    ```

<br>

6. `checkout`：切換分支，切換到名為 `new-branch` 的分支，切換後，工作目錄和 HEAD 指針將更新為反映 new-branch 分支的最新狀態。

    ```bash
    git checkout new-branch
    ```

7. `merge`：分支合併。

    ```bash
    git merge <被合併的分支>
    ```

<br>

8. `log`：日誌，可查看更改歷史。

    ```bash
    git log
    ```

<br>

9. `diff`：比對更改歷史。

    ```bash
    git diff HEAD~1
    ```

<br>

9. `git` 軟件可以與任何 Git 服務配合使用，包括 _GitHub、GitLab、Bitbucket_ 等。

<br>

10. `switch`，切換分支，從 `Git` 版本 `2.23` 起，可使用新的指令 `git switch` 來取代 `git checkout`。

    ```bash
    git switch new-branch
    ```

<br>

11. `switch -c`：建立並切換到新分支。

    ```bash
    git switch -c new-branch
    ```

<br>

___

_END_