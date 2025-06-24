#!/usr/bin/env python3
"""
データ保存テストスクリプト
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from diary_history import DiaryHistory

def test_data_saving():
    """データ保存をテスト"""
    print("📊 データ保存テスト開始...")
    
    # 履歴システムを初期化
    history = DiaryHistory("data")
    
    # テスト用プロフィールデータ
    test_profile = {
        "name": "テストユーザー",
        "age": "25歳", 
        "occupation": "エンジニア",
        "interests": ["プログラミング", "読書", "映画鑑賞"],
        "goals": ["スキルアップ", "健康維持", "新しい言語の習得"]
    }
    
    print("👤 プロフィール更新テスト...")
    profile_result = history.update_user_profile(test_profile)
    print(f"プロフィール更新: {'成功' if profile_result else '失敗'}")
    
    # テスト用日記データ
    test_diary_content = "今日はプログラミングの勉強をしました。新しいフレームワークを学んで充実した一日でした。"
    test_ai_analysis = {
        "emotions": {"overall_mood": "positive"},
        "summary": "プログラミング学習で充実した一日を過ごした",
        "advice": "継続的な学習は素晴らしいです。引き続き頑張ってください。"
    }
    
    print("📝 日記データ追加テスト...")
    diary_result = history.add_diary_entry("プログラミング学習の日", test_diary_content, test_ai_analysis)
    print(f"日記データ追加: {'成功' if diary_result else '失敗'}")
    
    # データ確認
    print("\n📋 保存されたデータ確認:")
    profile = history.get_user_profile()
    print(f"総日記数: {profile.get('total_entries', 0)}件")
    print(f"ユーザー名: {profile.get('name', '未設定')}")
    print(f"職業: {profile.get('occupation', '未設定')}")
    print(f"興味: {', '.join(profile.get('interests', []))}")
    
    recent_entries = history.get_recent_entries(7)
    print(f"最近の日記: {len(recent_entries)}件")
    
    if recent_entries:
        latest = recent_entries[0]
        print(f"最新日記: 「{latest['title']}」")
        print(f"作成日: {latest['created_at'][:19]}")
    
    # 文脈生成テスト
    print("\n🤖 AI用文脈生成テスト:")
    context = history.get_context_for_analysis()
    profile_context = history.get_profile_for_context()
    
    print("プロフィール文脈:")
    print(profile_context if profile_context else "なし")
    print("\n履歴文脈:")
    print(context if context else "なし")
    
    print("\n✅ テスト完了!")

if __name__ == "__main__":
    test_data_saving() 