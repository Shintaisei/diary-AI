#!/usr/bin/env python3
"""
Notionデータベースのプロパティ情報を確認するデバッグスクリプト
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from notion_client import Client
import config

def debug_database_properties():
    """データベースのプロパティ情報を表示"""
    client = Client(auth=config.NOTION_API_KEY)
    
    try:
        # データベース情報を取得
        database = client.databases.retrieve(database_id=config.NOTION_DATABASE_ID)
        
        print("📊 データベース情報:")
        print(f"名前: {database.get('title', [{}])[0].get('text', {}).get('content', 'N/A')}")
        print(f"ID: {database.get('id', 'N/A')}")
        
        print("\n📋 プロパティ一覧:")
        properties = database.get('properties', {})
        
        for prop_name, prop_info in properties.items():
            prop_type = prop_info.get('type', 'unknown')
            print(f"- {prop_name}: {prop_type}")
        
        print("\n" + "="*50)
        
        # 最新のエントリーも確認
        print("📄 最新のエントリー:")
        response = client.databases.query(
            database_id=config.NOTION_DATABASE_ID,
            page_size=1
        )
        
        entries = response.get("results", [])
        if entries:
            entry = entries[0]
            print(f"エントリーID: {entry.get('id', 'N/A')}")
            
            print("\nエントリーのプロパティ:")
            entry_properties = entry.get('properties', {})
            for prop_name, prop_value in entry_properties.items():
                print(f"- {prop_name}: {prop_value}")
        else:
            print("エントリーが見つかりませんでした。")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    debug_database_properties() 