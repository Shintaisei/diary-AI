# 日記AI - 個人的なAIアドバイザー

継続的な学習機能を持つ日記アプリケーション。あなたの日記を分析し、個人的な成長をサポートする個別化されたアドバイスを提供します。

## ✨ 主な機能

- **📝 日記の記録**: Web UI または CLI で日記を書ける
- **🤖 AI分析**: OpenAI GPT-4を使用した感情分析と個別アドバイス
- **📊 継続的学習**: 過去の記録を学習し、文脈を考慮したアドバイス
- **👤 プロフィール管理**: 静的・動的両方のプロフィール学習システム
- **📈 履歴・分析**: 成長パターンの可視化と詳細分析
- **🌐 Web UI**: 美しいGradio インターフェース
- **⚡ 1クリック起動**: デスクトップから簡単起動

## 🏗️ システム構成

```
日記AI/
├── src/                    # メインコード
│   ├── app.py             # Web版（Gradio UI）
│   ├── cli.py             # CLI版
│   ├── ai_analyzer.py     # AI分析エンジン
│   ├── diary_manager.py   # 日記管理
│   ├── diary_history.py   # 履歴システム
│   ├── profile_manager.py # プロフィール管理
│   ├── config.py.example  # 設定ファイルテンプレート
│   └── requirements.txt   # 依存関係
├── data/                   # データストレージ
│   ├── diary_history.json # 日記履歴データ
│   └── profile.json       # ユーザープロフィール
├── venv/                   # Python仮想環境
├── start.sh               # 起動スクリプト
└── 日記AI起動.command      # デスクトップ1クリック起動
```

## 🚀 クイックスタート

### デスクトップから1クリック起動（推奨）

1. **`日記AI起動.command`をダブルクリック**
2. 自動的にブラウザが開き、アプリが起動します

### 手動起動

```bash
# 1. 仮想環境の有効化
source venv/bin/activate

# 2. 依存関係のインストール
pip install -r src/requirements.txt

# 3. 設定ファイルの作成
cp src/config.py.example src/config.py

# 4. 起動（Web版 or CLI版を選択）
./start.sh
```

## ⚙️ 初期設定

### 1. APIキーの設定

`src/config.py`ファイルを編集：

```python
# OpenAI API設定
OPENAI_API_KEY = "your-openai-api-key-here"

# Notion API設定（オプション）
NOTION_TOKEN = "your-notion-token-here"
NOTION_DATABASE_ID = "your-database-id-here"
```

### 2. プロフィール設定

`data/profile.json`で個人情報を設定：

```json
{
  "basic_info": {
    "name": "あなたの名前",
    "age": "年齢",
    "occupation": "職業",
    "location": "住んでいる場所"
  },
  "personality": {
    "traits": ["性格の特徴"],
    "values": ["大切にしている価値観"]
  },
  // ... その他の設定
}
```

## 📚 使い方

### Web版（推奨）

1. ブラウザで `http://localhost:7862` にアクセス
2. **📝 日記記録** タブで日記を書く
3. **📊 履歴・分析** タブで成長を確認
4. **👤 プロフィール設定** タブで個人情報を管理

### CLI版

```bash
python src/cli.py
```

対話式で日記の記録と履歴確認ができます。

## 🧠 AIシステムの特徴

### ハイブリッド学習システム

- **静的プロフィール** (`data/profile.json`)
  - 手動で設定する基本的な個人情報
  - 長期的な特徴や価値観

- **動的学習** (`data/diary_history.json`)
  - 日記から自動学習する変化するパターン
  - 気分の傾向、成長領域、関心事の変化

### 文脈を考慮したアドバイス

- 過去7日間の日記内容を分析
- 個人のプロフィールと成長パターンを考慮
- 継続的な改善に焦点を当てたアドバイス

## 🛠️ 技術仕様

- **言語**: Python 3.9+
- **UI フレームワーク**: Gradio 4.44.0
- **AI エンジン**: OpenAI GPT-4
- **データストレージ**: JSON ファイル
- **統合**: Notion API（オプション）

## 📦 依存関係

```
notion-client==2.4.0
python-dotenv==1.0.1
requests==2.32.4
openai==1.90.0
gradio==4.44.0
```

## 🔧 開発・カスタマイズ

### ディレクトリ説明

- `src/ai_analyzer.py`: AI分析ロジック
- `src/diary_manager.py`: 日記の CRUD 操作
- `src/diary_history.py`: 履歴管理とデータ永続化
- `src/profile_manager.py`: プロフィール管理

### カスタマイズポイント

1. **AIプロンプトの調整** (`src/ai_analyzer.py`)
2. **UI レイアウトの変更** (`src/app.py`)
3. **プロフィール項目の追加** (`data/profile.json`)

## 🐛 トラブルシューティング

### よくある問題

**Q: アプリが起動しない**
- 仮想環境が有効化されているか確認
- `src/config.py`が正しく設定されているか確認

**Q: AIアドバイスが生成されない**
- OpenAI API キーが正しく設定されているか確認
- インターネット接続を確認

**Q: データが保存されない**
- `data/`フォルダへの書き込み権限を確認
- ディスク容量を確認

### ログの確認

アプリケーション実行時のコンソール出力でエラー詳細を確認できます。

## 📄 ライセンス

このプロジェクトは個人利用目的で開発されています。

## 🤝 貢献

改善提案や機能追加のアイデアがあれば、お気軽にお知らせください。

---

**🎯 目標**: あなたの日々の記録から学習し、個人的な成長をサポートする最適なAIパートナーを提供すること 