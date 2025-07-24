"""
Custom exceptions for AI Job Application Assistant

Provides comprehensive error handling for all agent communications and data validation.
"""
from typing import Dict, Any, List, Optional
from pydantic import ValidationError


class BaseJobAssistantException(Exception):
    """Base exception for all AI Job Application Assistant errors"""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses"""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }


class ValidationException(BaseJobAssistantException):
    """Exception for Pydantic validation errors"""
    
    def __init__(self, validation_error: ValidationError, context: str = None):
        self.validation_error = validation_error
        self.context = context or "Data validation"
        
        # Extract field-specific errors
        field_errors = []
        for error in validation_error.errors():
            field_path = " -> ".join(str(loc) for loc in error["loc"])
            field_errors.append({
                "field": field_path,
                "message": error["msg"],
                "type": error["type"],
                "input": error.get("input")
            })
        
        message = f"{self.context} failed: {len(field_errors)} validation error(s)"
        details = {
            "field_errors": field_errors,
            "error_count": len(field_errors)
        }
        
        super().__init__(message, "VALIDATION_ERROR", details)


class AgentCommunicationException(BaseJobAssistantException):
    """Exception for errors in CrewAI agent communications"""
    
    def __init__(self, agent_name: str, operation: str, message: str, details: Dict[str, Any] = None):
        self.agent_name = agent_name
        self.operation = operation
        
        full_message = f"Agent '{agent_name}' failed during '{operation}': {message}"
        error_details = {
            "agent_name": agent_name,
            "operation": operation,
            **(details or {})
        }
        
        super().__init__(full_message, "AGENT_COMMUNICATION_ERROR", error_details)


class KnowledgeGraphException(BaseJobAssistantException):
    """Exception for Neo4j knowledge graph operations"""
    
    def __init__(self, operation: str, message: str, query: str = None, parameters: Dict[str, Any] = None):
        self.operation = operation
        self.query = query
        self.parameters = parameters
        
        full_message = f"Knowledge graph operation '{operation}' failed: {message}"
        details = {
            "operation": operation,
            "query": query,
            "parameters": parameters
        }
        
        super().__init__(full_message, "KNOWLEDGE_GRAPH_ERROR", details)


class DatabaseConnectionException(BaseJobAssistantException):
    """Exception for database connection issues"""
    
    def __init__(self, database_type: str, connection_string: str = None, original_error: Exception = None):
        self.database_type = database_type
        self.connection_string = connection_string
        self.original_error = original_error
        
        message = f"Failed to connect to {database_type} database"
        details = {
            "database_type": database_type,
            "connection_string": connection_string,
            "original_error": str(original_error) if original_error else None
        }
        
        super().__init__(message, "DATABASE_CONNECTION_ERROR", details)


class ExternalAPIException(BaseJobAssistantException):
    """Exception for external API communication errors"""
    
    def __init__(self, api_name: str, endpoint: str, status_code: int = None, response_data: Any = None):
        self.api_name = api_name
        self.endpoint = endpoint
        self.status_code = status_code
        self.response_data = response_data
        
        message = f"External API '{api_name}' request to '{endpoint}' failed"
        if status_code:
            message += f" with status code {status_code}"
        
        details = {
            "api_name": api_name,
            "endpoint": endpoint,
            "status_code": status_code,
            "response_data": response_data
        }
        
        super().__init__(message, "EXTERNAL_API_ERROR", details)


class SkillVerificationException(BaseJobAssistantException):
    """Exception for skill verification failures"""
    
    def __init__(self, skill_name: str, user_id: str, reason: str):
        self.skill_name = skill_name
        self.user_id = user_id
        self.reason = reason
        
        message = f"Skill verification failed for '{skill_name}' (user: {user_id}): {reason}"
        details = {
            "skill_name": skill_name,
            "user_id": user_id,
            "reason": reason
        }
        
        super().__init__(message, "SKILL_VERIFICATION_ERROR", details)


class DocumentProcessingException(BaseJobAssistantException):
    """Exception for document processing errors"""
    
    def __init__(self, document_type: str, file_path: str = None, processing_stage: str = None, original_error: Exception = None):
        self.document_type = document_type
        self.file_path = file_path
        self.processing_stage = processing_stage
        self.original_error = original_error
        
        message = f"Document processing failed for {document_type}"
        if processing_stage:
            message += f" during {processing_stage}"
        
        details = {
            "document_type": document_type,
            "file_path": file_path,
            "processing_stage": processing_stage,
            "original_error": str(original_error) if original_error else None
        }
        
        super().__init__(message, "DOCUMENT_PROCESSING_ERROR", details)


class ResumeGenerationException(BaseJobAssistantException):
    """Exception for resume generation failures"""
    
    def __init__(self, user_id: str, job_id: str, stage: str, reason: str):
        self.user_id = user_id
        self.job_id = job_id
        self.stage = stage
        self.reason = reason
        
        message = f"Resume generation failed at stage '{stage}' for user {user_id}, job {job_id}: {reason}"
        details = {
            "user_id": user_id,
            "job_id": job_id,
            "stage": stage,
            "reason": reason
        }
        
        super().__init__(message, "RESUME_GENERATION_ERROR", details)


class ATSScoringException(BaseJobAssistantException):
    """Exception for ATS scoring failures"""
    
    def __init__(self, resume_id: str, job_id: str, scoring_component: str, reason: str):
        self.resume_id = resume_id
        self.job_id = job_id
        self.scoring_component = scoring_component
        self.reason = reason
        
        message = f"ATS scoring failed for component '{scoring_component}' (resume: {resume_id}, job: {job_id}): {reason}"
        details = {
            "resume_id": resume_id,
            "job_id": job_id,
            "scoring_component": scoring_component,
            "reason": reason
        }
        
        super().__init__(message, "ATS_SCORING_ERROR", details)


class ConfigurationException(BaseJobAssistantException):
    """Exception for configuration errors"""
    
    def __init__(self, setting_name: str, reason: str, suggested_fix: str = None):
        self.setting_name = setting_name
        self.reason = reason
        self.suggested_fix = suggested_fix
        
        message = f"Configuration error for '{setting_name}': {reason}"
        details = {
            "setting_name": setting_name,
            "reason": reason,
            "suggested_fix": suggested_fix
        }
        
        super().__init__(message, "CONFIGURATION_ERROR", details)


# Utility functions for error handling
def handle_pydantic_validation_error(error: ValidationError, context: str = None) -> ValidationException:
    """Convert Pydantic ValidationError to custom ValidationException"""
    return ValidationException(error, context)


def handle_agent_error(agent_name: str, operation: str, original_error: Exception) -> AgentCommunicationException:
    """Convert generic exception to AgentCommunicationException"""
    return AgentCommunicationException(
        agent_name=agent_name,
        operation=operation,
        message=str(original_error),
        details={"original_error_type": type(original_error).__name__}
    )


def validate_required_fields(data: Dict[str, Any], required_fields: List[str], context: str = "Data") -> None:
    """Validate that required fields are present in data dictionary"""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        raise ValidationException(
            ValidationError([
                {
                    "loc": (field,),
                    "msg": "field required",
                    "type": "value_error.missing"
                }
                for field in missing_fields
            ], model=dict),
            context=context
        )


def safe_model_parse(model_class, data: Dict[str, Any], context: str = None) -> Any:
    """Safely parse data into Pydantic model with proper error handling"""
    try:
        return model_class.parse_obj(data)
    except ValidationError as e:
        raise handle_pydantic_validation_error(e, context or f"{model_class.__name__} parsing")
    except Exception as e:
        raise BaseJobAssistantException(
            message=f"Unexpected error parsing {model_class.__name__}: {str(e)}",
            error_code="PARSING_ERROR",
            details={"model_class": model_class.__name__, "data": data}
        )