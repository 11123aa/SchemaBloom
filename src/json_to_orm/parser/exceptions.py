"""
Исключения для модуля парсинга JSON-схем.
"""


class JSONParseError(Exception):
    """Исключение, возникающее при ошибке парсинга JSON."""
    
    def __init__(self, message: str, line: int = None, column: int = None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.message)


class SchemaValidationError(Exception):
    """Исключение, возникающее при ошибке валидации схемы."""
    
    def __init__(self, message: str, field: str = None, value: any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)


class InvalidFieldTypeError(SchemaValidationError):
    """Исключение, возникающее при невалидном типе поля."""
    
    def __init__(self, field_name: str, field_type: str, valid_types: list = None):
        self.field_name = field_name
        self.field_type = field_type
        self.valid_types = valid_types or []
        
        message = f"Invalid field type '{field_type}' for field '{field_name}'"
        if self.valid_types:
            message += f". Valid types: {', '.join(self.valid_types)}"
        
        super().__init__(message, field=field_name, value=field_type)


class InvalidRelationshipError(SchemaValidationError):
    """Исключение, возникающее при невалидной связи между таблицами."""
    
    def __init__(self, relationship: dict, reason: str):
        self.relationship = relationship
        self.reason = reason
        
        message = f"Invalid relationship: {reason}. Relationship: {relationship}"
        super().__init__(message, field="relationship", value=relationship)


class DuplicateTableError(SchemaValidationError):
    """Исключение, возникающее при дублировании имени таблицы."""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        
        message = f"Duplicate table name: '{table_name}'"
        super().__init__(message, field="table_name", value=table_name)


class DuplicateFieldError(SchemaValidationError):
    """Исключение, возникающее при дублировании имени поля в таблице."""
    
    def __init__(self, table_name: str, field_name: str):
        self.table_name = table_name
        self.field_name = field_name
        
        message = f"Duplicate field name '{field_name}' in table '{table_name}'"
        super().__init__(message, field=field_name, value=field_name)


class MissingRequiredFieldError(SchemaValidationError):
    """Исключение, возникающее при отсутствии обязательного поля."""
    
    def __init__(self, field_name: str, context: str = None):
        self.field_name = field_name
        self.context = context
        
        message = f"Missing required field: '{field_name}'"
        if context:
            message += f" in {context}"
        
        super().__init__(message, field=field_name)


class InvalidConstraintError(SchemaValidationError):
    """Исключение, возникающее при невалидном ограничении поля."""
    
    def __init__(self, field_name: str, constraint: str, reason: str):
        self.field_name = field_name
        self.constraint = constraint
        self.reason = reason
        
        message = f"Invalid constraint '{constraint}' for field '{field_name}': {reason}"
        super().__init__(message, field=field_name, value=constraint) 