from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SoftwareWorkKind(str, Enum):
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    REVIEW = "review"
    DOCUMENTATION = "documentation"


@dataclass(frozen=True)
class SoftwareCapability:
    id: str
    agent_role: str
    work_kinds: tuple[SoftwareWorkKind, ...]
    required_tools: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class SoftwareTask:
    objective: str
    constraints: tuple[str, ...]
    work_kinds: tuple[SoftwareWorkKind, ...]
    required_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class SoftwareSelection:
    agent_role: str
    environment: str
    capability_ids: tuple[str, ...]
    tool_ids: tuple[str, ...]
