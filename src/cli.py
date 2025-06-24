#!/usr/bin/env python3
"""
日記AI - CLI版
コマンドライン版のインターフェース
"""

import sys
import os
from datetime import datetime

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
    print("エラー: src/config.pyファイルが見つかりません。")
    print("src/config.pyを確認して、適切な値を設定してください。")
    sys.exit(1)

def main():
    """メイン関数"""
    print("🗒️  日記AI - Notion連携アプリ")
    print("=" * 50)
    
    # OpenAI APIキーのチェック
    if OPENAI_API_KEY == "your_openai_api_key_here":
        print("⚠️  OpenAI APIキーが設定されていません。")
        print("src/config.pyファイルのOPENAI_API_KEYを実際のAPIキーに変更してください。")
        print("AI機能なしで続行しますか？ (y/N): ", end="")
        response = input().strip().lower()
        if response != 'y' and response != 'yes':
            sys.exit(1)
    
    # 日記管理システムを初期化
    try:
        diary_manager = DiaryManager(
            notion_api_key=NOTION_API_KEY,
            notion_database_id=NOTION_DATABASE_ID,
            openai_api_key=OPENAI_API_KEY
        )
        print("✅ システム初期化完了")
    except Exception as e:
        print(f"❌ システム初期化エラー: {e}")
        sys.exit(1)
    
    while True:
        print("\n" + "=" * 50)
        print("メニューを選択してください:")
        print("1. 新しい日記を作成")
        print("2. 最近の日記を表示")
        print("3. 既存の日記にコメントを追加")
        print("4. 終了")
        print("=" * 50)
        
        choice = input("選択 (1-4): ").strip()
        
        if choice == "1":
            create_new_diary(diary_manager)
        elif choice == "2":
            show_recent_diaries(diary_manager)
        elif choice == "3":
            add_comment_to_diary(diary_manager)
        elif choice == "4":
            print("👋 アプリを終了します。")
            break
        else:
            print("❌ 無効な選択です。1-4の数字を入力してください。")

def create_new_diary(diary_manager: DiaryManager):
    """新しい日記を作成"""
    print("\n📝 新しい日記を作成")
    print("-" * 30)
    
    print("内容を入力してください（終了するには空行で'end'と入力）:")
    content_lines = []
    while True:
        line = input()
        if line.strip().lower() == "end":
            break
        content_lines.append(line)
    
    content = "\n".join(content_lines).strip()
    if not content:
        print("❌ 内容は必須です。")
        return
    
    print("\n🔄 日記を作成中...")
    result = diary_manager.create_diary_with_analysis(content)
    
    if result["status"] == "success":
        print("✅ 日記の作成が完了しました！")
        
        # 生成されたタイトルを表示
        generated_title = result.get("generated_title", "タイトル生成エラー")
        print(f"📝 生成されたタイトル: {generated_title}")
        
        # AI分析結果を表示
        ai_analysis = result.get("ai_analysis", {})
        
        if ai_analysis:
            print(f"\n📊 AI分析結果:")
            print(f"要約: {ai_analysis.get('summary', 'N/A')}")
            print(f"アドバイス: {ai_analysis.get('advice', 'N/A')}")
            
            emotions = ai_analysis.get('emotions', {})
            if isinstance(emotions, dict) and 'overall_mood' in emotions:
                print(f"全体的な気分: {emotions['overall_mood']}")
    else:
        print(f"❌ エラー: {result.get('message', '不明なエラー')}")

def show_recent_diaries(diary_manager: DiaryManager):
    """最近の日記を表示"""
    print("\n📚 最近の日記")
    print("-" * 30)
    
    limit = input("表示件数 (デフォルト: 5): ").strip()
    try:
        limit = int(limit) if limit else 5
    except ValueError:
        limit = 5
    
    print(f"\n🔄 {limit}件の日記を取得中...")
    result = diary_manager.get_recent_diaries(limit)
    
    if result["status"] == "success":
        diary_entries = result.get("diary_entries", [])
        
        print(f"\n📝 最近の日記 ({len(diary_entries)}件):")
        for i, entry in enumerate(diary_entries, 1):
            print(f"\n{i}. {entry['title']}")
            print(f"   作成日: {entry['created_time'][:10] if entry['created_time'] else 'N/A'}")
            print(f"   ID: {entry['id']}")
    else:
        print(f"❌ エラー: {result.get('message', '不明なエラー')}")

def add_comment_to_diary(diary_manager: DiaryManager):
    """既存の日記にコメントを追加"""
    print("\n💭 既存の日記にコメントを追加")
    print("-" * 30)
    
    # 最近の日記を表示
    print("最近の日記:")
    result = diary_manager.get_recent_diaries(5)
    
    if result["status"] != "success":
        print(f"❌ エラー: {result.get('message', '不明なエラー')}")
        return
    
    diary_entries = result.get("diary_entries", [])
    if not diary_entries:
        print("❌ 日記が見つかりませんでした。")
        return
    
    # 日記リストを表示
    for i, entry in enumerate(diary_entries, 1):
        print(f"{i}. {entry['title']} ({entry['created_time'][:10] if entry['created_time'] else 'N/A'})")
    
    # 日記を選択
    try:
        choice = int(input("\nコメントを追加したい日記の番号を選択してください: ").strip())
        if choice < 1 or choice > len(diary_entries):
            print("❌ 無効な選択です。")
            return
        
        selected_entry = diary_entries[choice - 1]
        
        # コメントを入力
        comment = input("追加するコメント: ").strip()
        if not comment:
            print("❌ コメントは必須です。")
            return
        
        # コメントを追加
        print("\n🔄 コメントを追加中...")
        success = diary_manager.notion_client.add_comment_to_diary(selected_entry['id'], comment)
        
        if success:
            print("✅ コメントが追加されました！")
        else:
            print("❌ コメントの追加に失敗しました。")
            
    except ValueError:
        print("❌ 有効な数字を入力してください。")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    main() 