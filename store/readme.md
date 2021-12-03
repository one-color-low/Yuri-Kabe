# Description
リバースプロキシによって`http://store/`のリクエストはこちらのサーバーに転送されます。
`http://store/upload/`でアップロードされたファイル保存処理を実行します。
また、`http://sotore/room_xxx/index.html`等へのリクエストには直接レスポンスします。

# Todo
1. リバースプロキシを介してindex.htmlへのアクセスができるか確認
2. main.pyで保存処理できるか
3. 保存したroomにアクセスできるか

# memo
仕事は遊び。遊びが仕事。