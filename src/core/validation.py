"""
Validation utilities for AI Job Application Assistant

Provides comprehensive validation functions for all agent communications and data structures.
"""
from typing import Dict, Any, List, Optional, Type, Union
from pydantic import BaseModel, ValidationError
from datetime import datetime
import re

from .exceptions import ValidationException, SkillVerificationException
from ..models.knowledge_graph import SkillNode, ExperienceNode, ProjectNode


def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    return bool(re.match(pattern, url))


def validate_linkedin_url(url: str) -> bool:
    """Validate LinkedIn profile URL"""
    pattern = r'^https?://(www\.)?linkedin\.com/in/[\w-]+/?$'
    return bool(re.match(pattern, url))


def validate_github_url(url: str) -> bool:
    """Validate GitHub profile URL"""
    pattern = r'^https?://(www\.)?github\.com/[\w-]+/?$'
    return bool(re.match(pattern, url))


def validate_skill_verification(skill: SkillNode, experiences: List[ExperienceNode], projects: List[ProjectNode]) -> bool:
    """
    Validate that a verified skill has supporting evidence from experiences or projects
    
    Args:
        skill: The skill node to validate
        experiences: List of user's experience nodes
        projects: List of user's project nodes
    
    Returns:
        bool: True if skill verification is valid
    
    Raises:
        SkillVerificationException: If verified skill lacks supporting evidence
    """
    if not skill.verified:
        return True  # Unverified skills don't need validation
    
    # Check if skill is mentioned in any experience
    skill_in_experience = False
    for exp in experiences:
        if (skill.name.lower() in exp.description.lower() or 
            any(skill.name.lower() in achievement.lower() for achievement in exp.achievements)):
            skill_in_experience = True
            break
    
    # Check if skill is mentioned in any project
    skill_in_project = False
    for project in projects:
        if (skill.name.lower() in project.description.lower() or
            any(skill.name.lower() in tech.lower() for tech in project.technologies)):
            skill_in_project = True
            break
    
    # Verified skill must have supporting evidence
    if not (skill_in_experience or skill_in_project):
        raise SkillVerificationException(
            skill_name=skill.name,
            user_id=skill.id,  # Assuming skill has user context
            reason="Verified skill must be supported by experience or project evidence"
        )
    
    return True


def validate_date_range(start_date: datetime, end_date: Optional[datetime] = None) -> bool:
    """Validate that end date is after start date"""
    if end_date and start_date and end_date < start_date:
        return False
    return True


