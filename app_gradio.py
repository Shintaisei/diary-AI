#!/usr/bin/env python3
"""
日記AI - GradioベースWebアプリ
美しいUIで日記の作成・表示・AI分析ができるWebアプリケーション
"""

import sys
import os
from datetime import datetime
import gradio as gr
import pandas as pd

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from diary_manager import DiaryManager

# 設定ファイルの読み込み
try:
    import config
    NOTION_API_KEY = config.NOTION_API_KEY
    NOTION_DATABASE_ID = config.NOTION_DATABASE_ID
    OPENAI_API_KEY = config.OPENAI_API_KEY
except ImportError:
    raise Exception("src/config.pyファイルが見つかりません。適切な設定をしてください。")

# 日記管理システムを初期化
diary_manager = DiaryManager(
    notion_api_key=NOTION_API_KEY,
    notion_database_id=NOTION_DATABASE_ID,
    openai_api_key=OPENAI_API_KEY
)

def create_diary(content: str):
    """新しい日記を作成する関数（タイトル自動生成）"""
    if not content.strip():
        return "❌ 内容を入力してください"
    
    try:
        result = diary_manager.create_diary_with_analysis(content.strip())
        
        if result["status"] == "success":
            generated_title = result.get("generated_title", "タイトル生成エラー")
            return f"✅ 日記が作成されました！\n📝 タイトル: {generated_title}\n🤖 AI分析も完了し、Notionに保存されました"
        else:
            return f"❌ エラー: {result.get('message', '不明なエラー')}"
            
    except Exception as e:
        return f"❌ エラー: {str(e)}"

def get_recent_diaries(limit: int = 5):
    """最近の日記を取得する関数"""
    try:
        result = diary_manager.get_recent_diaries(limit)
        
        if result["status"] == "success":
            diary_entries = result.get("diary_entries", [])
            
            if not diary_entries:
                return "日記が見つかりませんでした。", None
            
            # DataFrameに変換して表示
            df_data = []
            for entry in diary_entries:
                df_data.append({
                    "タイトル": entry['title'],
                    "作成日": entry['created_time'][:10] if entry['created_time'] else 'N/A',
                    "ID": entry['id'][:8] + "..."  # IDは短縮表示
                })
            
            df = pd.DataFrame(df_data)
            return f"📝 最近の日記 ({len(diary_entries)}件)", df
        else:
            return f"❌ エラー: {result.get('message', '不明なエラー')}", None
            
    except Exception as e:
        return f"❌ エラー: {str(e)}", None

def get_ai_analysis_demo():
    """AI分析のデモを表示"""
    return """📊 AI分析機能について

このアプリは日記を作成すると、以下の分析を自動で実行します：

🎯 タイトル自動生成
- 日記の内容から適切なタイトルを生成
- 主要テーマや感情を反映

📊 要約作成  
- 日記の重要なポイントを簡潔にまとめ
- 3-4文で主要な出来事を要約

💡 アドバイス生成
- 建設的で励ましになるアドバイス
- 個人の成長や幸福に焦点

😊 感情分析
- 全体的な気分を分析（positive/neutral/negative）
- 検出された感情の詳細

すべての分析結果は日記と一緒にNotionに保存されます。"""

def add_comment_to_selected_diary(selected_row, comment: str):
    """選択された日記にコメントを追加する関数"""
    if not comment.strip():
        return "❌ コメントは必須です。"
    
    try:
        # 最近の日記を取得してIDを探す
        result = diary_manager.get_recent_diaries(10)
        if result["status"] != "success":
            return f"❌ エラー: {result.get('message', '不明なエラー')}"
        
        diary_entries = result.get("diary_entries", [])
        if not diary_entries or selected_row >= len(diary_entries):
            return "❌ 選択された日記が見つかりません。"
        
        selected_entry = diary_entries[selected_row]
        success = diary_manager.notion_client.add_comment_to_diary(
            selected_entry['id'], 
            comment.strip()
        )
        
        if success:
            return "✅ コメントが追加されました！"
        else:
            return "❌ コメントの追加に失敗しました。"
            
    except Exception as e:
        return f"❌ エラー: {str(e)}"

