from .models import ApprovalRecord


FORMAL_CHANNELS = frozenset(
    {"chatgpt", "gemini", "claude", "codex", "claude-code"}
)
FORMAL_APPROVERS = frozenset(
    {"ryunosuke matsumoto", "松本隆之介", "隆之介"}
)


def _normalize_channel(channel: str) -> str:
    return channel.strip().lower().replace("_", "-").replace(" ", "-")


def _normalize_approver(approver: str) -> str:
    return approver.strip().lower()


def has_formal_approval(
    request_id: str, scope: str, records: list[ApprovalRecord]
) -> bool:
    return any(
        record.request_id == request_id
        and record.scope == scope
        and _normalize_channel(record.channel) in FORMAL_CHANNELS
        and _normalize_approver(record.approver) in FORMAL_APPROVERS
        and record.approved
        for record in records
    )
