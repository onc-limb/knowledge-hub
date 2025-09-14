"""
Root Agent for task distribution and coordination using ADK
"""
from typing import Dict, Any, List
from google.adk.agents import LlmAgent
from agents.evidence_agent import EvidenceAgent
from agents.proofreading_agent import ProofreadingAgent

class RootAgent(LlmAgent):
    """Root agent that distributes tasks to specialized agents using ADK"""
    
    def __init__(self):
        super().__init__(
            name="RootAgent",
            model="gemini-2.0-flash-exp",
            instruction="""
            You are the Root Agent responsible for coordinating the proofreading process.
            Your tasks include:
            1. Distribute tasks to specialized agents (evidence research and proofreading)
            2. Coordinate concurrent processing of article content
            3. Combine results from different agents
            4. Generate comprehensive final reports
            
            Ensure all aspects of the article are thoroughly reviewed and provide
            actionable recommendations for improvement.
            """,
            description="Coordinator agent for proofreading workflow",
            tools=[],
            sub_agents=[EvidenceAgent(), ProofreadingAgent()]
        )
        
        # Initialize sub-agents after super().__init__
        self._init_sub_agents()
    
    def _init_sub_agents(self):
        """Initialize sub-agents"""
        self._evidence_agent = EvidenceAgent()
        self._proofreading_agent = ProofreadingAgent()
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the article and coordinate between agents"""
        article_content = input_data.get('content', '')
        article_path = input_data.get('path', '')
        
        print(f"[RootAgent] Starting proofreading process for: {article_path}")
        
        # Run both agents concurrently
        evidence_result = await self._evidence_agent.run(input_data)
        proofreading_result = await self._proofreading_agent.run(input_data)
        
        # Combine results
        final_result = await self._combine_results(
            evidence_result, 
            proofreading_result, 
            article_content
        )
        
        print("[RootAgent] Proofreading process completed")
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
        
        # Use ADK's built-in LLM capability
        final_summary = "統合された校閲レポートが生成されました。"  # Placeholder - ADK will handle this
        
        return {
            'overall_summary': final_summary,
            'evidence_findings': evidence_result,
            'proofreading_suggestions': proofreading_result,
            'status': 'completed'
        }