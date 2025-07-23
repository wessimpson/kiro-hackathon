"""
Notification API Routes for AI Job Application Assistant
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ...services.notification_service import notification_service
from ...services.application_workflow_service import application_workflow_service

router = APIRouter()


class NotificationResponse(BaseModel):
    id: str
    type: str
    title: str
    message: str
    priority: str
    created_at: datetime
    read: bool = False
    data: dict = {}


class NotificationActionRequest(BaseModel):
    action_id: str


class ApplicationApprovalRequest(BaseModel):
    refinements: Optional[dict] = None


@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    user_id: str = Query(..., description="User ID"),
    limit: int = Query(50, description="Maximum number of notifications"),
    unread_only: bool = Query(False, description="Only return unread notifications")
):
    """Get user notifications"""
    try:
        notifications = await notification_service.get_user_notifications(
            user_id=user_id,
            limit=limit,
            unread_only=unread_only
        )
        
        return [NotificationResponse(**notif) for notif in notifications]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    user_id: str = Query(..., description="User ID")
):
    """Mark notification as read"""
    try:
        success = await notification_service.mark_notification_read(
            notification_id=notification_id,
            user_id=user_id
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return {"success": True, "message": "Notification marked as read"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{notification_id}/action")
async def handle_notification_action(
    notification_id: str,
    request: NotificationActionRequest,
    user_id: str = Query(..., description="User ID")
):
    """Handle user action on notification"""
    try:
        result = await notification_service.handle_notification_action(
            notification_id=notification_id,
            action_id=request.action_id,
            user_id=user_id
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflows/{workflow_id}/status")
async def get_workflow_status(
    workflow_id: str,
    user_id: str = Query(..., description="User ID")
):
    """Get application workflow status"""
    try:
        status = await application_workflow_service.get_workflow_status(
            workflow_id=workflow_id,
            user_id=user_id
        )
        
        return status
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/{workflow_id}/approve")
async def approve_application(
    workflow_id: str,
    request: ApplicationApprovalRequest,
    user_id: str = Query(..., description="User ID")
):
    """Approve application for submission"""
    try:
        result = await application_workflow_service.approve_application_for_submission(
            workflow_id=workflow_id,
            user_id=user_id,
            refinements=request.refinements
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/workflows/{workflow_id}")
async def cancel_workflow(
    workflow_id: str,
    user_id: str = Query(..., description="User ID")
):
    """Cancel an active workflow"""
    try:
        success = await application_workflow_service.cancel_workflow(
            workflow_id=workflow_id,
            user_id=user_id
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to cancel workflow")
        
        return {"success": True, "message": "Workflow cancelled"}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))