"""Software-specific capabilities injected into the domain-neutral V1 core."""

from .evaluation import SoftwareEvaluation, evaluate_software_result
from .pack import SoftwareDomainPack
from .tools import LOCAL_SOFTWARE_TOOLS, SoftwareTool

__all__ = [
    "LOCAL_SOFTWARE_TOOLS",
    "SoftwareDomainPack",
    "SoftwareEvaluation",
    "SoftwareTool",
    "evaluate_software_result",
]