def validate_salary_range(min_salary: Optional[int], max_salary: Optional[int]) -> bool:
    """Validate that max salary is greater than min salary"""
    if min_salary and max_salary and max_salary < min_salary:
        return False
    return True


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """
    Validate that all required fields are present and not None
    
    Returns:
        List of missing field names
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    return missing_fields


def validate_field_types(data: Dict[str, Any], field_types: Dict[str, Type]) -> List[str]:
    """
    Validate that fields have correct types
    
    Returns:
        List of fields with incorrect types
    """
    type_errors = []
    for field, expected_type in field_types.items():
        if field in data and data[field] is not None:
            if not isinstance(data[field], expected_type):
                type_errors.append(f"{field}: expected {expected_type.__name__}, got {type(data[field]).__name__}")
    return type_errors


def validate_string_length(value: str, min_length: int = None, max_length: int = None) -> bool:
    """Validate string length constraints"""
    if min_length and len(value) < min_length:
        return False
    if max_length and len(value) > max_length:
        return False
    return True


def validate_list_constraints(value: List[Any], min_items: int = None, max_items: int = None) -> bool:
    """Validate list length constraints"""
    if min_items and len(value) < min_items:
        return False
    if max_items and len(value) > max_items:
        return False
    return True


def validate_numeric_range(value: Union[int, float], min_value: Union[int, float] = None, max_value: Union[int, float] = None) -> bool:
    """Validate numeric value constraints"""
    if min_value is not None and value < min_value:
        return False
    if max_value is not None and value > max_value:
        return False
    return True


def validate_pydantic_model(model_class: Type[BaseModel], data: Dict[str, Any], context: str = None) -> BaseModel:
    """
    Validate data against Pydantic model with comprehensive error handling
    
    Args:
        model_class: Pydantic model class to validate against
        data: Data dictionary to validate
        context: Context for error messages
    
    Returns:
        Validated Pydantic model instance
    
    Raises:
        ValidationException: If validation fails
    """
    try:
        return model_class.parse_obj(data)
    except ValidationError as e:
        raise ValidationException(e, context or f"{model_class.__name__} validation")


def validate_agent_input(agent_name: str, operation: str, input_data: Dict[str, Any], required_fields: List[str]) -> None:
    """
    Validate input data for CrewAI agent operations
    
    Args:
        agent_name: Name of the agent
        operation: Operation being performed
        input_data: Input data to validate
        required_fields: List of required field names
    
    Raises:
        ValidationException: If validation fails
    """
    context = f"{agent_name} - {operation}"
    
    # Check required fields
    missing_fields = validate_required_fields(input_data, required_fields)
    if missing_fields:
        raise ValidationException(
            ValidationError([
                {
                    "loc": (field,),
                    "msg": "field required",
                    "type": "value_error.missing",
                    "input": input_data.get(field)
                }
                for field in missing_fields
            ], model=dict),
            context=context
        )


def validate_agent_output(agent_name: str, operation: str, output_data: Any, expected_type: Type) -> None:
    """
    Validate output data from CrewAI agent operations
    
    Args:
        agent_name: Name of the agent
        operation: Operation that was performed
        output_data: Output data to validate
        expected_type: Expected type of output data
    
    Raises:
        ValidationException: If validation fails
    """
    context = f"{agent_name} - {operation} output"
    
    if not isinstance(output_data, expected_type):
        raise ValidationException(
            ValidationError([
                {
                    "loc": ("output",),
                    "msg": f"expected {expected_type.__name__}, got {type(output_data).__name__}",
                    "type": "type_error",
                    "input": output_data
                }
            ], model=dict),
            context=context
        )


def validate_knowledge_graph_data(node_type: str, node_data: Dict[str, Any]) -> None:
    """
    Validate data before inserting into knowledge graph
    
    Args:
        node_type: Type of node (USER, SKILL, EXPERIENCE, etc.)
        node_data: Node data to validate
    
    Raises:
        ValidationException: If validation fails
    """
    context = f"Knowledge Graph - {node_type} node"
    
    # Common required fields for all nodes
    common_required = ["id", "type"]
    missing_common = validate_required_fields(node_data, common_required)
    
    if missing_common:
        raise ValidationException(
            ValidationError([
                {
                    "loc": (field,),
                    "msg": "field required for knowledge graph node",
                    "type": "value_error.missing",
                    "input": node_data.get(field)
                }
                for field in missing_common
            ], model=dict),
            context=context
        )
    
    # Validate node type matches expected
    if node_data.get("type") != node_type:
        raise ValidationException(
            ValidationError([
                {
                    "loc": ("type",),
                    "msg": f"expected node type '{node_type}', got '{node_data.get('type')}'",
                    "type": "value_error.mismatch",
                    "input": node_data.get("type")
                }
            ], model=dict),
            context=context
        )


class ValidationContext:
    """Context manager for validation operations with detailed error tracking"""
    
    def __init__(self, operation: str, agent_name: str = None):
        self.operation = operation
        self.agent_name = agent_name
        self.errors = []
        self.warnings = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValidationError:
            # Convert to our custom exception
            context = f"{self.agent_name} - {self.operation}" if self.agent_name else self.operation
            raise ValidationException(exc_val, context)
        return False
    
    def add_error(self, field: str, message: str, value: Any = None):
        """Add a validation error"""
        self.errors.append({
            "field": field,
            "message": message,
            "value": value
        })
    
    def add_warning(self, field: str, message: str, value: Any = None):
        """Add a validation warning"""
        self.warnings.append({
            "field": field,
            "message": message,
            "value": value
        })
    
    def has_errors(self) -> bool:
        """Check if there are any validation errors"""
        return len(self.errors) > 0
    
    def raise_if_errors(self):
        """Raise ValidationException if there are any errors"""
        if self.has_errors():
            context = f"{self.agent_name} - {self.operation}" if self.agent_name else self.operation
            validation_errors = [
                {
                    "loc": (error["field"],),
                    "msg": error["message"],
                    "type": "value_error",
                    "input": error["value"]
                }
                for error in self.errors
            ]
            raise ValidationException(ValidationError(validation_errors, model=dict), context)