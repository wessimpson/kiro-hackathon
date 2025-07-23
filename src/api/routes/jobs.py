"""
Job API Routes for AI Job Application Assistant
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ...services.job_monitoring_service import job_monitoring_service

router = APIRouter()


class JobPreferences(BaseModel):
    preferred_locations: List[str] = []
    preferred_job_types: List[str] = []
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    remote_work_preference: str = "FLEXIBLE"  # REMOTE_ONLY, HYBRID, ON_SITE, FLEXIBLE
    min_match_score: float = 0.6
    max_notifications_per_scan: int = 3
    keywords: List[str] = []
    excluded_companies: List[str] = []


class MonitoringStatusResponse(BaseModel):
    monitoring_enabled: bool
    last_scan: Optional[datetime] = None
    preferences: Optional[JobPreferences] = None


@router.post("/monitoring/enable")
async def enable_job_monitoring(
    preferences: JobPreferences,
    user_id: str = Query(..., description="User ID")
):
    """Enable job monitoring for a user"""
    try:
        success = await job_monitoring_service.enable_monitoring_for_user(
            user_id=user_id,
            preferences=preferences.dict()
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to enable monitoring")
        
        return {
            "success": True,
            "message": "Job monitoring enabled",
            "preferences": preferences
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/monitoring/disable")
async def disable_job_monitoring(
    user_id: str = Query(..., description="User ID")
):
    """Disable job monitoring for a user"""
    try:
        success = await job_monitoring_service.disable_monitoring_for_user(user_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to disable monitoring")
        
        return {
            "success": True,
            "message": "Job monitoring disabled"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/status", response_model=MonitoringStatusResponse)
async def get_monitoring_status(
    user_id: str = Query(..., description="User ID")
):
    """Get job monitoring status for a user"""
    try:
        # This would query the database for user's monitoring status
        # For now, return a placeholder response
        return MonitoringStatusResponse(
            monitoring_enabled=True,
            last_scan=datetime.now(),
            preferences=JobPreferences()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/monitoring/preferences")
async def update_monitoring_preferences(
    preferences: JobPreferences,
    user_id: str = Query(..., description="User ID")
):
    """Update job monitoring preferences"""
    try:
        success = await job_monitoring_service.update_user_preferences(
            user_id=user_id,
            preferences=preferences.dict()
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update preferences")
        
        return {
            "success": True,
            "message": "Preferences updated",
            "preferences": preferences
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/stats")
async def get_monitoring_stats():
    """Get job monitoring service statistics (admin endpoint)"""
    try:
        stats = job_monitoring_service.get_monitoring_stats()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))