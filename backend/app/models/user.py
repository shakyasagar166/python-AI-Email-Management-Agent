"""
User Entity Model
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class User:
    id: Optional[int] = None
    email: str = ""
    password_hash: str = ""
    full_name: str = ""
    avatar_url: Optional[str] = None
    role: str = "User"
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self):
        d = asdict(self)
        d.pop("password_hash", None)
        return d

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            email=data.get("email", ""),
            password_hash=data.get("password_hash", ""),
            full_name=data.get("full_name", ""),
            avatar_url=data.get("avatar_url"),
            role=data.get("role", "User"),
            is_active=bool(data.get("is_active", 1)),
            created_at=str(data.get("created_at")) if data.get("created_at") else None,
            updated_at=str(data.get("updated_at")) if data.get("updated_at") else None,
        )