# Gradioインターフェースを構築
with gr.Blocks(
    theme=gr.themes.Soft(),
    title="📝 日記AI",
    css="""
        .main-container { max-width: 900px; margin: 0 auto; }
        .app-header { text-align: center; margin: 20px 0 30px 0; }
        .big-textbox textarea { 
            font-size: 16px !important; 
            line-height: 1.8 !important; 
            padding: 20px !important;
            border: none !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
        }
        .create-button { 
            margin: 20px 0 !important; 
            font-size: 18px !important;
            padding: 15px 30px !important;
        }
        .result-box { 
            font-size: 16px !important;
            background: #f8f9fa !important;
            border-radius: 10px !important;
            padding: 15px !important;
        }
        .diary-container {
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
        }
    """
) as app:
    
    # シンプルなヘッダー
    gr.HTML("""
        <div class="app-header">
            <h1 style="font-size: 2.5em; margin-bottom: 10px; color: #2d3748;">📝 日記AI</h1>
            <p style="font-size: 1.1em; color: #718096;">AIと一緒に日記を書こう</p>
        </div>
    """)
    
    # すべての機能をタブで整理
    with gr.Tabs():
        # タブ1: 日記作成（メイン）
        with gr.Tab("✍️ 日記を書く"):
            with gr.Column(elem_classes=["diary-container"]):
                gr.HTML("""
                    <div style="text-align: center; margin: 20px 0 30px 0;">
                        <h2 style="font-size: 1.8em; color: #4a5568; margin-bottom: 10px;">今日の日記</h2>
                        <p style="color: #718096;">今日あったことを自由に書いてください</p>
                    </div>
                """)
                
                content_input = gr.Textbox(
                    placeholder="""今日はどんな一日でしたか？

思ったこと、感じたこと、起こったこと...
何でも自由に書いてください。

AIがタイトルを生成し、感情や体験を分析してNotionに保存します。""",
                    lines=20,
                    elem_classes=["big-textbox"],
                    show_label=False,
                    container=False
                )
                
                create_btn = gr.Button(
                    "🤖 AI分析してNotionに保存", 
                    variant="primary", 
                    size="lg",
                    elem_classes=["create-button"]
                )
                
                result_output = gr.Textbox(
                    lines=3,
                    interactive=False,
                    elem_classes=["result-box"],
                    show_label=False,
                    visible=False,
                    container=False
                )
                
                create_btn.click(
                    create_diary,
                    inputs=[content_input],
                    outputs=[result_output]
                ).then(
                    lambda: gr.update(visible=True),
                    outputs=[result_output]
                )
        
        # タブ2: AI分析について
        with gr.Tab("🤖 AI分析機能"):
            gr.Markdown(get_ai_analysis_demo())
        
        # タブ3: これまでの日記
        with gr.Tab("📚 これまでの日記"):
            gr.Markdown("### 📖 過去の日記を振り返る")
            
            with gr.Row():
                limit_slider = gr.Slider(
                    minimum=1, 
                    maximum=20, 
                    value=5, 
                    step=1,
                    label="表示件数"
                )
                load_btn = gr.Button("📚 日記を読み込み", variant="secondary")
            
            diary_status = gr.Textbox(label="状態", lines=1)
            diary_table = gr.Dataframe(
                headers=["タイトル", "作成日", "ID"],
                label="日記一覧"
            )
            
            load_btn.click(
                get_recent_diaries,
                inputs=[limit_slider],
                outputs=[diary_status, diary_table]
            )
        
        # タブ4: 追加コメント
        with gr.Tab("💭 追加コメント"):
            gr.Markdown("### 💬 既存の日記に後からコメントを追加")
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("**1. まず日記を読み込んでください**")
                    load_for_comment_btn = gr.Button("📚 日記を読み込み", variant="secondary")
                    
                    comment_diary_table = gr.Dataframe(
                        headers=["タイトル", "作成日", "ID"],
                        label="日記一覧"
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("**2. コメントを追加**")
                    
                    selected_row = gr.Number(
                        label="日記番号（0から開始）",
                        value=0,
                        minimum=0
                    )
                    
                    comment_input = gr.Textbox(
                        label="追加するコメント",
                        placeholder="後から思ったことや気づいたことを書いてください...",
                        lines=4
                    )
                    
                    add_comment_btn = gr.Button("💭 コメントを追加", variant="primary")
                    comment_result = gr.Textbox(label="結果", lines=2)
            
            load_for_comment_btn.click(
                lambda: get_recent_diaries(10),
                outputs=[gr.Textbox(visible=False), comment_diary_table]
            )
            
            add_comment_btn.click(
                add_comment_to_selected_diary,
                inputs=[selected_row, comment_input],
                outputs=[comment_result]
            )
    
    gr.HTML("""
        <div style="text-align: center; margin-top: 30px; padding: 15px; color: #718096; background-color: #f7fafc; border-radius: 15px;">
            <p style="margin: 0; font-size: 0.9em;">🤖 Powered by OpenAI & Notion API</p>
        </div>
    """)

if __name__ == "__main__":
    print("🚀 日記AI Webアプリを起動しています...")
    print("ブラウザで http://localhost:7860 にアクセスしてください")
    
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 