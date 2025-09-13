"""
LLM Configuration for Google AI
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMConfig:
    """Configuration for Google AI LLM"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Only configure real API if not in test mode
        if not self.api_key.startswith('test_'):
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None  # Mock mode
    
    def get_model(self):
        """Get the configured model instance"""
        return self.model
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate response from the model"""
        try:
            # Check if this is a test environment
            if self.api_key.startswith('test_'):
                return self._generate_mock_response(prompt)
            
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _generate_mock_response(self, prompt: str) -> str:
        """Generate mock response for testing"""
        if "主張" in prompt or "抽出" in prompt:
            return """
            - APIの仕様について言及されています
            - ライブラリの使用方法が記載されています
            - 技術的な手順が説明されています
            """
        elif "校閲" in prompt or "改善" in prompt:
            return "記事の内容は適切で、読みやすく構成されています。特に大きな問題は見つかりませんでした。"
        elif "エビデンス" in prompt:
            return "エビデンス調査の結果、記載内容に信頼性のある情報源との整合性が確認されました。"
        else:
            return "Mock response: システムは正常に動作しています。"