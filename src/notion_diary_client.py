"""
Notion API連携クラス
日記データの取得・作成・更新を行う
"""

from notion_client import Client
from typing import List, Dict, Any, Optional
import logging

class NotionDiaryClient:
    def __init__(self, api_key: str, database_id: str):
        """
        Notion日記クライアントを初期化
        
        Args:
            api_key: Notion API キー
            database_id: 日記データベースのID
        """
        self.client = Client(auth=api_key)
        self.database_id = database_id
        self.logger = logging.getLogger(__name__)
    
    def get_diary_entries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        日記エントリーを取得
        
        Args:
            limit: 取得する件数
            
        Returns:
            日記エントリーのリスト
        """
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                sorts=[
                    {
                        "property": "作成日時",
                        "direction": "descending"
                    }
                ],
                page_size=limit
            )
            return response.get("results", [])
        except Exception as e:
            self.logger.error(f"日記エントリー取得エラー: {e}")
            return []
    
    def create_diary_entry(self, title: str, content: str, date: str = None) -> Optional[Dict[str, Any]]:
        """
        新しい日記エントリーを作成
        
        Args:
            title: 日記のタイトル
            content: 日記の内容
            date: 日付（ISO形式）
            
        Returns:
            作成されたページの情報
        """
        try:
            from datetime import datetime
            if date is None:
                # Notion APIが受け入れる形式にフォーマット（YYYY-MM-DD形式）
                date = datetime.now().strftime("%Y-%m-%d")
            
            properties = {
                "タイトル": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "作成日時": {
                    "date": {
                        "start": date
                    }
                }
            }
            
            children = [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": content
                                }
                            }
                        ]
                    }
                }
            ]
            
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )
            return response
        except Exception as e:
            self.logger.error(f"日記エントリー作成エラー: {e}")
            return None
    
    def add_comment_to_diary(self, page_id: str, comment: str) -> bool:
        """
        既存の日記にコメントを追加
        
        Args:
            page_id: 日記ページのID
            comment: 追加するコメント
            
        Returns:
            成功した場合True
        """
        try:
            # ページにコメントブロックを追加
            self.client.blocks.children.append(
                block_id=page_id,
                children=[
                    {
                        "object": "block",
                        "type": "callout",
                        "callout": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": f"💭 コメント: {comment}"
                                    }
                                }
                            ],
                            "icon": {
                                "emoji": "💭"
                            }
                        }
                    }
                ]
            )
            return True
        except Exception as e:
            self.logger.error(f"コメント追加エラー: {e}")
            return False
    
    def add_ai_analysis_to_diary(self, page_id: str, ai_analysis: dict) -> bool:
        """
        日記ページにAI分析結果を追加
        
        Args:
            page_id: 日記ページのID
            ai_analysis: AI分析結果
            
        Returns:
            成功した場合True
        """
        try:
            # AI分析結果のブロックを構築
            blocks_to_add = []
            
            # 区切り線
            blocks_to_add.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })
            
            # AI分析ヘッダー
            blocks_to_add.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "🤖 AI分析結果"
                            }
                        }
                    ]
                }
            })
            
            # 要約
            summary = ai_analysis.get('summary', 'N/A')
            if summary != 'N/A':
                blocks_to_add.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"📊 要約: {summary}"
                                }
                            }
                        ],
                        "icon": {
                            "emoji": "📊"
                        }
                    }
                })
            
            # アドバイス
            advice = ai_analysis.get('advice', 'N/A')
            if advice != 'N/A':
                blocks_to_add.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"💡 アドバイス: {advice}"
                                }
                            }
                        ],
                        "icon": {
                            "emoji": "💡"
                        }
                    }
                })
            
            # 感情分析
            emotions = ai_analysis.get('emotions', {})
            if isinstance(emotions, dict) and 'overall_mood' in emotions:
                mood = emotions.get('overall_mood', 'N/A')
                blocks_to_add.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"😊 全体的な気分: {mood}"
                                }
                            }
                        ],
                        "icon": {
                            "emoji": "😊"
                        }
                    }
                })
            
            # すべてのブロックを一度に追加
            self.client.blocks.children.append(
                block_id=page_id,
                children=blocks_to_add
            )
            return True
            
        except Exception as e:
            self.logger.error(f"AI分析結果追加エラー: {e}")
            return False