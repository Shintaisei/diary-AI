# 🗓️ 日記AI - Notion連携AIアシスタント

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Notion](https://img.shields.io/badge/Notion-API-black.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Notionデータベースと連携して、AIによる感情分析・日記管理機能を提供するPythonアプリケーションです。OpenAI GPTを活用した高度な日記分析とGradio WebUIによる直感的な操作を提供します。

## ✨ 主な機能

- 📝 **日記作成**: Notionデータベースに新しい日記エントリーを作成
- 🤖 **AI分析**: OpenAI GPTを使用した感情分析、要約、アドバイス生成
- 📊 **トレンド分析**: 複数の日記エントリーから気分の変化や傾向を分析
- 💡 **日次洞察**: 今日のおすすめアクションと気分の傾向を表示
- 🔍 **既存日記分析**: 過去の日記エントリーにAI分析を追加
- 🌐 **Gradio WebUI**: ブラウザベースの使いやすいインターフェース

## 🚀 クイックスタート

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/diary-ai.git
cd diary-ai
```

### 2. 仮想環境の作成とアクティベート

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境をアクティベート
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 設定ファイルの作成

```bash
# 設定テンプレートをコピー
cp config.py.example config.py
```

`config.py`ファイルを編集して、以下の値を設定してください：

- `NOTION_API_KEY`: Notion統合のAPIキー
- `NOTION_DATABASE_ID`: 日記用NotionデータベースのID
- `OPENAI_API_KEY`: OpenAI APIキー

### 5. アプリケーションの起動

```bash
# コマンドラインインターフェース
python main.py

# または Web UI (Gradio)
python app_gradio.py
```

Web UI の場合、ブラウザで `http://localhost:7860` にアクセスできます。

## 🔧 セットアップガイド

### Notionデータベースの準備

1. Notionで新しいデータベースを作成
2. 以下のプロパティを追加：
   - **タイトル** (Title): ページのタイトル
   - **日付** (Date): 日記の日付
   - **内容** (Rich Text): 日記の内容
   - **AI分析** (Rich Text): AI による分析結果 (オプション)

### APIキーの取得

#### Notion API キー
1. [Notion Developers](https://developers.notion.com/)にアクセス
2. 新しいintegrationを作成
3. APIキーをコピー
4. 日記データベースにintegrationを招待

#### OpenAI API キー  
1. [OpenAI API](https://platform.openai.com/api-keys)にアクセス
2. 新しいAPIキーを作成
3. キーをコピー

### 必要な権限設定

Notion integration に以下の権限を付与：
- Read content
- Update content
- Insert content

## 📖 使用方法

### コマンドラインモード

```bash
python main.py
```

メニューから以下の機能を選択：

1. **新しい日記を作成** - タイトルと内容を入力して日記を作成し、AI分析を実行
2. **最近の日記を表示・分析** - 最近の日記を取得してトレンド分析を実行
3. **既存の日記を分析** - 指定したページIDの日記にAI分析を追加
4. **今日の洞察を表示** - 今日のおすすめアクションと気分の傾向を表示
5. **終了** - アプリケーションを終了

### Web UIモード

```bash
python app_gradio.py
```

ブラウザでアクセスし、直感的なWebインターフェースで日記の作成・分析が可能です。

## 📁 プロジェクト構造

```
日記AI/
├── 📁 src/                     # メインソースコード
│   ├── __init__.py             # パッケージ初期化
│   ├── notion_diary_client.py  # Notion API連携
│   ├── ai_analyzer.py          # AI分析機能
│   ├── diary_manager.py        # 日記管理機能統合
│   └── config.py               # 設定ファイル
├── 📁 venv/                    # 仮想環境
├── main.py                     # コマンドラインエントリーポイント
├── app_gradio.py               # Web UI エントリーポイント
├── requirements.txt            # 依存関係
├── config.py.example           # 設定テンプレート
├── .gitignore                  # Git除外設定
└── README.md                   # このファイル
```

## 🛠️ 依存関係

- `notion-client==2.4.0` - Notion API連携
- `openai==1.90.0` - OpenAI GPT API連携
- `python-dotenv==1.1.0` - 環境変数管理
- `requests==2.32.4` - HTTPリクエスト処理
- `gradio==4.44.0` - Web UI フレームワーク

## 🔍 トラブルシューティング

### よくある問題

1. **設定ファイルエラー**
   ```
   ModuleNotFoundError: No module named 'config'
   ```
   - `config.py.example` を `config.py` にコピーして設定値を入力してください

2. **Notion API エラー**
   ```
   NotionClientError: The integration does not have access to the database
   ```
   - データベースIDが正しいか確認
   - Integrationがデータベースに招待されているか確認
   - データベースのプロパティ名が正しいか確認

3. **OpenAI API エラー**
   ```
   OpenAIError: Incorrect API key provided
   ```
   - APIキーが有効か確認
   - API使用量の制限に達していないか確認

### デバッグモード

`config.py` で `DEBUG = True` に設定すると、詳細なログが出力されます。

## 🤝 コントリビューション

プロジェクトへの貢献を歓迎します！

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 🔮 今後の予定

- [ ] 複数の日記データベース対応
- [ ] より高度な感情分析・トレンド予測
- [ ] データエクスポート機能
- [ ] モバイル対応の改善
- [ ] 他のAIモデル (Claude, Gemini) 対応
- [ ] グラフ・チャート表示機能

## 💬 サポート

質問やバグ報告は、GitHub Issues で報告してください。

---

**🤖 AIと共に、より良い日記習慣を築きましょう！** 