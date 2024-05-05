# pull.rebase

<br>

## 說明

1. 顧名思義， `rebase` 就是重新調整 `提交 commit` 的 `基線 base`，而 `pull.rebase` 選項就是定義 `拉取 pull` 的時候 _是否重建基線_，設定為 `true` 的時候，`git pull` 指令將自動使用 `rebase`，此時拉取遠程分支的變更時，Git 會先把本地的變更（尚未推送的提交）移動到拉取的變更之上，而不是通過創建一個合併提交來合併這些變更。

<br>

2. `pull.rebase` 選項的預設值是 `false`，也就是 `merge`，這會在本地分支上生成一個新的合併提交，將遠程分支的變更合併到本地的分支上。

<br>

3. 進行設定時須透過 `git config` 對 Git 進行設定。

    ```bash
    git config pull.rebase false
    ```

<br>

4. `git pull` 命令用於從遠端倉庫拉取最新的變更並合併到當前分支，其預設值為 `false` ，所以執行這個命令也就是執行了 `git fetch` 與 `git merge`，效果上會以合併 `merge` 的方式整合遠程倉庫的變更。

<br>

## 設定為 True

1. 若將 `pull.rebase` 配置設定為 `true` 時，這表示使用 `git pull` 命令時，Git 將自動使用 `rebase` 而不是 `merge` 來整合遠端分支的變更到本地分支，也就是執行 `git fetch` 從遠端倉庫拉取最新的變更，但不會自動合併或 rebase 這些變更到工作分支，而是以 `git rebase` 將當前分支的變更基於剛才 fetch 下來的最新遠端分支的狀態重新應用。

<br>

2. 由於 `rebase` 重新寫作了提交的歷史，這樣可避免在歷史中出現合併提交，讓歷史看起來更為簡潔和直觀。

<br>

## 使用注意事項

1. 避免在多人共同使用的公共分支上進行 rebase 操作，因為它會改變公共歷史，如果已經將提交推送到了遠端分支，然後又進行了 rebase，這將導致需要強制推送 `git push --force`，可能會干擾其他合作者的工作。

<br>

2. 解決衝突時會比合併 `merge` 更繁瑣，因為在 rebase 時如果遠端分支與本地的變更發生衝突，必須手動逐一解決這些衝突，因為每個衝突都需要在 rebase 過程中依次解決。

<br>

3. 設定 `pull.rebase` 為 `true` 對於保持乾淨線性歷史的需求上很合適，透過以下設定所有的 `git pull` 命令都會自動轉成使用 rebase 而非 merge。

    ```bash
    git config --global pull.rebase true
    ```

<br>

## 設定為全局 

1. 在個別倉庫中設定時不需加任何額外參數。

<br>

2. 全局設定要加上 `--global` 參數，所有的 `git pull` 操作默認將使用合併而非 `rebase`。

    ```bash
    git config --global pull.rebase false
    ```

<br>

___

_END_