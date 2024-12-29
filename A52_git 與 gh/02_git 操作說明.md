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

3. `add`：添加更改到 `暫存區 staging area`，也稱為索引，而 `暫存區` 是一個介於工作目錄和儲存庫提交之間的中間區域，所代表的意義是準備進行下一次提交的等候區，如此便可以繼續在工作目錄中工作而不影響即將進行的提交。

    ```bash
    # 加入特定文件的更改到暫存區
    git add <文件名稱>
    # 加入所有已修改的文件到暫存區
    git add .
    # 啟動互動式選單進行添加
    git add -i
    git add --interactive
    ```

<br>

4. `commit`：提交更改到本地倉庫，也就是將更改正式記錄在 Git 的版本歷史中，這些紀錄可視為一個 `快照`，允許未來退回到指定的快照時間點上。

    ```bash
    # 建立一個新的提交
    git commit -m "說明提交資訊"
    # 修改前一次的提交，而不要建立新提交
    git commit --amend
    ```
    
    _補充說明 `git commit --amend`_
    ```bash
    # 使用 git add 將遺漏的更改或文件添加到暫存區
    git add forgotten-file.txt
    # 修改前一次的提交，而不要建立新提交，會開啟編輯器
    git commit --amend
    # 修改前一次的提交且沿用原本的訊息，不會開啟編輯器
    git commit --amend --no-edit
    # 若要修改已經推送到遠端的前一次提交，需使用 `-f` 選項
    git push -f
    ```

    _因為 `--amend` 會改寫已經推送儲存庫分支的歷史，所以在共享的分支上不建議使用。_

<br>

5. `push` 和 `pull`：推送變更到遠程倉庫、從遠端倉庫拉取變更。

    ```bash
    # 推送
    git push origin main
    # 拉取
    git pull origin main
    ```

<br>

6. `branch`：建立分支，建立一個名為 new-branch 的新分支，這個新分支將會從你當前所在的分支基點開始分叉。執行這個命令後，new-branch 將包含當前分支的所有提交。

    ```bash
    git branch new-branch
    ```

<br>

7. `checkout`：切換分支，切換到名為 `new-branch` 的分支，切換後，工作目錄和 HEAD 指針將更新為反映 new-branch 分支的最新狀態。

    ```bash
    git checkout new-branch
    ```

8. `merge`：分支合併。

    ```bash
    git merge <被合併的分支>
    ```

<br>

9. `log`：日誌，可查看更改歷史。

    ```bash
    git log
    ```

<br>

10. `diff`：比對更改歷史。

    ```bash
    git diff HEAD~1
    ```

<br>

11. `git` 軟件可以與任何 Git 服務配合使用，包括 _GitHub、GitLab、Bitbucket_ 等。

<br>

12. `switch`，切換分支，從 `Git` 版本 `2.23` 起，可使用新的指令 `git switch` 來取代 `git checkout`。

    ```bash
    git switch new-branch
    ```

<br>

13. `switch -c`：建立並切換到新分支。

    ```bash
    git switch -c new-branch
    ```

<br>

___

_END_