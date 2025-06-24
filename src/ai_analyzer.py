"""
AI分析機能
日記の内容を分析して感情分析、要約、アドバイスなどを提供
"""

import openai
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

class DiaryAIAnalyzer:
    def __init__(self, api_key: str):
        """
        日記AI分析クライアントを初期化
        
        Args:
            api_key: OpenAI API キー
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
    
    def analyze_emotion(self, diary_content: str) -> Dict[str, Any]:
        """
        日記の感情分析を行う
        
        Args:
            diary_content: 日記の内容
            
        Returns:
            感情分析結果
        """
        try:
            prompt = f"""
以下の日記の内容から感情を分析してください。
結果はJSON形式で、以下の項目を含めてください：
- overall_mood: 全体的な気分（positive/neutral/negative）
- emotions: 検出された感情のリスト（喜び、悲しみ、怒り、不安、期待など）
- confidence: 分析の信頼度（0-1の数値）
- summary: 感情についての簡潔な説明

日記内容:
{diary_content}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは日記の感情分析を行う専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            try:
                import json
                return json.loads(result)
            except:
                return {"error": "JSON解析エラー", "raw_response": result}
                
        except Exception as e:
            self.logger.error(f"感情分析エラー: {e}")
            return {"error": str(e)}
    
    def generate_summary(self, diary_content: str) -> str:
        """
        日記の要約を生成
        
        Args:
            diary_content: 日記の内容
            
        Returns:
            要約文
        """
        try:
            prompt = f"""
以下の日記を簡潔に要約してください。
重要なポイントや出来事を3-4文でまとめてください。

日記内容:
{diary_content}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは日記の要約を作成する専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"要約生成エラー: {e}")
            return f"要約生成中にエラーが発生しました: {e}"
    
    def generate_advice(self, diary_content: str, context: str = "") -> str:
        """
        日記に基づいてアドバイスを生成（履歴を考慮）
        
        Args:
            diary_content: 日記の内容
            context: 過去の日記履歴からの文脈情報
            
        Returns:
            アドバイス文
        """
        try:
            # 文脈情報を含むプロンプトを作成
            if context.strip():
                prompt = f"""
あなたは長期間にわたってこのユーザーの日記を見守っている優しいカウンセラーです。
以下の情報を参考に、継続的で個人的なアドバイスを提供してください。

【ユーザーの履歴・傾向】
{context}

【今日の日記】
{diary_content}

以下の点を考慮してアドバイスしてください：
- 過去の経験や成長の軌跡を踏まえる
- 繰り返しのパターンがあれば指摘し、改善のヒントを提供
- 前向きな変化があれば認めて励ます
- 継続的なサポートの姿勢を示す
- 個人の成長と幸福に焦点を当てる
"""
            else:
                prompt = f"""
以下の日記を読んで、建設的で励ましになるアドバイスを提供してください。
個人の成長や幸福に焦点を当てて、優しく支援的な言葉で回答してください。

日記内容:
{diary_content}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは親身になって相談に乗る優しいカウンセラーです。長期的な関係性を大切にし、継続的なサポートを提供します。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"アドバイス生成エラー: {e}")
            return f"アドバイス生成中にエラーが発生しました: {e}"
    
    def generate_title(self, diary_content: str) -> str:
        """
        日記の内容からタイトルを生成
        
        Args:
            diary_content: 日記の内容
            
        Returns:
            生成されたタイトル
        """
        try:
            prompt = f"""
以下の日記の内容から、適切なタイトルを生成してください。
タイトルは：
- 10-20文字程度
- 日記の主要なテーマや感情を表現
- 読みやすく親しみやすい表現
- 日本語で自然な表現

日記内容:
{diary_content}

タイトルのみを返答してください。
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは日記のタイトルを作成する専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )
            
            title = response.choices[0].message.content.strip()
            # クォートを除去
            title = title.strip('"').strip("'").strip()
            
            return title
            
        except Exception as e:
            self.logger.error(f"タイトル生成エラー: {e}")
            return f"日記 - {datetime.now().strftime('%Y/%m/%d')}" 