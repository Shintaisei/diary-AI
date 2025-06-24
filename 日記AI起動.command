#!/bin/bash

# 日記AI ワンクリック起動スクリプト (.command)
# このファイルをデスクトップにコピーしてダブルクリックで起動

echo "🚀 日記AI を起動しています..."

# 日記AIのディレクトリパス
DIARY_AI_DIR="/Users/komatsuzakiharutoshi/Desktop/自己開発/日記AI"

# ディレクトリに移動
echo "📁 ディレクトリに移動: $DIARY_AI_DIR"
cd "$DIARY_AI_DIR"

# 仮想環境をアクティブ化
echo "🔧 仮想環境をアクティブ化中..."
source venv/bin/activate

# Pythonアプリを起動
echo "🤖 日記AIアプリを起動中..."
python app_gradio.py &

# プロセスIDを保存
APP_PID=$!

# アプリが起動するまで待機
echo "⏳ アプリの起動を待機中..."
sleep 4

# ブラウザでアプリを開く
echo "🌐 ブラウザでアプリを開いています..."
open http://localhost:7860

echo ""
echo "✅ 日記AIが起動しました！"
echo "🌐 ブラウザで http://localhost:7860 が開かれます"
echo ""
echo "📝 このターミナルを閉じるとアプリも終了します"
echo "🔄 アプリを停止するには、このウィンドウを閉じるか Ctrl+C を押してください"
echo ""

# フォアグラウンドでプロセスを待機
wait $APP_PID

echo "👋 日記AIを終了しました" 