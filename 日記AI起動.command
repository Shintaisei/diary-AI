#!/bin/bash

# 日記AI デスクトップ起動ファイル（Gradio自動起動版）
# このファイルをデスクトップにコピーしてダブルクリックで起動

echo "🚀 日記AI を起動しています..."

# 日記AIのディレクトリパス（自動検出）
DIARY_AI_DIR="/Users/komatsuzakiharutoshi/Desktop/自己開発/日記AI"

# ディレクトリが存在するかチェック
if [ ! -d "$DIARY_AI_DIR" ]; then
    echo "❌ 日記AIディレクトリが見つかりません: $DIARY_AI_DIR"
    echo "パスを確認してください。"
    echo "現在のディレクトリ一覧:"
    ls -la "/Users/komatsuzakiharutoshi/Desktop/自己開発/"
    echo ""
    echo "このウィンドウを閉じるまで待機中..."
    read -p "Enterキーを押して終了..."
    exit 1
fi

# ディレクトリに移動
echo "📁 ディレクトリに移動: $DIARY_AI_DIR"
cd "$DIARY_AI_DIR"

# 現在の仮想環境を解除（もしアクティブなら）
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "🔧 現在の仮想環境を解除中..."
    deactivate 2>/dev/null || true
fi

# 仮想環境をアクティブ化
echo "🔧 仮想環境をアクティブ化中..."
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ venv フォルダが見つかりません。"
    echo "最初に 'python -m venv venv' を実行してください。"
    echo ""
    echo "このウィンドウを閉じるまで待機中..."
    read -p "Enterキーを押して終了..."
    exit 1
fi

# 必要なパッケージをインストール
echo "📦 必要なパッケージをインストール中..."
pip install -r src/requirements.txt --quiet

# 設定ファイルの確認
if [ ! -f "src/config.py" ]; then
    echo "⚠️  設定ファイルが見つかりません。"
    echo "src/config.py.example を src/config.py にコピーして設定してください。"
    echo "設定ファイルを自動作成します..."
    cp src/config.py.example src/config.py
    echo "✅ src/config.py を作成しました。"
    echo ""
    echo "⚠️  APIキーの設定が必要です。"
    echo "src/config.py ファイルを編集してAPIキーを設定してください。"
    echo ""
    echo "設定完了後、再度このファイルをダブルクリックして起動してください。"
    echo ""
    echo "このウィンドウを閉じるまで待機中..."
    read -p "Enterキーを押して終了..."
    exit 1
fi

# Gradio Web版を自動起動
echo "🌐 日記AI Web版を起動中..."
python src/app.py &
APP_PID=$!

# アプリが起動するまで待機
echo "⏳ アプリの起動を待機中..."
sleep 4

# ブラウザでアプリを開く
echo "🌐 ブラウザでアプリを開いています..."
open http://localhost:7862

echo ""
echo "✅ 日記AI Web版が起動しました！"
echo "🌐 ブラウザで http://localhost:7862 が開かれます"
echo ""
echo "📝 このターミナルを閉じるとアプリも終了します"
echo "🔄 アプリを停止するには、このウィンドウを閉じるか Ctrl+C を押してください"
echo ""

# フォアグラウンドでプロセスを待機（Ctrl+Cで終了可能）
wait $APP_PID

echo ""
echo "👋 日記AIを終了しました"
echo "このウィンドウを閉じることができます。" 