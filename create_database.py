#!/usr/bin/env python3
"""
新しい日記データベースを自動作成するスクリプト
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from notion_client import Client
import config

def create_diary_database():
    """新しい日記データベースを作成"""
    client = Client(auth=config.NOTION_API_KEY)
    
    try:
        # 新しいデータベースを作成
        response = client.databases.create(
            parent={
                "type": "page_id", 
                "page_id": "YOUR_PARENT_PAGE_ID"  # ここを実際のページIDに変更する必要があります
            },
            title=[
                {
                    "type": "text",
                    "text": {
                        "content": "日記データベース（自動作成）"
                    }
                }
            ],
            properties={
                "タイトル": {
                    "title": {}
                },
                "作成日時": {
                    "date": {}
                },
                "内容": {
                    "rich_text": {}
                }
            }
        )
        
        database_id = response["id"]
        print(f"✅ 新しいデータベースが作成されました！")
        print(f"データベースID: {database_id}")
        print(f"このIDをconfig.pyのNOTION_DATABASE_IDに設定してください。")
        
        return database_id
        
    except Exception as e:
        print(f"❌ データベース作成エラー: {e}")
        return None

if __name__ == "__main__":
    create_diary_database() 