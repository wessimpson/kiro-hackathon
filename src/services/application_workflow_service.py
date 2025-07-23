"""
Application Workflow Service for AI Job Application Assistant

Orchestrates the complete job application workflow from discovery to submission.
"""
from typing import Dict, List, Optional
from datetime import datetime
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class WorkflowStatus(str, Enum):
    PENDING = "pending"
    GENERATING_RESUME = "generating_resume"
    GENERATING_COVER_LETTER = "generating_cover_letter"
    CALCULATING_ATS_SCORE = "calculating_ats_score"
    READY_FOR_REVIEW = "ready_for_review"
    UNDER_REVIEW = "under_review"
    APPROVED_FOR_SUBMISSION = "approved_for_submission"
    SUBMITTING = "submitting"
    SUBMITTED = "submitted"
    FAILED = "failed"


class ApplicationWorkflowService:
    """Service for orchestrating job application workflows"""
    
    def __init__(self):
        self.active_workflows = {}  # In-memory storage for demo, would use database
    
    async def start_application_workflow(self, user_id: str, job_data: Dict) -> str:
        """Start the complete application workflow"""
        try:
            workflow_id = f"workflow_{user_id}_{job_data['id']}_{datetime.now().timestamp()}"
            
            workflow = {
                "id": workflow_id,
                "user_id": user_id,
                "job_data": job_data,
                "status": WorkflowStatus.PENDING,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "steps": {
                    "resume_generation": {"status": "pending", "result": None},
                    "cover_letter_generation": {"status": "pending", "result": None},
                    "ats_scoring": {"status": "pending", "result": None},
                    "user_review": {"status": "pending", "result": None},
                    "submission": {"status": "pending", "result": None}
                },
                "application_data": {}
            }
            
            self.active_workflows[workflow_id] = workflow
            
            # Start the workflow asynchronously
            await self._execute_workflow(workflow_id)
            
            logger.info(f"Started application workflow {workflow_id} for user {user_id}")
            return workflow_id
            
        except Exception as e:
            logger.error(f"Failed to start application workflow: {e}")
            raise
    
    async def _execute_workflow(self, workflow_id: str) -> None:
        """Execute the application workflow steps"""
        try:
            workflow = self.active_workflows[workflow_id]
            
            # Step 1: Generate Resume
            await self._generate_resume(workflow)
            
            # Step 2: Generate Cover Letter
            await self._generate_cover_letter(workflow)
            
            # Step 3: Calculate ATS Score
            await self._calculate_ats_score(workflow)
            
            # Step 4: Notify user for review
            await self._notify_user_for_review(workflow)
            
        except Exception as e:
            logger.error(f"Workflow execution failed for {workflow_id}: {e}")
            await self._mark_workflow_failed(workflow_id, str(e))
    
    async def _generate_resume(self, workflow: Dict) -> None:
        """Generate tailored resume for the job"""
        try:
            workflow["status"] = WorkflowStatus.GENERATING_RESUME
            workflow["steps"]["resume_generation"]["status"] = "in_progress"
            workflow["updated_at"] = datetime.now()
            
            # Use Resume Generation Agent
            from ..agents.resume_generation_agent import ResumeGenerationAgent
            resume_agent = ResumeGenerationAgent()
            
            resume_data = await resume_agent.generate_tailored_resume(
                user_id=workflow["user_id"],
                job_id=workflow["job_data"]["id"]
            )
            
            workflow["steps"]["resume_generation"]["status"] = "completed"
            workflow["steps"]["resume_generation"]["result"] = resume_data
            workflow["application_data"]["resume"] = resume_data
            
            logger.info(f"Resume generated for workflow {workflow['id']}")
            
        except Exception as e:
            workflow["steps"]["resume_generation"]["status"] = "failed"
            workflow["steps"]["resume_generation"]["error"] = str(e)
            logger.error(f"Resume generation failed for workflow {workflow['id']}: {e}")
            raise
    
    async def _generate_cover_letter(self, workflow: Dict) -> None:
        """Generate personalized cover letter"""
        try:
            workflow["status"] = WorkflowStatus.GENERATING_COVER_LETTER
            workflow["steps"]["cover_letter_generation"]["status"] = "in_progress"
            workflow["updated_at"] = datetime.now()
            
            # Use Cover Letter Agent
            from ..agents.cover_letter_agent import CoverLetterAgent
            cover_letter_agent = CoverLetterAgent()
            
            cover_letter_data = await cover_letter_agent.generate_personalized_cover_letter(
                user_id=workflow["user_id"],
                job_id=workflow["job_data"]["id"],
                company_id=workflow["job_data"]["company_id"]
            )
            
            workflow["steps"]["cover_letter_generation"]["status"] = "completed"
            workflow["steps"]["cover_letter_generation"]["result"] = cover_letter_data
            workflow["application_data"]["cover_letter"] = cover_letter_data
            
            logger.info(f"Cover letter generated for workflow {workflow['id']}")
            
        except Exception as e:
            workflow["steps"]["cover_letter_generation"]["status"] = "failed"
            workflow["steps"]["cover_letter_generation"]["error"] = str(e)
            logger.error(f"Cover letter generation failed for workflow {workflow['id']}: {e}")
            raise
    
    async def _calculate_ats_score(self, workflow: Dict) -> None:
        """Calculate ATS compatibility score"""
        try:
            workflow["status"] = WorkflowStatus.CALCULATING_ATS_SCORE
            workflow["steps"]["ats_scoring"]["status"] = "in_progress"
            workflow["updated_at"] = datetime.now()
            
            # Use ATS Scoring Agent
            from ..agents.ats_scoring_agent import ATSScoringAgent
            ats_agent = ATSScoringAgent()
            
            ats_result = await ats_agent.score_resume_compatibility(
                resume=workflow["application_data"]["resume"],
                job_requirements=workflow["job_data"]["requirements"]
            )
            
            workflow["steps"]["ats_scoring"]["status"] = "completed"
            workflow["steps"]["ats_scoring"]["result"] = ats_result
            workflow["application_data"]["ats_score"] = ats_result["score"]
            workflow["application_data"]["ats_recommendations"] = ats_result["recommendations"]
            
            logger.info(f"ATS score calculated for workflow {workflow['id']}: {ats_result['score']}")
            
        except Exception as e:
            workflow["steps"]["ats_scoring"]["status"] = "failed"
            workflow["steps"]["ats_scoring"]["error"] = str(e)
            logger.error(f"ATS scoring failed for workflow {workflow['id']}: {e}")
            raise
    
    async def _notify_user_for_review(self, workflow: Dict) -> None:
        """Notify user that application is ready for review"""
        try:
            workflow["status"] = WorkflowStatus.READY_FOR_REVIEW
            workflow["updated_at"] = datetime.now()
            
            # Send notification to user
            from .notification_service import notification_service
            
            application_data = {
                "id": workflow["id"],
                "job_title": workflow["job_data"]["title"],
                "company": workflow["job_data"]["company"],
                "ats_score": workflow["application_data"]["ats_score"]
            }
            
            await notification_service.send_application_ready_notification(
                user_id=workflow["user_id"],
                application_data=application_data
            )
            
            logger.info(f"User notified for review - workflow {workflow['id']}")
            
        except Exception as e:
            logger.error(f"Failed to notify user for review - workflow {workflow['id']}: {e}")
            raise
    
    async def approve_application_for_submission(self, workflow_id: str, user_id: str, refinements: Optional[Dict] = None) -> Dict:
        """User approves application for submission"""
        try:
            workflow = self.active_workflows.get(workflow_id)
            
            if not workflow or workflow["user_id"] != user_id:
                raise ValueError("Workflow not found or access denied")
            
            if workflow["status"] != WorkflowStatus.READY_FOR_REVIEW:
                raise ValueError(f"Workflow not ready for approval. Current status: {workflow['status']}")
            
            # Apply any user refinements
            if refinements:
                await self._apply_refinements(workflow, refinements)
            
            workflow["status"] = WorkflowStatus.APPROVED_FOR_SUBMISSION
            workflow["steps"]["user_review"]["status"] = "completed"
            workflow["steps"]["user_review"]["approved_at"] = datetime.now()
            workflow["updated_at"] = datetime.now()
            
            # Start submission process
            submission_result = await self._submit_application(workflow)
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "submission_result": submission_result
            }
            
        except Exception as e:
            logger.error(f"Failed to approve application for submission: {e}")
            raise
    
    async def _apply_refinements(self, workflow: Dict, refinements: Dict) -> None:
        """Apply user refinements to the application"""
        try:
            if "resume_changes" in refinements:
                # Apply resume changes
                resume_changes = refinements["resume_changes"]
                current_resume = workflow["application_data"]["resume"]
                
                # Use LLM to apply specific changes
                from ..services.llm_service import llm_service
                
                refined_resume = await llm_service.refine_document(
                    document=current_resume,
                    changes=resume_changes,
                    document_type="resume"
                )
                
                workflow["application_data"]["resume"] = refined_resume
            
            if "cover_letter_changes" in refinements:
                # Apply cover letter changes
                cover_letter_changes = refinements["cover_letter_changes"]
                current_cover_letter = workflow["application_data"]["cover_letter"]
                
                from ..services.llm_service import llm_service
                
                refined_cover_letter = await llm_service.refine_document(
                    document=current_cover_letter,
                    changes=cover_letter_changes,
                    document_type="cover_letter"
                )
                
                workflow["application_data"]["cover_letter"] = refined_cover_letter
            
            # Recalculate ATS score if resume was changed
            if "resume_changes" in refinements:
                await self._calculate_ats_score(workflow)
            
            logger.info(f"Applied refinements to workflow {workflow['id']}")
            
        except Exception as e:
            logger.error(f"Failed to apply refinements: {e}")
            raise
    
    async def _submit_application(self, workflow: Dict) -> Dict:
        """Submit the application using the appropriate method"""
        try:
            workflow["status"] = WorkflowStatus.SUBMITTING
            workflow["steps"]["submission"]["status"] = "in_progress"
            workflow["updated_at"] = datetime.now()
            
            # Use Job Application Agent
            from ..agents.job_application_agent import JobApplicationAgent
            application_agent = JobApplicationAgent()
            
            application_data = {
                "user_id": workflow["user_id"],
                "job_data": workflow["job_data"],
                "resume": workflow["application_data"]["resume"],
                "cover_letter": workflow["application_data"]["cover_letter"],
                "job_source": workflow["job_data"].get("source", "platform")
            }
            
            submission_result = await application_agent.apply_to_job(application_data)
            
            if submission_result["success"]:
                workflow["status"] = WorkflowStatus.SUBMITTED
                workflow["steps"]["submission"]["status"] = "completed"
                workflow["steps"]["submission"]["result"] = submission_result
                
                # Send success notification
                await self._notify_application_submitted(workflow, submission_result)
                
                # Store application in database for tracking
                await self._store_application_record(workflow, submission_result)
                
            else:
                workflow["status"] = WorkflowStatus.FAILED
                workflow["steps"]["submission"]["status"] = "failed"
                workflow["steps"]["submission"]["error"] = submission_result.get("error")
            
            workflow["updated_at"] = datetime.now()
            
            logger.info(f"Application submission completed for workflow {workflow['id']}: {submission_result['success']}")
            return submission_result
            
        except Exception as e:
            workflow["status"] = WorkflowStatus.FAILED
            workflow["steps"]["submission"]["status"] = "failed"
            workflow["steps"]["submission"]["error"] = str(e)
            logger.error(f"Application submission failed for workflow {workflow['id']}: {e}")
            raise
    
    async def _notify_application_submitted(self, workflow: Dict, submission_result: Dict) -> None:
        """Notify user that application has been submitted"""
        try:
            from .notification_service import notification_service
            
            application_data = {
                "id": workflow["id"],
                "job_title": workflow["job_data"]["title"],
                "company": workflow["job_data"]["company"],
                "method": submission_result["method"],
                "submitted_at": submission_result["applied_at"]
            }
            
            await notification_service.send_application_submitted_notification(
                user_id=workflow["user_id"],
                application_data=application_data
            )
            
        except Exception as e:
            logger.error(f"Failed to send submission notification: {e}")
    
    async def _store_application_record(self, workflow: Dict, submission_result: Dict) -> None:
        """Store application record in database for tracking"""
        try:
            from .application_service import application_service
            
            await application_service.create_application_record(
                user_id=workflow["user_id"],
                job_data=workflow["job_data"],
                application_data=workflow["application_data"],
                submission_result=submission_result,
                workflow_id=workflow["id"]
            )
            
        except Exception as e:
            logger.error(f"Failed to store application record: {e}")
    
    async def _mark_workflow_failed(self, workflow_id: str, error_message: str) -> None:
        """Mark workflow as failed"""
        try:
            workflow = self.active_workflows.get(workflow_id)
            if workflow:
                workflow["status"] = WorkflowStatus.FAILED
                workflow["error"] = error_message
                workflow["updated_at"] = datetime.now()
                
                # Notify user of failure
                # TODO: Implement failure notification
                
        except Exception as e:
            logger.error(f"Failed to mark workflow as failed: {e}")
    
    async def get_workflow_status(self, workflow_id: str, user_id: str) -> Dict:
        """Get current workflow status"""
        try:
            workflow = self.active_workflows.get(workflow_id)
            
            if not workflow or workflow["user_id"] != user_id:
                raise ValueError("Workflow not found or access denied")
            
            return {
                "workflow_id": workflow_id,
                "status": workflow["status"],
                "created_at": workflow["created_at"],
                "updated_at": workflow["updated_at"],
                "steps": workflow["steps"],
                "job_data": {
                    "title": workflow["job_data"]["title"],
                    "company": workflow["job_data"]["company"]
                },
                "application_data": {
                    "ats_score": workflow["application_data"].get("ats_score"),
                    "has_resume": "resume" in workflow["application_data"],
                    "has_cover_letter": "cover_letter" in workflow["application_data"]
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get workflow status: {e}")
            raise
    
    async def cancel_workflow(self, workflow_id: str, user_id: str) -> bool:
        """Cancel an active workflow"""
        try:
            workflow = self.active_workflows.get(workflow_id)
            
            if not workflow or workflow["user_id"] != user_id:
                raise ValueError("Workflow not found or access denied")
            
            if workflow["status"] in [WorkflowStatus.SUBMITTED, WorkflowStatus.FAILED]:
                raise ValueError("Cannot cancel completed or failed workflow")
            
            workflow["status"] = "cancelled"
            workflow["updated_at"] = datetime.now()
            
            logger.info(f"Cancelled workflow {workflow_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cancel workflow: {e}")
            return False


# Global service instance
application_workflow_service = ApplicationWorkflowService()