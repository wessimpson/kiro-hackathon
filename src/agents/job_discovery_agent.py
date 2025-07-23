"""
Job Discovery Agent for AI Job Application Assistant

This CrewAI agent handles autonomous job discovery, matching, and notification.
"""
from crewai import Agent
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class JobDiscoveryAgent:
    """CrewAI agent for autonomous job discovery and matching"""
    
    def __init__(self):
        self.agent = Agent(
            role="Job Discovery Specialist",
            goal="Continuously monitor job boards and identify relevant opportunities for users",
            backstory="""You are an expert job market analyst with deep knowledge of job boards, 
            hiring patterns, and job matching algorithms. You excel at finding the perfect job 
            opportunities that match user profiles and preferences.""",
            verbose=True,
            allow_delegation=False
        )
    
    async def monitor_job_boards(self, user_preferences: Dict) -> List[Dict]:
        """Monitor multiple job boards for relevant opportunities"""
        try:
            # Job board sources to monitor
            job_sources = [
                "linkedin",
                "indeed", 
                "glassdoor",
                "stackoverflow",
                "angellist",
                "remote_ok",
                "weworkremotely"
            ]
            
            discovered_jobs = []
            
            for source in job_sources:
                jobs = await self._scrape_job_source(source, user_preferences)
                discovered_jobs.extend(jobs)
            
            logger.info(f"Discovered {len(discovered_jobs)} jobs from {len(job_sources)} sources")
            return discovered_jobs
            
        except Exception as e:
            logger.error(f"Failed to monitor job boards: {e}")
            raise
    
    async def _scrape_job_source(self, source: str, preferences: Dict) -> List[Dict]:
        """Scrape specific job board source"""
        # Implementation will vary by source
        # This is a placeholder for the actual scraping logic
        
        scrapers = {
            "linkedin": self._scrape_linkedin,
            "indeed": self._scrape_indeed,
            "glassdoor": self._scrape_glassdoor,
            "stackoverflow": self._scrape_stackoverflow,
            "angellist": self._scrape_angellist,
            "remote_ok": self._scrape_remote_ok,
            "weworkremotely": self._scrape_weworkremotely
        }
        
        if source in scrapers:
            return await scrapers[source](preferences)
        else:
            logger.warning(f"Unknown job source: {source}")
            return []
    
    async def calculate_job_match_score(self, user_id: str, job_data: Dict) -> float:
        """Calculate how well a job matches user profile"""
        try:
            # Get user knowledge graph
            from ..services.knowledge_graph_service import knowledge_graph_service
            user_repo = await knowledge_graph_service.get_user_repository(user_id)
            
            if not user_repo:
                return 0.0
            
            # Calculate match based on multiple factors
            skill_match = await self._calculate_skill_match(user_repo.skills, job_data.get("required_skills", []))
            experience_match = await self._calculate_experience_match(user_repo.experiences, job_data)
            location_match = await self._calculate_location_match(user_repo.user.location, job_data.get("location"))
            salary_match = await self._calculate_salary_match(user_repo, job_data.get("salary_range"))
            
            # Weighted average
            total_score = (
                skill_match * 0.4 +
                experience_match * 0.3 +
                location_match * 0.2 +
                salary_match * 0.1
            )
            
            return min(total_score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            logger.error(f"Failed to calculate job match score: {e}")
            return 0.0
    
    async def _calculate_skill_match(self, user_skills: List, job_skills: List[str]) -> float:
        """Calculate skill compatibility score"""
        if not job_skills or not user_skills:
            return 0.0
        
        user_skill_names = {skill.name.lower() for skill in user_skills}
        job_skill_names = {skill.lower() for skill in job_skills}
        
        matching_skills = user_skill_names.intersection(job_skill_names)
        return len(matching_skills) / len(job_skill_names)
    
    async def _calculate_experience_match(self, user_experiences: List, job_data: Dict) -> float:
        """Calculate experience compatibility score"""
        required_years = job_data.get("years_required", 0)
        if required_years == 0:
            return 1.0
        
        total_experience = sum(
            (exp.end_date or datetime.now()).year - exp.start_date.year 
            for exp in user_experiences
        )
        
        if total_experience >= required_years:
            return 1.0
        else:
            return total_experience / required_years
    
    async def _calculate_location_match(self, user_location: str, job_location: str) -> float:
        """Calculate location compatibility score"""
        if not job_location or not user_location:
            return 0.5  # Neutral if location info missing
        
        # Remote jobs always match
        if "remote" in job_location.lower():
            return 1.0
        
        # Simple city/state matching (can be enhanced with geocoding)
        user_parts = user_location.lower().split(",")
        job_parts = job_location.lower().split(",")
        
        # Check for city or state matches
        for user_part in user_parts:
            for job_part in job_parts:
                if user_part.strip() in job_part.strip() or job_part.strip() in user_part.strip():
                    return 1.0
        
        return 0.0
    
    async def _calculate_salary_match(self, user_repo, salary_range: Dict) -> float:
        """Calculate salary compatibility score"""
        if not salary_range:
            return 0.5  # Neutral if no salary info
        
        # This would ideally check user preferences for salary expectations
        # For now, return neutral score
        return 0.5
    
    async def create_job_notification(self, user_id: str, job_data: Dict, match_score: float) -> Dict:
        """Create a job notification for the user"""
        notification = {
            "id": f"job_notif_{datetime.now().timestamp()}",
            "user_id": user_id,
            "job_data": job_data,
            "match_score": match_score,
            "created_at": datetime.now(),
            "status": "pending",  # pending, approved, rejected
            "notification_type": "job_opportunity",
            "priority": self._calculate_priority(match_score),
            "summary": {
                "title": job_data.get("title"),
                "company": job_data.get("company"),
                "location": job_data.get("location"),
                "salary": job_data.get("salary_range"),
                "match_percentage": int(match_score * 100),
                "key_matches": job_data.get("matching_skills", [])[:5]  # Top 5 matching skills
            }
        }
        
        return notification
    
    def _calculate_priority(self, match_score: float) -> str:
        """Calculate notification priority based on match score"""
        if match_score >= 0.8:
            return "high"
        elif match_score >= 0.6:
            return "medium"
        else:
            return "low"
    
    # Job board specific scrapers (placeholders for now)
    async def _scrape_linkedin(self, preferences: Dict) -> List[Dict]:
        """Scrape LinkedIn jobs"""
        # Implementation will use LinkedIn API or web scraping
        return []
    
    async def _scrape_indeed(self, preferences: Dict) -> List[Dict]:
        """Scrape Indeed jobs"""
        # Implementation will use Indeed API or web scraping
        return []
    
    async def _scrape_glassdoor(self, preferences: Dict) -> List[Dict]:
        """Scrape Glassdoor jobs"""
        return []
    
    async def _scrape_stackoverflow(self, preferences: Dict) -> List[Dict]:
        """Scrape Stack Overflow jobs"""
        return []
    
    async def _scrape_angellist(self, preferences: Dict) -> List[Dict]:
        """Scrape AngelList jobs"""
        return []
    
    async def _scrape_remote_ok(self, preferences: Dict) -> List[Dict]:
        """Scrape Remote OK jobs"""
        return []
    
    async def _scrape_weworkremotely(self, preferences: Dict) -> List[Dict]:
        """Scrape We Work Remotely jobs"""
        return []