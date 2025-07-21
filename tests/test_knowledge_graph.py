"""
Tests for Knowledge Graph functionality
"""
import pytest
from src.models.knowledge_graph import UserNode, SkillNode, CompanyNode, JobPostingNode
from src.services.knowledge_graph_service import knowledge_graph_service
from datetime import datetime


class TestKnowledgeGraphModels:
    """Test knowledge graph data models"""
    
    def test_user_node_creation(self):
        """Test UserNode model creation"""
        user_data = {
            "id": "user_123",
            "user_id": "user_123",
            "name": "John Doe",
            "email": "john@example.com",
            "location": "San Francisco, CA"
        }
        
        user_node = UserNode(**user_data)
        assert user_node.name == "John Doe"
        assert user_node.email == "john@example.com"
        assert user_node.type == "USER"
    
    def test_skill_node_creation(self):
        """Test SkillNode model creation"""
        skill_data = {
            "id": "skill_123",
            "name": "Python",
            "category": "technical",
            "proficiency": "advanced",
            "years_of_experience": 5
        }
        
        skill_node = SkillNode(**skill_data)
        assert skill_node.name == "Python"
        assert skill_node.category == "technical"
        assert skill_node.proficiency == "advanced"
        assert skill_node.type == "SKILL"
    
    def test_company_node_creation(self):
        """Test CompanyNode model creation"""
        company_data = {
            "id": "company_123",
            "name": "Tech Corp",
            "industry": "Technology",
            "size": "large",
            "website": "https://techcorp.com",
            "description": "Leading technology company"
        }
        
        company_node = CompanyNode(**company_data)
        assert company_node.name == "Tech Corp"
        assert company_node.industry == "Technology"
        assert company_node.size == "large"
        assert company_node.type == "COMPANY"
    
    def test_job_posting_node_creation(self):
        """Test JobPostingNode model creation"""
        job_data = {
            "id": "job_123",
            "title": "Senior Python Developer",
            "description": "We are looking for a senior Python developer...",
            "location": "Remote",
            "posted_date": datetime.now(),
            "url": "https://techcorp.com/jobs/123"
        }
        
        job_node = JobPostingNode(**job_data)
        assert job_node.title == "Senior Python Developer"
        assert job_node.location == "Remote"
        assert job_node.type == "JOB_POSTING"


class TestKnowledgeGraphService:
    """Test knowledge graph service operations"""
    
    @pytest.mark.asyncio
    async def test_service_initialization(self):
        """Test service initialization"""
        assert knowledge_graph_service is not None
        assert hasattr(knowledge_graph_service, 'neo4j')
    
    # Additional integration tests will be added when database is properly set up
    # These tests require a running Neo4j instance


if __name__ == "__main__":
    pytest.main([__file__])