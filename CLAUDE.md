# Learning Platform Delivery Agents

Read `project.json` to locate the target application and `context/learning-platform.md` for domain requirements. Inspect the actual target code before planning. Never assume a framework, test suite, deployed feature or available tool.

The workflow is `/plan` → operator approval → `/build` → `/test` → `/review`. A failed stage returns to implementation. The operator decides whether and where to release the change; do not deploy from this workspace.

Each feature uses one Markdown tracker. Its directory records its current stage. Read `features/TEMPLATE.md` for the format. Keep evidence attached to the feature, including command exit status and any unverified behaviour. Do not mark a stage complete merely because an agent says it passed.

Run `python3 scripts/run_checks.py` for configured application checks. An empty configuration is a failure, not a skipped success. Use an available browser tool when acceptance criteria require visual or interactive verification; report a verification limit when unavailable.

Keep credentials, learner records and production data out of trackers and commits. Preserve source attribution for learning content. Do not describe a prototype or specification as deployed functionality.
