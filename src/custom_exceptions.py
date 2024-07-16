class EntityNotFoundError(Exception):
    def __init__(self, entity_name: str, entity_id: int):
        super().__init__(f"{entity_name} with ID {entity_id} does not exist")
        self.entity_name = entity_name
        self.entity_id = entity_id
