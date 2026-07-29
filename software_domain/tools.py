from __future__ import annotations

from dataclasses import dataclass

from v1_core.models import CostKind


@dataclass(frozen=True)
class SoftwareTool:
    id: str
    command: tuple[str, ...]
    purpose: str
    cost_kind: CostKind
    network_access: bool
    mutates_repository: bool


LOCAL_SOFTWARE_TOOLS: dict[str, SoftwareTool] = {
    "python-unittest": SoftwareTool(
        id="python-unittest",
        command=("python", "-m", "unittest", "discover", "-s", "tests", "-v"),
        purpose="Run the repository's Python tests.",
        cost_kind=CostKind.LOCAL_FREE,
        network_access=False,
        mutates_repository=False,
    ),
    "python-compile": SoftwareTool(
        id="python-compile",
        command=("python", "-m", "compileall", "-q", "v1_core", "software_domain"),
        purpose="Check that Python modules compile.",
        cost_kind=CostKind.LOCAL_FREE,
        network_access=False,
        mutates_repository=False,
    ),
    "rg": SoftwareTool(
        id="rg",
        command=("rg",),
        purpose="Search source and canonical documents locally.",
        cost_kind=CostKind.LOCAL_FREE,
        network_access=False,
        mutates_repository=False,
    ),
    "git-diff": SoftwareTool(
        id="git-diff",
        command=("git", "diff", "--check"),
        purpose="Inspect local changes and whitespace errors.",
        cost_kind=CostKind.LOCAL_FREE,
        network_access=False,
        mutates_repository=False,
    ),
}
