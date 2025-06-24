#!/usr/bin/env python3
"""
プロフィール機能テストスクリプト
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from profile_manager import ProfileManager

def test_profile():
    """プロフィール機能をテスト"""
    print("👤 プロフィール機能テスト開始...")
    
    profile_manager = ProfileManager("data")
    
    # 現在のプロフィールを表示
    print("\n📋 現在のプロフィール:")
    current_profile = profile_manager.load_profile()
    if current_profile:
        print("設定済みです")
    else:
        print("まだ設定されていません")
    
    # AI用文脈を生成
    print("\n🤖 AI用プロフィール文脈:")
    ai_context = profile_manager.get_profile_for_ai()
    if ai_context:
        print(ai_context)
    else:
        print("プロフィール文脈が生成されていません（まだ設定されていない可能性があります）")
    
    # プロフィール要約
    print("\n📊 プロフィール要約:")
    summary = profile_manager.get_profile_summary()
    print(summary)
    
    print("\n💡 プロフィールを編集するには:")
    print("   data/profile.json ファイルを直接編集してください")
    print("   または、Webアプリのプロフィールタブから編集できます")
    
    print("\n✅ テスト完了!")

if __name__ == "__main__":
    test_profile() 