"""
Suggestion generation functionality
"""
from typing import List, Dict

class SuggestionGenerator:
    """Generates improvement suggestions based on analysis results"""
    
    async def check_readability(self, content: str, agent) -> Dict[str, any]:
        """Check readability and comprehensibility"""
        
        prompt = f"""
        以下の技術文書の読みやすさを評価してください:
        
        評価項目:
        1. 文章の長さと複雑さ
        2. 専門用語の説明の適切さ
        3. 論理的な構成
        4. 例やサンプルコードの効果性
        
        文書内容:
        {content[:800]}...
        
        読みやすさを5段階で評価し、改善提案をしてください:
        """
        
        response = await agent.call_llm(prompt)
        return {
            'readability_feedback': response,
            'needs_simplification': '複雑' in response or '難しい' in response
        }
    
    async def generate_suggestions(self, content: str, grammar: Dict, 
                                  style: Dict, readability: Dict, agent) -> List[str]:
        """Generate comprehensive improvement suggestions"""
        
        suggestions = []
        
        if grammar.get('issues_found'):
            suggestions.append("文法と表現の見直しが推奨されます")
        
        if style.get('needs_improvement'):
            suggestions.append("文体とスタイルの統一が必要です")
        
        if readability.get('needs_simplification'):
            suggestions.append("読みやすさの向上が推奨されます")
        
        # Generate specific suggestions using LLM
        prompt = f"""
        技術文書の改善提案を具体的に生成してください。
        現在の課題:
        - 文法問題: {grammar.get('issues_found', False)}
        - スタイル問題: {style.get('needs_improvement', False)}
        - 読みやすさ問題: {readability.get('needs_simplification', False)}
        
        具体的な改善提案を3-5個リストアップしてください:
        """
        
        llm_suggestions = await agent.call_llm(prompt)
        
        # Parse LLM suggestions
        parsed_suggestions = [
            line.strip().lstrip('- ').lstrip('・').lstrip('1.').lstrip('2.').lstrip('3.')
            for line in llm_suggestions.split('\n')
            if line.strip() and ('提案' in line or '改善' in line or '修正' in line)
        ]
        
        suggestions.extend(parsed_suggestions[:3])
        return suggestions
    
    async def generate_summary(self, suggestions: List[str], agent) -> str:
        """Generate summary of proofreading results"""
        
        if not suggestions:
            return "記事の品質は良好です。大きな問題は見つかりませんでした。"
        
        prompt = f"""
        校閲結果の要約を作成してください。
        
        発見された改善点:
        {chr(10).join(f"- {s}" for s in suggestions)}
        
        全体的な校閲結果の要約を生成してください:
        """
        
        return await agent.call_llm(prompt)