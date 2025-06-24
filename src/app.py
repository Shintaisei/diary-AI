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

# 現在のディレクトリをパスに追加
sys.path.append(os.path.dirname(__file__))

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
            context_used = result.get("context_used", False)
            context_msg = "\n📊 過去の日記履歴を考慮したアドバイスを生成しました" if context_used else "\n💡 初回または履歴が少ないため、一般的なアドバイスを生成しました"
            return f"✅ 日記が作成されました！\n📝 タイトル: {generated_title}\n🤖 AI分析も完了し、Notionに保存されました{context_msg}"
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
    return """📊 AI分析機能について（履歴対応版）

このアプリは日記を作成すると、以下の分析を自動で実行します：

🎯 タイトル自動生成
- 日記の内容から適切なタイトルを生成
- 主要テーマや感情を反映
- ユニークな名前を心がけてほしい

📊 要約作成  
- 日記の重要なポイントを簡潔にまとめ
- 3-4文で主要な出来事を要約

💡 アドバイス生成（履歴対応）
- 過去の日記履歴を考慮した継続的なアドバイス
- 成長の軌跡や繰り返しパターンを分析
- 個人の成長と幸福に焦点を当てた長期的サポート
- お母さんのような優しい目線でアドバイス励まし

😊 感情分析
- 全体的な気分を分析（positive/neutral/negative）
- 検出された感情の詳細
- 気分の変化や傾向を追跡

📈 継続的な記録
- すべての日記をローカルに保存
- ユーザープロファイルを自動更新
- パターン分析とトレンド把握

すべての分析結果は日記と一緒にNotionに保存され、
ローカルファイルにも履歴として蓄積されます。"""

def get_user_analytics():
    """ユーザーの分析情報を取得する関数"""
    try:
        result = diary_manager.get_user_analytics()
        
        if result["status"] == "success":
            profile = result.get("user_profile", {})
            patterns = result.get("patterns", {})
            
            analytics_text = "📊 あなたの日記分析レポート\n\n"
            
            # 基本統計
            total_entries = profile.get("total_entries", 0)
            analytics_text += f"📝 総日記数: {total_entries}件\n"
            
            # 気分の傾向
            if "recent_mood_trend" in profile:
                trend = profile["recent_mood_trend"]
                positive_ratio = trend.get("positive_ratio", 0) * 100
                dominant_mood = trend.get("dominant_mood", "不明")
                analytics_text += f"😊 最近の気分: ポジティブ{positive_ratio:.1f}% (主な気分: {dominant_mood})\n"
            
            # パターン分析
            if "mood_patterns" in patterns:
                mood_patterns = patterns["mood_patterns"]
                if "most_common_mood" in mood_patterns:
                    most_common = mood_patterns["most_common_mood"]
                    analytics_text += f"🎭 最も多い気分: {most_common}\n"
            
            # 成長の指標
            if "growth_indicators" in patterns:
                growth = patterns["growth_indicators"]
                if "writing_length_trend" in growth:
                    trend = growth["writing_length_trend"]
                    if trend.get("improvement", False):
                        analytics_text += f"📈 文章量が増加傾向にあります（成長の兆し！）\n"
                    else:
                        analytics_text += f"📝 文章量は安定しています\n"
            
            return analytics_text
        else:
            return f"❌ エラー: {result.get('message', '不明なエラー')}"
            
    except Exception as e:
        return f"❌ エラー: {str(e)}"

def get_history_summary(days: int = 30):
    """履歴の要約を取得する関数"""
    try:
        result = diary_manager.get_diary_history_summary(days)
        
        if result["status"] == "success":
            if "message" in result:
                return result["message"], None
            
            summary = result["summary"]
            summary_text = f"📅 過去{days}日間の日記履歴\n"
            summary_text += f"📝 総数: {summary['total_entries']}件\n"
            summary_text += f"📆 期間: {summary['date_range']['start']} ～ {summary['date_range']['end']}\n"
            
            # DataFrameに変換
            df_data = []
            for entry in summary["entries"]:
                df_data.append({
                    "日付": entry["date"],
                    "タイトル": entry["title"],
                    "気分": entry["mood"],
                    "要約": entry["summary"][:50] + "..." if len(entry["summary"]) > 50 else entry["summary"]
                })
            
            df = pd.DataFrame(df_data)
            return summary_text, df
        else:
            return f"❌ エラー: {result.get('message', '不明なエラー')}", None
            
    except Exception as e:
        return f"❌ エラー: {str(e)}", None

