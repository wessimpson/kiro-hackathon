"""
Base CrewAI Agent Configuration
"""
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any, Optional
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class BaseCrewAIAgent:
    """Base class for all CrewAI agents"""
    
    def __init__(self, role: str, goal: str, backstory: str, tools: Optional[List] = None):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.1
        )
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent"""
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_task(self, description: str, expected_output: str, context: Optional[List] = None) -> Task:
        """Create a task for this agent"""
        return Task(
            description=description,
            expected_output=expected_output,
            agent=self.agent,
            context=context or []
        )
    
    def execute_task(self, task: Task) -> str:
        """Execute a single task"""
        try:
            crew = Crew(
                agents=[self.agent],
                tasks=[task],
                verbose=True
            )
            result = crew.kickoff()
            return result
        except Exception as e:
            logger.error(f"Task execution failed for {self.role}: {e}")
            raise


class CrewAIOrchestrator:
    """Orchestrates multiple CrewAI agents for complex workflows"""
    
    def __init__(self):
        self.agents: Dict[str, BaseCrewAIAgent] = {}
        self.crews: Dict[str, Crew] = {}
    
    def register_agent(self, name: str, agent: BaseCrewAIAgent) -> None:
        """Register an agent with the orchestrator"""
        self.agents[name] = agent
        logger.info(f"Registered agent: {name}")
    
    def create_crew(self, name: str, agent_names: List[str], tasks: List[Task]) -> Crew:
        """Create a crew with specified agents and tasks"""
        agents = [self.agents[name].agent for name in agent_names if name in self.agents]
        
        if not agents:
            raise ValueError(f"No valid agents found for crew: {name}")
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process="sequential"  # Can be "sequential" or "hierarchical"
        )
        
        self.crews[name] = crew
        return crew
    
    def execute_crew(self, crew_name: str) -> str:
        """Execute a registered crew"""
        if crew_name not in self.crews:
            raise ValueError(f"Crew not found: {crew_name}")
        
        try:
            result = self.crews[crew_name].kickoff()
            logger.info(f"Crew {crew_name} execution completed")
            return result
        except Exception as e:
            logger.error(f"Crew execution failed for {crew_name}: {e}")
            raise


# Global orchestrator instance
orchestrator = CrewAIOrchestrator()