"""
Job Application Agent for AI Job Application Assistant

This CrewAI agent handles the actual job application process across different platforms.
"""
from crewai import Agent
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class JobApplicationAgent:
    """CrewAI agent for handling job applications"""
    
    def __init__(self):
        self.agent = Agent(
            role="Job Application Specialist",
            goal="Handle job applications across multiple platforms with high success rates",
            backstory="""You are an expert in job application processes across different platforms.
            You understand the nuances of each job board, application tracking systems, and 
            can navigate complex application workflows to ensure successful submissions.""",
            verbose=True,
            allow_delegation=False
        )
    
    async def apply_to_job(self, application_data: Dict) -> Dict:
        """Apply to a job using the appropriate method"""
        try:
            job_source = application_data.get("job_source", "platform")
            
            if job_source == "platform":
                return await self._apply_via_platform(application_data)
            elif job_source == "linkedin":
                return await self._apply_via_linkedin(application_data)
            elif job_source == "indeed":
                return await self._apply_via_indeed(application_data)
            elif job_source == "glassdoor":
                return await self._apply_via_glassdoor(application_data)
            else:
                return await self._apply_via_email(application_data)
                
        except Exception as e:
            logger.error(f"Failed to apply to job: {e}")
            return {
                "success": False,
                "error": str(e),
                "application_id": None
            }
    
    async def _apply_via_platform(self, application_data: Dict) -> Dict:
        """Apply through our own platform"""
        try:
            # Store application in our database
            from ..services.application_service import application_service
            
            application_id = await application_service.create_application(
                user_id=application_data["user_id"],
                job_data=application_data["job_data"],
                resume_content=application_data["resume"],
                cover_letter_content=application_data["cover_letter"],
                application_method="platform"
            )
            
            # Send application to company (email, API, etc.)
            notification_sent = await self._notify_company(application_data)
            
            return {
                "success": True,
                "application_id": application_id,
                "method": "platform",
                "notification_sent": notification_sent,
                "applied_at": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Platform application failed: {e}")
            raise
    
    async def _apply_via_linkedin(self, application_data: Dict) -> Dict:
        """Apply through LinkedIn using automation"""
        try:
            from ..services.web_automation_service import linkedin_automation
            
            result = await linkedin_automation.apply_to_job(
                job_url=application_data["job_data"]["url"],
                resume_path=application_data.get("resume_file_path"),
                cover_letter_text=application_data.get("cover_letter"),
                user_credentials=application_data.get("linkedin_credentials")
            )
            
            return {
                "success": result["success"],
                "application_id": result.get("application_id"),
                "method": "linkedin",
                "applied_at": datetime.now(),
                "automation_log": result.get("log")
            }
            
        except Exception as e:
            logger.error(f"LinkedIn application failed: {e}")
            raise
    
    async def _apply_via_indeed(self, application_data: Dict) -> Dict:
        """Apply through Indeed using automation"""
        try:
            from ..services.web_automation_service import indeed_automation
            
            result = await indeed_automation.apply_to_job(
                job_url=application_data["job_data"]["url"],
                resume_path=application_data.get("resume_file_path"),
                cover_letter_text=application_data.get("cover_letter"),
                user_profile=application_data.get("user_profile")
            )
            
            return {
                "success": result["success"],
                "application_id": result.get("application_id"),
                "method": "indeed",
                "applied_at": datetime.now(),
                "automation_log": result.get("log")
            }
            
        except Exception as e:
            logger.error(f"Indeed application failed: {e}")
            raise
    
    async def _apply_via_glassdoor(self, application_data: Dict) -> Dict:
        """Apply through Glassdoor using automation"""
        # Similar implementation to LinkedIn/Indeed
        pass
    
    async def _apply_via_email(self, application_data: Dict) -> Dict:
        """Apply via email when job posting provides email contact"""
        try:
            from ..services.email_service import email_service
            
            job_data = application_data["job_data"]
            contact_email = job_data.get("contact_email")
            
            if not contact_email:
                raise ValueError("No contact email provided for email application")
            
            # Compose professional application email
            email_content = await self._compose_application_email(application_data)
            
            # Send email with attachments
            result = await email_service.send_application_email(
                to_email=contact_email,
                subject=f"Application for {job_data['title']} - {application_data['user_name']}",
                body=email_content["body"],
                attachments=[
                    {
                        "filename": "resume.pdf",
                        "content": application_data["resume_pdf"]
                    },
                    {
                        "filename": "cover_letter.pdf", 
                        "content": application_data["cover_letter_pdf"]
                    }
                ]
            )
            
            return {
                "success": result["success"],
                "application_id": result.get("message_id"),
                "method": "email",
                "applied_at": datetime.now(),
                "recipient": contact_email
            }
            
        except Exception as e:
            logger.error(f"Email application failed: {e}")
            raise
    
    async def _compose_application_email(self, application_data: Dict) -> Dict:
        """Compose professional application email"""
        job_data = application_data["job_data"]
        user_name = application_data["user_name"]
        
        subject = f"Application for {job_data['title']} Position"
        
        body = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_data['title']} position at {job_data['company']}. 

{application_data.get('cover_letter', 'Please find my resume attached for your consideration.')}

I have attached my resume and cover letter for your review. I would welcome the opportunity to discuss how my skills and experience align with your team's needs.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
{user_name}

---
This application was sent via AI Job Application Assistant
"""
        
        return {
            "subject": subject,
            "body": body
        }
    
    async def _notify_company(self, application_data: Dict) -> bool:
        """Notify company about new application through our platform"""
        try:
            # This could be:
            # 1. Email notification to company
            # 2. API call to company's ATS
            # 3. Webhook notification
            # 4. Dashboard notification
            
            company_contact = application_data["job_data"].get("company_contact")
            if company_contact:
                from ..services.email_service import email_service
                
                await email_service.send_company_notification(
                    company_email=company_contact,
                    application_data=application_data
                )
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to notify company: {e}")
            return False
    
    async def track_application_status(self, application_id: str, job_source: str) -> Dict:
        """Track the status of a submitted application"""
        try:
            if job_source == "linkedin":
                return await self._track_linkedin_application(application_id)
            elif job_source == "indeed":
                return await self._track_indeed_application(application_id)
            elif job_source == "platform":
                return await self._track_platform_application(application_id)
            else:
                return {"status": "unknown", "last_updated": datetime.now()}
                
        except Exception as e:
            logger.error(f"Failed to track application status: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _track_linkedin_application(self, application_id: str) -> Dict:
        """Track LinkedIn application status"""
        # Implementation would check LinkedIn for application status
        return {"status": "submitted", "last_updated": datetime.now()}
    
    async def _track_indeed_application(self, application_id: str) -> Dict:
        """Track Indeed application status"""
        # Implementation would check Indeed for application status
        return {"status": "submitted", "last_updated": datetime.now()}
    
    async def _track_platform_application(self, application_id: str) -> Dict:
        """Track platform application status"""
        try:
            from ..services.application_service import application_service
            return await application_service.get_application_status(application_id)
        except Exception as e:
            logger.error(f"Failed to track platform application: {e}")
            raise