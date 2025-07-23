"""
Notification Service for AI Job Application Assistant

Handles user notifications for job opportunities and application updates.
"""
from typing import Dict, List, Optional
from datetime import datetime
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class NotificationType(str, Enum):
    JOB_OPPORTUNITY = "job_opportunity"
    APPLICATION_READY = "application_ready"
    APPLICATION_SUBMITTED = "application_submitted"
    APPLICATION_UPDATE = "application_update"
    SYSTEM_UPDATE = "system_update"


class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NotificationService:
    """Service for managing user notifications"""
    
    def __init__(self):
        self.notification_channels = {
            "in_app": True,
            "email": True,
            "push": False,  # Can be enabled later
            "sms": False    # Can be enabled later
        }
    
    async def send_job_opportunity_notification(self, user_id: str, job_data: Dict, match_score: float) -> str:
        """Send job opportunity notification to user"""
        try:
            notification_data = {
                "type": NotificationType.JOB_OPPORTUNITY,
                "user_id": user_id,
                "priority": self._calculate_priority(match_score),
                "title": f"New Job Match: {job_data['title']}",
                "message": self._create_job_opportunity_message(job_data, match_score),
                "data": {
                    "job_id": job_data["id"],
                    "job_data": job_data,
                    "match_score": match_score,
                    "actions": [
                        {
                            "id": "apply",
                            "label": "Apply Now",
                            "type": "primary",
                            "action": "apply_to_job"
                        },
                        {
                            "id": "skip",
                            "label": "Skip",
                            "type": "secondary", 
                            "action": "skip_job"
                        },
                        {
                            "id": "save",
                            "label": "Save for Later",
                            "type": "tertiary",
                            "action": "save_job"
                        }
                    ]
                },
                "created_at": datetime.now(),
                "expires_at": datetime.now().replace(hour=23, minute=59, second=59)  # Expires end of day
            }
            
            notification_id = await self._store_notification(notification_data)
            await self._send_notification_via_channels(notification_data)
            
            logger.info(f"Sent job opportunity notification {notification_id} to user {user_id}")
            return notification_id
            
        except Exception as e:
            logger.error(f"Failed to send job opportunity notification: {e}")
            raise
    
    async def send_application_ready_notification(self, user_id: str, application_data: Dict) -> str:
        """Send notification when application is ready for review"""
        try:
            notification_data = {
                "type": NotificationType.APPLICATION_READY,
                "user_id": user_id,
                "priority": NotificationPriority.HIGH,
                "title": "Your Application is Ready for Review",
                "message": f"Your application for {application_data['job_title']} at {application_data['company']} has been generated and is ready for your review.",
                "data": {
                    "application_id": application_data["id"],
                    "job_title": application_data["job_title"],
                    "company": application_data["company"],
                    "ats_score": application_data.get("ats_score"),
                    "actions": [
                        {
                            "id": "review",
                            "label": "Review & Submit",
                            "type": "primary",
                            "action": "review_application"
                        },
                        {
                            "id": "regenerate",
                            "label": "Regenerate",
                            "type": "secondary",
                            "action": "regenerate_application"
                        }
                    ]
                },
                "created_at": datetime.now()
            }
            
            notification_id = await self._store_notification(notification_data)
            await self._send_notification_via_channels(notification_data)
            
            logger.info(f"Sent application ready notification {notification_id} to user {user_id}")
            return notification_id
            
        except Exception as e:
            logger.error(f"Failed to send application ready notification: {e}")
            raise
    
    async def send_application_submitted_notification(self, user_id: str, application_data: Dict) -> str:
        """Send notification when application has been submitted"""
        try:
            notification_data = {
                "type": NotificationType.APPLICATION_SUBMITTED,
                "user_id": user_id,
                "priority": NotificationPriority.MEDIUM,
                "title": "Application Submitted Successfully",
                "message": f"Your application for {application_data['job_title']} at {application_data['company']} has been submitted successfully via {application_data['method']}.",
                "data": {
                    "application_id": application_data["id"],
                    "job_title": application_data["job_title"],
                    "company": application_data["company"],
                    "method": application_data["method"],
                    "submitted_at": application_data["submitted_at"],
                    "actions": [
                        {
                            "id": "track",
                            "label": "Track Application",
                            "type": "primary",
                            "action": "track_application"
                        }
                    ]
                },
                "created_at": datetime.now()
            }
            
            notification_id = await self._store_notification(notification_data)
            await self._send_notification_via_channels(notification_data)
            
            logger.info(f"Sent application submitted notification {notification_id} to user {user_id}")
            return notification_id
            
        except Exception as e:
            logger.error(f"Failed to send application submitted notification: {e}")
            raise
    
    async def get_user_notifications(self, user_id: str, limit: int = 50, unread_only: bool = False) -> List[Dict]:
        """Get notifications for a user"""
        try:
            # This would query the database for user notifications
            # For now, return empty list as placeholder
            return []
            
        except Exception as e:
            logger.error(f"Failed to get user notifications: {e}")
            raise
    
    async def mark_notification_read(self, notification_id: str, user_id: str) -> bool:
        """Mark a notification as read"""
        try:
            # Update notification status in database
            # For now, return True as placeholder
            return True
            
        except Exception as e:
            logger.error(f"Failed to mark notification as read: {e}")
            return False
    
    async def handle_notification_action(self, notification_id: str, action_id: str, user_id: str) -> Dict:
        """Handle user action on notification"""
        try:
            # Get notification data
            notification = await self._get_notification(notification_id)
            
            if not notification or notification["user_id"] != user_id:
                raise ValueError("Notification not found or access denied")
            
            # Handle different actions
            if action_id == "apply_to_job":
                return await self._handle_apply_action(notification)
            elif action_id == "skip_job":
                return await self._handle_skip_action(notification)
            elif action_id == "save_job":
                return await self._handle_save_action(notification)
            elif action_id == "review_application":
                return await self._handle_review_action(notification)
            else:
                raise ValueError(f"Unknown action: {action_id}")
                
        except Exception as e:
            logger.error(f"Failed to handle notification action: {e}")
            raise
    
    def _calculate_priority(self, match_score: float) -> NotificationPriority:
        """Calculate notification priority based on match score"""
        if match_score >= 0.9:
            return NotificationPriority.URGENT
        elif match_score >= 0.8:
            return NotificationPriority.HIGH
        elif match_score >= 0.6:
            return NotificationPriority.MEDIUM
        else:
            return NotificationPriority.LOW
    
    def _create_job_opportunity_message(self, job_data: Dict, match_score: float) -> str:
        """Create job opportunity notification message"""
        match_percentage = int(match_score * 100)
        
        message = f"""
🎯 {match_percentage}% Match Found!

**{job_data['title']}** at **{job_data['company']}**
📍 {job_data.get('location', 'Location not specified')}
💰 {job_data.get('salary_range', 'Salary not specified')}

**Why it's a great match:**
"""
        
        # Add matching skills/reasons
        if job_data.get('matching_skills'):
            message += "\n• " + "\n• ".join(job_data['matching_skills'][:3])
        
        return message.strip()
    
    async def _store_notification(self, notification_data: Dict) -> str:
        """Store notification in database"""
        try:
            # This would store in PostgreSQL notifications table
            # For now, generate a mock ID
            notification_id = f"notif_{datetime.now().timestamp()}"
            
            # TODO: Implement actual database storage
            logger.info(f"Stored notification {notification_id}")
            return notification_id
            
        except Exception as e:
            logger.error(f"Failed to store notification: {e}")
            raise
    
    async def _send_notification_via_channels(self, notification_data: Dict) -> None:
        """Send notification through enabled channels"""
        try:
            user_id = notification_data["user_id"]
            
            # In-app notification (always enabled)
            await self._send_in_app_notification(notification_data)
            
            # Email notification (if enabled for user)
            if await self._is_channel_enabled(user_id, "email"):
                await self._send_email_notification(notification_data)
            
            # Push notification (if enabled)
            if await self._is_channel_enabled(user_id, "push"):
                await self._send_push_notification(notification_data)
                
        except Exception as e:
            logger.error(f"Failed to send notification via channels: {e}")
            raise
    
    async def _send_in_app_notification(self, notification_data: Dict) -> None:
        """Send in-app notification"""
        # This would typically use WebSocket or Server-Sent Events
        # to push real-time notifications to the web app
        logger.info(f"Sent in-app notification to user {notification_data['user_id']}")
    
    async def _send_email_notification(self, notification_data: Dict) -> None:
        """Send email notification"""
        try:
            from .email_service import email_service
            
            # Get user email
            user_email = await self._get_user_email(notification_data["user_id"])
            
            if user_email:
                await email_service.send_notification_email(
                    to_email=user_email,
                    subject=notification_data["title"],
                    content=notification_data["message"],
                    notification_type=notification_data["type"]
                )
                
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
    
    async def _send_push_notification(self, notification_data: Dict) -> None:
        """Send push notification"""
        # Implementation for push notifications (Firebase, etc.)
        logger.info(f"Push notification sent to user {notification_data['user_id']}")
    
    async def _is_channel_enabled(self, user_id: str, channel: str) -> bool:
        """Check if notification channel is enabled for user"""
        # This would check user preferences in database
        # For now, return default channel settings
        return self.notification_channels.get(channel, False)
    
    async def _get_user_email(self, user_id: str) -> Optional[str]:
        """Get user email address"""
        # This would query the user database
        # For now, return None as placeholder
        return None
    
    async def _get_notification(self, notification_id: str) -> Optional[Dict]:
        """Get notification by ID"""
        # This would query the database
        # For now, return None as placeholder
        return None
    
    async def _handle_apply_action(self, notification: Dict) -> Dict:
        """Handle apply to job action"""
        try:
            job_data = notification["data"]["job_data"]
            user_id = notification["user_id"]
            
            # Trigger application generation workflow
            from .application_workflow_service import application_workflow_service
            
            workflow_id = await application_workflow_service.start_application_workflow(
                user_id=user_id,
                job_data=job_data
            )
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "message": "Application generation started"
            }
            
        except Exception as e:
            logger.error(f"Failed to handle apply action: {e}")
            raise
    
    async def _handle_skip_action(self, notification: Dict) -> Dict:
        """Handle skip job action"""
        try:
            # Mark job as skipped for this user
            job_id = notification["data"]["job_id"]
            user_id = notification["user_id"]
            
            # TODO: Store skip action in database for learning
            
            return {
                "success": True,
                "message": "Job skipped"
            }
            
        except Exception as e:
            logger.error(f"Failed to handle skip action: {e}")
            raise
    
    async def _handle_save_action(self, notification: Dict) -> Dict:
        """Handle save job action"""
        try:
            # Save job for later review
            job_data = notification["data"]["job_data"]
            user_id = notification["user_id"]
            
            # TODO: Store saved job in database
            
            return {
                "success": True,
                "message": "Job saved for later"
            }
            
        except Exception as e:
            logger.error(f"Failed to handle save action: {e}")
            raise
    
    async def _handle_review_action(self, notification: Dict) -> Dict:
        """Handle review application action"""
        try:
            application_id = notification["data"]["application_id"]
            
            return {
                "success": True,
                "redirect_url": f"/applications/{application_id}/review",
                "message": "Redirecting to application review"
            }
            
        except Exception as e:
            logger.error(f"Failed to handle review action: {e}")
            raise


# Global service instance
notification_service = NotificationService()