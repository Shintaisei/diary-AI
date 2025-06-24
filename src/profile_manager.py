"""
プロフィール管理システム
data/profile.jsonを読み書きして、AIの文脈に使用
"""

import json
import os
from typing import Dict, Any, List
import logging

class ProfileManager:
    def __init__(self, data_dir: str = "data"):
        """
        プロフィール管理システムを初期化
        
        Args:
            data_dir: データ保存ディレクトリ
        """
        self.data_dir = data_dir
        self.profile_file = os.path.join(data_dir, "profile.json")
        self.logger = logging.getLogger(__name__)
        
        # データディレクトリを作成
        os.makedirs(data_dir, exist_ok=True)
    
    def load_profile(self) -> Dict[str, Any]:
        """
        プロフィールを読み込む
        
        Returns:
            プロフィールデータ
        """
        try:
            if os.path.exists(self.profile_file):
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            self.logger.error(f"プロフィール読み込みエラー: {e}")
            return {}
    
    def save_profile(self, profile_data: Dict[str, Any]) -> bool:
        """
        プロフィールを保存
        
        Args:
            profile_data: 保存するプロフィールデータ
            
        Returns:
            成功の場合True
        """
        try:
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"プロフィール保存エラー: {e}")
            return False
    
    def get_profile_for_ai(self) -> str:
        """
        AI用のプロフィール文脈を生成
        
        Returns:
            AI分析用のプロフィール文字列
        """
        try:
            profile = self.load_profile()
            
            if not profile:
                return ""
            
            context_parts = []
            
            # 基本情報
            basic_info = profile.get("basic_info", {})
            if basic_info:
                context_parts.append("【基本情報】")
                for key, value in basic_info.items():
                    if value and value != f"{key}":  # デフォルト値でない場合
                        context_parts.append(f"- {key}: {value}")
            
            # 性格・価値観
            personality = profile.get("personality", {})
            if personality:
                traits = personality.get("traits", [])
                values = personality.get("values", [])
                
                if traits or values:
                    context_parts.append("\n【性格・価値観】")
                    if traits:
                        valid_traits = [t for t in traits if t and not t.startswith("性格の特徴")]
                        if valid_traits:
                            context_parts.append(f"- 性格: {', '.join(valid_traits)}")
                    if values:
                        valid_values = [v for v in values if v and not v.startswith("大切にしている")]
                        if valid_values:
                            context_parts.append(f"- 価値観: {', '.join(valid_values)}")
            
            # 興味・趣味
            interests = profile.get("interests_and_hobbies", [])
            if interests:
                valid_interests = [i for i in interests if i and not i.startswith("趣味")]
                if valid_interests:
                    context_parts.append(f"\n【興味・趣味】")
                    context_parts.append(f"- {', '.join(valid_interests)}")
            
            # 目標
            goals = profile.get("goals", {})
            if goals:
                short_term = goals.get("short_term", [])
                long_term = goals.get("long_term", [])
                
                if short_term or long_term:
                    context_parts.append("\n【目標】")
                    if short_term:
                        valid_short = [g for g in short_term if g and not g.startswith("短期目標")]
                        if valid_short:
                            context_parts.append(f"- 短期目標: {', '.join(valid_short)}")
                    if long_term:
                        valid_long = [g for g in long_term if g and not g.startswith("長期目標")]
                        if valid_long:
                            context_parts.append(f"- 長期目標: {', '.join(valid_long)}")
            
            # 生活状況
            life_situation = profile.get("life_situation", {})
            if life_situation:
                context_parts.append("\n【生活状況】")
                for key, value in life_situation.items():
                    if key == "challenges" and isinstance(value, list):
                        valid_challenges = [c for c in value if c and not c.startswith("現在の課題")]
                        if valid_challenges:
                            context_parts.append(f"- 現在の課題: {', '.join(valid_challenges)}")
                    elif value and not any(default in str(value) for default in ["家族構成", "仕事スタイル", "日常のルーティン"]):
                        context_parts.append(f"- {key}: {value}")
            
            # アドバイス設定
            preferences = profile.get("preferences", {})
            if preferences:
                advice_style = preferences.get("advice_style", "")
                focus_areas = preferences.get("focus_areas", [])
                
                if advice_style and not advice_style.startswith("どんな"):
                    context_parts.append(f"\n【アドバイス設定】")
                    context_parts.append(f"- 好むアドバイススタイル: {advice_style}")
                
                if focus_areas:
                    valid_focus = [f for f in focus_areas if f and not f.startswith("特に重視")]
                    if valid_focus:
                        if not advice_style or advice_style.startswith("どんな"):
                            context_parts.append(f"\n【アドバイス設定】")
                        context_parts.append(f"- 重視する分野: {', '.join(valid_focus)}")
            
            # その他のメモ
            notes = profile.get("notes", "")
            if notes and not notes.startswith("その他"):
                context_parts.append(f"\n【その他】")
                context_parts.append(f"- {notes}")
            
            return "\n".join(context_parts) if context_parts else ""
            
        except Exception as e:
            self.logger.error(f"AI用プロフィール生成エラー: {e}")
            return ""
    
    def get_profile_summary(self) -> str:
        """
        プロフィールの要約を取得
        
        Returns:
            プロフィール要約文字列
        """
        try:
            profile = self.load_profile()
            
            if not profile:
                return "プロフィールが設定されていません。"
            
            summary_parts = []
            
            # 基本情報
            basic_info = profile.get("basic_info", {})
            name = basic_info.get("name", "")
            if name and not name.startswith("あなたの"):
                summary_parts.append(f"名前: {name}")
            
            age = basic_info.get("age", "")
            if age and age != "年齢":
                summary_parts.append(f"年齢: {age}")
            
            occupation = basic_info.get("occupation", "")
            if occupation and occupation != "職業":
                summary_parts.append(f"職業: {occupation}")
            
            # 目標の数
            goals = profile.get("goals", {})
            short_term = goals.get("short_term", [])
            long_term = goals.get("long_term", [])
            valid_short = [g for g in short_term if g and not g.startswith("短期目標")]
            valid_long = [g for g in long_term if g and not g.startswith("長期目標")]
            
            if valid_short or valid_long:
                goal_count = len(valid_short) + len(valid_long)
                summary_parts.append(f"設定済み目標: {goal_count}個")
            
            # 興味の数
            interests = profile.get("interests_and_hobbies", [])
            valid_interests = [i for i in interests if i and not i.startswith("趣味")]
            if valid_interests:
                summary_parts.append(f"興味・趣味: {len(valid_interests)}個")
            
            return "\n".join(summary_parts) if summary_parts else "プロフィールの詳細が設定されていません。"
            
        except Exception as e:
            self.logger.error(f"プロフィール要約生成エラー: {e}")
            return "プロフィール要約の生成に失敗しました。" 