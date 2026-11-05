"""
Email Category Entity Model
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class EmailCategory:
    id: Optional[int] = None
    name: str = ""
    color: str = "#3b82f6"
    description: Optional[str] = None
    icon: str = "mail"
    is_system: bool = True
    created_at: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            color=data.get("color", "#3b82f6"),
            description=data.get("description"),
            icon=data.get("icon", "mail"),
            is_system=bool(data.get("is_system", 1)),
            created_at=str(data.get("created_at")) if data.get("created_at") else None,
        )
