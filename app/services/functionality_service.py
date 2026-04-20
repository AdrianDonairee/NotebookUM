from app.models.functionality_model import (
    Functionality,
    FunctionalityCreate,
    FunctionalityUpdate,
)


class FunctionalityService:
    """In-memory CRUD for project functionalities."""

    def __init__(self):
        self._items: list[Functionality] = []
        self._next_id = 1

    def get_all(self) -> list[dict]:
        return [item.model_dump() for item in self._items]

    def get_by_id(self, functionality_id: int) -> dict | None:
        item = self._find_by_id(functionality_id)
        return item.model_dump() if item else None

    def create(self, payload: FunctionalityCreate) -> dict:
        new_item = Functionality(id=self._next_id, **payload.model_dump())
        self._items.append(new_item)
        self._next_id += 1
        return new_item.model_dump()

    def update(self, functionality_id: int, payload: FunctionalityUpdate) -> dict | None:
        item = self._find_by_id(functionality_id)
        if item is None:
            return None

        data = payload.model_dump(exclude_unset=True)
        if "name" in data:
            item.name = data["name"]
        if "description" in data:
            item.description = data["description"]

        return item.model_dump()

    def delete(self, functionality_id: int) -> bool:
        item = self._find_by_id(functionality_id)
        if item is None:
            return False

        self._items.remove(item)
        return True

    def _find_by_id(self, functionality_id: int) -> Functionality | None:
        for item in self._items:
            if item.id == functionality_id:
                return item
        return None
