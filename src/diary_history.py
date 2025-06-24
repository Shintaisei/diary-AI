"""
日記履歴管理システム
日記の履歴を保存し、継続的な文脈での分析を可能にする
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

class DiaryHistory:
    def __init__(self, data_dir: str = "data"):
        """
        日記履歴管理システムを初期化
        
        Args:
            data_dir: データ保存ディレクトリ
        """
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, "diary_history.json")
        self.logger = logging.getLogger(__name__)
        
        # データディレクトリを作成
        os.makedirs(data_dir, exist_ok=True)
        
        # 履歴ファイルを初期化
        self._init_history_file()
    
    def _init_history_file(self):
        """履歴ファイルを初期化"""
        if not os.path.exists(self.history_file):
            initial_data = {
                "diaries": [],
                "user_profile": {
                    "created_at": datetime.now().isoformat(),
                    "total_entries": 0,
                    "name": "",
                    "age": "",
                    "occupation": "",
                    "interests": [],
                    "goals": [],
                    "personality_traits": {},
                    "recurring_themes": [],
                    "growth_areas": []
                }
            }
            self._save_history(initial_data)
    
    def _load_history(self) -> Dict[str, Any]:
        """履歴を読み込む"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"履歴読み込みエラー: {e}")
            return {"diaries": [], "user_profile": {}}
    
    def _save_history(self, data: Dict[str, Any]):
        """履歴を保存"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"履歴保存エラー: {e}")
    
    def add_diary_entry(self, title: str, content: str, ai_analysis: Dict[str, Any]) -> bool:
        """
        新しい日記エントリを追加
        
        Args:
            title: 日記のタイトル
            content: 日記の内容
            ai_analysis: AI分析結果
            
        Returns:
            成功の場合True
        """
        try:
            history = self._load_history()
            
            entry = {
                "id": len(history["diaries"]) + 1,
                "title": title,
                "content": content,
                "created_at": datetime.now().isoformat(),
                "ai_analysis": ai_analysis,
                "word_count": len(content)
            }
            
            history["diaries"].append(entry)
            history["user_profile"]["total_entries"] = len(history["diaries"])
            
            # ユーザープロファイルを更新
            self._update_user_profile(history, entry)
            
            self._save_history(history)
            return True
            
        except Exception as e:
            self.logger.error(f"日記エントリ追加エラー: {e}")
            return False
    
    def _update_user_profile(self, history: Dict[str, Any], new_entry: Dict[str, Any]):
        """ユーザープロファイルを更新"""
        profile = history["user_profile"]
        
        # 感情の傾向を分析
        if "emotions" in new_entry["ai_analysis"]:
            emotions = new_entry["ai_analysis"]["emotions"]
            if isinstance(emotions, dict) and "overall_mood" in emotions:
                mood = emotions["overall_mood"]
                if "mood_history" not in profile:
                    profile["mood_history"] = []
                profile["mood_history"].append({
                    "date": new_entry["created_at"][:10],
                    "mood": mood
                })
                
                # 最近30日間の気分の分析
                recent_moods = profile["mood_history"][-30:]
                positive_count = sum(1 for m in recent_moods if m["mood"] == "positive")
                profile["recent_mood_trend"] = {
                    "positive_ratio": positive_count / len(recent_moods),
                    "dominant_mood": max(set([m["mood"] for m in recent_moods]), 
                                       key=[m["mood"] for m in recent_moods].count)
                }
    
    def get_recent_entries(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        最近の日記エントリを取得
        
        Args:
            days: 過去何日分を取得するか
            
        Returns:
            最近の日記エントリリスト
        """
        try:
            history = self._load_history()
            cutoff_date = datetime.now() - timedelta(days=days)
            
            recent_entries = []
            for entry in history["diaries"]:
                entry_date = datetime.fromisoformat(entry["created_at"])
                if entry_date >= cutoff_date:
                    recent_entries.append(entry)
            
            return sorted(recent_entries, key=lambda x: x["created_at"], reverse=True)
            
        except Exception as e:
            self.logger.error(f"最近のエントリ取得エラー: {e}")
            return []
    
    def get_user_profile(self) -> Dict[str, Any]:
        """ユーザープロファイルを取得"""
        try:
            history = self._load_history()
            return history.get("user_profile", {})
        except Exception as e:
            self.logger.error(f"ユーザープロファイル取得エラー: {e}")
            return {}
    
    def get_context_for_analysis(self, days: int = 7) -> str:
        """
        AI分析用の文脈情報を生成
        
        Args:
            days: 過去何日分の文脈を含めるか
            
        Returns:
            文脈情報の文字列
        """
        try:
            recent_entries = self.get_recent_entries(days)
            profile = self.get_user_profile()
            
            context_parts = []
            
            # ユーザーの基本情報
            if profile:
                total_entries = profile.get("total_entries", 0)
                context_parts.append(f"このユーザーは{total_entries}回日記を書いています。")
                
                if "recent_mood_trend" in profile:
                    trend = profile["recent_mood_trend"]
                    positive_ratio = trend.get("positive_ratio", 0) * 100
                    dominant_mood = trend.get("dominant_mood", "不明")
                    context_parts.append(f"最近の気分傾向: ポジティブ{positive_ratio:.1f}%, 主要な気分: {dominant_mood}")
            
            # 最近の日記の要約
            if recent_entries:
                context_parts.append(f"\n過去{days}日間の日記:")
                for entry in recent_entries[-3:]:  # 最新3件
                    date = entry["created_at"][:10]
                    title = entry["title"]
                    summary = entry["ai_analysis"].get("summary", "要約なし")
                    context_parts.append(f"- {date}: 「{title}」- {summary}")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            self.logger.error(f"文脈情報生成エラー: {e}")
            return ""
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """
        日記のパターンを分析
        
        Returns:
            パターン分析結果
        """
        try:
            history = self._load_history()
            entries = history["diaries"]
            
            if not entries:
                return {"message": "分析に十分なデータがありません"}
            
            patterns = {
                "writing_frequency": self._analyze_frequency(entries),
                "common_themes": self._analyze_themes(entries),
                "mood_patterns": self._analyze_mood_patterns(entries),
                "growth_indicators": self._analyze_growth(entries)
            }
            
            return patterns
            
        except Exception as e:
            self.logger.error(f"パターン分析エラー: {e}")
            return {"error": str(e)}
    
    def _analyze_frequency(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """書く頻度を分析"""
        if len(entries) < 2:
            return {"message": "頻度分析には2つ以上のエントリが必要です"}
        
        dates = [datetime.fromisoformat(entry["created_at"]).date() for entry in entries]
        dates.sort()
        
        # 日記を書いた日数と期間を計算
        unique_dates = list(set(dates))
        total_days = (dates[-1] - dates[0]).days + 1
        writing_days = len(unique_dates)
        
        return {
            "total_entries": len(entries),
            "writing_days": writing_days,
            "total_period_days": total_days,
            "frequency_percentage": (writing_days / max(total_days, 1)) * 100
        }
    
    def _analyze_themes(self, entries: List[Dict[str, Any]]) -> List[str]:
        """共通テーマを分析（簡易版）"""
        # 実際の実装では、より高度なNLP技術を使用
        common_words = {}
        for entry in entries:
            content = entry["content"]
            # 簡単な単語カウント（実際はもっと高度な処理が必要）
            words = content.split()
            for word in words:
                if len(word) > 2:  # 2文字以上の単語のみ
                    common_words[word] = common_words.get(word, 0) + 1
        
        # 頻出単語トップ5
        sorted_words = sorted(common_words.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:5]]
    
    def _analyze_mood_patterns(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """気分のパターンを分析"""
        moods = []
        for entry in entries:
            ai_analysis = entry.get("ai_analysis", {})
            emotions = ai_analysis.get("emotions", {})
            if isinstance(emotions, dict) and "overall_mood" in emotions:
                moods.append(emotions["overall_mood"])
        
        if not moods:
            return {"message": "気分データが不足しています"}
        
        mood_counts = {}
        for mood in moods:
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        return {
            "mood_distribution": mood_counts,
            "most_common_mood": max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else "不明"
        }
    
    def _analyze_growth(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """成長の指標を分析"""
        if len(entries) < 5:
            return {"message": "成長分析には5つ以上のエントリが必要です"}
        
        # 文字数の変化
        word_counts = [entry["word_count"] for entry in entries]
        recent_avg = sum(word_counts[-5:]) / 5
        early_avg = sum(word_counts[:5]) / 5
        
        return {
            "writing_length_trend": {
                "early_average": early_avg,
                "recent_average": recent_avg,
                "improvement": recent_avg > early_avg
            },
            "consistency": {
                "total_entries": len(entries),
                "writing_consistency": "良好" if len(entries) > 10 else "改善の余地あり"
            }
        }
    
    def update_user_profile(self, profile_data: Dict[str, Any]) -> bool:
        """
        ユーザープロフィールを更新
        
        Args:
            profile_data: 更新するプロフィールデータ
            
        Returns:
            成功の場合True
        """
        try:
            history = self._load_history()
            profile = history["user_profile"]
            
            # プロフィールデータを更新
            for key, value in profile_data.items():
                if key in ["name", "age", "occupation", "interests", "goals"]:
                    profile[key] = value
            
            self._save_history(history)
            return True
            
        except Exception as e:
            self.logger.error(f"プロフィール更新エラー: {e}")
            return False
    
    def get_profile_for_context(self) -> str:
        """
        AI分析用のプロフィール情報を生成
        
        Returns:
            プロフィール情報の文字列
        """
        try:
            profile = self.get_user_profile()
            
            if not profile:
                return ""
            
            context_parts = []
            
            # 基本情報
            name = profile.get("name", "")
            age = profile.get("age", "")
            occupation = profile.get("occupation", "")
            
            if name:
                context_parts.append(f"名前: {name}")
            if age:
                context_parts.append(f"年齢: {age}")
            if occupation:
                context_parts.append(f"職業: {occupation}")
            
            # 興味・関心
            interests = profile.get("interests", [])
            if interests:
                context_parts.append(f"興味・関心: {', '.join(interests)}")
            
            # 目標
            goals = profile.get("goals", [])
            if goals:
                context_parts.append(f"目標: {', '.join(goals)}")
            
            return "\n".join(context_parts) if context_parts else ""
            
        except Exception as e:
            self.logger.error(f"プロフィール文脈生成エラー: {e}")
            return "" 