"""
日記管理メインクラス
NotionクライアントとAI分析機能を統合して日記アプリの中核機能を提供
"""

from notion_diary_client import NotionDiaryClient
from ai_analyzer import DiaryAIAnalyzer
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

class DiaryManager:
    def __init__(self, notion_api_key: str, notion_database_id: str, openai_api_key: str):
        """
        日記管理システムを初期化
        
        Args:
            notion_api_key: Notion API キー
            notion_database_id: 日記データベースID
            openai_api_key: OpenAI API キー
        """
        self.notion_client = NotionDiaryClient(notion_api_key, notion_database_id)
        self.ai_analyzer = DiaryAIAnalyzer(openai_api_key)
        self.logger = logging.getLogger(__name__)
        
        # ログ設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def create_diary_with_analysis(self, content: str, title: str = None, date: str = None) -> Dict[str, Any]:
        """
        日記を作成し、AI分析も同時に実行（タイトル自動生成対応）
        
        Args:
            content: 日記の内容
            title: 日記のタイトル（省略時はAIが生成）
            date: 日付（ISO形式、省略時は現在日時）
            
        Returns:
            作成結果とAI分析結果（生成されたタイトル含む）
        """
        try:
            # タイトルが指定されていない場合はAIで生成
            if not title:
                generated_title = self.ai_analyzer.generate_title(content)
            else:
                generated_title = title
            
            # 日記をNotionに作成
            diary_entry = self.notion_client.create_diary_entry(generated_title, content, date)
            
            if diary_entry:
                # AI分析を実行
                emotion_analysis = self.ai_analyzer.analyze_emotion(content)
                summary = self.ai_analyzer.generate_summary(content)
                advice = self.ai_analyzer.generate_advice(content)
                
                ai_analysis = {
                    "emotions": emotion_analysis,
                    "summary": summary,
                    "advice": advice
                }
                
                # AI分析結果をNotionページに追加
                page_id = diary_entry.get("id")
                if page_id:
                    self.notion_client.add_ai_analysis_to_diary(page_id, ai_analysis)
                
                result = {
                    "diary_entry": diary_entry,
                    "generated_title": generated_title,
                    "ai_analysis": ai_analysis,
                    "status": "success"
                }
                
                self.logger.info(f"日記作成完了: {generated_title}")
                return result
            else:
                return {"status": "error", "message": "日記の作成に失敗しました"}
                
        except Exception as e:
            self.logger.error(f"日記作成・分析エラー: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_recent_diaries(self, limit: int = 5) -> Dict[str, Any]:
        """
        最近の日記を取得
        
        Args:
            limit: 取得する件数
            
        Returns:
            日記リスト
        """
        try:
            diary_entries = self.notion_client.get_diary_entries(limit)
            
            if not diary_entries:
                return {"status": "error", "message": "日記が見つかりませんでした"}
            
            processed_entries = []
            for entry in diary_entries:
                title = "タイトル取得エラー"
                
                try:
                    if "properties" in entry and "タイトル" in entry["properties"]:
                        title_prop = entry["properties"]["タイトル"]
                        if "title" in title_prop and title_prop["title"]:
                            title = title_prop["title"][0]["text"]["content"]
                except Exception as e:
                    self.logger.warning(f"日記タイトル取得エラー: {e}")
                
                processed_entries.append({
                    "id": entry["id"],
                    "title": title,
                    "created_time": entry.get("created_time", "")
                })
            
            return {
                "diary_entries": processed_entries,
                "status": "success"
            }
            
        except Exception as e:
            self.logger.error(f"日記取得エラー: {e}")
            return {"status": "error", "message": str(e)} 