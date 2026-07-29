# Week 2 Software self-improvement case

## Purpose

Use Raphael's domain-neutral V1 core with an injected Software domain pack,
without adding software-specific logic to `v1_core`.

## Baseline

After Week 1, `v1_core.Orchestrator` could execute injected callbacks, but the
repository had no software-specific definitions for:

- classifying software work;
- selecting development capabilities;
- selecting safe local development tools;
- evaluating software evidence.

An application could manually supply arbitrary callbacks, but Raphael could not
derive a software capability set from a software request.

## Change

`software_domain` now supplies:

- software work classification;
- a capability registry;
- local-free tool connection definitions;
- a callback adapter for the generic core;
- a Week 2 invariant-based evaluation pack.

The first case is this change itself: improve Raphael so that it can select and
verify software capabilities while leaving the generic core unchanged.

## Comparison

| Requirement | Before | After |
|---|---|---|
| Software work classification | Caller-defined only | Domain pack classifies review, implementation, testing, and documentation |
| Capability selection | No software registry | Minimum matching capability set is selected |
| Tool safety metadata | Not defined for software | Cost, network, mutation, and purpose are explicit |
| Software verification | Generic `passed` callback only | Week 2 invariants produce named checks and evidence |
| Generic-core isolation | Software callbacks possible, not demonstrated | Tested with `v1_core` unchanged |

## Evidence and limits

- Only Python's standard library and existing local commands are used.
- No paid, billable, cost-uncertain, or external API was introduced or run.
- The pack selects definitions; it does not yet launch Codex, Claude Code, or
  other AI environments automatically.
- The evaluation uses only Issue #13's Week 2 completion invariants. The
  unapproved weighted criteria recorded in `INCIDENT_LOG.md` remain unused.
- Main merge remains Ryunosuke's decision.
