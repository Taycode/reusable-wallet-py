class EntityNotFound(BaseException):
    def __init__(self, entity: str):
        message = f"{entity} entity not found"
        super().__init__(message)
