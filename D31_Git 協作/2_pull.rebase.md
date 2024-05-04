_未完成_

# pull.rebase

## 說明

1. `rebase` 顧名思義就是重新調整提交 `commit` 的基線 `base`，`pull.rebase` 選項就是拉取 `pull` 的時候是否重建基線的設定，這個設定的預設值就是 `false`。

2. 參數 `config` 可對 Git 進行設定，透過以下指令可將 `pull.rebase` 選項設定為 `false`，這會影響 `git pull` 命令的行為。
```bash
git config pull.rebase false
```

3. `git pull` 命令用於從遠端倉庫拉取最新的變更並合併到當前分支，其預設值為 `false` ，所以執行這個命令也就是執行了 `git fetch` 與 `git merge`，效果上會以合併 `merge` 的方式整合遠程倉庫的變更。

## 設定為 True

1. 若將 `pull.rebase` 配置設定為 `true` 時，這表示使用 `git pull` 命令時，Git 將自動使用 `rebase` 而不是 `merge` 來整合遠端分支的變更到本地分支，也就是執行 `git fetch` 從遠端倉庫拉取最新的變更，但不會自動合併或 rebase 這些變更到你的工作分支，而是以 `git rebase` 將當前分支的變更基於剛才 fetch 下來的最新遠端分支的狀態重新應用。

2. 由於 `rebase` 重新寫作了提交的歷史，這樣可避免在歷史中出現合併提交，讓歷史看起來更為簡潔和直觀。

### 使用 `pull.rebase` 的注意事項

- **避免在公共分支上使用**：正如先前所提，不應在多人共同使用的公共分支上進行 rebase 操作，因為它會改變公共歷史。如果你已經將提交推送到了遠端分支，然後又進行了 rebase，這將導致需要強制推送（`git push --force`），可能會干擾其他合作者的工作。
- **解決衝突**：在 rebase 過程中，如果遠端分支上的變更與你本地的變更發生衝突，你必須手動解決這些衝突。這可能會比合併時更繁瑣，因為每個衝突都需要在 rebase 過程中依次解決。

設定 `pull.rebase` 為 `true` 是一種常見的做法，尤其是在那些偏好保持乾淨線性歷史的團隊中。這個設定可以通過下面的命令來配置：

```bash
git config --global pull.rebase true
```

這樣設定之後，所有的 `git pull` 命令都會自動轉成使用 rebase 而非 merge。


## 設定為全局 

1. 倉庫級設定不加任何額外參數。

2. 全局設定加上 `--global` 參數，所有的 `git pull` 操作默認將使用合併而非變基（rebase），這有助於保持分支的合併歷史，尤其是在團隊合作時，能夠清楚地看到合併的時間點和上下文。。
```bash
git config --global pull.rebase false
```