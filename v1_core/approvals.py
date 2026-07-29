from .models import ApprovalRecord


FORMAL_CHANNEL = "chatgpt"


def has_formal_approval(
    request_id: str, scope: str, records: list[ApprovalRecord]
) -> bool:
    return any(
        record.request_id == request_id
        and record.scope == scope
        and record.channel.lower() == FORMAL_CHANNEL
        and record.approved
        for record in records
    )
