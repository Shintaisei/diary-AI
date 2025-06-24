#!/bin/bash

# 日記AI 自動起動スクリプト
# ワンクリックで日記AIを起動してブラウザで開きます

echo "🚀 日記AI を起動しています..."

# スクリプトのディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 ディレクトリ: $SCRIPT_DIR"

# 仮想環境をアクティブ化
echo "🔧 仮想環境をアクティブ化中..."
source venv/bin/activate

# Pythonアプリを起動（バックグラウンドで実行）
echo "🤖 日記AIアプリを起動中..."
python app_gradio.py &

# プロセスIDを保存
APP_PID=$!
echo "📝 アプリのプロセスID: $APP_PID"

# アプリが起動するまで少し待機
echo "⏳ アプリの起動を待機中..."
sleep 3

# ブラウザでアプリを開く
echo "🌐 ブラウザでアプリを開いています..."
open http://localhost:7860

echo "✅ 日記AIが起動しました！"
echo "🌐 ブラウザで http://localhost:7860 が開かれます"
echo ""
echo "📝 使い方:"
echo "   - ブラウザでアプリが開きます"
echo "   - 終了するには Ctrl+C を押してください"
echo ""
echo "🔄 アプリを停止するには、ターミナルで Ctrl+C を押すか"
echo "   以下のコマンドを実行してください:"
echo "   kill $APP_PID"

# フォアグラウンドでプロセスを待機（Ctrl+Cで終了可能）
wait $APP_PID 