def update_profile(name: str, age: str, occupation: str, interests: str, goals: str):
    """プロフィールを更新する関数"""
    try:
        # 興味と目標をリストに変換
        interests_list = [i.strip() for i in interests.split(',') if i.strip()] if interests else []
        goals_list = [g.strip() for g in goals.split(',') if g.strip()] if goals else []
        
        profile_data = {
            "name": name.strip(),
            "age": age.strip(),
            "occupation": occupation.strip(),
            "interests": interests_list,
            "goals": goals_list
        }
        
        result = diary_manager.update_user_profile(profile_data)
        
        if result["status"] == "success":
            return f"✅ {result['message']}\n\n📝 更新されたプロフィール:\n名前: {name}\n年齢: {age}\n職業: {occupation}\n興味: {', '.join(interests_list)}\n目標: {', '.join(goals_list)}"
        else:
            return f"❌ エラー: {result.get('message', '不明なエラー')}"
            
    except Exception as e:
        return f"❌ エラー: {str(e)}"

def get_current_profile():
    """現在のプロフィールを取得する関数"""
    try:
        profile = diary_manager.history.get_user_profile()
        
        if not profile:
            return "プロフィールが設定されていません。", "", "", "", "", ""
        
        name = profile.get("name", "")
        age = profile.get("age", "")
        occupation = profile.get("occupation", "")
        interests = ", ".join(profile.get("interests", []))
        goals = ", ".join(profile.get("goals", []))
        
        profile_text = f"📋 現在のプロフィール\n\n"
        profile_text += f"名前: {name or '未設定'}\n"
        profile_text += f"年齢: {age or '未設定'}\n"
        profile_text += f"職業: {occupation or '未設定'}\n"
        profile_text += f"興味・関心: {interests or '未設定'}\n"
        profile_text += f"目標: {goals or '未設定'}\n"
        
        return profile_text, name, age, occupation, interests, goals
        
    except Exception as e:
        return f"❌ エラー: {str(e)}", "", "", "", "", ""

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

