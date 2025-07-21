"""
Knowledge Graph Service for AI Job Application Assistant

Provides high-level operations for knowledge graph management.
"""
from typing import Dict, List, Optional, Any
from ..database.neo4j_client import neo4j_client
from ..models.knowledge_graph import (
    UserNode, SkillNode, ExperienceNode, ProjectNode,
    CompanyNode, JobPostingNode, RequirementNode,
    UserRepository, CompanyRepository
)
import logging

logger = logging.getLogger(__name__)


class KnowledgeGraphService:
    """Service for knowledge graph operations"""
    
    def __init__(self):
        self.neo4j = neo4j_client
    
    async def create_user_repository(self, user_data: Dict[str, Any]) -> str:
        """Create a new user repository in the knowledge graph"""
        try:
            # Create user node
            user_node = UserNode(**user_data)
            user_id = self.neo4j.create_node("USER", user_node.dict())
            
            logger.info(f"Created user repository for user: {user_id}")
            return user_id
        except Exception as e:
            logger.error(f"Failed to create user repository: {e}")
            raise
    
    async def add_user_skill(self, user_id: str, skill_data: Dict[str, Any]) -> str:
        """Add a skill to user's knowledge graph"""
        try:
            # Create skill node
            skill_node = SkillNode(**skill_data)
            skill_id = self.neo4j.create_node("SKILL", skill_node.dict())
            
            # Create relationship
            self.neo4j.create_relationship(
                user_id, skill_id, "HAS_SKILL",
                {
                    "proficiency": skill_data.get("proficiency"),
                    "years_of_experience": skill_data.get("years_of_experience", 0),
                    "verified": skill_data.get("verified", False)
                }
            )
            
            logger.info(f"Added skill {skill_data['name']} to user {user_id}")
            return skill_id
        except Exception as e:
            logger.error(f"Failed to add user skill: {e}")
            raise
    
    async def add_user_experience(self, user_id: str, experience_data: Dict[str, Any]) -> str:
        """Add work experience to user's knowledge graph"""
        try:
            # Create experience node
            experience_node = ExperienceNode(**experience_data)
            experience_id = self.neo4j.create_node("EXPERIENCE", experience_node.dict())
            
            # Create relationship
            self.neo4j.create_relationship(user_id, experience_id, "HAS_EXPERIENCE")
            
            logger.info(f"Added experience at {experience_data['company']} to user {user_id}")
            return experience_id
        except Exception as e:
            logger.error(f"Failed to add user experience: {e}")
            raise
    
    async def create_company_repository(self, company_data: Dict[str, Any]) -> str:
        """Create a new company repository in the knowledge graph"""
        try:
            # Create company node
            company_node = CompanyNode(**company_data)
            company_id = self.neo4j.create_node("COMPANY", company_node.dict())
            
            logger.info(f"Created company repository for: {company_data['name']}")
            return company_id
        except Exception as e:
            logger.error(f"Failed to create company repository: {e}")
            raise
    
    async def add_job_posting(self, company_id: str, job_data: Dict[str, Any]) -> str:
        """Add a job posting to company's knowledge graph"""
        try:
            # Create job posting node
            job_node = JobPostingNode(**job_data)
            job_id = self.neo4j.create_node("JOB_POSTING", job_node.dict())
            
            # Create relationship
            self.neo4j.create_relationship(company_id, job_id, "OFFERS_JOB")
            
            logger.info(f"Added job posting {job_data['title']} to company {company_id}")
            return job_id
        except Exception as e:
            logger.error(f"Failed to add job posting: {e}")
            raise
    
    async def get_user_repository(self, user_id: str) -> Optional[UserRepository]:
        """Retrieve complete user repository"""
        try:
            graph_data = self.neo4j.get_user_knowledge_graph(user_id)
            if not graph_data:
                return None
            
            # Convert to UserRepository model
            user_repo = UserRepository(
                user=UserNode(**graph_data.get("user", {})),
                skills=[SkillNode(**skill) for skill in graph_data.get("skills", [])],
                experiences=[ExperienceNode(**exp) for exp in graph_data.get("experiences", [])],
                projects=[ProjectNode(**proj) for proj in graph_data.get("projects", [])]
            )
            
            return user_repo
        except Exception as e:
            logger.error(f"Failed to retrieve user repository: {e}")
            raise
    
    async def get_company_repository(self, company_id: str) -> Optional[CompanyRepository]:
        """Retrieve complete company repository"""
        try:
            graph_data = self.neo4j.get_company_knowledge_graph(company_id)
            if not graph_data:
                return None
            
            # Convert to CompanyRepository model
            company_repo = CompanyRepository(
                company=CompanyNode(**graph_data.get("company", {})),
                job_postings=[JobPostingNode(**job) for job in graph_data.get("job_postings", [])]
            )
            
            return company_repo
        except Exception as e:
            logger.error(f"Failed to retrieve company repository: {e}")
            raise
    
    async def calculate_job_compatibility(self, user_id: str, job_id: str) -> Dict[str, Any]:
        """Calculate compatibility score between user and job"""
        try:
            match_score = self.neo4j.calculate_job_match_score(user_id, job_id)
            
            # Get detailed matching information
            # This will be expanded in later tasks
            
            return {
                "compatibility_score": match_score,
                "user_id": user_id,
                "job_id": job_id,
                "calculated_at": "2024-01-01T00:00:00Z"  # Will use actual timestamp
            }
        except Exception as e:
            logger.error(f"Failed to calculate job compatibility: {e}")
            raise
    
    async def find_skill_gaps(self, user_id: str, job_id: str) -> List[str]:
        """Find skill gaps between user and job requirements"""
        try:
            query = """
            MATCH (u:USER {user_id: $user_id})-[:HAS_SKILL]->(us:SKILL)
            MATCH (j:JOB_POSTING {id: $job_id})-[:REQUIRES_SKILL]->(jr:REQUIREMENT)-[:RELATES_TO_SKILL]->(js:SKILL)
            WITH collect(us.name) as user_skills, collect(js.name) as job_skills
            RETURN [skill IN job_skills WHERE NOT skill IN user_skills] as missing_skills
            """
            
            result = self.neo4j.execute_query(query, {"user_id": user_id, "job_id": job_id})
            return result[0]["missing_skills"] if result else []
        except Exception as e:
            logger.error(f"Failed to find skill gaps: {e}")
            raise


# Global service instance
knowledge_graph_service = KnowledgeGraphService()