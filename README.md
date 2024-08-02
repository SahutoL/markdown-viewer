# Markdown Viewer PWA

Markdown Viewer PWAは、Markdownファイルをアップロードして閲覧するためのシンプルで使いやすいウェブアプリケーションです。PWA（Progressive Web App）として実装されているため、デスクトップにインストールして使用することもできます。

## デモ

アプリケーションのライブデモは以下のURLで確認できます：
[https://markdown-viewer.onrender.com/](https://markdown-viewer.onrender.com/)

## 機能

- Markdownファイルのアップロード
- アップロードされたファイルの一覧表示
- Markdownの表示（HTMLへの変換）
- レスポンシブデザイン
- PWA機能（オフライン対応、ホーム画面へのインストール）

## 技術スタック

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Markdown処理: Python-Markdown
- セキュリティ: Bleach (HTMLサニタイズ)
- PWA: Service Worker

## ローカルでの実行方法

1. リポジトリをクローンします：
   ```
   git clone https://github.com/SahutoL/markdown-viewer.git
   cd markdown-viewer
   ```

2. 仮想環境を作成し、アクティベートします：
   ```
   python -m venv venv
   . venv/bin/activate  # Windowsの場合: venv\Scripts\activate
   ```

3. 必要なパッケージをインストールします：
   ```
   pip install -r requirements.txt
   ```

4. アプリケーションを実行します：
   ```
   python app.py
   ```

5. ブラウザで `http://localhost:5000` にアクセスします。

## デプロイ

このアプリケーションは[Render](https://render.com/)にデプロイされています。Renderでデプロイする場合は、以下の設定を使用してください：

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

## 注意事項

- Renderの無料プランを使用している場合、アップロードされたファイルは永続的に保存されません。

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
