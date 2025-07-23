"""
Job Monitoring Service for AI Job Application Assistant

Continuously monitors job boards and matches opportunities with users.
"""
import asyncio
from typing import Dict, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class JobMonitoringService:
    """Service for continuous job monitoring and matching"""
    
    def __init__(self):
        self.monitoring_active = False
        self.monitoring_interval = 300  # 5 minutes
        self.last_scan_time = {}  # Track last scan time per user
    
    async def start_monitoring(self) -> None:
        """Start continuous job monitoring"""
        if self.monitoring_active:
            logger.warning("Job monitoring is already active")
            return
        
        self.monitoring_active = True
        logger.info("Starting job monitoring service")
        
        # Start monitoring loop
        asyncio.create_task(self._monitoring_loop())
    
    async def stop_monitoring(self) -> None:
        """Stop job monitoring"""
        self.monitoring_active = False
        logger.info("Stopped job monitoring service")
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                await self._scan_for_jobs()
                await asyncio.sleep(self.monitoring_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def _scan_for_jobs(self) -> None:
        """Scan for new job opportunities"""
        try:
            # Get all active users with job search enabled
            active_users = await self._get_active_users()
            
            logger.info(f"Scanning jobs for {len(active_users)} active users")
            
            for user in active_users:
                try:
                    await self._scan_jobs_for_user(user)
                except Exception as e:
                    logger.error(f"Failed to scan jobs for user {user['id']}: {e}")
            
        except Exception as e:
            logger.error(f"Failed to scan for jobs: {e}")
    
    async def _scan_jobs_for_user(self, user: Dict) -> None:
        """Scan for jobs for a specific user"""
        try:
            user_id = user["id"]
            preferences = user.get("preferences", {})
            
            # Skip if user was scanned recently
            if self._was_recently_scanned(user_id):
                return
            
            # Use Job Discovery Agent to find opportunities
            from ..agents.job_discovery_agent import JobDiscoveryAgent
            job_agent = JobDiscoveryAgent()
            
            # Monitor job boards
            discovered_jobs = await job_agent.monitor_job_boards(preferences)
            
            # Filter and score jobs
            relevant_jobs = []
            for job in discovered_jobs:
                # Skip if we've already notified about this job
                if await self._job_already_notified(user_id, job["id"]):
                    continue
                
                # Calculate match score
                match_score = await job_agent.calculate_job_match_score(user_id, job)
                
                # Only consider jobs above minimum threshold
                min_score = preferences.get("min_match_score", 0.6)
                if match_score >= min_score:
                    job["match_score"] = match_score
                    relevant_jobs.append(job)
            
            # Sort by match score (highest first)
            relevant_jobs.sort(key=lambda x: x["match_score"], reverse=True)
            
            # Limit notifications per scan to avoid spam
            max_notifications = preferences.get("max_notifications_per_scan", 3)
            relevant_jobs = relevant_jobs[:max_notifications]
            
            # Send notifications for relevant jobs
            for job in relevant_jobs:
                await self._send_job_notification(user_id, job)
            
            # Update last scan time
            self.last_scan_time[user_id] = datetime.now()
            
            logger.info(f"Found {len(relevant_jobs)} relevant jobs for user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to scan jobs for user {user['id']}: {e}")
    
    async def _get_active_users(self) -> List[Dict]:
        """Get list of users with active job monitoring"""
        try:
            # This would query the database for users with:
            # - Active account
            # - Job monitoring enabled
            # - Valid preferences set
            
            # For now, return empty list as placeholder
            # In real implementation, this would be:
            # return await user_service.get_active_job_seekers()
            
            return []
            
        except Exception as e:
            logger.error(f"Failed to get active users: {e}")
            return []
    
    def _was_recently_scanned(self, user_id: str) -> bool:
        """Check if user was scanned recently"""
        if user_id not in self.last_scan_time:
            return False
        
        last_scan = self.last_scan_time[user_id]
        time_since_scan = datetime.now() - last_scan
        
        # Don't scan same user more than once per hour
        return time_since_scan < timedelta(hours=1)
    
    async def _job_already_notified(self, user_id: str, job_id: str) -> bool:
        """Check if user was already notified about this job"""
        try:
            # This would check the database for existing notifications
            # For now, return False as placeholder
            return False
            
        except Exception as e:
            logger.error(f"Failed to check job notification history: {e}")
            return False
    
    async def _send_job_notification(self, user_id: str, job_data: Dict) -> None:
        """Send job opportunity notification to user"""
        try:
            from .notification_service import notification_service
            
            await notification_service.send_job_opportunity_notification(
                user_id=user_id,
                job_data=job_data,
                match_score=job_data["match_score"]
            )
            
            # Record that we notified about this job
            await self._record_job_notification(user_id, job_data["id"])
            
        except Exception as e:
            logger.error(f"Failed to send job notification: {e}")
    
    async def _record_job_notification(self, user_id: str, job_id: str) -> None:
        """Record that user was notified about a job"""
        try:
            # This would store in database to prevent duplicate notifications
            # For now, just log
            logger.info(f"Recorded job notification: user {user_id}, job {job_id}")
            
        except Exception as e:
            logger.error(f"Failed to record job notification: {e}")
    
    async def enable_monitoring_for_user(self, user_id: str, preferences: Dict) -> bool:
        """Enable job monitoring for a specific user"""
        try:
            # This would update user preferences in database
            # For now, just log
            logger.info(f"Enabled job monitoring for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enable monitoring for user {user_id}: {e}")
            return False
    
    async def disable_monitoring_for_user(self, user_id: str) -> bool:
        """Disable job monitoring for a specific user"""
        try:
            # This would update user preferences in database
            # For now, just log
            logger.info(f"Disabled job monitoring for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disable monitoring for user {user_id}: {e}")
            return False
    
    async def update_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update job monitoring preferences for a user"""
        try:
            # This would update preferences in database
            # For now, just log
            logger.info(f"Updated preferences for user {user_id}: {preferences}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update preferences for user {user_id}: {e}")
            return False
    
    def get_monitoring_stats(self) -> Dict:
        """Get monitoring service statistics"""
        return {
            "monitoring_active": self.monitoring_active,
            "monitoring_interval": self.monitoring_interval,
            "users_tracked": len(self.last_scan_time),
            "last_scan_times": {
                user_id: scan_time.isoformat() 
                for user_id, scan_time in self.last_scan_time.items()
            }
        }


# Global service instance
job_monitoring_service = JobMonitoringService()