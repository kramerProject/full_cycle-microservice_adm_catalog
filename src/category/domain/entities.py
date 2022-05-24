from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from __seedwork.domain.entities import Entity

@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(default_factory=lambda: datetime.now())


    def update(self, name: str, description: str):
        self._set('name', name)
        self._set('description', description)
        return f"Category name and description to {name} and {description} respectively"

    def activate(self):
        self._set('is_active', True)
        return f"Category {self.name} has been activated"

    def deactivate(self):
        self._set('is_active', False)
        return f"Category {self.name} has been deactivated"
        