def create_app():
    """Gradioアプリケーションを作成"""
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
                        lines=25,
                        elem_classes=["big-textbox"],
                        show_label=False,
                        container=False
                    )
                    
                    create_btn = gr.Button(
                        "✍️ 日記を保存してAI分析",
                        variant="primary",
                        elem_classes=["create-button"]
                    )
                    
                    result_output = gr.Textbox(
                        label="結果",
                        interactive=False,
                        elem_classes=["result-box"],
                        lines=5
                    )
                    
                    # ボタンクリック時の処理
                    create_btn.click(
                        fn=create_diary,
                        inputs=[content_input],
                        outputs=[result_output]
                    )
            
            # タブ2: 最近の日記
            with gr.Tab("📚 最近の日記"):
                with gr.Column():
                    gr.HTML("""
                        <div style="text-align: center; margin: 20px 0;">
                            <h2 style="color: #4a5568;">最近の日記</h2>
                            <p style="color: #718096;">保存された日記を確認できます</p>
                        </div>
                    """)
                    
                    limit_input = gr.Slider(
                        minimum=1,
                        maximum=20,
                        value=5,
                        step=1,
                        label="表示件数"
                    )
                    
                    load_btn = gr.Button("📚 日記を読み込み", variant="secondary")
                    
                    diaries_status = gr.Textbox(
                        label="ステータス",
                        interactive=False,
                        lines=2
                    )
                    
                    diaries_table = gr.DataFrame(
                        headers=["タイトル", "作成日", "ID"],
                        label="日記一覧"
                    )
                    
                    # 日記読み込み処理
                    load_btn.click(
                        fn=get_recent_diaries,
                        inputs=[limit_input],
                        outputs=[diaries_status, diaries_table]
                    )
            
            # タブ3: プロフィール設定
            with gr.Tab("👤 プロフィール"):
                with gr.Column():
                    gr.HTML("""
                        <div style="text-align: center; margin: 20px 0;">
                            <h2 style="color: #4a5568;">プロフィール設定</h2>
                            <p style="color: #718096;">AIがあなたをより理解して、個人的なアドバイスを提供します</p>
                        </div>
                    """)
                    
                    # 現在のプロフィール表示
                    load_profile_btn = gr.Button("📋 現在のプロフィールを表示", variant="secondary")
                    current_profile_display = gr.Textbox(
                        label="現在のプロフィール",
                        interactive=False,
                        lines=8
                    )
                    
                    # プロフィール編集フォーム
                    gr.HTML("<h3 style='color: #4a5568; margin-top: 30px;'>プロフィール編集</h3>")
                    
                    with gr.Row():
                        name_input = gr.Textbox(label="お名前", placeholder="例: 田中太郎")
                        age_input = gr.Textbox(label="年齢", placeholder="例: 25歳")
                    
                    occupation_input = gr.Textbox(label="職業", placeholder="例: エンジニア、学生、主婦など")
                    interests_input = gr.Textbox(
                        label="興味・関心",
                        placeholder="例: 読書, 映画鑑賞, 料理, プログラミング（カンマ区切りで入力）",
                        lines=2
                    )
                    goals_input = gr.Textbox(
                        label="目標",
                        placeholder="例: 健康的な生活, スキルアップ, 新しい趣味を見つける（カンマ区切りで入力）",
                        lines=2
                    )
                    
                    update_profile_btn = gr.Button("💾 プロフィールを更新", variant="primary")
                    profile_update_result = gr.Textbox(
                        label="更新結果",
                        interactive=False,
                        lines=6
                    )
                    
                    # イベント処理
                    def load_and_populate_profile():
                        result = get_current_profile()
                        return result[0], result[1], result[2], result[3], result[4], result[5]
                    
                    load_profile_btn.click(
                        fn=load_and_populate_profile,
                        outputs=[current_profile_display, name_input, age_input, occupation_input, interests_input, goals_input]
                    )
                    
                    update_profile_btn.click(
                        fn=update_profile,
                        inputs=[name_input, age_input, occupation_input, interests_input, goals_input],
                        outputs=[profile_update_result]
                    )
            
            # タブ4: 日記履歴・分析
            with gr.Tab("📊 履歴・分析"):
                with gr.Column():
                    gr.HTML("""
                        <div style="text-align: center; margin: 20px 0;">
                            <h2 style="color: #4a5568;">あなたの日記分析</h2>
                            <p style="color: #718096;">継続的な記録から見えるパターンと成長</p>
                        </div>
                    """)
                    
                    # 分析レポート
                    analytics_btn = gr.Button("📊 分析レポートを生成", variant="secondary")
                    analytics_output = gr.Textbox(
                        label="分析レポート",
                        interactive=False,
                        lines=10
                    )
                    
                    # 履歴要約
                    with gr.Row():
                        history_days = gr.Slider(
                            minimum=7,
                            maximum=90,
                            value=30,
                            step=7,
                            label="履歴期間（日）"
                        )
                        history_btn = gr.Button("📅 履歴を表示", variant="secondary")
                    
                    history_status = gr.Textbox(
                        label="履歴ステータス",
                        interactive=False,
                        lines=3
                    )
                    
                    history_table = gr.DataFrame(
                        headers=["日付", "タイトル", "気分", "要約"],
                        label="日記履歴"
                    )
                    
                    # イベント処理
                    analytics_btn.click(
                        fn=get_user_analytics,
                        outputs=[analytics_output]
                    )
                    
                    history_btn.click(
                        fn=get_history_summary,
                        inputs=[history_days],
                        outputs=[history_status, history_table]
                    )
            
            # タブ5: AI分析について
            with gr.Tab("🤖 AI分析について"):
                gr.HTML("""
                    <div style="text-align: center; margin: 20px 0;">
                        <h2 style="color: #4a5568;">AI分析機能</h2>
                    </div>
                """)
                
                analysis_info = gr.Textbox(
                    value=get_ai_analysis_demo(),
                    label="AI分析機能の詳細",
                    interactive=False,
                    lines=15
                )
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7862) 