"""
Root Agent for task distribution and coordination
"""
import asyncio
from typing import Dict, Any, List
from agents.base_agent import BaseAgent, AgentTask

class RootAgent(BaseAgent):
    """Root agent that distributes tasks to specialized agents"""
    
    def __init__(self):
        super().__init__("RootAgent")
        self.evidence_agent = None
        self.proofreading_agent = None
    
    def set_agents(self, evidence_agent, proofreading_agent):
        """Set the specialized agents"""
        self.evidence_agent = evidence_agent
        self.proofreading_agent = proofreading_agent
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the article and coordinate between agents"""
        article_content = input_data.get('content', '')
        article_path = input_data.get('path', '')
        
        self.log(f"Starting proofreading process for: {article_path}")
        
        # Create tasks for both agents
        evidence_task = AgentTask("evidence_check", {
            'content': article_content,
            'path': article_path
        })
        
        proofreading_task = AgentTask("proofreading", {
            'content': article_content,
            'path': article_path
        })
        
        # Run both agents concurrently
        evidence_result = await self.evidence_agent.process(evidence_task.data)
        proofreading_result = await self.proofreading_agent.process(proofreading_task.data)
        
        # Combine results
        final_result = await self._combine_results(
            evidence_result, 
            proofreading_result, 
            article_content
        )
        
        self.log("Proofreading process completed")
        return final_result
    
    async def _combine_results(self, evidence_result: Dict, 
                             proofreading_result: Dict, 
                             original_content: str) -> Dict[str, Any]:
        """Combine results from both agents into final output"""
        
        prompt = f"""
        記事の校閲結果をまとめてください。

        元の記事内容:
        {original_content[:500]}...

        エビデンス調査結果:
        {evidence_result.get('summary', 'エビデンス調査が完了しました')}

        文章校閲結果:
        {proofreading_result.get('summary', '文章校閲が完了しました')}

        以下の形式で最終的な校閲レポートを作成してください:
        1. 全体的な評価
        2. 主要な指摘事項
        3. 推奨される修正点
        4. 追加調査が必要な項目
        """
        
        final_summary = await self.call_llm(prompt)
        
        return {
            'overall_summary': final_summary,
            'evidence_findings': evidence_result,
            'proofreading_suggestions': proofreading_result,
            'status': 'completed'
        }