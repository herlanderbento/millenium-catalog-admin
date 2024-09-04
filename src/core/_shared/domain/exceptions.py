class NotFoundException(Exception):
    def __init__(self, ids, entity_class):
        ids_message = (
            ",".join(map(str, ids)) if isinstance(ids, (list, tuple)) else str(ids)
        )
        message = f"{entity_class.__name__} Not Found using ID {ids_message}"
        super().__init__(message)
        self.name = "NotFoundException"
