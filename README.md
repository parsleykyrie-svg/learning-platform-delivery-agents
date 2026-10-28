# Learning Platform Delivery Agents

A Claude Code workspace for planning, implementing, testing and reviewing learning-platform features. Four specialist agents coordinate through versioned feature documents and explicit review stages.

## Agents and commands

| Agent | Responsibility | Command |
| --- | --- | --- |
| Architect | Define the goal, acceptance criteria, affected files, risks and test approach | `/plan` |
| Developer | Implement an approved plan and run the configured checks | `/build` |
| Tester | Verify acceptance criteria and record evidence independently of implementation | `/test` |
| Reviewer | Review the implementation and test evidence before release | `/review` |

`/ship` coordinates the stages with operator approval. `/status` reports feature progress.

## Use

1. Open this repository in Claude Code, alongside the application you are working on.
2. Set `source_directory` and explicit check commands in `project.json`. Paths are resolved relative to this repository. At least one check is required before a verification gate can pass.
3. Run `/plan <feature request>`, review the plan, then continue with `/build <feature-slug>`.
4. Run `/test` and `/review` to collect independent evidence. No command automatically deploys an application.

Feature documents move through `features/planned/`, `built/`, `tested/` and `done/`. The learning context emphasises accessible interfaces, accurate educational material and consistent assessment behaviour. This repository supplies the delivery workflow, not a learning application or a claim of education-sector client employment.

## Scripts

Requires Python 3.10+; no Python packages are needed.

```sh
python3 scripts/feature_status.py
python3 scripts/feature_status.py --json
python3 scripts/run_checks.py
python3 -m unittest discover -s tests -v
```

The check runner executes only the argument arrays configured by the repository operator, without a shell. It fails on empty checks, an invalid source directory, a failed command or a timeout. Review `project.json` before running it.

## Implementation and provenance

The agent responsibilities, staged feature handoffs and verification procedure are adapted from an existing application-delivery workflow. This public version removes project-specific dependencies and provides portable configuration and scripts. It uses AI-assisted development and requires the operator's review; separate agent roles do not by themselves establish correctness.
