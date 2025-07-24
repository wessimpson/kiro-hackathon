"""
Tests for Pydantic models and validation in AI Job Application Assistant
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from src.models.knowledge_graph import (
    UserNode, SkillNode, ExperienceNode, ProjectNode,
    ManualJobInput, ProcessedJobPosting, CompanyData, NewsData,
    Resume, CoverLetter, ATSScore, SkillGap, ProjectRecommendation,
    UserRepositoryComplete, CompanyRepositoryComplete,
    SkillCategory, ProficiencyLevel, CompanySize, ImportanceLevel, JobStatus
)
from src.core.exceptions import ValidationException
from src.core.validation import (
    validate_email, validate_url, validate_linkedin_url, validate_github_url,
    validate_skill_verification, validate_pydantic_model
)


class TestUserNode:
    """Test UserNode Pydantic model"""
    
    def test_valid_user_node(self):
        """Test creating a valid UserNode"""
        user_data = {
            "id": "user_123",
            "user_id": "user_123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "location": "San Francisco, CA",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "github_url": "https://github.com/johndoe"
        }
        
        user = UserNode(**user_data)
        assert user.name == "John Doe"
        assert user.email == "john.doe@example.com"
        assert user.type == "USER"
    
    def test_invalid_email(self):
        """Test UserNode with invalid email"""
        user_data = {
            "id": "user_123",
            "user_id": "user_123",
            "name": "John Doe",
            "email": "invalid-email"
        }
        
        with pytest.raises(ValidationError):
            UserNode(**user_data)
    
    def test_invalid_linkedin_url(self):
        """Test UserNode with invalid LinkedIn URL"""
        user_data = {
            "id": "user_123",
            "user_id": "user_123",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "linkedin_url": "https://facebook.com/johndoe"
        }
        
        with pytest.raises(ValidationError):
            UserNode(**user_data)


class TestSkillNode:
    """Test SkillNode Pydantic model"""
    
    def test_valid_skill_node(self):
        """Test creating a valid SkillNode"""
        skill_data = {
            "id": "skill_123",
            "name": "Python",
            "category": SkillCategory.TECHNICAL,
            "proficiency": ProficiencyLevel.ADVANCED,
            "years_of_experience": 5,
            "verified": True
        }
        
        skill = SkillNode(**skill_data)
        assert skill.name == "Python"
        assert skill.category == SkillCategory.TECHNICAL
        assert skill.proficiency == ProficiencyLevel.ADVANCED
        assert skill.years_of_experience == 5
        assert skill.verified is True
    
    def test_invalid_years_experience(self):
        """Test SkillNode with invalid years of experience"""
        skill_data = {
            "id": "skill_123",
            "name": "Python",
            "category": SkillCategory.TECHNICAL,
            "years_of_experience": 60  # Too high
        }
        
        with pytest.raises(ValidationError):
            SkillNode(**skill_data)
    
    def test_skill_verification_validation(self):
        """Test skill verification logic"""
        # Create a verified skill
        skill = SkillNode(
            id="skill_123",
            name="Python",
            category=SkillCategory.TECHNICAL,
            proficiency=ProficiencyLevel.ADVANCED,
            verified=True,
            years_of_experience=5
        )
        
        # Create supporting experience
        experience = ExperienceNode(
            id="exp_123",
            company="Tech Corp",
            position="Software Engineer",
            start_date=datetime(2020, 1, 1),
            description="Developed Python applications for data processing"
        )
        
        # Create supporting project
        project = ProjectNode(
            id="proj_123",
            name="Data Pipeline",
            description="Built a data pipeline using Python",
            technologies=["Python", "PostgreSQL"]
        )
        
        # Should pass validation
        assert validate_skill_verification(skill, [experience], [project]) is True


class TestExperienceNode:
    """Test ExperienceNode Pydantic model"""
    
    def test_valid_experience_node(self):
        """Test creating a valid ExperienceNode"""
        exp_data = {
            "id": "exp_123",
            "company": "Tech Corp",
            "position": "Software Engineer",
            "start_date": datetime(2020, 1, 1),
            "end_date": datetime(2023, 1, 1),
            "description": "Developed web applications using Python and React",
            "achievements": ["Increased performance by 30%", "Led team of 5 developers"]
        }
        
        experience = ExperienceNode(**exp_data)
        assert experience.company == "Tech Corp"
        assert experience.position == "Software Engineer"
        assert len(experience.achievements) == 2
    
    def test_invalid_date_range(self):
        """Test ExperienceNode with invalid date range"""
        exp_data = {
            "id": "exp_123",
            "company": "Tech Corp",
            "position": "Software Engineer",
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2020, 1, 1),  # End before start
            "description": "Developed web applications"
        }
        
        with pytest.raises(ValidationError):
            ExperienceNode(**exp_data)


class TestManualJobInput:
    """Test ManualJobInput Pydantic model"""
    
    def test_valid_job_input(self):
        """Test creating a valid ManualJobInput"""
        job_data = {
            "title": "Senior Python Developer",
            "company_name": "Tech Startup",
            "company_website": "https://techstartup.com",
            "job_description": "We are looking for a senior Python developer with 5+ years of experience...",
            "location": "San Francisco, CA",
            "salary_min": 120000,
            "salary_max": 180000,
            "application_url": "https://techstartup.com/careers/python-dev",
            "remote_allowed": True,
            "status": JobStatus.INTERESTED
        }
        
        job_input = ManualJobInput(**job_data)
        assert job_input.title == "Senior Python Developer"
        assert job_input.salary_min == 120000
        assert job_input.salary_max == 180000
        assert job_input.remote_allowed is True
    
    def test_invalid_salary_range(self):
        """Test ManualJobInput with invalid salary range"""
        job_data = {
            "title": "Senior Python Developer",
            "company_name": "Tech Startup",
            "job_description": "We are looking for a senior Python developer...",
            "location": "San Francisco, CA",
            "salary_min": 180000,
            "salary_max": 120000  # Max less than min
        }
        
        with pytest.raises(ValidationError):
            ManualJobInput(**job_data)


class TestCompanyData:
    """Test CompanyData Pydantic model"""
    
    def test_valid_company_data(self):
        """Test creating valid CompanyData"""
        company_data = {
            "name": "Tech Innovations Inc",
            "website": "https://techinnovations.com",
            "industry": "Software Development",
            "size": CompanySize.MEDIUM,
            "description": "A leading software development company specializing in AI solutions",
            "culture_keywords": ["innovative", "collaborative", "fast-paced"],
            "technologies": ["Python", "React", "AWS", "Docker"]
        }
        
        company = CompanyData(**company_data)
        assert company.name == "Tech Innovations Inc"
        assert company.size == CompanySize.MEDIUM
        assert len(company.technologies) == 4


class TestATSScore:
    """Test ATSScore Pydantic model"""
    
    def test_valid_ats_score(self):
        """Test creating a valid ATSScore"""
        ats_data = {
            "score": 85.5,
            "keyword_match": 90.0,
            "format_score": 80.0,
            "structure_score": 87.0,
            "recommendations": []
        }
        
        ats_score = ATSScore(**ats_data)
        assert ats_score.score == 85.5
        assert ats_score.keyword_match == 90.0
    
    def test_invalid_score_range(self):
        """Test ATSScore with invalid score range"""
        ats_data = {
            "score": 150.0,  # Over 100
            "keyword_match": 90.0,
            "format_score": 80.0,
            "structure_score": 87.0
        }
        
        with pytest.raises(ValidationError):
            ATSScore(**ats_data)


class TestUserRepositoryComplete:
    """Test UserRepositoryComplete composite model"""
    
    def test_valid_user_repository(self):
        """Test creating a valid complete user repository"""
        user_repo_data = {
            "id": "repo_123",
            "user_id": "user_123",
            "personal_info": {"name": "John Doe", "email": "john@example.com"},
            "experiences": [],
            "skills": [
                {
                    "id": "skill_1",
                    "name": "Python",
                    "category": "technical",
                    "proficiency": "advanced",
                    "years_of_experience": 5,
                    "verified": True
                }
            ],
            "projects": [
                {
                    "id": "proj_1",
                    "name": "Web App",
                    "description": "Built a web application using Python and Flask",
                    "technologies": ["Python", "Flask"]
                }
            ],
            "social_profiles": [],
            "documents": []
        }
        
        user_repo = UserRepositoryComplete(**user_repo_data)
        assert user_repo.user_id == "user_123"
        assert len(user_repo.skills) == 1
        assert len(user_repo.projects) == 1


class TestValidationUtilities:
    """Test validation utility functions"""
    
    def test_email_validation(self):
        """Test email validation function"""
        assert validate_email("test@example.com") is True
        assert validate_email("invalid-email") is False
        assert validate_email("test@") is False
    
    def test_url_validation(self):
        """Test URL validation function"""
        assert validate_url("https://example.com") is True
        assert validate_url("http://example.com") is True
        assert validate_url("invalid-url") is False
    
    def test_linkedin_url_validation(self):
        """Test LinkedIn URL validation"""
        assert validate_linkedin_url("https://linkedin.com/in/johndoe") is True
        assert validate_linkedin_url("https://www.linkedin.com/in/johndoe") is True
        assert validate_linkedin_url("https://facebook.com/johndoe") is False
    
    def test_github_url_validation(self):
        """Test GitHub URL validation"""
        assert validate_github_url("https://github.com/johndoe") is True
        assert validate_github_url("https://www.github.com/johndoe") is True
        assert validate_github_url("https://gitlab.com/johndoe") is False
    
    def test_pydantic_model_validation(self):
        """Test Pydantic model validation wrapper"""
        valid_data = {
            "id": "user_123",
            "user_id": "user_123",
            "name": "John Doe",
            "email": "john@example.com"
        }
        
        # Should succeed
        user = validate_pydantic_model(UserNode, valid_data, "Test context")
        assert isinstance(user, UserNode)
        
        # Should fail with ValidationException
        invalid_data = {
            "id": "user_123",
            "user_id": "user_123",
            "name": "John Doe",
            "email": "invalid-email"
        }
        
        with pytest.raises(ValidationException):
            validate_pydantic_model(UserNode, invalid_data, "Test context")


if __name__ == "__main__":
    pytest.main([__file__])