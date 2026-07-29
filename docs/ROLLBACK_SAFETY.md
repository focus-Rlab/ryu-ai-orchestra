# Rollback safety boundary

V1 rollback reverses only side effects with an explicitly registered handler.

- Handler failure becomes `rollback_failed`; success is not claimed.
- A produced result without a handler is rejected.
- A completed rollback cannot run twice.
- Simulated/reserved budget is restored only after handler success.
- Real external charges are irreversible and are not erased by rollback.
- Multi-step compensation and durable crash recovery remain future work.
