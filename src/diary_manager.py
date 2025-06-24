"""
日記管理メインクラス
NotionクライアントとAI分析機能を統合して日記アプリの中核機能を提供
"""

from notion_diary_client import NotionDiaryClient
from ai_analyzer import DiaryAIAnalyzer
from diary_history import DiaryHistory
from profile_manager import ProfileManager
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

class DiaryManager:
    def __init__(self, notion_api_key: str, notion_database_id: str, openai_api_key: str, data_dir: str = "data"):
        """
        日記管理システムを初期化
        
        Args:
            notion_api_key: Notion API キー
            notion_database_id: 日記データベースID
            openai_api_key: OpenAI API キー
            data_dir: データ保存ディレクトリ
        """
        self.notion_client = NotionDiaryClient(notion_api_key, notion_database_id)
        self.ai_analyzer = DiaryAIAnalyzer(openai_api_key)
        self.history = DiaryHistory(data_dir)
        self.profile_manager = ProfileManager(data_dir)
        self.logger = logging.getLogger(__name__)
        
        # ログ設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def create_diary_with_analysis(self, content: str, title: str = None, date: str = None) -> Dict[str, Any]:
        """
        日記を作成し、AI分析も同時に実行（履歴を考慮したタイトル自動生成対応）
        
        Args:
            content: 日記の内容
            title: 日記のタイトル（省略時はAIが生成）
            date: 日付（ISO形式、省略時は現在日時）
            
        Returns:
            作成結果とAI分析結果（生成されたタイトル含む）
        """
        try:
            # 履歴からの文脈情報を取得
            context = self.history.get_context_for_analysis()
            
            # プロフィールファイルから文脈情報を取得
            profile_context = self.profile_manager.get_profile_for_ai()
            
            # プロフィール情報と履歴を統合
            full_context = ""
            if profile_context:
                full_context += f"【ユーザープロフィール】\n{profile_context}\n\n"
            if context:
                full_context += f"【日記履歴】\n{context}"
            
            # タイトルが指定されていない場合はAIで生成
            if not title:
                generated_title = self.ai_analyzer.generate_title(content)
            else:
                generated_title = title
            
            # 日記をNotionに作成
            diary_entry = self.notion_client.create_diary_entry(generated_title, content, date)
            
            if diary_entry:
                # AI分析を実行（履歴を考慮）
                emotion_analysis = self.ai_analyzer.analyze_emotion(content)
                summary = self.ai_analyzer.generate_summary(content)
                advice = self.ai_analyzer.generate_advice(content, full_context)  # 完全な文脈を追加
                
                ai_analysis = {
                    "emotions": emotion_analysis,
                    "summary": summary,
                    "advice": advice
                }
                
                # ローカル履歴にも保存
                self.history.add_diary_entry(generated_title, content, ai_analysis)
                
                # AI分析結果をNotionページに追加
                page_id = diary_entry.get("id")
                if page_id:
                    self.notion_client.add_ai_analysis_to_diary(page_id, ai_analysis)
                
                result = {
                    "diary_entry": diary_entry,
                    "generated_title": generated_title,
                    "ai_analysis": ai_analysis,
                    "status": "success",
                    "context_used": bool(full_context.strip())  # 文脈が使用されたかを示す
                }
                
                self.logger.info(f"日記作成完了: {generated_title} (履歴考慮: {bool(full_context.strip())})")
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
    
    def get_user_analytics(self) -> Dict[str, Any]:
        """
        ユーザーの分析情報を取得
        
        Returns:
            分析結果
        """
        try:
            profile = self.history.get_user_profile()
            patterns = self.history.analyze_patterns()
            
            return {
                "user_profile": profile,
                "patterns": patterns,
                "status": "success"
            }
            
        except Exception as e:
            self.logger.error(f"分析情報取得エラー: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_diary_history_summary(self, days: int = 30) -> Dict[str, Any]:
        """
        日記履歴の要約を取得
        
        Args:
            days: 過去何日分を取得するか
            
        Returns:
            履歴要約
        """
        try:
            recent_entries = self.history.get_recent_entries(days)
            
            if not recent_entries:
                return {"status": "success", "message": "指定期間内の日記がありません"}
            
            summary = {
                "total_entries": len(recent_entries),
                "date_range": {
                    "start": recent_entries[-1]["created_at"][:10] if recent_entries else "",
                    "end": recent_entries[0]["created_at"][:10] if recent_entries else ""
                },
                "entries": []
            }
            
            for entry in recent_entries:
                summary["entries"].append({
                    "title": entry["title"],
                    "date": entry["created_at"][:10],
                    "summary": entry["ai_analysis"].get("summary", "要約なし"),
                    "mood": entry["ai_analysis"].get("emotions", {}).get("overall_mood", "不明")
                })
            
            return {"status": "success", "summary": summary}
            
        except Exception as e:
            self.logger.error(f"履歴要約取得エラー: {e}")
            return {"status": "error", "message": str(e)}
    
    def update_user_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ユーザープロフィールを更新
        
        Args:
            profile_data: 更新するプロフィールデータ
            
        Returns:
            更新結果
        """
        try:
            success = self.history.update_user_profile(profile_data)
            
            if success:
                return {"status": "success", "message": "プロフィールが更新されました"}
            else:
                return {"status": "error", "message": "プロフィール更新に失敗しました"}
                
        except Exception as e:
            self.logger.error(f"プロフィール更新エラー: {e}")
            return {"status": "error", "message": str(e)} 