# 使用するベースイメージ
FROM rasa/rasa:latest

# 作業ディレクトリの設定
WORKDIR /app

# 必要な依存パッケージをコピー（requirements.txt があれば）
COPY requirements.txt /app/

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルのコピー
COPY . /app/

# ポートの公開
EXPOSE 3001

# Rasa のサーバーを起動（PORT 環境変数でポート番号を指定）
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "3001"]