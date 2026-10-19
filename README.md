# 段考闖關總站（quiz.efetl.com/exam/）

- `catalog.json`：開關清單。學段／科目／冊別的 `status`：`open` 開放、`soon` 敬請期待、`closed` 暫停開放（選單不顯示，直接開網址會看到「暫停開放」）。
- 結構：`<學段>/<科目>/<冊別>/`，學段 `jh` 國中、`es` 國小、`hs` 高中職。
- `assets/hub.js`＋`hub.css`：各層選單（依 catalog.json 即時畫卡片）。
- 闖關頁內嵌共用模組：手寫筆、換科目＋開放檢查（efetl-exam.js）、姓名共用與登出、錯題本＋隨機總測驗。
