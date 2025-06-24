#!/bin/bash

# 日記AI 起動スクリプト
# Web版とCLI版の両方に対応

echo "🚀 日記AI を起動しています..."

# スクリプトのディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 ディレクトリ: $SCRIPT_DIR"

# 仮想環境をアクティブ化
echo "🔧 仮想環境をアクティブ化中..."
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ venv フォルダが見つかりません。"
    echo "最初に 'python -m venv venv' を実行してください。"
    exit 1
fi

# 必要なパッケージをインストール
echo "📦 必要なパッケージをインストール中..."
pip install -r src/requirements.txt

# 設定ファイルの確認
if [ ! -f "src/config.py" ]; then
    echo "⚠️  設定ファイルが見つかりません。"
    echo "src/config.py.example を src/config.py にコピーして設定してください。"
    echo "設定ファイルを自動作成しますか？ (y/N): "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cp src/config.py.example src/config.py
        echo "✅ src/config.py を作成しました。"
        echo "ファイルを編集してAPIキーを設定してください。"
        echo "編集しますか？ (y/N): "
        read -r edit_response
        if [[ "$edit_response" =~ ^[Yy]$ ]]; then
            nano src/config.py
        fi
    else
        echo "❌ 設定ファイルが必要です。終了します。"
        exit 1
    fi
fi

# 起動モードを選択
echo ""
echo "起動モードを選択してください:"
echo "1. Web版 (Gradio UI)"
echo "2. CLI版 (コマンドライン)"
echo "3. 終了"
echo ""
echo "選択 (1-3): "
read -r mode

case $mode in
    1)
        echo "🌐 Web版を起動中..."
        python src/app.py &
        APP_PID=$!
        
        echo "⏳ アプリの起動を待機中..."
        sleep 3
        
        echo "🌐 ブラウザでアプリを開いています..."
        open http://localhost:7860
        
        echo "✅ 日記AI Web版が起動しました！"
        echo "🌐 ブラウザで http://localhost:7860 が開かれます"
        echo "🔄 アプリを停止するには Ctrl+C を押してください"
        
        # フォアグラウンドでプロセスを待機
        wait $APP_PID
        ;;
    2)
        echo "💻 CLI版を起動中..."
        python src/cli.py
        ;;
    3)
        echo "👋 終了します。"
        exit 0
        ;;
    *)
        echo "❌ 無効な選択です。"
        exit 1
        ;;
esac 