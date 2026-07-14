# Tickets by Target — 1342 raw actions across 491 targets

Each action tagged by recency of the capture it came from. LIVE = last 3 weeks.


## Agent Workflow Builder  (95 actions, 0 live)

- [STALE 2026-04-03] Separate the workflow object model (nodes/schemas/UI definition) from any specific UI so it can embed in host apps like the support app
- [STALE 2026-04-03] Rebuild Agent Workflow Builder as a standalone application on AppyStack with unit tests
- [STALE 2026-04-03] Add autopilot with optional non-blocking nodes and refactor to work via API endpoints instead of the Claude harness
- [STALE 2026-04-02] Create and maintain an up-to-date README/index as AWB's documentation source of truth
- [STALE 2026-04-01] Set up a new repository for the AWB rebuild
- [STALE 2026-04-01] Draft requirements and spec for a new Agent Workflow Builder harness (plug-in + embedded-in-SupportSignal variants)
- [STALE 2026-04-01] Create a migration/startup plan for a new AWB built directly on a fresh AppyStack install
- [STALE 2026-03-31] Use Mythos beta access (if granted) to rebuild Agent Workflow Builder as a standalone project
- [STALE 2026-03-13] Update Angela feedback document to flag that the registry config file exists and needs her YAML path after first-install auto-seeding
- [STALE 2026-03-13] Run Playwright MCP against the live server on port 6040 to review all pages and propose look-and-feel fixes
- [STALE 2026-03-13] Re-implement the configurable git-ignored registry JSON with prepopulated Angela (Windows, no YLO) and David (Mac, with YLO) example files
- [STALE 2026-03-13] Make restart/error messages adaptive to source workflow and application (Signal Studio vs FliHub)
- [STALE 2026-03-13] Fix the W01 bug in parallel with the workflow-system improvement
- [STALE 2026-03-13] Document the improved workflow pattern for running W01 with human-in-loop stop points
- [STALE 2026-03-13] Design per-machine registry.json of workflow base folders, git-ignored with Angela and David example files
- [STALE 2026-03-12] Work through all input fields and fix their styling, adding a visual distinction for inputs that don't match template fields
- [STALE 2026-03-12] Validate incoming SRT data and confirm the correct SRT content field name
- [STALE 2026-03-12] Review the write-chapter-titles YAML/JSON schema and propose improvements including token usage display
- [STALE 2026-03-12] Rename the 'FliHub chatgpt' feature to 'video'
- [STALE 2026-03-12] Implement the FliHub chapter display and YAML/schema changes with unit tests and full test-suite verification
- [STALE 2026-03-12] Implement copy button near the pencil icon on the modal dialog
- [STALE 2026-03-12] Generate a discrepancy report across all workflow schemas, HBS files and templates, stepping workflow-to-workflow
- [STALE 2026-03-12] Fix DX/UX highlighter logic so the AI response persists when switching from engineer to pilot view
- [STALE 2026-03-12] Commit the code, clean up the data folder, and start an AWB instance
- [STALE 2026-03-12] Add copy-to-clipboard controls to the transcript modal and beside the edit pencil icon
- [STALE 2026-03-11] Use Playwright MCP to visually validate each UI change before considering it done
- [STALE 2026-03-11] Stop opening a new tab on resume since data populates the existing tab
- [STALE 2026-03-11] Restore DX/UX buttons as pure visual-highlighter toggles that no longer change state or hide the developer panel
- [STALE 2026-03-11] Redesign the data views (badge terminology, scrolling, table layout) iterating via Playwright MCP loaded with realistic data
- [STALE 2026-03-11] Implement the discussed label-clarity and developer-area font fixes
- [STALE 2026-03-11] Fix workflow resume so it returns to the saved step instead of an earlier one
- [STALE 2026-03-11] Action the approved design guidelines and top-toolbar hierarchy fixes, keeping them revertable
- [STALE 2026-03-10] Write chapter-generation prompt critique as a handover for the AWB system
- [STALE 2026-03-10] Verify origin and accuracy of screens.json feeding the rendered HTML
- [STALE 2026-03-10] Show template and schema file names with hover detail, open-folder and open-in-editor actions
- [STALE 2026-03-10] Show input/output schema in modal sidebar and rework hover-card truncation/scroll behavior
- [STALE 2026-03-10] Run backlog health check and remove irrelevant items
- [STALE 2026-03-10] Run background Playwright MCP task to check CR11
- [STALE 2026-03-10] Restore template/interpolated toggle, copy buttons, and schema display on the prompt template page
- [STALE 2026-03-10] Pause/kill the HTML screen generator to keep MVP focus
- [STALE 2026-03-10] Improve the refined-chapters HBS template per prompt-engineer review
- [STALE 2026-03-10] Get front-end designer UX/design opinion on the inputs/outputs screen
- [STALE 2026-03-10] Fix non-functional regenerate button and stuck spinner/continue state
- [STALE 2026-03-10] Document backlog best practices for David and Angela and enforce on both accounts
- [STALE 2026-03-10] Commit and push current changes
- [STALE 2026-03-10] Clean up the triage/backlog board, deleting low-value items
- [STALE 2026-03-10] Check load-from-AWB.json capability and required format; if missing, write prompt to add it
- [STALE 2026-03-10] Audit unit test coverage for the application schemas
- [STALE 2026-03-10] Add save button to transcript abridgment edit flow
- [STALE 2026-03-10] Add copy button to both prompt template and interpolated views
- [STALE 2026-03-09] Treat the edited final-video SRT as the authoritative transcript instead of concatenated partial files
- [STALE 2026-03-09] Search the SDK docs for tool-blocking settings/hooks and update the next round brief
- [STALE 2026-03-09] Run a deeper research task (GitHub repos + web) on analysis persistence patterns
- [STALE 2026-03-09] Reuse collapsed/expandable transcript display on the human review checkpoint screen
- [STALE 2026-03-09] Research existing JavaScript/GitHub layout-engine and component-composition libraries for wizard-step pages
- [STALE 2026-03-09] Rename 'Sent to AWB' label to just 'AWB'
- [STALE 2026-03-09] Refactor UAT into complete walkthrough specs and locate the per-memory UAT documents Playwright MCP must drive
- [STALE 2026-03-09] Make e2e tests run proactively on push (pre-push hook or CI trigger)
- [STALE 2026-03-09] Document the back-button/persistence problems and output-file locations in a findable place
- [STALE 2026-03-09] Design chat mode to explicitly target a designated field (AI-improve-this mode, schema-constrained)
- [STALE 2026-03-09] Delete obsolete b54 single-app UX prompt video; run C15-C25 through the workflow engine
- [STALE 2026-03-09] Compile the UX issues (text edit, FliHub data, empty statistics, Escape close, schema pills, thumbnail text) into requirements for the next Ralph loop
- [STALE 2026-03-09] Build FliHub-style dispatch sending incident data to the POEM application via AWB
- [STALE 2026-03-09] Add save affordance and visual target indicator to the transcript-abridgment chat-with-output area
- [STALE 2026-03-08] Confirm AWB web-components-instead-of-iframes capability is complete and usable
- [STALE 2026-03-06] Write documentation for the new FliDeck concept and display YAML, reference it in the handover, and instruct recipients to update their own docs
- [STALE 2026-03-06] Fix step-back navigation so returning to a previous step does not trap forward progression
- [STALE 2026-03-06] Fix modal dialog edge spacing and add Escape-key close
- [STALE 2026-03-06] Fix dark-green brand colors on AWB light and dark screens
- [STALE 2026-03-06] Expose output-field visualizations in the engineer/developer view alongside the green output box
- [STALE 2026-03-06] Deep-review the system and produce a unit-test coverage report with Vitest recommendations, backfilling missing wave tests
- [STALE 2026-03-06] Create a holding document listing conversational chat use cases before designing chat output
- [STALE 2026-03-06] Consolidate nested/flat/table overview visualizations to at most two and improve screen real-estate use
- [STALE 2026-03-06] Change output-fields accordion so multiple sections can be expanded simultaneously
- [STALE 2026-03-06] Add generic reusable clipboard-copy and open-in-Finder handlers to the output file list
- [STALE 2026-03-04] Restore top and bottom left/right navigation arrows and chevron-style progress bar
- [STALE 2026-03-04] Research Restream and ensure it appears in the platforms list
- [STALE 2026-03-04] Rename preview mode to Pilot after impact assessment and unit test review
- [STALE 2026-03-04] Rename agent workflow builder from WUI and record where that information lives
- [STALE 2026-03-04] Rename WUI (web user interface) to Agent Workflow Builder (AWB) and abstract it into its own application
- [STALE 2026-03-04] Rename POEM WUI references to AWB across the system
- [STALE 2026-03-04] Move files out of TMP into durable locations before session close
- [STALE 2026-03-04] Develop implementation plan in a background agent and confirm context/data before building
- [STALE 2026-03-04] Build generalized chat-with-output control on data fields (incl. all 12 extraction values)
- [STALE 2026-03-04] Background agent to locate old brand document with affiliate/social/related-video settings (team folder/Dropbox/AWB v1)
- [STALE 2026-03-04] Add toggle between horizontal and vertical section/station workflow orientations
- [STALE 2026-03-03] Run refactor and unit tests as background tasks, then execute UAT via Playwright and report back
- [STALE 2026-03-03] Propose best-practice design for first-class output/autosave configuration in workflow YAML
- [STALE 2026-03-03] Migrate WUI naming to Agent Workflow Builder and abstract it to its own application
- [STALE 2026-03-03] Implement preview and engineer view modes and document the future polished mode in the architecture
- [STALE 2026-03-03] Execute plan→code→unit tests→YAML docs→UAT (new-incident + YLO) via Playwright MCP in a git worktree
- [STALE 2026-02-24] Write up the required workflow data panel and configurability changes (optionally as a TMP file) for developer handoff
- [STALE 2026-02-24] Produce a UI gap-analysis report comparing the old agent workflow UI with the YouTube Launch Optimizer, including JSON vs markdown/HTML AI-response formatting
- [STALE 2026-02-24] Investigate whether Hexfield and Leonardo AI can be driven via a skill, MCP server, or true Chrome-extension shim
- [STALE 2026-02-24] Fix workflow picker so new-workflow/start-session stops defaulting to YouTube Launch Optimizer

## SupportSignal  (58 actions, 2 live)

- [LIVE 2026-07-07] Redeploy the SupportSignal application on a new Vercel + Supabase instance as a working demo
- [LIVE 2026-06-22] Bring the directors' sync forward from Thursday to Tuesday and send the engagement email
- [RECENT 2026-06-12] Record prompts used at feedback time so metrics from older prompts aren't misapplied
- [RECENT 2026-06-12] Angela to hammer incident workflow over the weekend and submit detailed feedback directly into the product
- [STALE 2026-04-01] Share the absolute path of the generated story so incident-data ingestion prep can start
- [STALE 2026-04-01] Investigate incident visibility (blocked/orphaned incidents, which user account sees them) via Supabase query
- [STALE 2026-03-31] Write feature request for deep entity retrieval with child-entity flag (Epic 0 story)
- [STALE 2026-03-31] Review new build errors and assess if easily resolvable
- [STALE 2026-03-31] Process SupportSignal epic-5 tickets on secondary computer
- [STALE 2026-03-31] Git commit and push current code changes
- [STALE 2026-03-31] Document the token/permission exposure risk in the brain document; defer revocation until end of work
- [STALE 2026-03-12] Verify an incident list exists and UAT coverage for incidents
- [STALE 2026-03-12] Unravel the UAT vs E2E naming conflict and align tests with the system design
- [STALE 2026-03-12] Start showing the participant onboarding flow to a client this week or next with a rough interface
- [STALE 2026-03-12] Investigate saved-session mechanism so the app resumes logged-in instead of starting from the not-logged-in state
- [STALE 2026-03-11] Shift Angela's focus to moments-that-matter and incident workflow planning grounded in the schema, documented separately from general feedback
- [STALE 2026-03-11] Set the application domain to app.supportsignal.com.au and update configurations
- [STALE 2026-03-11] Rename the marketing repo to www.supportsignal.com.au and add a Claude MD warning about updating the Cloudflare dashboard
- [STALE 2026-03-11] Hold the guardrails alignment session with Angela and Rodi to agree the high-level flow, data-vs-visualization distinction, and change-introduction rules
- [STALE 2026-03-10] Seed one valid realistic record now; park Angela's Excel-based data as a later todo
- [STALE 2026-03-10] Proceed straight to the Wygham build
- [STALE 2026-03-10] Copy Angela's current data set instead of creating separate UAT data
- [STALE 2026-03-09] Specify system-admin vs company-admin roles including seed-data implications
- [STALE 2026-03-09] Reorder epics: foundation/security/API skeleton first, push integration before incident/moment epics
- [STALE 2026-03-09] Design system-admin vs company-admin role split
- [STALE 2026-03-09] Analyze incident data in app.supportsignal, list rich-sample records, and design the Wave 12 incident data model
- [STALE 2026-03-04] Start BMAD-driven cloud build (database schema, REST API, app) from MVP specs on Monday
- [STALE 2026-03-04] Create SupportSignal observation document describing updated plans
- [STALE 2026-03-04] Build a SupportSignal observation document comparing current plans, the old app, the Studio MVP with Angela, and the new AWB incident workflow
- [STALE 2026-03-04] Angela and Ronnie to review the structured data model together Friday afternoon
- [STALE 2026-03-03] Kick off SupportSignal observation document covering current plans, old app, studio MVP, and new incident workflow
- [STALE 2026-03-01] Resume SupportSignal work tomorrow
- [STALE 2026-02-13] Run and verify every npm script added to package.json and confirm all tooling works
- [STALE 2026-02-13] Produce a plan of action to clean up lint issues, stabilise TypeScript, validate all npm scripts, and apply Prettier formatting consistently
- [STALE 2026-02-10] Write handover/transference document for Angela's next session and commit+push
- [STALE 2026-02-10] Review all documentation (topology, indexes, health dashboard) for system soundness
- [STALE 2026-02-10] Replace shadow-mode comparison table with an on-upload JSON discrepancy report covering input placeholders, output fields, and full old/new prompt text
- [STALE 2026-02-10] Move production cutover story 12.5 to end of Epic 12 and add warning that Epic 12 cannot proceed until POEM prompt upload and validation are tested
- [STALE 2026-02-10] Investigate Bob's workflow so every story ends with a CEO executive summary
- [STALE 2026-02-10] Deprecate the UI enhancement prompts once the predicate/observation system is stable
- [STALE 2026-02-10] Build human-in-the-loop confirmation in the application (worker accepts accountability for AI text) before broad market release
- [STALE 2026-02-10] Build UX folder via background agents: database/ (json + schema), data-mapping tool, requirements/ (10 specs), index.html + 10 generated visualization sites
- [STALE 2026-02-10] Apply the Jest-to-Vitest migration process to the web application tests
- [STALE 2026-02-10] Adopt three-part structure per predicate: predicate (true/false), observation (narrative), classification (finite labels e.g. severity)
- [STALE 2026-02-02] Run SupportSignal unit tests this morning, then incident capture until 13:00
- [STALE 2026-01-19] Write an inline handover specification with absolute file paths and continue the E3 KDD restructure in a fresh conversation
- [STALE 2026-01-19] Verify commit flows and debug the fill-Q&A developer-experience button error
- [STALE 2026-01-19] Rework the data grouping structure and names without delegating to the architect/ChatGPT
- [STALE 2026-01-19] Review Angela's AMS reporting dataset together tomorrow and distill it into predicate/classification prompt structures for Penny the prompt engineer
- [STALE 2026-01-19] Redesign the enhanced-review screen from a single enhanced narrative to human-confirmable true/false and classification signals
- [STALE 2026-01-19] Rebuild the Epic 3 index file with missing sections per index-page formatting documentation
- [STALE 2026-01-19] Fold E3 KDD index/tab/documents into Epic 3 as submenus, mirroring the Epic 4 approach
- [STALE 2026-01-19] Fix Q&A regeneration so regenerated questions clear/invalidate previously stored answers
- [STALE 2026-01-19] Compare David's .claude file and bmad-core (Taylor agent, appydave workflow, KDD changes) against the project's setup and report differences before any changes
- [STALE 2026-01-19] Audit and instrument the new-incident/edit-incident area to find the regression point
- [STALE 2026-01-19] Audit all documents and reorganize them into a coherent information architecture, optionally via background agents
- [STALE 2026-01-13] Run recurring daily 1-hour Angela training sessions starting tomorrow at noon
- [STALE 2026-01-13] Angela to research and install a Windows voice dictation tool (e.g. Whisper Flow) for prompt writing

## Signal Studio  (48 actions, 0 live)

- [STALE 2026-04-01] Decide whether to build a temporary CRUD incident endpoint as a stopgap for holding/starter incidents
- [STALE 2026-04-01] Add a copy button for verification/non-verification info in the verify flow, matching the push flow
- [STALE 2026-03-31] Review Signal Studio push instructions against recent participant-data changes
- [STALE 2026-03-31] Centralize sync verification on the push dashboard rather than duplicating controls on every listing page
- [STALE 2026-03-30] Prepare handover message covering work done, rationale, and testing pointers
- [STALE 2026-03-30] Align schemas with Signal Studio for all future stories in the epic
- [STALE 2026-03-11] Run the full UAT plan, not a single concept
- [STALE 2026-03-11] Run a gap analysis to bring Signal Studio in line with current AppyStack capabilities (including the NPX-style upgrade tool)
- [STALE 2026-03-11] Resolve the publish command issue and publish the SupportSignal product from Studio
- [STALE 2026-03-11] Reset and seed the development data directory and clean up the hundreds of stray JSON files to reach a clean commit
- [STALE 2026-03-11] Recover the corrupted user's data from git history, accounting for the directory restructure
- [STALE 2026-03-11] Record in flood.md that MCP Playwright e2e tests are broken and why
- [STALE 2026-03-11] Nuke and clean the development data directory, distinguishing tracked seed files from generated junk
- [STALE 2026-03-11] Firm up production/UAT/development database separation, stable unique-ID primary keys shown in the UI, and an explicit written schema with validation/error-check buttons per database
- [STALE 2026-03-11] Create an up-to-date human-walkthrough UAT test plan
- [STALE 2026-03-11] Add the standard port-conflict handling code that other servers already have
- [STALE 2026-03-10] Tighten company scoping so non-system-admins see only their own company's users, sites, and incidents
- [STALE 2026-03-10] Run code integrity, delete/cascade impact, and unit test audits in next planning wave
- [STALE 2026-03-10] Rework company-admin companies view (role-appropriate display, no add-company, reconsider pluralized label)
- [STALE 2026-03-10] Replace environment badge with color-per-environment fixed footer, using front-end designer
- [STALE 2026-03-10] Redesign incidents interface and simplify dropdowns
- [STALE 2026-03-10] Investigate slow environment switching between production/integration data sets
- [STALE 2026-03-10] Group user selection list by company, order by role, show ~20 rows, highlight company admins
- [STALE 2026-03-10] Flatten menu to a single wide tabular line
- [STALE 2026-03-10] Expand badge palette to ~10 colors and add a Style Guide page of shared components
- [STALE 2026-03-10] Create backlog item to add participant entity support to company admin
- [STALE 2026-03-10] Add local JSON memory file (not in git) tracking UAT/integration/production environment state
- [STALE 2026-03-09] Run Playwright test suite and investigate issue B72
- [STALE 2026-03-09] Revisit Signal Studio and epics plan against the data-reflection-engine framing
- [STALE 2026-03-09] Resolve recurring gitignore/data-addition sync error
- [STALE 2026-03-09] Rebuild documentation into the machine-readable structures that generate the Python requirements/UI documents
- [STALE 2026-03-09] Investigate Git sync API 500 error during moments sync
- [STALE 2026-03-09] Fix the ad site label
- [STALE 2026-03-09] Design incident search/management screens wired to participants/users/companies
- [STALE 2026-03-09] Deep-dive research the new incident YAML and .display.yaml structures (not yet ratified — assume cautiously)
- [STALE 2026-03-09] Create 'David observations' feedback doc alongside Angela feedback in the repo
- [STALE 2026-03-09] Angela to keep using the app and logging feedback rather than re-running UAT scripts
- [STALE 2026-03-05] Verify unit and end-to-end tests on the generated build and hand it back to Angela for validation
- [STALE 2026-03-05] Send Ronnie a video asking for suggestive (not prescriptive) client-side validation per Signal Studio field
- [STALE 2026-03-05] Run integration tests based on the UAT plan
- [STALE 2026-03-05] Merge participant-system worktree into main branch
- [STALE 2026-03-05] Generate a UAT plan for the updated participant system
- [STALE 2026-03-05] Finish scaffolding the Mochaccino mockup skill in the Claude skills folder and ping Angela to pull
- [STALE 2026-03-04] Send Loom walkthrough of Signal Studio local setup to Ronnie and Angela by end of day
- [STALE 2026-03-04] Run Ralph Wiggum loop to build Angela's tiered participant data model into the prototype
- [STALE 2026-03-03] Prepare detailed theming architecture plan supporting current, SupportSignal, and AWB themes
- [STALE 2026-03-03] Investigate and fix the Sync-to-Git button bug, reproducing via Playwright if needed
- [STALE 2026-03-01] Review Signal Studio details and keep them referenced for tomorrow

## AngelEye  (34 actions, 2 live)

- [LIVE 2026-06-24] Review AngelEye vs AngelEye Sentinel daemon overlap, compatibility, and correct hook target
- [LIVE 2026-06-24] Restart AngelEye so telemetry is captured around the ticket sessions
- [RECENT 2026-06-13] Build AngelEye Sentinel with hook capture, MCP server and API
- [STALE 2026-04-03] Isolate the ingestion framework as a robust JSON/HTTP endpoint that starts at boot, separate from the crash-prone web app
- [STALE 2026-04-03] Fix AngelEye session discovery so edge sessions of the 7-session BMAD workflow register reliably
- [STALE 2026-04-03] Document data discovery patterns plus a repeatable pattern-rediscovery process (evaluate Archon for automation)
- [STALE 2026-04-01] Write the pre-reboot backup steps for AngelEye session/hook data into a file before rebooting
- [STALE 2026-04-01] Update and improve AngelEye planning documents based on recent learnings
- [STALE 2026-04-01] Read the 'Angel Eye Architecture and Requirements' document
- [STALE 2026-04-01] Make the ingestion service auto-start on boot and investigate frequent app crashes and cache clearing
- [STALE 2026-04-01] Draft requirements to separate the ingestion/hook service from the web application and add to planning docs
- [STALE 2026-03-31] Integrate predicate/observation views into the AngelEye interface
- [STALE 2026-03-30] Write up and build the chat panel plus the four incoming workflow items
- [STALE 2026-03-30] Finish the user stories for Ronnie
- [STALE 2026-03-30] Build the missing runner, wiring, and AngelEye enrichment pipeline
- [STALE 2026-03-30] Build BMAD visual harness in AngelEye for the Lars demo
- [STALE 2026-03-29] Write documentation for Sentinel, Relay, and Lisa's KDD curation roles
- [STALE 2026-03-29] Reverse-engineer and canonically document the six BMAD review sub-agents in the SupportSignal app
- [STALE 2026-03-29] Note Ralph Wiggum loop visualization and UX guidelines in agents.md
- [STALE 2026-03-29] Maintain a living document of predicates, observations, classifiers, and event agent call-offs
- [STALE 2026-03-28] Compile the wave visualization requirements into a design document, define JSON structures and agent metadata profiles, and build 3-4 Mochaccino mocks from story 2.4 data
- [STALE 2026-03-28] Build the agent-workflow wave visualization over the weekend and enable app auto-update for Lars
- [STALE 2026-03-18] Create gap analysis between Claude Code hook/event surface and AngelEye's current capture coverage
- [STALE 2026-03-16] Make the startup script self-healing: port-conflict checks, existing-process detection, graceful stop-hook failure when app is down
- [STALE 2026-03-16] Fix the visually inverted hide-junk/show-all toggle
- [STALE 2026-03-16] Diagnose why the session data directory was empty after restart and add backfill/persistence safeguards
- [STALE 2026-03-16] Add pagination to the session browser to avoid overloading it with 671+ sessions
- [STALE 2026-03-13] Vibe-code own telemetry system by pillaging patterns from existing telemetry projects
- [STALE 2026-03-13] Vibe-code his own unified telemetry system (transcripts, hooks, tool calls across all terminals/projects) by pillaging the best of existing telemetry projects
- [STALE 2026-03-12] Write up the E2E logging/feedback design and an ASCII interface mockup in-conversation
- [STALE 2026-03-12] Write AngelEye detailed requirements (multi-format ingestion, workspaces/inbox model, future pattern intelligence) in the apps folder alongside DeckHand/ThumbRack/AppyStack
- [STALE 2026-03-12] Send Chris the AngelEye v0-alpha repo and schema once built tonight; compare against his DB schema
- [STALE 2026-03-12] Rename the application to Angel I and redesign storage away from Supabase toward file-system/JSONL
- [STALE 2026-03-12] Commit tonight's library-meeting agenda file into the AngelEye repo and push

## brains repo  (31 actions, 0 live)

- [RECENT 2026-06-13] Commit and push the video-as-code / hyperframes brain-related content
- [RECENT 2026-06-12] Check brains are up to date with remote and that local brain knowledge is pushed
- [STALE 2026-04-01] Review the .mochaccino folder at the repo root and decide what to do with it
- [STALE 2026-03-31] Write detailed pain-and-problems learnings report to the brains folder root
- [STALE 2026-03-31] Expand brain support document with full diagnostics plus anonymization instruction for the Anthropic support request
- [STALE 2026-03-31] Document when to use local network vs Tailscale vs SSH for remote access
- [STALE 2026-03-28] Define the three test brains, ontology example files, and judging criteria before running the multi-brain tag tests
- [STALE 2026-03-06] Close the compensation note, then commit and push recent changes
- [STALE 2026-03-05] Run the 14-step brain health check across all brains changed in the past week using background agents
- [STALE 2026-03-05] Create a Skool brain alongside the creator-economy brain
- [STALE 2026-03-04] Probe Ecamm Live undocumented HTTP API and document capabilities in the ecamm brain
- [STALE 2026-03-04] Mark cowork-upgrade as sandbox proof-of-concept in its CLAUDE.md
- [STALE 2026-03-04] Create Krisp AI brain, record its absolute path, and fold in existing Krisp research
- [STALE 2026-03-02] Research Hammerspoon deeply with background agents and create a Hammerspoon brain covering the two use cases, Q&A on more
- [STALE 2026-03-01] Clarify index.md scope and add links from the to-do brain to the other brains
- [STALE 2026-02-28] Audit all brains for frontmatter coverage and per-brain tagging ontology, then run a multi-hour three-brains-at-a-time processing flow
- [STALE 2026-02-24] Commit any outstanding brain files
- [STALE 2026-02-22] Rename the second-brain document-pattern doc and refresh the README, then commit
- [STALE 2026-02-22] Remove the Playwright MCP folder and move useful README content into CLAUDE.md
- [STALE 2026-02-22] Do a general check and cleanup of the brains folder root structure and files
- [STALE 2026-02-22] Create a second brain for macOS best practices and tips
- [STALE 2026-02-22] Commit the untracked files
- [STALE 2026-02-21] List all brains created this session and create one health-check task per brain
- [STALE 2026-02-12] Create a Tailscale-focused standalone second brain referenced by the agent OS
- [STALE 2026-02-02] Proceed with options one and two on documentation structure
- [STALE 2026-02-02] Identify leftover files from recent work needing cleanup
- [STALE 2026-02-02] Complete frontmatter for the remaining 47 documents, ideally via background agent
- [STALE 2026-02-02] Commit all current work and produce a handover structure for the next batch
- [STALE 2026-02-02] Build the brain health dashboard, then run topology validation
- [STALE 2026-01-31] Create and verify the twitterx second brain covering Premium features, Grok access, and X Pro
- [STALE 2026-01-31] Create a second brain for the online inference engine and research models, usage, and developer-plan costs

## Claude Code  (22 actions, 0 live)

- [RECENT 2026-06-14] Set up a recurring loop giving David progress updates on long-running research tasks
- [RECENT 2026-06-13] Review the Anthropic connector portal before recommending it to clients
- [RECENT 2026-06-13] One-shot build the Daily Support Plan app under the Supporting Potential folder using AppyStack
- [RECENT 2026-06-13] Locate the AppyDave and AI-TLDR video transcript catalogues across both machines
- [RECENT 2026-06-13] Locate folders and session IDs for the Fable 5 video session and Angela's Supporting Potential session to build resume commands
- [RECENT 2026-06-13] Draft a handover message and revive the outstanding probe tasks in the new session
- [RECENT 2026-06-13] Background-research the hyperframes-style motion graphics tool vs Remotion and find existing skills for it
- [STALE 2026-03-16] Run a visible background web-server + Playwright MCP check of the SupportSignal work instead of manual testing
- [STALE 2026-03-13] Write handover instructions for starting the two upstream repos in a new session with correct data
- [STALE 2026-03-11] Produce a self-contained handover message covering brand, community, content pillars, repos, apps and agentic OS for the next session
- [STALE 2026-03-11] Deep-research the AppyDave/Signal Studio/Agentic OS repos before asking further questions; verify agentic OS machine count (5, not 3) in the reference implementation
- [STALE 2026-03-09] Update CLAUDE.md so Claude proactively suggests /loop use-cases in context
- [STALE 2026-03-09] Research Claude API and /loop semantics and community lessons-learned beyond official documentation
- [STALE 2026-03-06] Process the dropped image batch and rate research as background tasks in one worktree, then show the result via Playwright MCP
- [STALE 2026-03-05] Research whether other users are missing the Claude Code remote-control rollout and format findings as a pasteable comment
- [STALE 2026-02-13] Write a spot-check verification prompt a second agent can use to confirm the application still works
- [STALE 2026-02-02] Spin up background agents to mine the Vitest migration files for learnings worth integrating
- [STALE 2026-02-02] Produce a handover message after compaction preserving patterns, anti-patterns, learnings and decisions, and verify via written artifacts and commit messages whether combos 1-3 are complete or have open loops
- [STALE 2026-02-02] Have background agents locate Claude conversation JSONL files, extract session IDs, and summarize each so sessions can be selectively reloaded
- [STALE 2026-01-31] Try sub-agent frontmatter skills autoloading so the librarian agent's ontology/topology docs only load when the librarian is active
- [STALE 2026-01-12] Produce a conversational handover encoding the option 3 -> 1 -> 2 sequence for the next session
- [STALE 2026-01-11] Produce a plan of action (not implementation) for a unified start.sh/go startup command

## DeckHand  (22 actions, 0 live)

- [STALE 2026-03-12] Run Playwright MCP smoke test on DeckHand and verify deckhand.json has not regressed
- [STALE 2026-03-11] Verify button drag-and-drop onto the deck in a headed Chrome Playwright run
- [STALE 2026-03-11] Fix the data in staging and production and push the unpushed commits
- [STALE 2026-03-11] Fix clear/delete so items can actually be removed from the deck
- [STALE 2026-03-10] Work out how to discover the full Ecamm Live API endpoint set and how to trigger preconfigured Stream Deck buttons remotely from the web app
- [STALE 2026-03-10] Update StauDocs and audit UAT coverage so tests match current capabilities at the end of every loop
- [STALE 2026-03-10] Test every Ecamm button individually and confirm the code executes
- [STALE 2026-03-10] Run the app via Playwright for exploratory functionality + design review with the front-end designer persona
- [STALE 2026-03-10] Run every UAT and either fix issues or compile a recommendation document; delete tests that don't reflect reality
- [STALE 2026-03-10] Remove the prompt template section from the main screen, add the missing copy button, and display real schema info (values and output-format structure) on the right panel
- [STALE 2026-03-10] Remove deadweight and resolve loose ends in the workspace-automation project
- [STALE 2026-03-10] Implement a Stream Deck-style profile system in DeckHand and add one Ecamm Live profile first, with a detailed executable plan
- [STALE 2026-03-10] Fix Stream Deck UI: larger fonts/wider right section, device→profile→actions hierarchy, draggable buttons, editable colors and names — follow Elgato's established best practices
- [STALE 2026-03-09] Design phase-1 Stream Deck visualization app, phase-2 Elgato SDK integration
- [STALE 2026-03-05] Build DeckHand integration that pushes Ecamm Live buttons, reads config, and exposes an API for skills
- [STALE 2026-03-04] Run GET-only background tests on Krisp SDK and Ecamm HTTP API and document real findings
- [STALE 2026-03-04] Produce flow graph, unit tests, executed UAT plan and fact sheet with recommendations
- [STALE 2026-03-04] Document all Ecamm Live automation and Stream Deck workflow knowledge under the DeckHand apps folder
- [STALE 2026-03-02] Research Stream Deck and Ajazz AKP03 button/dial/multi-step capabilities to design the multi-deck configuration model
- [STALE 2026-03-01] Rename the AppyDeck system to DeckHand everywhere and centralize its documentation
- [STALE 2026-03-01] Figure out how to run Ian's VibeDeck locally and draft instructions for a skill that talks to it
- [STALE 2026-03-01] Assess feasibility of assigning commands/configs to all four button devices as a virtual Stream Deck and decide where the requirements documentation lives

## Kyber Extension SDK  (20 actions, 16 live)

- [LIVE 2026-07-13] Verify the tool's architecture fits the Kyber Extension SDK and import it once publishable
- [LIVE 2026-07-11] Build the extensions layer as micro-apps embedded in the KyberAgent desktop (menu of bespoke business apps with pre-baked agents/skills)
- [LIVE 2026-07-07] Merge to David's branch and run option-2 end-to-end tests for the frame extension changes
- [LIVE 2026-07-07] Apply the approved doc plan and remove test-only screenshots from the repository
- [LIVE 2026-07-04] Re-evaluate each of the five batch-built extensions from the perspective of real human and agent usage, adding search, inferred metadata, summaries, and documentation
- [LIVE 2026-06-30] Review the Kyber Extension SDK before implementation
- [LIVE 2026-06-24] Run a full architecture audit of channel/endpoint naming and adopt convention over configuration
- [LIVE 2026-06-24] Render a single usable Mochaccino foundation mock and treat the Extension SDK generated capabilities doc as canonical when rebuilding Scene Probe React and iframe versions
- [LIVE 2026-06-24] Remove obsolete extensions from the packages
- [LIVE 2026-06-24] Make Scene Probe composable elements usable in the chat interface and test filters, dropdowns, and extension-to-chat integration
- [LIVE 2026-06-24] Extract host interface into its own package and implement a fake host for proper extension unit testing
- [LIVE 2026-06-24] Explore host-managed scheduled-task capability declared by extensions via data channels
- [LIVE 2026-06-24] Check whether the Extension SDK overhaul branch name is still relevant
- [LIVE 2026-06-24] Build a watch-and-poll extension for OMI transcripts with configurable polling interval
- [LIVE 2026-06-23] Run a preliminary spike of the landscape and return with questions before building
- [LIVE 2026-06-23] Audit all Extension SDK capabilities into a rich JSON capability graph and test iframe vs in-proc parity
- [RECENT 2026-06-20] Work through and expand 3-4 use cases each for composer and contextual menu surfaces before designing the architecture
- [RECENT 2026-06-20] Expand the seam demo extension to show real data (chat, brain access, custom extension data), not just schema-shaped OK checks
- [RECENT 2026-06-12] Run a background agent on why KAD uses a brain provider while KBDE calls directly, and resolve the inconsistency
- [RECENT 2026-06-05] Pressure-test KBDE extension architecture toward decoupled plugin/API with backward-compatible contract

## brains  (19 actions, 1 live)

- [LIVE 2026-07-04] Track down the prior video-editing conversation (video-as-code brain) and locate the agentic editing repo in upstream
- [RECENT 2026-06-14] Document the named-collaborator crew + orchestrator pattern in the prompt-patterns brain
- [RECENT 2026-06-13] Research Boris Cherny's plan-less, file-memory way of building apps as input to the DSP one-shot
- [STALE 2026-04-06] Document outstanding tmux + multi-agent team swarm issues in the brain
- [STALE 2026-04-01] Reference upstream Hermes harness (not the brain alias) in the OMI brain configuration
- [STALE 2026-03-31] Git pull brains repo and review Paperclip/AngelEye updates via background agent
- [STALE 2026-03-28] Run the multi-model tagging comparison with a metrics table across brains
- [STALE 2026-03-10] Record the Ecamm/Stream Deck API learnings into the Ecamm second brain
- [STALE 2026-03-01] Run deep research on prompt patterns (recipes, capability signaling, discovery) and spin it into a prompt-engineering brain
- [STALE 2026-03-01] Identify which brains changed in the last three days
- [STALE 2026-02-13] Create browser acceptance testing second brain with install steps and a website health spot-check prompt
- [STALE 2026-02-10] Update the 11Labs brain to reference the downloaded SDKs
- [STALE 2026-02-10] Research a mechanism so link counts only reflect current, non-historical links before touching agents or code
- [STALE 2026-02-10] Locate the Ruby transaction classification tool (possibly near appydave-tools) and seed a banking second brain
- [STALE 2026-02-10] Download BMAD v6 (out of alpha) and bring brain documentation up to date
- [STALE 2026-02-10] Add SDK status files with option-B status flags consistently across all downloaded SDKs
- [STALE 2026-02-07] Write up available IndyDevDan information into a second brain
- [STALE 2026-01-11] Document the start.sh alias and numbering system centrally in the second brain
- [STALE 2026-01-11] Create handover conversation summarizing start.sh alias decisions for the second brain

## AppyStack  (19 actions, 0 live)

- [STALE 2026-03-17] Write up recurring server startup/port failures as backlog items in AppyStack, not DSS
- [STALE 2026-03-17] File AppyStack backlog item for broken start script/template and port issues
- [STALE 2026-03-16] Undo the unintended downgrade and produce a handover with correct absolute paths + instructions so AppyStack gets fixed
- [STALE 2026-03-16] Report the out-of-date start.sh startup-script malfunction back with details
- [STALE 2026-03-13] Research and propose the unified startup capability (ports, single instance, auto browser open) across the three directory structures
- [STALE 2026-03-12] Move server data storage to the monorepo root with docs, unit tests, and a handover note for DeckHand
- [STALE 2026-03-11] Review AppyStack recipes for a Zod schema and create one tied to the file-CRUD recipe if missing
- [STALE 2026-03-11] Delete the global Mochaccino skill installation and generalize it as an AppyStack skill
- [STALE 2026-03-09] Design recipe for systems talking to ElevenLabs
- [STALE 2026-03-05] Update the badly outdated AppyStack README and surface installation steps early
- [STALE 2026-03-05] Fix recipes feature that errors on click
- [STALE 2026-03-04] Write the AppyStack API recipe (expose entities as endpoints with Swagger) as an on-the-side task
- [STALE 2026-03-04] Document AppyStack recipes from skill.md into the repo's GitHub README
- [STALE 2026-03-04] Deep-define requirements for a 100%-complete API endpoint recipe (entity list -> working testable Swagger APIs)
- [STALE 2026-03-04] Create AppyStack recipes file, link the two existing recipes, and draft the new API recipe
- [STALE 2026-03-03] Write third AppyStack recipe: expose entities as endpoints with Swagger API, as an on-the-side task
- [STALE 2026-03-03] Plan two-part AppyStack series: Stream Deck-style visual front end, then API hookup
- [STALE 2026-03-02] Write discoverable UI-shell and file-CRUD recipe docs with sample-data scenario child folder
- [STALE 2026-03-01] Deep-research AppyStack architecture and draft visual-shell + file-persistence recipes plus at least two more common UI patterns

## KDD  (17 actions, 3 live)

- [LIVE 2026-07-04] Wire KDD document reading into structural workflow points (PR validation, knowledge update)
- [LIVE 2026-07-04] Register the KDD bridge MCP in the application registry with clear purpose/ownership docs
- [LIVE 2026-07-04] Enforce one-learning-document-per-ticket convention instead of spawning KDD branches
- [STALE 2026-02-13] Run full documentation audit and health check: validate topology, regenerate indexes, health dashboard, and report on the validate-internal-markdown-links task
- [STALE 2026-02-13] Regenerate the web testing knowledge and migrate it into KDD as discussed
- [STALE 2026-02-13] Locate and scope-verify all Ralph Wiggum loop web-layer Vitest learnings, then plan their migration into KDD with folder-structure decision
- [STALE 2026-02-13] Investigate why missing indexes are treated as low priority and what causes false positives in the querying system
- [STALE 2026-02-13] Implement redirects for files in the planning/learnings directory without deleting originals
- [STALE 2026-02-13] File n8n, ComfyUI, and Kybernesis documentation as standalone research documents, not core architecture
- [STALE 2026-02-10] Write implementation notes for Lisa to review and file before switching workflows
- [STALE 2026-02-02] Resolve archive vs historical distinction via KDD documentation and the librarian
- [STALE 2026-02-02] Report KDD migration completion percentage and missing content
- [STALE 2026-02-02] Move two legacy KDD files and remove the legacy folder
- [STALE 2026-02-02] Fix the two broken links
- [STALE 2026-02-02] Execute the next KDD batch per the refactoring report and handover document
- [STALE 2026-02-02] Document and think through the convex function structure issue via knowledge-driven development
- [STALE 2026-02-02] Analyze the topology problem and whether the flagged file is too large

## Dark Factory  (17 actions, 14 live)

- [LIVE 2026-07-13] Run a conversational (not ask-tool) Q&A walkthrough of the Dark Factory roadmap, one idea at a time, pinpointing the major constellation applications to sequence
- [LIVE 2026-07-10] Ultrathink and decide the cross-repo context architecture: reference folders vs MCP server vs centralized execution
- [LIVE 2026-07-09] Start and maintain a document mapping what control surfaces (MCP/API, permissions, deployment, comms channels) Dark Factory needs over KyberAgent
- [LIVE 2026-07-09] Review and unwind the unapproved 'war room' namespace back to factory lanes/stations naming
- [LIVE 2026-07-09] Evaluate Tony's smart-contract approach for strengthening rubric/eval contracts at the end of the factory pipeline
- [LIVE 2026-07-09] Decide policy: block/flag tickets that modify factory-running code instead of executing them through the factory
- [LIVE 2026-07-09] Consolidate task launching onto the orchestrator/Switchboard-WatchTower path instead of ad-hoc claude invocations
- [LIVE 2026-07-09] Add a chaperone/observer over the main factory conversation window
- [LIVE 2026-07-04] Deprecate broken Gemini integration out of the system
- [LIVE 2026-07-03] Propose the prioritized list of micro apps/extensions to build, with reasons and how they connect
- [LIVE 2026-07-03] Build prototypes as KyberAgent / Claude Agent SDK extensions that exercise the dark factory harness rather than only the Claude Code harness
- [LIVE 2026-07-02] Define a visualization system for dark factory apps, tickets and morning status summaries
- [LIVE 2026-07-02] Create dark factory architecture documentation covering events, hooks, pipelines and communication channels
- [LIVE 2026-06-24] Analyze ~10 BMAD stories' sessions without over-summarizing to preserve the workflow machinery as a dark-factory pattern
- [RECENT 2026-06-21] Run session archaeology over the last 5-10 dark-factory and suborch sessions to build a clean sequential audit
- [RECENT 2026-06-13] Build the AppyDave thumbnail builder app (title + design + thumbnail text + subliminal text) using prior thumbnail research
- [RECENT 2026-06-12] Re-review every document and commit for documentation drift and build a Q&A backlog to get back on track

## agentic-os  (15 actions, 0 live)

- [STALE 2026-03-31] Run gap analysis between David's agentic OS and Lars's setup
- [STALE 2026-03-17] Build a strong JSON structure representing the agentic OS components
- [STALE 2026-03-16] Update agentic OS design docs with the horizontal file communication capability
- [STALE 2026-03-16] Deliver midnight tech-summit talk on the agentic operating system (unprepared as of call)
- [STALE 2026-03-13] Research Automator and AppleScript and how Claude Code can drive them; add to the agentic OS design
- [STALE 2026-03-13] Research Automator and AppleScript and how Claude Code can drive them, then add the integration concept to the agentic OS design
- [STALE 2026-03-10] Do a full audit of everything in the agent setup on Tuesday
- [STALE 2026-03-04] Send the agentic-architecture JSON document to the collaborator so he can make infographics of it
- [STALE 2026-03-04] Send the agentic-architecture JSON document to the collaborator for infographics
- [STALE 2026-03-04] Process OpenClaw meetup content into the inbox area through the agentic-OS lens
- [STALE 2026-03-04] Evaluate Matrix/Element (Synapse) as the multi-agent multi-channel routing layer versus the planned Supabase-over-Tailscale ingestion bus
- [STALE 2026-02-24] Verify NanoGPT is integrated somewhere in the agentic OS
- [STALE 2026-02-22] Verify Tailscale is installed on the fleet machines and locate the prior Tailscale/VPS setup documentation
- [STALE 2026-02-22] Update agentic OS config to record machine locations and support remote-desktop access that survives the M2 Mini moving to the shop
- [STALE 2026-02-22] Confirm Assembey is Ansible-managed and review agentic OS against the Ansible config for needed updates

## Captain's Log  (15 actions, 14 live)

- [LIVE 2026-07-13] Route all transcripts and synopses through a vocabulary correction system keyed to David's real product names
- [LIVE 2026-07-13] Make OMI/Claude transcript ingestion a durable launchd-style job (30-min cadence, 07:00-22:00) with a manual trigger in the app
- [LIVE 2026-07-13] Hide empty/noise captures by default behind a toggle and add semantic source coloring (OMI green, Plaud blue)
- [LIVE 2026-07-13] Centralize tag storage/governance so missing tags (captains-log, kybernesis, lars) are fixed future-proof, possibly a dedicated tag-management app
- [LIVE 2026-07-13] Automate the Plaud refresh-token refetch (currently a manual browser-console paste), likely via Playwright
- [LIVE 2026-07-13] Add filter toggles for tags, timeframe, keyword search, and noise (hidden by default)
- [LIVE 2026-07-13] Add a show-markdown/show-transcript button and a light theme to the capture view
- [LIVE 2026-07-12] Mine prior Claude conversations on captains-log/OMI/Plaud into a detailed requirements doc and spec, then build the extension
- [LIVE 2026-07-12] Build an easy refresh-token re-fetch plus storage against the Plaud ingestion provider
- [LIVE 2026-07-12] Add ingestion-destination configuration for Plaud/OMI raw transcripts
- [LIVE 2026-07-11] Extend Captain's Log ingestion beyond OMI/Plaud to email-forwarded YouTube links (transcript extraction) and articles (scraping), with analyze/summarize/ontology-tag pipeline
- [LIVE 2026-07-09] Make the Captain's Log pulse configurable (daily window, ~10-minute cadence) through the extension system
- [LIVE 2026-07-09] Host the Captain's Log viewer as a KyberAgent extension with LLM access via the daemon
- [LIVE 2026-07-05] Research a Claude-based transcription pipeline that ingests OMI/Plaud audio+video and runs tagging/ontology
- [STALE 2026-04-12] Pull OMI transcripts from the API endpoint into a central inbox and run a tagging ontology over them

## FliVideo  (14 actions, 1 live)

- [LIVE 2026-07-11] Wire FliHub to launch Gling with videos and keywords preloaded after a recording
- [STALE 2026-03-12] Deep dive FliHub assets and inboxes concepts and design git-based bidirectional image workflow with Jan
- [STALE 2026-03-10] Write a FliVideo handover brief describing the required data formatting
- [STALE 2026-03-10] Review FliHub codebase/docs and consolidate challenges, issues, and gap analysis into a scratch-pad document
- [STALE 2026-03-10] Front-end designer cleanup of file counts/sizes/transcription area and relocate YouTube copy near recordings
- [STALE 2026-03-10] Expose AWB JSON output file in the UI with hover path and click-to-open-AWB-preloaded
- [STALE 2026-03-10] Create FliVideo handover message specifying timestamp, chapter name, and first 50 transcript words per chapter (JSON)
- [STALE 2026-03-10] Commit and push current FliHub changes
- [STALE 2026-03-09] Rename all 'poemvoid' button labels to 'AWB'
- [STALE 2026-03-09] Fix transcript payload bug: send all transcripts concatenated, not a single SRT file
- [STALE 2026-03-04] Investigate FliHub brain config shape mismatch
- [STALE 2026-02-10] Test FliHub server endpoint connectivity (possible deprecated endpoint behind 404 failures)
- [STALE 2026-02-02] Remotion session between 14:00 and 16:00
- [STALE 2026-01-19] Rename the voice-agent codebase and move it into the FliVideo repository area

## agentic-os brain  (14 actions, 0 live)

- [STALE 2026-03-17] Document SyncThing setup and DavidJan relay folder in the agentic OS
- [STALE 2026-03-17] Add synthesized/canonical/provenance-chain terms to the agentic OS glossary
- [STALE 2026-03-17] Add level four (observability, self-improvement, workflow/memory agents) to the agent capability model
- [STALE 2026-03-12] Document control plane, orchestrators and executors concepts
- [STALE 2026-03-12] Add AngelEye as the observability layer in the agentic OS design
- [STALE 2026-03-06] Run background-agent gap analysis of paperclipAI/paperkit and Valor Agent versus Agentic OS
- [STALE 2026-03-06] Clarify what KyberBot actually is (sleep-time memory over a second brain, sits between harness and David) and document it
- [STALE 2026-03-01] Update agentic OS with Bun/pnpm learnings using primary/optional convention
- [STALE 2026-03-01] Run gap analysis of current vertical stack versus an OpenClaw-like architecture
- [STALE 2026-03-01] Research package-manager consensus and pick primary + secondary for greenfield agentic systems
- [STALE 2026-03-01] Produce relation-based JSON documents for vertical stack, horizontal stack, and full system incl. Ansible's place
- [STALE 2026-03-01] Document in-development systems across apps, core content pillars, and the agentic OS
- [STALE 2026-02-22] Record in the architecture document that two Philippines Mac minis (16GB/512GB, likely no Ecamm Live) will join the network
- [STALE 2026-02-22] Monitor Agent OS project health via the brain library

## POEM OS  (13 actions, 0 live)

- [STALE 2026-03-01] Research agents across POEM and BMAD systems and build an agent-name list aligned with planned computer names
- [STALE 2026-02-10] Update Oscar agent to understand LLM parallel and conditional-parallel workflow steps (7a/7b/7c chaining) and feed changes back to the original POEM framework
- [STALE 2026-02-10] Research classification prompt templates and fix observation template so outputs are never phrased as questions
- [STALE 2026-01-22] Rename external-consultants plugin to consultants across command name, folder, and versions, leaving no remnants — research plugin docs first
- [STALE 2026-01-22] Diagnose the installation error introduced with the Astro 6 upgrade
- [STALE 2026-01-13] Redo the visual design of stories 4.1-4.3 which did not improve after the earlier change request
- [STALE 2026-01-13] Commit story 1.6 plus documentation changes and add an out-of-sequence callout under epic one
- [STALE 2026-01-12] Test dual-schema API behavior using the existing generate-titles prompt
- [STALE 2026-01-12] Organize raw Nano Banana research data with transient notes before defining any schemas or prompts
- [STALE 2026-01-12] Do not act; research and explicitly define the correct input and output schema for the prompt from planning docs, architecture and PRD
- [STALE 2026-01-12] Consolidate raw data and create asset ideas for the Nano Banana image-generation prompt system data feed
- [STALE 2026-01-11] Implement the refine command properly (preview with data, generate schema) in story 3.6, adding one-liner list and view commands to the prompt engineer beforehand
- [STALE 2026-01-11] Create a task list covering product owner, architect, and Scrum Master perspectives for the epic 3 schema course-correction

## OMI pipeline  (12 actions, 0 live)

- [STALE 2026-04-02] Review omi-fetch/art-fetch architecture to separate deterministic execution from nondeterministic AI steps (possibly via claude -p)
- [STALE 2026-04-02] Harden OMI extraction against Gemini bad-JSON so the pipeline heals instead of stopping after one retry
- [STALE 2026-04-02] Fix the token-burning issue in the OMI automation file setup
- [STALE 2026-04-02] Add the server log file to .gitignore
- [STALE 2026-04-02] Add healing fallback for missing brains_index.json plus 1-2 Gemini retry attempts to the OMI script
- [STALE 2026-04-01] Run another fetch incorporating new info for the additional project
- [STALE 2026-04-01] Run OMI fetch and process this morning's AngelEye/AWB file
- [STALE 2026-03-30] Create OMI scripts directory in the GitHub repo
- [STALE 2026-03-30] Build Python backfill script for OMI extraction, accepting it may span two days of quota
- [STALE 2026-03-20] Adopt Bangkok-first-then-UTC timestamp display for all OMI transcript listings
- [STALE 2026-03-11] Explore a /loop-driven background ingestion pipeline that routes incoming OMI, email and chat data to the right brain locations
- [STALE 2026-02-28] Research how to ingest OMI device transcripts into own endpoint/app and design the receiving endpoint

## VibeDeck  (11 actions, 0 live)

- [STALE 2026-01-19] Share the exact Ajazz deck link so the whole team buys the same device and starts daily testing/hardening
- [STALE 2026-01-19] Set up GitHub org and push the mono-repo (app, plugins, website), then make it public before Feb 7
- [STALE 2026-01-19] Prepare open-source dev-kit lightning-talk demo for the February 7 Claude event
- [STALE 2026-01-19] Finalize marketing website with Stripe preorders and spin up the Discord community
- [STALE 2026-01-12] Work out how to recover from the incorrect implementation 3.7 — dev-only fix or revisit story/context information
- [STALE 2026-01-12] Run deep research on context-engineering workflows and produce three summaries: by persona, by workflow stage, by toolchain
- [STALE 2026-01-12] Fix the broken deck slides using the newly supplied information and guide images
- [STALE 2026-01-12] Each member builds a solo software proof-of-concept / UX variant of the vibe deck, then reconvene to merge best ideas
- [STALE 2026-01-12] Design the local software shim layer (JSON-configurable, multi-backend: Claude/Gemini/OpenAI/Codex) rather than talking directly to Claude Code
- [STALE 2026-01-12] Build an agent that generates ~20 alternative front-end design variants from the same data
- [STALE 2026-01-12] Build VibeDeck HTML front end plus Socket.IO backend with file watching and app-focus integration

## OMI  (10 actions, 1 live)

- [LIVE 2026-07-04] Add last-pulled timestamp and new-data visibility to the OMI fetch app
- [RECENT 2026-06-14] Write support ticket to OMI about the lost conversation (only head and tail retained), noting the OpenAI embedding hookup as a possible cause
- [STALE 2026-04-01] Session tomorrow 14:00 Asia/Bangkok with Lars to explore OMI and scheduled tasks
- [STALE 2026-03-09] Discuss Desktop Scheduled Tasks in tomorrow's OMI morning to-do/email session
- [STALE 2026-03-04] Verify Omi app browser login is working as first priority
- [STALE 2026-03-04] Retrieve 'David plans daily systems' capture to temp dir and analyze ingestion/backup/routing plus status of three reported bugs
- [STALE 2026-03-04] Record the border-run experience via OMI and send the transcript writeup to friend for his blog
- [STALE 2026-03-04] Deep-research OMI automation approaches and search inside the app via Playwright MCP
- [STALE 2026-02-23] Send Adam the OMI recording once processing finishes
- [STALE 2026-01-10] Research OMI SDK/APIs and how to send transcripts to Kybernesis

## KyberAgent  (10 actions, 8 live)

- [LIVE 2026-07-13] Prepare a 2-3 minute demo of Captain's Log, the Extension SDK fit, the brain, and agents for the Lars call
- [LIVE 2026-07-13] Have that agent read KDD docs and commits and write a recurring report on new KyberAgent/Kybernesis changes by Ian and Martin
- [LIVE 2026-07-13] Build the first agent — a KyberAgent-knowledge brain agent — on Roamy using the $100 credits
- [LIVE 2026-07-03] Research a KDD inspection extension showing projects, decisions, documents and patterns at a glance
- [LIVE 2026-07-03] Adopt iframe-based, dynamically-loaded extensions with one GitHub repo per extension and package.json pointing at the SDK for host interface contracts
- [LIVE 2026-06-30] Scope the thumbnail generator micro app as a KyberAgent extension
- [LIVE 2026-06-29] Build an app/port registry extension (apps, locations, ports) separate from locations.json
- [LIVE 2026-06-24] Get Jan and Mary using KyberAgent starting at the next team meeting
- [RECENT 2026-06-13] Write up a ticket for the backup-database cleanup question and provide its URL
- [RECENT 2026-06-13] Create a shutdown script that runs when closing Kyber Agent Enterprise

## KyberBot  (9 actions, 0 live)

- [RECENT 2026-06-14] Release brain version 12 with the data migration system
- [RECENT 2026-06-13] Set up a 2-minute progress loop reporting baseline run done/remaining/ETA
- [RECENT 2026-06-13] Proceed with the recommended spec work and check if a schema update/migration is required
- [RECENT 2026-06-13] Persist session learnings somewhere more durable than agent memories
- [RECENT 2026-06-13] Document study-setting defaults, on/off rationale, and probe findings
- [RECENT 2026-06-13] Define how to redo probes with a clean test set
- [RECENT 2026-06-12] Install KyberBot brain for Angela as test guinea pig for per-client FDE brains
- [RECENT 2026-06-05] Merge the brain PR into the application tonight with Martin and Ian
- [STALE 2026-02-24] Set up KyberBot for second-brain memory

## calendar  (8 actions, 0 live)

- [RECENT 2026-06-12] Set standing Monday 1pm 30-minute meeting, afternoons only, one meeting per day
- [STALE 2026-03-16] Push Angela's change-request sync to Wednesday
- [STALE 2026-03-10] Send calendar invite for the Wednesday 2 PM meeting
- [STALE 2026-03-06] Follow-up call tentatively set for Saturday 07:30
- [STALE 2026-03-01] Schedule Tuesday kickoff meeting with Lars for the three-month Project Theodore collaboration
- [STALE 2026-02-10] Schedule a one-hour session for Ian at Guy's studio for social media training
- [STALE 2026-01-31] Register for the official Anthropic Claude Code event on Feb 7 at CMU
- [STALE 2026-01-31] Catch up with Lars Friday afternoon before he leaves Chiang Mai

## Claude Code session  (8 actions, 0 live)

- [RECENT 2026-06-12] Write handover document for Spec A and update the spec with completed work before merge
- [STALE 2026-04-01] Write a handover message in-conversation to continue testing data delivery from code to Signal Studio
- [STALE 2026-02-24] Write a conversation fact sheet of the machine-setup decisions (what/why/how-to-replicate)
- [STALE 2026-02-23] Compile troubleshooting factsheet with absolute file paths for SupportSignal handoff
- [STALE 2026-02-02] Write batch-20 handover document usable in a new conversation window
- [STALE 2026-02-02] Write a concise agent handover capturing the philosophical/decision-making lessons only
- [STALE 2026-02-02] Prepare a handover for the next conversation
- [STALE 2026-02-02] Load original conversation session and prepare handover for the next batch

## appydave-plugins  (8 actions, 0 live)

- [RECENT 2026-06-20] Build a loop selector/orchestrator skill and adapt the six external loops into AppyDave plugins
- [RECENT 2026-06-14] Build voice.md for the AppyDave brand from raw transcripts via a voice-forge skill, with drift-reflection against newer transcripts
- [STALE 2026-04-01] Provide conversational skill-based testing instructions, or come back with a Q&A if the right skills don't exist yet
- [STALE 2026-04-01] Get the relay skills installed on the other system today
- [STALE 2026-03-31] Define skill structure for writing data consumable by NotebookLM
- [STALE 2026-03-30] Move extraction schema into skill references
- [STALE 2026-03-13] Fix Ralphie loop logging and document the Ralphie plugin vs Anthropic /loop distinction
- [STALE 2026-02-24] Check the Ralphie second brain and plugin and report what capabilities Ralphie has

## SupportSignal requirements doc  (8 actions, 0 live)

- [STALE 2026-02-24] Specify export capability (API or UI) for incidents, participants, moments, workers, sites, companies to feed POEM
- [STALE 2026-02-24] Reframe 'notification of high severity' as in-system highlighting since no notifier exists
- [STALE 2026-02-24] Note that the application is designed to be friendly to agent-based systems wherever possible
- [STALE 2026-02-24] List definitions for RBAC and other acronyms near where they appear
- [STALE 2026-02-24] Do a comprehensive pass over all related data documents and rerun the generator so outputs match the latest spec
- [STALE 2026-02-24] Define Moments That Matter menu/data-entry (time-based notes grouped by day or shift, owned by the support worker, speech-to-text via Groq)
- [STALE 2026-02-24] Add bulk company and participant upload via validated CSV/spreadsheet paste
- [STALE 2026-02-24] Add authentication/impersonation guidance (off-the-shelf libraries, no roll-your-own) into the requirements document wherever relevant

## Mochaccino  (8 actions, 5 live)

- [LIVE 2026-06-25] When designs need missing data, either raise a feature spec or generate schema-based mock data instead of hallucinating
- [LIVE 2026-06-25] Reorganize the channels/hosts/extensions/permissions list into a logical, readable order
- [LIVE 2026-06-25] Build screens around the API surface that directly reflect real working code
- [LIVE 2026-06-24] Move Mochaccino mock content from hardcoded HTML into structured JSON/schema data files so visuals render from data
- [LIVE 2026-06-24] Create one HTML page visualizing capabilities driven off real system data
- [STALE 2026-03-17] Run Mocaccino skill to produce four data visualizations using AppyStack styling recipe
- [STALE 2026-03-11] Give Mochaccino theme-awareness so mock UIs respect the host app's style, and clone/reshape data for mocks instead of touching production data shape
- [STALE 2026-03-11] Constrain Mochaccino to read and respect the current data schema, producing gap-analysis output for any schema change requests

## NotebookLM  (7 actions, 0 live)

- [STALE 2026-03-31] Draft NotebookLM presentation prompt using style guidelines
- [STALE 2026-03-31] Build 8-slide agentic-OS presentation for Lars
- [STALE 2026-03-05] Create the Ansible/agentic-OS dataset and markdown document packaged as one drag-in file
- [STALE 2026-03-02] Export all menu and branding docs to a single NotebookLM-importable file with style prompt
- [STALE 2026-03-01] Write a strong JSON description of the agentic OS vertical/horizontal stacks and import into NotebookLM to generate the Lars presentation
- [STALE 2026-03-01] Produce list of required files plus handover instructions for the NotebookLM transfer package
- [STALE 2026-02-28] Experiment sending meetup transcripts to NotebookLM to auto-generate a podcast for remote participants

## SupportSignal micro app  (7 actions, 0 live)

- [STALE 2026-03-02] Review every page in dark mode via Playwright MCP, fix all dark-theme issues, and commit
- [STALE 2026-03-02] Rename the Configure section to Project Info
- [STALE 2026-03-02] Open 3-4 screens in dark mode via Playwright MCP and assess contrast/color scheming
- [STALE 2026-03-02] Investigate localStorage-vs-database conflicts causing ghost users and phantom active participants
- [STALE 2026-03-02] Design button-driven fake record generator backed by a /fake data folder (possibly Faker)
- [STALE 2026-03-02] Commit current work and verify light/dark mode both function
- [STALE 2026-03-02] Build reset-database function, reusable modal dialog component, and client-side validation framework (AB/NDIS numbers)

## GitHub  (7 actions, 0 live)

- [RECENT 2026-06-13] Commit and push the DSP app to a private repo under David's organisation and grant the partner access
- [STALE 2026-03-12] Create public GitHub remotes for DeckHand and AngelEye
- [STALE 2026-03-11] Rename the old supportsignal.com.au remote so a new remote can be created
- [STALE 2026-03-11] Create the BMAD learnings GitHub repo under an AppyDave org with a Brian liaison document and agent-to-agent coordination pattern; give Jan edit access
- [STALE 2026-03-11] Archive historical clutter repos (Klueless JS/GPT sites, appydave-flivideo) without deleting
- [STALE 2026-03-11] Add a GitHub CLI audit of all organizations David controls (active vs inactive) to the ecosystem overview
- [STALE 2026-03-03] Create private repo for Lars following the Guy Monroe client repository pattern, auto-created if possible

## Stream Deck  (7 actions, 0 live)

- [STALE 2026-03-11] Get a powered USB hub to fix Stream Deck wake-from-sleep dropouts
- [STALE 2026-03-10] Investigate why the Stream Deck SDK is needed versus plain HTTP-endpoint buttons for Ian's app
- [STALE 2026-03-10] Enumerate candidate API endpoints via Bonjour/binary extraction and test them, flagging any destructive-looking ones before execution
- [STALE 2026-03-10] Deep background research: can the Stream Deck SDK (or reverse engineering) read decks/profiles/buttons/config, and what workarounds exist for the platform limits
- [STALE 2026-03-05] Set up StreamDeck pedal multi-actions: left button record/stop (waiting for Ecamm recording to finish), right button pause/resume
- [STALE 2026-03-05] Configure Stream Deck pedal: left-button multi-action for record/stop (with wait-for-finish) and right button for pause/resume, then document the setup
- [STALE 2026-03-03] Get working scenes on the Stream Deck

## Ecamm Live  (7 actions, 0 live)

- [STALE 2026-03-10] Clarify mapping between Stream Deck plugin structure and documented Ecamm API endpoints
- [STALE 2026-03-05] Delete videos from the Ecamm recordings directory after checking contents
- [STALE 2026-03-05] Delete recordings in the old Ecamm location
- [STALE 2026-03-04] Re-check Ecamm Live after quit-and-reload
- [STALE 2026-03-04] Create new Ecamm Live scene named code-plus-c2
- [STALE 2026-03-04] Call each Ecamm Live button individually to observe what it does
- [STALE 2026-03-04] Call each Ecamm Live button individually to observe what it does

## ITO voice-input project docs  (6 actions, 0 live)

- [STALE 2026-01-16] Write two linked requirements documents (Rust Fn-key/mic tool + JavaScript Groq-processing app) instead of building now
- [STALE 2026-01-16] Write the technology validation report for the voice-input tool research
- [STALE 2026-01-16] Validate ITO tech stack: was Rust needed vs JavaScript, and are the chosen technologies the best options
- [STALE 2026-01-16] Research the ITO open-source project's architecture (Fn key access, microphone/MIDI hookup) as the basis for requirements
- [STALE 2026-01-16] Report muddied/inconsistent aspects across the research docs without fixing them
- [STALE 2026-01-16] Clarify PV recorder 'commercial pre-compiled' licensing (payment required?)

## client-lars  (6 actions, 0 live)

- [STALE 2026-03-31] Schedule week-one BMAD agent-building session plus near-daily 30-minute follow-ups
- [STALE 2026-03-18] Prepare omi-fetch skill and Paperclip orchestrator installation (plus possibly AngelEye) for Lars session Friday
- [STALE 2026-03-17] Plan budget request to Lars: Claude $100/$20 plans plus two WhisperFlow seats for Jan and Mary
- [STALE 2026-03-04] Send Lars a short packaged email with a Loom about the YouTube Launch Optimizer
- [STALE 2026-01-31] Send Lars an invoice for the smaller month-one prepayment
- [STALE 2026-01-31] Kick off the 3-month engagement March 1 with at least one solid weekly meeting

## agentic OS  (6 actions, 0 live)

- [STALE 2026-03-04] Create apps folder for technical requirements and move Stream Deck info into it
- [STALE 2026-02-10] Record the full hardware inventory in the agentic OS brain
- [STALE 2026-02-10] Have Lisa record all documentation updates
- [STALE 2026-02-10] Design a central index file grouping agents and SDKs by semantic role (voice agent vs underlying tech) and tag context-engineering frameworks (BMAD v4/v6, spec-kit, GSD, NanoBot, ClawBot, Pi-AI)
- [STALE 2026-02-10] Build a list of male/female agent names and roles for future agents beyond Samantha
- [STALE 2026-02-07] Import ideas from the SQL/AI data-organisation post into a database section of the agent OS brain

## M4 migration file transfer  (6 actions, 0 live)

- [STALE 2026-02-28] Verify whether .zshrc/profile/bash shell config files were transferred off the failing MacBook Pro
- [STALE 2026-02-28] Verify the committed folder is on the M4 and re-copy it
- [STALE 2026-02-28] Scan for and quickly transfer secrets and environment config files
- [STALE 2026-02-28] Migrate everything from the failing MacBook Pro to the M4 over SSH
- [STALE 2026-02-28] Copy the video projects folder first, then the full dev directory in priority order via background agents
- [STALE 2026-02-28] Copy the Claude site + voice agent and repo-audit repos to the new machine

## appydave plugin skills  (6 actions, 2 live)

- [LIVE 2026-07-10] Build a self-learning context-aware formatting/reporting skill (tabular exec-style output on demand, context- and state-aware)
- [LIVE 2026-07-09] Build a session post-processing router skill that extracts tweets, YouTube material, and lead-magnet knowledge packets from coding sessions
- [RECENT 2026-06-14] Locate the cortex monorepo README commits and prior research, then build a repeatable first-class README-writing skill
- [STALE 2026-04-01] Review existing relay skills and decide new skill vs extend existing for the Dropbox relay
- [STALE 2026-03-07] Make digit-prefix an at-invocation prompt and merge the two image skills into one under the right plugin
- [STALE 2026-03-07] Build the rename-images skill via skill-creator with folder-default, optional digit prefix, and subfolder-move capabilities

## Agent Workflow Builder POC  (6 actions, 0 live)

- [STALE 2026-03-13] Run a status loop on kickoff (logged-out state, diagnostic output format) and verify Ansible has the needed config, adding it if missing
- [STALE 2026-03-13] Run a background agent check that recent system changes haven't broken UAT-related functionality
- [STALE 2026-03-13] Rename the proof of concept to 'agent workflow builder proof of concept'
- [STALE 2026-03-13] Reimplement starter page using mock v15 with v13's lighter background/content-area colors
- [STALE 2026-03-13] Inspect YAML and HBS config (not code) for the moments-that-matter input misconfiguration
- [STALE 2026-03-13] Generate 10 new design variations combining v1, v3 and v6 (variants 8-17) and open them all for review

## Skool  (5 actions, 0 live)

- [RECENT 2026-06-13] Build the school/community asset builder
- [STALE 2026-03-17] Set Skool agentic-OS community introductory price at $14.95/month and lift content quality
- [STALE 2026-02-22] Have the friend join and audit the Skool community for missing engagement opportunities and report back
- [STALE 2026-02-22] Follow up with Jan/Mary on packaging the Remotion video series into a paid course
- [STALE 2026-01-11] Finish the comprehensive project starter guide and publish it to the Skool community

## email  (5 actions, 1 live)

- [LIVE 2026-07-07] Send Linda follow-up with engagement options (weekly session + monthly tool-build retainer, subscription/credit breakdown)
- [STALE 2026-03-05] Send Lars the email with the Ansible repo URL, Loom videos, and proposed session times (Saturday 7-8am / 3pm tomorrow / Monday)
- [STALE 2026-03-03] Send the follow-up email about the ingestion naming decision
- [STALE 2026-03-03] Email Lars a starter guide: install/run Ansible playbook and create ~/dev/brains second-brain structure
- [STALE 2026-01-22] Send introduction email to Wiphu proposing a one-hour meeting next week

## YouTube  (5 actions, 0 live)

- [STALE 2026-03-04] Produce the Signal Studio Raffy Loop extension video showing side-by-side before/after from a one-shot prompt
- [STALE 2026-03-04] Produce the Signal Studio Raffy Loop extension video
- [STALE 2026-03-04] Produce the Ansible / Project Theodore agentic-OS intro video
- [STALE 2026-03-04] Produce the 5-8 minute Ansible / Project Theodore agentic-OS intro video (concept overview, community funnel, context for Lars)
- [STALE 2026-01-31] Rebrand appydave research channel to the Coding Lab and start daily livestreams across YouTube, Twitter, Facebook and LinkedIn

## Chiang Mai AI Community  (5 actions, 2 live)

- [LIVE 2026-07-04] Send Angela's project documents through by email to progress her onboarding
- [LIVE 2026-07-04] Coordinate onboarding session with Angela and Stravan
- [STALE 2026-02-13] Introduce Tony to Ian, Nick, and Steve after tomorrow's AI meetup
- [STALE 2026-02-10] Connect Ian and Steve with Tony about free/low-cost AI community space in his building
- [STALE 2026-02-07] Steer Thursday Clauding Lab sessions to an agentic-OS theme for the coming months

## FliHub  (5 actions, 0 live)

- [STALE 2026-03-18] Jan to work on FliHub menus tomorrow
- [STALE 2026-03-10] Split chapter number and folder name into separate JSON fields and decide whether FliHub must be updated to emit the new structure
- [STALE 2026-03-04] Review FliHub personalization and vocabulary settings and investigate the MC integration
- [STALE 2026-03-02] Test the YouTube launch optimizer by sending information through it and get it running
- [STALE 2026-02-10] Validate the three 11Labs tool configurations that should call FliHub, using a background agent to check how each system works

## dev environment  (5 actions, 0 live)

- [STALE 2026-02-22] Delete iTerm node modules and AutoClose Cloud entirely, then continue the sync
- [STALE 2026-02-22] Create an exclude-from-copy registry of large files/folders at the root of ~/dev
- [STALE 2026-02-22] Compare dev.zip against dev in a background task
- [STALE 2026-02-10] Investigate what recently introduced shell/startup change is making new terminals slow to open
- [STALE 2026-02-10] Add a minimal timer to the startup sequence showing session load time

## M4 Mini  (5 actions, 0 live)

- [STALE 2026-03-12] Sync the two specified folders over to the M4 Mini
- [STALE 2026-03-05] Install the chosen Whisper CLI (MLX Whisper vs whisper.cpp — keep only the better) on the M4 Mini
- [STALE 2026-03-05] Check ffmpeg is installed, install if missing
- [STALE 2026-03-01] Get Ecamm Live and the Blackmagic 4K camera working on the M4 main so it becomes the primary machine today
- [STALE 2026-02-28] Replicate MacBook Pro environment and get FliDeck video conversation working on the M4 Mini

## agent-os brain  (5 actions, 0 live)

- [STALE 2026-03-01] Unpack AppyStack recipes and compound recipes into Q&A form for a research go/no-go pass
- [STALE 2026-03-01] Review vertical/horizontal-stack JSON documents for missing fields and currency
- [STALE 2026-03-01] Replace the NotebookLM export skill with a general agent OS doc describing where to gather data and the TMP-folder + Finder drag-in convention
- [STALE 2026-03-01] Persist architecture research with date/time metadata and back up the presentation-generation prompt beside the notebook collection
- [STALE 2026-03-01] Build the full application inventory (filename, description, location, port) including the POEM port-registry behavior

## YouTube Launch Optimizer  (5 actions, 0 live)

- [STALE 2026-03-03] Test YouTube Launch Optimizer for exactly two hours recording per-page developer/agent/designer observations
- [STALE 2026-03-03] Add dark mode and light mode support
- [STALE 2026-03-02] Update or add unit tests based on captured learnings
- [STALE 2026-03-02] Run three-pass process: per-file problem inventory, fix all, document anti-patterns and good patterns as learnings
- [STALE 2026-03-02] Assess which generic application-stack best practices were missing during development

## ansible repo  (5 actions, 0 live)

- [STALE 2026-03-16] Split Ansible into public repo + private sibling inventory, moving Tailscale IPs and Jan/Mary/Lars host data private
- [STALE 2026-03-16] Document the Homebrew curl bootstrap command in the Ansible repository README
- [STALE 2026-03-05] Update the Ansible playbook config for Lars with his GitHub username and email
- [STALE 2026-03-03] Rename Mini Lars playbook to a Mac mini client template with Joe Blow placeholder username/email
- [STALE 2026-03-03] Refactor Ansible playbooks to separate David-specific tools from a generic client template

## Joy Juice  (5 actions, 0 live)

- [STALE 2026-03-18] Jan and David to work on fruit juice menus tomorrow
- [STALE 2026-03-09] Start daily 5pm sampling: one drink split into shot glasses given free with written ratings collected
- [STALE 2026-03-09] Redesign menu around 8 base fruits with Thai/foreigner variants, dual-language, color-coded by fruit (Mary or Jan to produce menus)
- [STALE 2026-03-09] Fix the overhead head-hazard in the shop
- [STALE 2026-03-09] Add chairs/seating out front to capture red-bus foot traffic

## fleet  (4 actions, 0 live)

- [RECENT 2026-06-21] Migrate day-to-day development control to the M4 machines with coding tasks delegated over SSH and synced via git
- [STALE 2026-04-01] Set up second laptop with new Anthropic account and test Hermes as memory/agent harness
- [STALE 2026-04-01] Configure git pull of SupportSignal app code and rsync-over-SSH of Claude session files to second laptop
- [STALE 2026-01-31] Buy a new M4 Mac and set up the M2 as a ClaudeBot/OpenClaw machine, livestreaming both setup tracks as guidance for Lars

## file migration project  (4 actions, 0 live)

- [STALE 2026-02-02] Update documentation to reflect phase one complete / phase two in progress
- [STALE 2026-02-02] Sanity-check all migrated files against the intended migration list
- [STALE 2026-02-02] Review batches through ~24 to confirm no files were missed in migration
- [STALE 2026-02-02] Re-run the documentation health check after recent additions

## personal  (4 actions, 0 live)

- [STALE 2026-03-18] Verify online banking sign-in works before departure
- [STALE 2026-03-18] Get Joanne a passport
- [STALE 2026-03-18] Confirm backup plan: friend with valid passport accompanies Joy across border in an emergency
- [STALE 2026-02-10] Review Ian's step-by-step document before his Thursday class for Claude community leaders

## agentic-os second brain  (4 actions, 0 live)

- [STALE 2026-02-12] Write design guidelines keeping layout separate from visual aesthetics for HTML/game graphics generation
- [STALE 2026-02-12] Create the Tech Stack Hotel JSON schema first, with self-updating rules so JSON documents follow schema changes
- [STALE 2026-02-12] Create a visual index of all Agentic OS documentation files in the second brain
- [STALE 2026-02-12] Build an HTML shell view (game-like 8-bit hotel) that reads external JSON data for floors/rooms

## appydave plugin  (4 actions, 0 live)

- [STALE 2026-03-12] Improve plugin reload output to surface context about the last work done
- [STALE 2026-03-12] Decide the plugin area for the AngelEye app and create a skill for it
- [STALE 2026-03-03] Create a skill that manages SSH access to other machines so Claude remembers cross-machine capability
- [STALE 2026-02-21] Wire David's aliases into the appropriate locations so plugin namespace lookups stop failing

## MacBook Pro  (4 actions, 0 live)

- [STALE 2026-03-31] Verify the existing backup of Claude sessions before uninstall/reinstall
- [STALE 2026-03-31] Reinstall Claude Code linked to the appydave account after system assessment via Ansible config
- [STALE 2026-03-31] Document detailed steps to fully remove Claude/Claude Code and reinstall under a new account
- [STALE 2026-02-28] Resolve MacBook Pro screen repair within two weeks before Vietnam conference travel

## Loom  (4 actions, 0 live)

- [STALE 2026-03-06] Voz records ongoing podcast-style Loom interviews with Kip to mine film-production knowledge
- [STALE 2026-03-05] Send the micro-app demo Loom to Lars
- [STALE 2026-03-04] Record and send Loom on daily AI graphics/animations workflow to Lars and key contacts
- [STALE 2026-03-01] Record a Loom week-in-review for Lars covering the week's work plus agentic and personal stacks

## AI-TLDR  (4 actions, 1 live)

- [LIVE 2026-06-24] Set up paywalled packaging (PDF + zip + community) for skill distribution
- [STALE 2026-03-13] Mary to start building agentic operating system content on the AI-TLDR channel, blended with Nano Banana infographics
- [STALE 2026-03-13] Mary to start building agentic operating system content mixed with graphics
- [STALE 2026-03-01] Jan to produce a Nano Banana 2 infographic 8-9 video series for AI-TLDR mirroring the agentic OS build

## Joy Juice menu system  (4 actions, 0 live)

- [STALE 2026-03-02] Pick eight fruits and build Thai/English side-by-side comparison table with per-fruit menu JSON schema
- [STALE 2026-03-02] Import the two downloaded menu images and describe their visual style for reproduction
- [STALE 2026-03-02] Document brand and menu schemas in Schema.md
- [STALE 2026-03-02] Convert menu data to menu.json and build an HTML/JS rendering capability

## team-ops  (4 actions, 0 live)

- [STALE 2026-03-13] Jan/Mary to photograph all purchase receipts and email them to David
- [STALE 2026-03-13] Jan/Mary to learn the agentic stack so they can later teach Vasilios Kapenekas about orchestrators
- [STALE 2026-03-09] Mary to research Philippines purchase options (Australian card/Wise, Amazon vs authorized dealers, customs) for Mac mini + keyboard + 2 monitors and present prepared on a follow-up call
- [STALE 2026-03-03] Get detailed specs for each candidate monitor before purchase decision

## ecamm brain  (4 actions, 0 live)

- [STALE 2026-03-05] Search Ecamm brain docs and Take One Tech upstream material for how to start a recording programmatically
- [STALE 2026-03-04] Write up Ecamm Live button and scene mapping into the appropriate brain
- [STALE 2026-03-04] Harvest Ecamm Live training video transcripts into the ecamm brain under Take One Tech tubescripts location
- [STALE 2026-03-04] Deepen understanding of the full Ecamm Live playlist plist schema and how to add Ecamm actions to it

## Ecamm Live integration skill  (4 actions, 0 live)

- [STALE 2026-03-04] Maintain UAT/decision log mapping Ecamm UI actions to configuration changes
- [STALE 2026-03-04] Give the Ecamm integration skill pixel-level crop/position adjustment via window coordinate data
- [STALE 2026-03-04] Build Ecamm Live integration skill covering HTTP API endpoints plus plist/XML read-modify-write with backup/rewind
- [STALE 2026-03-04] Add print-settings command to inspect available Ecamm data before changes

## OMI ingestion pipeline  (4 actions, 0 live)

- [RECENT 2026-06-14] Split the long morning transcript into three documentation streams and propose where to place each
- [STALE 2026-03-05] Research OMI ingestion as a dedicated skill and design context-quality/observability/routing mechanisms
- [STALE 2026-03-05] Design context-quality checks (prompt injection, noise, alignment) plus observability and approval decision points for incoming context
- [STALE 2026-03-05] Audit project-level skills in the brains folder and research whether OMI ingestion should become a dedicated skill (check GitHub + OMI docs for prior art)

## Dizzler  (4 actions, 0 live)

- [STALE 2026-03-12] Stop the Dizzler application and review it without letting it influence the new build
- [STALE 2026-03-12] Set up webhooks for Dizzler multi-agent observability and any Claude Replay hooks
- [STALE 2026-03-12] Get front-end designer observations on Dizzler via background tasks
- [STALE 2026-03-12] Complete Dizzler agent configuration, restart it, and confirm whether Claude sessions need restarting

## incident management UI  (4 actions, 0 live)

- [STALE 2026-03-13] Sweep all screens via Playwright/HTML for the off-brand dark-blue and red button inconsistencies
- [STALE 2026-03-13] Run an observation-only Playwright pass documenting all UI issues before fixing anything
- [STALE 2026-03-13] Remove severity field from the incident creation form (AI-inferred, shown later only)
- [STALE 2026-03-13] Drop company and reporter columns and shorten event date/time on the incident list

## Lisa  (4 actions, 2 live)

- [LIVE 2026-07-07] Keep Lisa scoped to the KDD folder; do not customize her for per-repo documentation quirks
- [LIVE 2026-07-04] Add deterministic menuing/clarification step to Lisa's workflow so she routes to the right path or asks the human
- [STALE 2026-03-31] Log the resync-failure steps as a learning for Lisa to track
- [STALE 2026-03-31] Have Lisa keep story and documentation updated as stories progress

## Lars collaboration  (4 actions, 0 live)

- [STALE 2026-03-31] Teach Lars BMAD agent building for his growth-hacking workflow, then configure Agent Workflow Builder
- [STALE 2026-03-31] Start daily 30-minute sessions with Lars from tomorrow at agreed time
- [STALE 2026-03-31] Send Lars an invoice tonight
- [STALE 2026-03-31] Create shared 'relay-lars' Dropbox folder as shared memory and confirm which email/Dropbox account (moving to appydave.com)

## Media Studio  (4 actions, 0 live)

- [RECENT 2026-06-12] Schedule one-hour Media Studio session with Steve
- [RECENT 2026-06-12] Jan to figure out automated graphics workflows for Ronnie and Vaz using Joy's brands as test bed
- [RECENT 2026-06-12] Install Media Studio on Mary's computer for automated image generation via Claude Code
- [RECENT 2026-06-05] Collect a file of reference images/styles for Joy's brands to turn into Media Studio presets in a morning session

## KyberBot Desktop  (4 actions, 0 live)

- [RECENT 2026-06-13] Surface reconciliation progress (done/remaining) in the desktop application
- [RECENT 2026-06-13] Stop snapshot/database-clone disk blowout — detect and shut down the desktop agent instead of cloning to dodge write locks
- [RECENT 2026-06-13] Document selectable memory modes (plain folder vs watched brain) and their on/off configuration
- [RECENT 2026-06-13] Diagnose and permanently fix the 'No files being watched' sources bug

## client-achieve  (4 actions, 4 live)

- [LIVE 2026-07-07] Invoice Angela $1000 and set up Claude Max plan billing on her card
- [LIVE 2026-07-07] Create private achieve-mvp repo under Supporting Potential org and grant Angela write access
- [LIVE 2026-07-07] Angela to load her Achieve mapping/workflow outputs into the repo for Claude context-load
- [LIVE 2026-07-07] Angela to generate 100 one-minute NDIS scripts via Claude Code and record them for daily video release

## LLM Council pipeline  (3 actions, 0 live)

- [STALE 2026-01-16] Extract questions + open loops (plus any third category) from the three transcripts into CSV/JSONL machine-readable output
- [STALE 2026-01-16] Build a transparent UI/dashboard surfacing council decisions, tracked questions, and anonymous disagreements
- [STALE 2026-01-16] Adopt Karpathy's LLM Council repo as the base and start feeding meeting transcripts into it

## SupportSignal deck/JSON docs  (3 actions, 0 live)

- [STALE 2026-01-19] Run background process to consolidate original + retrospective Epic 4 conversations into a single semantic JSON document before slide creation
- [STALE 2026-01-19] Load and fully understand style files (components, main colors) before deck work
- [STALE 2026-01-19] Build Epic 4 + retrospective deck with KDD changes, standard index tabs in both JSON documents, positioned after Epic 4

## vOz repo  (3 actions, 0 live)

- [STALE 2026-01-22] Maintain docs/handover folder with dated handovers plus changelog as audit trail
- [STALE 2026-01-22] Gitignore personal settings files and cleanse them from git cache so collaborators' settings don't cross-pollute
- [STALE 2026-01-22] Create Deep in the Woods project folder from documented project-setup patterns and transcribe the supplied MP3

## SupportSignal migration tracking file  (3 actions, 0 live)

- [STALE 2026-02-02] Read progress metrics from a single consistent source before writing the next handover
- [STALE 2026-02-02] Produce a side-by-side listing of completed vs remaining files to restore trust in the queue
- [STALE 2026-02-02] Background agent to check whether the migration tracking file increased and by how much

## outreach  (3 actions, 0 live)

- [STALE 2026-03-30] Send BMAD discovery-session video invitation by 12:00
- [STALE 2026-02-02] Send invitation to Lars and talk to Steve about it
- [STALE 2026-02-02] Contact Guy and talk to Ian about Project Theodore

## WhatsApp  (3 actions, 0 live)

- [STALE 2026-03-06] Draft WhatsApp message to Ian asking if MOTUS is up to date and still his agent org-chart system
- [STALE 2026-02-21] Developer to message David to set up a lunch meeting comparing workflow-orchestration approaches
- [STALE 2026-02-10] Send Guy the link to the OMI wearable transcription device once Ian responds to the referral message

## link audit  (3 actions, 0 live)

- [STALE 2026-02-10] Remove commented-out links causing link-checker false negatives, then continue with remaining easy fixes
- [STALE 2026-02-10] Commit baseline, then assess ~150 broken links individually and fix quick wins
- [STALE 2026-02-10] Background task: verify 20 file-not-exist links and produce delete-vs-update reference mapping with affected source files

## upstream repos  (3 actions, 0 live)

- [RECENT 2026-06-12] Verify upstream brain-related repos (Jebra etc.) are up to date
- [STALE 2026-03-12] Add the referenced repository to upstreams
- [STALE 2026-02-10] Delete Auto GPT, ComfyUI, ComfyUI frontend, Context7 and Crew AI; git pull/assess MOTUS; investigate Tally, Swarm and pi-mono

## workflow orchestrator (Oscar)  (3 actions, 0 live)

- [STALE 2026-02-12] Get the front-end designer involved to improve the index page UX
- [STALE 2026-02-12] Confirm whether the orchestrator run is actually progressing or hung
- [STALE 2026-02-12] Classify the uppercase markdown files in the repo root and decide moves or deprecations

## Ralph Wiggum loop repo  (3 actions, 0 live)

- [STALE 2026-02-12] Write documentation of what was done and reference the UX PoC system from the main docs
- [STALE 2026-02-12] Verify the 10 HTML files are all working
- [STALE 2026-02-12] Merge the UX PoC pull request into the main branch

## SupportSignal app  (3 actions, 0 live)

- [STALE 2026-02-24] Plan the two-week Convex-free rebuild ordered by sign-in, basic roles, and data management, with a Convex data-sync migration section
- [STALE 2026-02-24] Fix data not persisting in incident wizard steps one and two, including session data keys not updating
- [STALE 2026-02-24] Commit round seven, merge the code, and clean up worktrees

## ralphy requirements  (3 actions, 0 live)

- [STALE 2026-02-24] Review requirements items 15, 16, 17 from a UX perspective
- [STALE 2026-02-24] Provide a simple what/why/where overview of all outstanding issues and restart round six tracking
- [STALE 2026-02-24] Hold new hover/popup UX requirements for round eight and extend requirements from the temp file and conversation notes

## workflow web UI  (3 actions, 0 live)

- [STALE 2026-02-24] Show absolute data-folder paths with copy buttons per workflow on the start page
- [STALE 2026-02-24] Filter step navigation to only the current section's steps (top bar and left sidebar)
- [STALE 2026-02-24] File issue: incident workflow selection runs YouTube launch optimizer instead

## dtv brain  (3 actions, 0 live)

- [STALE 2026-03-05] Call immigration agent to clarify what the 4,300 THB service covers and capture provider details
- [STALE 2026-03-05] Book immigration/visa appointment for the 18th
- [STALE 2026-03-01] Deep-research whether property purchase in Vietnam confers residency/visa rights and store findings in the visa brain

## appydave-tools  (3 actions, 1 live)

- [LIVE 2026-06-30] Locate the old TUI image-prompt processing app in the Ruby gems / appydave-tools codebase
- [STALE 2026-04-06] Write a proper appydave-tools spec including unit tests and knowledge of all prior workaround changes
- [STALE 2026-03-01] Get DAM tool and clipboard gem working on the new M4, decide global-gem vs in-DAM, and update Ansible if needed

## Ansible fleet setup  (3 actions, 0 live)

- [STALE 2026-03-13] Schedule Ansible-first provisioning session for the new Mac (weekend or Monday), screencasting the whole install
- [STALE 2026-03-01] Resolve Tailscale login issue and document Tailscale as a post-Ansible setup step
- [STALE 2026-03-01] Research best-practice Tailscale install (App Store vs vendor site) and add the recommendation to Ansible documentation

## todo brain  (3 actions, 0 live)

- [STALE 2026-03-03] Define primary/secondary overview format shown when focusing the todo brain
- [STALE 2026-03-01] Handle the Apple Mac warranty today and process r6.txt items into the to-do list
- [STALE 2026-03-01] Design an inbox/router layer for the to-do system that leans on the second-brain index topology

## YouTube Launch app  (3 actions, 0 live)

- [STALE 2026-03-03] Review whole app and docs to design data persistence strategy (folders, naming, location)
- [STALE 2026-03-03] Fix ingestion regressions: F5 returning to starter page, missing import banner after seed/export, unclear revision IDs (tc04-tc08)
- [STALE 2026-03-03] Add copy-to-clipboard button for collected workflow data

## personal/dtv  (3 actions, 0 live)

- [STALE 2026-03-04] Receive land border run contact details from friend
- [STALE 2026-03-04] Go to bus terminal today and arrange the same-day DTV visa run
- [STALE 2026-03-04] Call/message Tanisha Imran to book the same-day DTV border run

## Ansible presentation slide deck  (3 actions, 0 live)

- [STALE 2026-03-05] Document the commands for reading and running sections of machine fleet profiles
- [STALE 2026-03-05] Create a three-to-four page slide deck covering the composable Ansible configuration playbooks
- [STALE 2026-03-05] Add slides showing terminal playbook commands for provisioning and partial-config runs

## aionui brain research  (3 actions, 0 live)

- [STALE 2026-03-06] Run deep background research on ACP/AionUI and its multi-agent delegation fit for the agentic OS
- [STALE 2026-03-06] Identify 4-5 AionUI competitors, compare with KyberBot, and verify ACP vs A2A usage from the repo
- [STALE 2026-03-06] Download and evaluate the AionUI repo (iOFFICE AI) for where it fits in the agentic OS

## FliLaunch  (3 actions, 0 live)

- [RECENT 2026-06-13] Build the YouTube launch optimiser (YLO) micro app
- [STALE 2026-04-11] Draft detailed diagrammatic UX-first requirements spec (pages, decisions, data flow) for the YouTube Launch Optimizer
- [STALE 2026-03-09] Ship YouTube launch app today

## AngelEye test suite  (3 actions, 0 live)

- [STALE 2026-03-12] Skip the flaky test with a reason, commit and push, and clean the churning data directory
- [STALE 2026-03-12] Investigate failing tests 12 and 13; git restore the data directory and other spec files to clear churn
- [STALE 2026-03-12] Implement generic smarter polling, rerun the suite with a progress loop, and measure new-vs-old speed

## appydave plugins  (3 actions, 0 live)

- [STALE 2026-03-31] Decide whether to add a development-review skill and update Nate's review responsibilities
- [STALE 2026-03-31] Capture SyncThing relay-skill requirements in a temp folder, then build the skill with Anthropic's skill creator
- [STALE 2026-03-12] Start building the Nano Banana skill from a handover document into appydave-plugins

## fleet-infra / Ansible  (3 actions, 0 live)

- [STALE 2026-03-16] Set up Mary's machine with Jan at his house on Saturday, with Jan recording a video of the process
- [STALE 2026-03-16] Set up Mary's Mac Mini this week to complete the 5-machine network
- [STALE 2026-03-16] Get Tailscale, remote login and SSH working on Mary's machine using the session transcript

## digital-stage-summit app  (3 actions, 0 live)

- [STALE 2026-03-17] Use MCP Playwright to self-test more UI use cases instead of manual testing
- [STALE 2026-03-17] Refactor Loom storage: transcripts as sibling SRT files linked one-to-one from JSON records
- [STALE 2026-03-17] Add mailing-list and Loom-showcase CTAs as scannable QR/Nano Banana images

## appydave.com  (3 actions, 0 live)

- [STALE 2026-03-20] Review appydave.com and apply AppyStack styling guidelines sitewide
- [STALE 2026-03-20] Design auto-publishing blog pipeline from video transcripts and learnings
- [STALE 2026-03-20] Decide rebuild-from-scratch on latest Astro/Tailwind vs incremental upgrade

## skills-tooling  (3 actions, 2 live)

- [LIVE 2026-06-24] Investigate and consolidate overlapping audit/review skills into a routed system-audit with subtypes
- [LIVE 2026-06-24] Build a skill that generates a recipe from an existing skill
- [STALE 2026-03-28] Research OpenRouter tagging models and expose the API key via environment variable for skills

## Signal Studio story pipeline  (3 actions, 0 live)

- [STALE 2026-03-31] Relook the story implementation against the original document and expand it to cover all fields and user controls
- [STALE 2026-03-31] Produce comprehensive handover message for the story 5.3 upgrade drawing on 0.7 learnings
- [STALE 2026-03-31] Fix the data schema and spin up an epic zero to hand data over to the Signal Studio system

## agentic OS slide deck  (3 actions, 0 live)

- [STALE 2026-03-31] Revise system diagram: agent-layer ratios, Paperclip as external autonomous system, Mythos badge top-right
- [STALE 2026-03-31] Rebuild page one as simple horizontal + vertical Agentic OS slides with the four development sections and Lars integration gaps
- [STALE 2026-03-31] Add one wow-factor slide teasing exclusive Anthropic access, leaving the rest of the deck unchanged

## Lars system  (3 actions, 0 live)

- [STALE 2026-04-01] Verify Tailscale and Ansible are actually working on Lars' system
- [STALE 2026-04-01] Set up a Dropbox knowledge-sharing pattern between Lars' agents
- [STALE 2026-04-01] Implement/fix push capabilities so incidents appear on the push dashboard with meaningful error messages

## Linear  (3 actions, 1 live)

- [LIVE 2026-07-04] Validate ticket 176 tests then close it; open 192 in a new session; defer 191 until loose ends are cleaned
- [RECENT 2026-06-12] Update Linear for the Spec C coding handoff and produce a paste-ready handover message
- [RECENT 2026-06-12] Create Linear ticket for the completed Spec A work against the correct project

## Kybernesis  (3 actions, 3 live)

- [LIVE 2026-07-12] Raise Kybernesis tickets for missing SDK/host capabilities (e.g. daemon-managed cron invoking extension hooks) and refactor the extension to offload them later
- [LIVE 2026-07-03] Decide the GitHub organization name for extension repos (appydave-kyber / kybernesis / kyber-extensions)
- [LIVE 2026-06-27] Decide who leads the Angela consulting engagement and where the Kybernesis consulting line sits (peer to discuss with Ian)

## Gling  (3 actions, 3 live)

- [LIVE 2026-07-11] Investigate injecting an MCP/API control layer into the unobfuscated Gling Electron app at startup, starting from the existing Gling second-brain notes
- [LIVE 2026-07-11] Add automation hooks (add video, open project, remote control) directly into the application via a TS/JS library instead of recreating Gling
- [LIVE 2026-07-04] Cancel/avoid Gling.ai subscription renewal before the upcoming charge

## Achieve MVP  (3 actions, 3 live)

- [LIVE 2026-07-09] Run AI analysis across legacy/current/v2 SupportSignal apps and DSP documentation (moments-that-matter) to map JSON structures for workflows and data shapes
- [LIVE 2026-07-09] Build synthetic-data agents plus read-only micro-app/dashboard visualizations from those schemas
- [LIVE 2026-07-09] Break the merged 30,000-ft process flow into red-circled project areas ordered by dependency chain

## v-voz repo  (2 actions, 0 live)

- [STALE 2026-01-10] Voz to explore the generated docs via Claude starter questions before reconnecting next week
- [STALE 2026-01-10] Set up the video project folder with starter files and a README documenting the full expected structure

## workspace hardware  (2 actions, 0 live)

- [STALE 2026-01-11] Order Stream Deck Plus online (available ~Jan 13)
- [STALE 2026-01-11] Buy Stream Deck Neo immediately to experiment with

## v-Voz repo / Languish the Artist  (2 actions, 0 live)

- [STALE 2026-01-13] Fix readability of story 4.1-4.3 command cheat sheets and update the audit trail from the correct Voz client directory
- [STALE 2026-01-13] Analyze the story 4.3 mock generator (images 3-5): what it does, why it falls short, proposed better approach — before changing anything

## Chiang Mai AI Community governance  (2 actions, 0 live)

- [STALE 2026-01-16] Schedule online call with Marcus next week re group ownership, governance, and folding his Saturday meetup into the shared model
- [STALE 2026-01-16] Let the council pick the group name from the shortlist (Compact, Hive, Loom, Lurk, North Star)

## POEM OS port registry  (2 actions, 0 live)

- [STALE 2026-01-22] Fix POEM port registry to list all registered ports, not just the collision
- [STALE 2026-01-22] Clean up port registry so every registered port has a name and folder, and identify what 'installation 17689' is

## ChatGPT  (2 actions, 0 live)

- [STALE 2026-04-01] Create a reusable ChatGPT prompt comparing iCloud, Dropbox and the current Syncthing setup
- [STALE 2026-01-31] Open a new ChatGPT chat, paste the Loom transcript as seed context, generate scenario categories for the 20 scripts, then annotate each script with 2 scenarios and 3 hooks plus a suggested outro

## content-production  (2 actions, 0 live)

- [STALE 2026-01-31] Engage Guy at a lower consistent monthly rate to cut livestream footage, with Jan doing polish, republished to the AppyDave channel
- [STALE 2026-01-31] Bring video materials and instructions to the collaborator today or tomorrow so he can start producing the videos

## SupportSignal migration tracking docs  (2 actions, 0 live)

- [STALE 2026-02-02] Update migration tracking data and the failed-tests section with the new count (169)
- [STALE 2026-02-02] Confirm migration/testing documentation was updated with the files fixed in batch 24

## Claude Code async orchestration  (2 actions, 0 live)

- [STALE 2026-02-02] Start comms integration with Telegram only; document other channel options for later
- [STALE 2026-02-02] Proceed with option A (recommended approach) for async multi-agent execution

## Beauty & Joy shop marketing  (2 actions, 0 live)

- [STALE 2026-02-10] Research flyer and loyalty card printing options in Chiang Mai (local printers vs GogoPrint online)
- [STALE 2026-02-10] Design professional dual-brand flyers (nail + juice) with map, QR code, and writable specials area

## KDD system  (2 actions, 0 live)

- [STALE 2026-02-10] Keep migration lessons with the migration docs; route any KDD entry through the librarian
- [STALE 2026-02-10] Create KDD learnings via the librarian so a future full rebuild avoids these mistakes

## project repo  (2 actions, 0 live)

- [STALE 2026-02-10] Establish and document a stamp-in-time baseline commit enabling rollback and commit retrospectives before the test-migration campaign
- [STALE 2026-02-10] Create s9 web test following s4 and start.sh script patterns (don't touch legacy s5/s8)

## learnings docs  (2 actions, 0 live)

- [STALE 2026-02-10] Document session learnings (haiku-vs-OSS comparison, librarian QC bot concept) plus a handover before context runs out
- [STALE 2026-02-10] Capture voice/ElevenLabs mistake learnings and confirm config changes go through the ElevenLabs skill

## validation script  (2 actions, 0 live)

- [STALE 2026-02-10] Rerun broken-links validation writing output directly into the conversation folder (no hidden files)
- [STALE 2026-02-10] Adopt RuboCop-style ignore-comment pattern so the Python link-validation tool auto-skips marked items

## Beauty & Joy content pipeline  (2 actions, 0 live)

- [STALE 2026-02-12] Joy to photograph every nail art item individually on a white background and send all photos to David
- [STALE 2026-02-12] Ask Mary to create a Beauty & Joy nail art video from Joy's photos

## fruit shop art experiment  (2 actions, 0 live)

- [STALE 2026-02-12] Have staff (Cat) take many photos of the fruit shop inside and outside
- [STALE 2026-02-12] Generate AI painted-art design concepts over the shop photos before deciding what to physically paint

## Joy Tours  (2 actions, 0 live)

- [STALE 2026-02-13] Use AI to generate experience-package ideas for the shop and scout Thai providers to resell
- [STALE 2026-02-13] Set up Joy Tours as third business brand and list packaged experiences (nail art classes, mocktails, tours) on Ian's booking platform at launch

## juice shop  (2 actions, 0 live)

- [STALE 2026-03-02] Buy rubber foam and silicone glue for the low-ceiling display fix
- [STALE 2026-02-20] Buy a blender so the juice shop can open

## AWB workflow POC  (2 actions, 0 live)

- [STALE 2026-02-21] Use client-server architecture with the server handling engine and Claude token authenticator communication
- [STALE 2026-02-21] Build the workflow POC isolated in its own folder/worktree on a B2B branch so it can be discarded later

## zsh config  (2 actions, 0 live)

- [STALE 2026-02-22] Move the configuration into its own dedicated aliases .zsh file
- [STALE 2026-02-22] Decide location and name for an ansible-playbook alias (general aliases vs alias-my)

## M4 Mini filesystem  (2 actions, 0 live)

- [STALE 2026-02-22] Show the delete-script list for review before running trash cleanup, then run du to explain 650GB used
- [STALE 2026-02-22] Audit trash folders across all yard project directories and report file count and total GB

## brains knowledge system  (2 actions, 0 live)

- [STALE 2026-03-08] Document how to access the delegation protocol in future sessions
- [STALE 2026-02-24] Restructure Obsidian findings as a data-oriented source of truth renderable to Markdown or Mermaid

## Claude Code skills  (2 actions, 0 live)

- [STALE 2026-03-12] Create the 'clotting lab event' skill: navigate the calendar site, document event-creation steps, set up as a recurring event
- [STALE 2026-02-24] Fold the teammate-communication and cleanup conventions into a skill later

## incident workflow web UI  (2 actions, 0 live)

- [STALE 2026-02-24] Update Angela's docs and package for an easy one-step way to run the app
- [STALE 2026-02-24] Stabilise the more advanced (currently broken) web UI version before handing to Angela

## email/Loom  (2 actions, 0 live)

- [STALE 2026-03-03] Send short packaged email with Loom to Lars about YouTube launch work today
- [STALE 2026-02-28] Send video update email to Lars

## repo audit tool  (2 actions, 0 live)

- [STALE 2026-02-28] Fix repo audit to report repo locations only, verify the code's accuracy, and make it rerunnable
- [STALE 2026-02-28] Add absolute file path and remote info to the folder view

## DTV VC group message  (2 actions, 0 live)

- [STALE 2026-02-28] Reframe the DTV VC group message to lead with the 'has anyone done DTV recently with a problem' question
- [STALE 2026-02-28] Frame a DTV VC group question combining David's original question with Stan Moore's response

## migration tracking file  (2 actions, 0 live)

- [STALE 2026-02-28] Update the existing copied/uncopied repository tracking file
- [STALE 2026-02-28] Create a machine-readable twin of the tracking file to support gap analysis

## team hardware  (2 actions, 0 live)

- [STALE 2026-03-09] Complete purchase of two Mac mini M4 512GB setups + LG 27US500-W monitors via Wise-loaded debit card, pickup SM North
- [STALE 2026-02-28] Jan to investigate 32-inch monitors for both staff machines

## prompt-patterns brain  (2 actions, 0 live)

- [STALE 2026-03-03] Update agent handshake pattern with lead/follower/mutual-collaborator roles and consistent per-pattern headers for future slide decks
- [STALE 2026-03-01] Research discovery-prompt and recipe prompt patterns and expand the framework if warranted

## agent-os  (2 actions, 0 live)

- [STALE 2026-03-01] Execute Project Theodore roadmap: Samantha voice loop, cross-machine coordination, overseas nodes, FliGen media production, morning briefing
- [STALE 2026-03-01] Design the application registry: shared-across-agents via Supabase bus vs local per-machine utilities, and its place in the vertical stack

## YouTube WAI workflow  (2 actions, 0 live)

- [STALE 2026-03-02] Run the ~15 UAT tests in a background agent using the workflow tool itself
- [STALE 2026-03-02] Run the UAT via the agent web browser focusing on the three key areas including aging

## iCare repair shop  (2 actions, 0 live)

- [STALE 2026-03-02] Take the MacBook Pro in for screen repair on March 3
- [STALE 2026-03-02] Bring the MacBook Pro in for AppleCare screen repair once backup completes

## workspace-automation brain  (2 actions, 0 live)

- [STALE 2026-03-03] Create a starter document capturing the discussed automation knowledge
- [STALE 2026-03-02] Commit and push all completed work

## Ansible fleet config  (2 actions, 0 live)

- [STALE 2026-03-02] Deep-research whether single-profile-only behavior is now achievable for the coding profile
- [STALE 2026-03-02] Check whether Ansible has access to the M4 Pro iTerm2 settings and explain why the past Hammerspoon layout attempt failed

## workspace-automation  (2 actions, 0 live)

- [STALE 2026-03-02] Research Moom company, pricing, and Moom Classic status vs Hammerspoon alternative
- [STALE 2026-03-02] Extract and document Rectangle/Moom install source, settings, and keyboard shortcuts from M4 Pro and M4 Mini (check Ansible config)

## brand-dave brain  (2 actions, 1 live)

- [LIVE 2026-07-13] Analyze the kybernesis.ai design system and produce a DESIGN.md under brand-dave
- [STALE 2026-03-02] Deep-research the Be Mad POEM slide-deck styling and produce a formal AppyDave style guide

## pattern-visualization app  (2 actions, 0 live)

- [STALE 2026-03-02] Determine which NPM publish steps automate fully and surface the human-in-the-loop points
- [STALE 2026-03-02] Design one-command install flow (port + app name) writing to a temp folder opened in Finder

## Byron branding agent (vOz)  (2 actions, 0 live)

- [STALE 2026-03-02] Test Byron GSB (studio view) and TV (project view) commands and fix the misspelled TV markdown file
- [STALE 2026-03-02] Create Next Agent file outlining the storyteller agent concept, role, problem, and name ideas

## lars communications folder  (2 actions, 0 live)

- [STALE 2026-03-03] Remove brand references, Jan/Mary contacts, draft-invoice concept and style guide from Lars materials
- [STALE 2026-03-03] Add raw inbox folder for unprocessed OMI transcripts

## lars brain  (2 actions, 0 live)

- [STALE 2026-03-05] Register Lars's available timeframes in the scheduling knowledge (as done previously for Voz)
- [STALE 2026-03-03] Process this kickoff recording into Lars's client brain

## FliHub workflow engine UI  (2 actions, 0 live)

- [STALE 2026-03-03] Investigate dev-tools panel remaining visible after debug-to-user mode switch and review debug-only enablement system
- [STALE 2026-03-03] Add minor UI hint marking JSON fields even before a real editor component exists

## FliHub workflow engine  (2 actions, 0 live)

- [STALE 2026-03-03] Research JSON editor components and plan integration into workflow UI and schemas
- [STALE 2026-03-03] Check/create unit test best-practices doc and decide tests for new component boundary

## RADAR backlog  (2 actions, 0 live)

- [STALE 2026-03-03] Add dedicated todo app concept to radar backlog with the new HTML-based layout
- [STALE 2026-03-03] Add Claude conversation-hooks watcher app to radar backlog

## brains research  (2 actions, 0 live)

- [STALE 2026-03-12] Run A/B research tests on the cloned memory systems and report build-vs-adopt findings
- [STALE 2026-03-03] Save ChatGPT agent-workflow conversation into markdown research doc

## brains/stream-deck  (2 actions, 0 live)

- [STALE 2026-03-05] Document the step-by-step pedal setup into the stream-deck documentation
- [STALE 2026-03-04] Write up the StreamDeck button to Ecamm Live scene mapping

## DTV visa compliance  (2 actions, 0 live)

- [STALE 2026-03-04] Phone call at 08:00 to discuss border-run details
- [STALE 2026-03-04] Book paid border-run service for Chong Chom crossing

## Playwright  (2 actions, 0 live)

- [STALE 2026-03-05] Use Playwright server to exercise the new onboarding UI end-to-end
- [STALE 2026-03-04] Visually test Dartmode using Playwright MCP

## app inventory  (2 actions, 0 live)

- [STALE 2026-03-05] Establish a unified audit log of all applications and decide where app knowledge lives
- [STALE 2026-03-05] Establish a unified audit log of all applications (experiments, client apps, internal tools) and decide where app planning knowledge lives

## agentic-os-ansible repo  (2 actions, 0 live)

- [STALE 2026-03-05] Promote shared machine settings up to the common all.yml group vars so they stay consistent across the fleet
- [STALE 2026-03-05] Document the remaining manual post-install configuration and permission steps that Ansible cannot automate

## Angela's machine  (2 actions, 0 live)

- [STALE 2026-03-05] Angela to install the Front End Designer skill via the Anthropic plugin system
- [STALE 2026-03-05] Angela to install a voice-typing tool such as Whisper Flow

## Ansible fleet playbooks  (2 actions, 0 live)

- [STALE 2026-03-05] Investigate and fix the Ansible playbook so it never SSHes into the machine it is already running on (M4 Mini)
- [STALE 2026-03-05] Fix Earful configuration and rerun the escort playbook against the M4 Mini

## content pipeline  (2 actions, 0 live)

- [STALE 2026-03-06] Gather everything built/discovered in the skills reverse-engineering and draft a verbal plan for an under-8-minute video with JSON slide structures
- [STALE 2026-03-05] List the six video concepts including the FliHub/Ecamm-competition video and YouTube Shop to Miser

## anthropic-claude brain  (2 actions, 0 live)

- [STALE 2026-03-12] Research top open-source observability contenders (stars, commit activity) adaptable to Claude Code
- [STALE 2026-03-06] Add a high-level index of interesting new Claude Code capabilities to the anthropic-claude brain

## Agent Workflow Builder / slide app  (2 actions, 0 live)

- [STALE 2026-03-06] Research web-component and DOM alternatives to iframes for embedding styled slide components, via background agent
- [STALE 2026-03-06] Build and work through a consolidated task list covering unit tests, architecture review, dead code, API contracts, and type safety

## todo  (2 actions, 0 live)

- [STALE 2026-03-06] Track the January 24 country-acceptance deadline
- [STALE 2026-03-06] Set advance reminder for the US-dollar task a few days before it is due

## AppyDave ecosystem  (2 actions, 0 live)

- [STALE 2026-03-11] Decide the repo name and absolute local path for the BMAD learnings before the brains-restructure move
- [STALE 2026-03-11] Create liaison files for Jan and Brian as a recurring collaborator pattern

## SupportSignal MVP  (2 actions, 0 live)

- [STALE 2026-03-11] Run the app with Playwright MCP in a background agent for a UX/accessibility review (font/icon sizes, no scrollbars, no sidebar wrapping)
- [STALE 2026-03-11] Clean up uncommitted work and stray worktrees, then feed backlog + quality-of-life items into a Ralphy planning session

## vOz studio agents  (2 actions, 0 live)

- [STALE 2026-03-13] Have Byron create a starter org chart and discuss the first three hypothetical hires with Voss, Jan and Kip
- [STALE 2026-03-13] Byron writes a studio-state report for David; Jan forwards it through

## requirements doc  (2 actions, 0 live)

- [STALE 2026-03-16] Rewrite FR14 and apply the remaining functional-requirement changes before moving to the next section
- [STALE 2026-03-16] Add SaaS B2B tier (pricing TBA) and role-based authentication requirements into the system

## SupportSignal v2 planning  (2 actions, 0 live)

- [STALE 2026-03-16] Rewrite the BMAD task list into one contiguous planning flow to feed the BMAD session
- [STALE 2026-03-16] Research pros/cons of greenfield vs brownfield using BMAD files, the legacy Convex app, Signal Studio MVP and planning docs

## local LLM benchmarking harness  (2 actions, 0 live)

- [STALE 2026-03-28] Pull Phi-4 14B, Gemma 3 12B, Llama 3 8B, Qwen 2.5 and present a 4-5 prompt test plan across the five target brains
- [STALE 2026-03-28] Kick off background-agent tag ontology execution (serialised where agents share the llama model) on David's go signal

## slide deck  (2 actions, 0 live)

- [STALE 2026-04-01] List technologies to implement including Hermes and order them into a next-steps slide
- [STALE 2026-04-01] Generate a basic three-slide deck in the hand-drawn soft-pencil style, adding OMI and OMI scheduling to the list

## relay skill (appydave-plugins)  (2 actions, 0 live)

- [STALE 2026-04-01] Update the relay skill via skill-creator: relay info/help command, full folder paths plus Syncthing IDs, non-destructive handling of existing folders (disconnect Syncthing share first), folder patterns across internal/public privacy types
- [STALE 2026-04-01] Once folder and relay conventions are settled, update the relay skills to match

## Claude Code setup  (2 actions, 0 live)

- [STALE 2026-04-01] Verify downloaded repos are original (not reshaped) and identify the trusted source of truth
- [STALE 2026-04-01] Audit prior session activity for exfiltration or prompt-injection exposure

## Lars Dropbox relay  (2 actions, 0 live)

- [STALE 2026-04-02] Place omiscript in the shared memory system now and plan a proper repository home
- [STALE 2026-04-02] Design a sustainable folder structure for recurring education sessions and accumulating shared brain knowledge

## Storyline app  (2 actions, 0 live)

- [STALE 2026-04-02] Build requirements document for the new Storyline app referencing the original app's JSON structures
- [STALE 2026-04-02] Build a requirements document for the storyline/previs application to feed the early-access Anthropic app-builder

## vOz  (2 actions, 0 live)

- [STALE 2026-04-02] Send Voz a link to buy an OMI device and route the OMI explainer document to Jan
- [STALE 2026-04-02] Organize ~3-hour brainstorming session with Kip/vOz team plus the shot-by-shot book author on movie-creation requirements

## AWB docs  (2 actions, 0 live)

- [STALE 2026-04-06] Write three m-prefixed marketing documents reframing the product for selling/explaining
- [STALE 2026-04-06] Write the d33 document to finish the d-series planning set

## app tracker (app-01)  (2 actions, 0 live)

- [STALE 2026-04-11] Research the prior AppyDave 30-apps-in-30-days tracking experiment and draft app tracker requirements
- [STALE 2026-04-11] Draft starter requirements for skills management and YouTube video management sibling apps, then decide where requirements docs live

## brain probe system  (2 actions, 0 live)

- [RECENT 2026-06-12] Run wave two on the probes in a background agent after coding starts
- [RECENT 2026-06-12] Produce handover documents for the spec-writing and probe-running systems so probes account for the 375 missing files

## voice script writer system  (2 actions, 0 live)

- [RECENT 2026-06-14] Redesign voice script writer blueprint as a coordinated multi-agent (Mochaccino-style) pattern or propose a better concept
- [RECENT 2026-06-14] Deep-research the MVC pattern applied to tone-of-voice script writing, including distilling the full video transcript corpus into a voice/design document

## KDD/Lisa  (2 actions, 2 live)

- [LIVE 2026-07-03] Write a pasteable high-level synopsis of the KDD structure for sharing
- [LIVE 2026-07-03] Adopt a .kdd dotfolder inside the project as interim home for KDD working/archive files, then migrate when the KDD home exists

## OMI Ingestor app  (2 actions, 2 live)

- [LIVE 2026-07-04] Introduce a sequential primary-key code scheme (A00–A99 → B00... pattern, sized for volume) for OMI list items
- [LIVE 2026-07-04] Add ontology, tagging, and synopsis metadata (with a detail toggle) to items in the OMI list view

## skill registry (skills-tooling)  (2 actions, 2 live)

- [LIVE 2026-07-04] Design skill registry data structures covering last-accessed, staleness, and captured learnings per skill
- [LIVE 2026-07-04] Build dynamic search/filter (name, description, taxonomy, type-ahead) plus a skill detail viewer

## captains-log  (2 actions, 2 live)

- [LIVE 2026-07-05] Suggest 3-4 names for the unified ingestion controller tool
- [LIVE 2026-07-05] Compare OMI vs Plaud transcript data structures for format quirks before unifying

## dark-factory  (2 actions, 2 live)

- [LIVE 2026-07-06] Write Dark Factory ticket for Captain's Log extension (duplicate capture of same directive)
- [LIVE 2026-07-06] Write Dark Factory ticket for Captain's Log extension (conversation ingestion visibility, project mapping, machine-routing telemetry) and add to pipeline

## kyberagent  (2 actions, 2 live)

- [LIVE 2026-07-06] Set up a KyberAgent on Roamy that watches Kybernesis product documentation repos with a searchable brain
- [LIVE 2026-07-06] Set up KyberAgent docs-watcher on Roamy (duplicate capture of same directive)

## Gmail  (2 actions, 2 live)

- [LIVE 2026-07-13] Answer the Challenge DV contact's last email (Canva how-to) and pitch the demo plus A$3,300/month FDE retainer
- [LIVE 2026-07-12] Gather and assess all affiliate inquiry emails (scam/real/follow-up/forgotten outreach) and draft responses

## auto-claude brain  (1 actions, 0 live)

- [STALE 2026-01-09] Analyze Autoclawed codebase and produce complexity + RAG-quality + Claude-spawning analysis report

## stream-deck brain  (1 actions, 0 live)

- [STALE 2026-01-11] Research why Stream Decks fail through USB hubs vs direct USB-C connection

## AI macro keyboard project  (1 actions, 0 live)

- [STALE 2026-01-11] Run a weekend hackathon to proof-of-concept the AI macro keyboard on existing StreamDecks (David loaning his small unit), then design custom hardware and launch a Kickstarter

## iTerm  (1 actions, 0 live)

- [STALE 2026-01-11] Investigate why iTerm Cmd+Shift+D stopped splitting terminals

## Voz client correspondence  (1 actions, 0 live)

- [STALE 2026-01-13] Draft scheduling email to Voz offering Wednesday or Thursday with both time zones shown

## friend's YouTube/outreach setup  (1 actions, 0 live)

- [STALE 2026-01-15] Help the friend systematize his YouTube posting and simple email outreach (offer made)

## vibe coding harness project  (1 actions, 0 live)

- [STALE 2026-01-15] Continue the 50-week harness series: add one small app per weekly session on top of the week-1 harness

## Claude Code settings  (1 actions, 0 live)

- [STALE 2026-01-16] Investigate why plan files ignore the global plan-location setting and land in the wrong folder

## Chiang Mai AI Community events  (1 actions, 0 live)

- [STALE 2026-01-16] Run the Saturday Jan 24 test meetup at the new venue (locked in)

## Shopee  (1 actions, 0 live)

- [STALE 2026-01-19] Buy the push-to-talk hardware device via Shopee

## teammate Windows machine  (1 actions, 0 live)

- [STALE 2026-01-22] Teammate to fix Windows/WSL environment and learn Claude conversation resumption

## Remotion  (1 actions, 0 live)

- [STALE 2026-01-31] Re-familiarize with Remotion + the new Claude skill, make 4-5 sample videos, then hand the team 10 categories with 5 image prompts each for 10 Remotion videos

## Ecamm Live support  (1 actions, 0 live)

- [STALE 2026-01-31] Write and send debug email to Ecamm support explaining Twitter/X auth spinner issue and asking how to check logs

## Whisper research  (1 actions, 0 live)

- [STALE 2026-01-31] Determine Whisper free developer plan limits for ~8h/day intermittent streaming transcription

## salon marketing initiative  (1 actions, 0 live)

- [STALE 2026-02-02] Identify a salon employee with daily AI marketing production as a formal job responsibility

## test suite project  (1 actions, 0 live)

- [STALE 2026-02-02] Reprocess and regroup the test-failure list, then fix or delete-with-documented-intent

## SupportSignal test suites  (1 actions, 0 live)

- [STALE 2026-02-02] Index the locations of all Vitest migration fixes/learnings for transfer to React and Cloudflare Worker tests

## SupportSignal migration audit file  (1 actions, 0 live)

- [STALE 2026-02-02] Process group-one failing tests to zero, updating status + timestamp per file in the audit file

## SupportSignal codebase  (1 actions, 0 live)

- [STALE 2026-02-02] Investigate whether production code was changed to hide breakage behind passing tests (report only)

## SupportSignal repo  (1 actions, 0 live)

- [STALE 2026-02-02] Commit the current work regardless of optional items

## Lexi  (1 actions, 0 live)

- [STALE 2026-02-02] Kick off the librarian to extract learnings from this session

## handover-pattern skill / Claude Code handover instructions  (1 actions, 0 live)

- [STALE 2026-02-02] Update handover format and instructions: explicitly name the chosen next action, mark other options as future plans

## SupportSignal test migration  (1 actions, 0 live)

- [STALE 2026-02-02] Run the migration verification protocol

## SupportSignal test suite  (1 actions, 0 live)

- [STALE 2026-02-02] Verify tests were truly migrated from old system, not invented; focus on fixing what was broken

## Lisa / SupportSignal test suite  (1 actions, 0 live)

- [STALE 2026-02-02] Run Lisa health-check commands to identify remaining gaps blocking A+ grade

## Claude Code background agent  (1 actions, 0 live)

- [STALE 2026-02-02] Hand phase three continuation off to a background agent and await its feedback

## session workflow / handover document  (1 actions, 0 live)

- [STALE 2026-02-02] Adopt option A rolling task management with ~6 hours/day commitment

## KDD documentation  (1 actions, 0 live)

- [STALE 2026-02-02] Compress replicated data-mesh content to summaries with links, preserving decision rationale/history

## migration repo  (1 actions, 0 live)

- [STALE 2026-02-02] Do NOT perform the previously requested commit

## migration project tracking  (1 actions, 0 live)

- [STALE 2026-02-02] Search stories, issues, and backlogs for prior context on the migration problem

## BMAD/vMAD collaboration  (1 actions, 0 live)

- [STALE 2026-02-02] Connect during the week to discuss vMAD side-project collaboration

## meetup  (1 actions, 0 live)

- [STALE 2026-02-02] Pitch Shane a Thursday-night whiteboard/conversation session on Project Theodore (library venue)

## research  (1 actions, 0 live)

- [STALE 2026-02-07] Search for an existing index of video transcripts or content-tracking system to leverage

## AppyDave  (1 actions, 0 live)

- [STALE 2026-02-07] Record an Opus 4.6 video building an ElevenLabs voice agent

## Beauty & Joy socials  (1 actions, 0 live)

- [STALE 2026-02-10] Joy to post all her nail designs on social media today

## rebuild project scripts  (1 actions, 0 live)

- [STALE 2026-02-10] Rerun the script at session end and diagnose files where directives are not recognized

## rebuild project  (1 actions, 0 live)

- [STALE 2026-02-10] Save current state and produce a handover for a fresh conversation

## documentation system  (1 actions, 0 live)

- [STALE 2026-02-10] Deep-review all remaining documentation files and assign each a disposition (review, human input, delete, comment out)

## agent-launch.ai  (1 actions, 0 live)

- [STALE 2026-02-10] Get agent-launch.ai link and instructions from Tony's team to connect David's own agent

## KDD project  (1 actions, 0 live)

- [STALE 2026-02-10] Background task: determine whether meta-archive folders are archives or archiving instructions (naming-convention question)

## task list  (1 actions, 0 live)

- [STALE 2026-02-10] Add task to review all archive-related files before excluding them

## librarian docs  (1 actions, 0 live)

- [STALE 2026-02-10] Document the broken-link remediation pattern for librarian reuse and propagate it to the documentation system

## voice agent app  (1 actions, 0 live)

- [STALE 2026-02-10] Add console-log, conversation, and combined copy-to-clipboard debug buttons via a background agent, watching for log flood/recursion issues

## background agent research  (1 actions, 0 live)

- [STALE 2026-02-10] Research background-agent starter repositories and rank found SDKs by language and suitability for modeling

## voice agent setup  (1 actions, 0 live)

- [STALE 2026-02-10] Work out per-application audio input routing on macOS for voice agent vs Ecamm Live

## voice agent research  (1 actions, 0 live)

- [STALE 2026-02-10] Check whether the 11Labs sample orb application (which Ian based his Samantha on) was found during the repository research

## FliHub project repos  (1 actions, 0 live)

- [STALE 2026-02-12] Git add, commit, and push the 4-5 Opus video projects with updated package dependencies

## project workspace  (1 actions, 0 live)

- [STALE 2026-02-12] Delete the outdated installation file and prompt file, then move the remaining files

## assistant/Claude Code  (1 actions, 0 live)

- [STALE 2026-02-12] Prepare a 2-3 minute project status summary to context-load David at tomorrow's team call

## team learning / ComfyUI  (1 actions, 0 live)

- [STALE 2026-02-12] Team member to watch, understand, and potentially reproduce Steve's ComfyUI kie.ai workflow

## Steve / Skool  (1 actions, 0 live)

- [STALE 2026-02-12] Send Steve the recorded feedback: publish the ComfyUI JSON + auto-generated blog post in his Skool community

## Beauty & Joy shop  (1 actions, 0 live)

- [STALE 2026-02-12] Set up a computer at the shop and have a video team member train staff on AI video tools

## Ralph Wiggum loop agent  (1 actions, 0 live)

- [STALE 2026-02-12] Always label generated audio as AI or human going forward

## SupportSignal training  (1 actions, 0 live)

- [STALE 2026-02-12] Send Angela two more Loom training videos and check in tomorrow health permitting

## SupportSignal sales  (1 actions, 0 live)

- [STALE 2026-02-12] Angela to seek AMS commitment to a trial site at Tuesday meeting

## SupportSignal KDD  (1 actions, 0 live)

- [STALE 2026-02-12] Silo experimental Convex-vs-React testing patterns from the main KDD until ratified; remove redundant KDD files (not archive)

## Agent OS brain  (1 actions, 0 live)

- [STALE 2026-02-12] Dispatch a background agent to investigate the new subsidiary CLI and load findings into the Agent OS brain

## testing-patterns brain  (1 actions, 0 live)

- [STALE 2026-02-13] Merge the Playwright MCP debugging guide with the existing testing resource into one file and install it

## Agentic OS  (1 actions, 0 live)

- [STALE 2026-02-20] Add Slack integration to Ansible and potentially the agentic OS

## Skyscanner  (1 actions, 0 live)

- [STALE 2026-02-20] Check flights to Vietnam or Malaysia for the March 24 visa exit

## Dent platform  (1 actions, 0 live)

- [STALE 2026-02-20] Finish the value canvas through pain, deep fear, and prize sections

## Luma  (1 actions, 0 live)

- [STALE 2026-02-21] Set up David's Friday event as a Luma event for easier distribution

## Ansible / fleet provisioning  (1 actions, 0 live)

- [STALE 2026-02-22] Compare both machines' configs via Claude over SSH to diagnose drift

## fleet/Ansible  (1 actions, 0 live)

- [STALE 2026-02-22] Check whether anything changed on the M2 that should be ported to the M4

## Ansible  (1 actions, 0 live)

- [STALE 2026-02-22] Rerun playbook checks for M2 and M4 from within Claude and rectify issues

## fleet hardware  (1 actions, 0 live)

- [STALE 2026-02-22] Buy/price the new Macs for Jan and Mary at end of month and wire them into the Tailscale network

## Mac mini M2  (1 actions, 0 live)

- [STALE 2026-02-22] Identify the correct network name of the Mac mini M2 (find, do not recreate)

## Tailscale  (1 actions, 0 live)

- [STALE 2026-02-22] Research and reconcile Tailscale vs Start Tailscale app usage

## ralphy skill/plugin  (1 actions, 0 live)

- [STALE 2026-02-24] Document open items, updated paths (brain vs skill), and renderer propagation so a new campaign can start in a separate conversation

## ralphy campaign  (1 actions, 0 live)

- [STALE 2026-02-24] Upload the assessment document to a temp folder for the Ralph loop to process

## FliVideo/FliHub content pipeline  (1 actions, 0 live)

- [STALE 2026-02-24] Add copy-raw-text-to-clipboard button next to SRT files wherever they appear, starting with S3 staging

## workflow repo  (1 actions, 0 live)

- [STALE 2026-02-24] Track or ignore the .obsidian folder so git commits leave a clean tree

## SupportSignal incident app  (1 actions, 0 live)

- [STALE 2026-02-24] Produce a simple UAT checklist covering all manual tests for incident participant data

## npm/RubyGems accounts  (1 actions, 0 live)

- [STALE 2026-02-24] Find the semantic-versioning NPM package/gem and the cluelessjs account details

## til brain  (1 actions, 0 live)

- [STALE 2026-02-24] Process the LLM SaaS text-stats lab conversation into a TIL entry

## agentic-os fleet  (1 actions, 0 live)

- [STALE 2026-02-24] Give every fleet machine its own email, GitHub account, and SSH keys for isolation

## agent-os Ansible  (1 actions, 0 live)

- [STALE 2026-02-24] Get shell aliases and dotfiles consistently deployed via the Ansible playbook (last run did not apply the change)

## machine-control / SSH setup  (1 actions, 0 live)

- [STALE 2026-02-24] Fix SSH shell environment loading so remote Claude Code sees Homebrew/tmux

## git tooling  (1 actions, 0 live)

- [STALE 2026-02-28] Build a script to commit and push all 00x subfolders with remote-existence checking

## machine-control brain / Ansible  (1 actions, 0 live)

- [STALE 2026-02-28] Document remote access + Screen Sharing vs Remote Management troubleshooting for MBP-M4 bidirectional sessions

## audit system  (1 actions, 0 live)

- [STALE 2026-02-28] Check and resolve the DS_Store noise issue and add pre-emptive noise concepts to the audit system

## M4 git configuration  (1 actions, 0 live)

- [STALE 2026-02-28] Produce the list of files to add to git config on the other computer

## migration disk cleanup  (1 actions, 0 live)

- [STALE 2026-02-28] Run du to identify top 5 disk-consuming folders and flag safe low-value deletions

## mural design project  (1 actions, 0 live)

- [STALE 2026-02-28] Reconvene with the designer next week (Tue/Wed) to decide mural design and price

## VS Code setup  (1 actions, 0 live)

- [STALE 2026-02-28] Remove/disable the 'build with agent' component from the fresh VS Code install

## migration gap analysis  (1 actions, 0 live)

- [STALE 2026-02-28] Spin up a background agent to gap-analyse non-dev folders that were never requested for transfer

## repository cleanup  (1 actions, 0 live)

- [STALE 2026-02-28] Remove dead repos and the historical folder (keep Canva only if it contains images)

## team payroll  (1 actions, 0 live)

- [STALE 2026-02-28] Send Mary's bank details to Daniel so he can make the payment by tomorrow

## architecture visualization  (1 actions, 0 live)

- [STALE 2026-02-28] Send JSON workflow structures to meetup friend so he can propose prompts/image concepts to visualize and animate agent architectures

## brains/kie-ai  (1 actions, 0 live)

- [STALE 2026-03-01] Refresh kie-ai brain with NanoBanana 2 and web-search-grounded image generation for infographics

## fleet provisioning (Ansible)  (1 actions, 0 live)

- [STALE 2026-03-01] Adopt a tool to provision new machines with a consistent software set

## fleet SSH (machine-control)  (1 actions, 0 live)

- [STALE 2026-03-01] Audit size/file count of /Users/davidcruwys/images on the M4 Pro and copy it to the current machine

## M4 Pro MacBook  (1 actions, 0 live)

- [STALE 2026-03-01] Fix the MacBook hostname and run system updates

## presentation assets  (1 actions, 0 live)

- [STALE 2026-03-01] Share horizontal OS, agentic OS, and personal-agent slide decks with requesters

## presentation (ai-meetups)  (1 actions, 0 live)

- [STALE 2026-03-01] Build the session: architecture slides, second-brain + librarian demo, AppyStack micro-app generation from extracted data

## session copy / brand-dave  (1 actions, 0 live)

- [STALE 2026-03-01] Fix bio to 'since 1990' and 'educator of BMAD method, not creator' in the session copy and system text

## session copy  (1 actions, 0 live)

- [STALE 2026-03-01] Produce five alternative session titles and a goal-based rewrite of the session description

## brand-dave/dent docs  (1 actions, 0 live)

- [STALE 2026-03-01] Collect brand + Dent JSON documents into a temp folder and open in Finder

## colleague handover  (1 actions, 0 live)

- [STALE 2026-03-01] Draft a message to a colleague about converting the JSON docs into infographics or diagrams

## agentic-os planning  (1 actions, 0 live)

- [STALE 2026-03-01] Fill out the 'Agents in the World' document

## AppleCare  (1 actions, 0 live)

- [STALE 2026-03-01] Take the 10-month-old MacBook with failed display to AppleCare for repair

## Joy's shop  (1 actions, 0 live)

- [STALE 2026-03-01] Start free sample-drink promotion (shot glasses of green tea soda) before the shop is fully open

## personal finances  (1 actions, 0 live)

- [STALE 2026-03-01] Transfer money and pay Jen, Mary, Cat, and Joy's mother; chase incoming payments from Ronnie and Lars

## Facebook  (1 actions, 0 live)

- [STALE 2026-03-01] Clean up and post the warranty-repair help request to the Chiang Mai Facebook group

## NotebookLM / Joy Juice branding  (1 actions, 0 live)

- [STALE 2026-03-02] Create image prompt three and a style-guide prompt listing the eight fruits side by side

## Joy Juice asset folder  (1 actions, 0 live)

- [STALE 2026-03-02] Provide an absolute path / Finder location for dropping Joy Juice images

## brand-dave  (1 actions, 0 live)

- [STALE 2026-03-02] Re-evaluate the Joy Juice name — decide what the juice store brand really is

## juice shop notes  (1 actions, 0 live)

- [STALE 2026-03-02] Write up the frozen-product/avocado ideas in Thai

## machine-control  (1 actions, 0 live)

- [STALE 2026-03-02] Persist fleet machine SSH/hostname connection details so they never need re-supplying

## app pipeline  (1 actions, 0 live)

- [STALE 2026-03-02] Add todo: brand management application (or DB-driven document management system) pulling info from AI-TLDR and elsewhere

## SupportSignal micro app repo  (1 actions, 0 live)

- [STALE 2026-03-02] Find the -bak sibling folder's remote and push current code there (history reset acceptable)

## SupportSignal prompt workspace  (1 actions, 0 live)

- [STALE 2026-03-02] Commit current project state to the repository

## YouTube WAI docs  (1 actions, 0 live)

- [STALE 2026-03-02] Document the IR compiler and HTML runner (YAML + Handlebars wizard UI) clearly in the handover doc, then commit and push

## brains/workspace-automation  (1 actions, 0 live)

- [STALE 2026-03-02] Check the brain workspace automation folder for the previously chosen application name

## workspace-automation app  (1 actions, 0 live)

- [STALE 2026-03-02] Produce 2-3 alternative names for the Mac Window Layout Engine app

## AppyDave/AI-TLDR channels  (1 actions, 0 live)

- [STALE 2026-03-02] Make a dedicated video featuring Ian's Kybernesis products rather than just mentions

## Signal Studio repo  (1 actions, 0 live)

- [STALE 2026-03-02] Force-push the updated repo so Angela can git pull, npm install, npm run dev

## Ronnie meeting  (1 actions, 0 live)

- [STALE 2026-03-02] Angela to message Ronnie postponing the 12:00 meeting to a Wednesday progress report

## Signal Studio onboarding tool  (1 actions, 0 live)

- [STALE 2026-03-02] Set up the Angela_feedback.md capture workflow with CLAUDE.md instructions and a single schema definition David owns

## Signal Studio codebase  (1 actions, 0 live)

- [STALE 2026-03-02] Run a deep background review of the session's changes, refactor, then plan comprehensive tests and coverage

## Signal Studio onboarding app  (1 actions, 0 live)

- [STALE 2026-03-02] Git pull, resolve the dev environment index issue, and fix outstanding problems as needed

## juice shop menu pipeline  (1 actions, 0 live)

- [STALE 2026-03-02] Generate bilingual A4 laminated comparison cards with clear pricing for the top 10 drinks using AI

## Gather skill  (1 actions, 0 live)

- [STALE 2026-03-02] Add Gather command that converts a JSON folder into a transient markdown doc with diagram/style header for NotebookLM

## Moments That Matter app (AppyStack)  (1 actions, 0 live)

- [STALE 2026-03-02] Build CRUD management, focus-employee selector, and moments-that-matter record entry following the file-CRUD recipe with root data folder

## upstream repo  (1 actions, 0 live)

- [STALE 2026-03-02] Migrate indie-dev-dan transcripts to upstream/tubescripts, drop the 'review' name, and verify system health after

## indiedevdan brain  (1 actions, 0 live)

- [STALE 2026-03-02] Write a small markdown doc describing each indie-dev-dan tool (what/why/how) and the future skill option

## vOz machines  (1 actions, 0 live)

- [STALE 2026-03-02] Work out MacBook-to-Mac-mini push/pull sync workflow for Voss before daylight-savings schedule shift

## OMI/Stream Deck  (1 actions, 0 live)

- [STALE 2026-03-03] Resolve OMI import blocker first, then set up 2-5 basic Stream Deck scenes and buttons

## lars client repo (GitHub)  (1 actions, 0 live)

- [STALE 2026-03-03] Fix broken agentic-OS links in README, commit and push

## jump / locations.json  (1 actions, 0 live)

- [STALE 2026-03-03] Create jLars jump command mirroring jVoz

## hardware procurement  (1 actions, 0 live)

- [STALE 2026-03-03] Choose and validate 4K monitors for staff, including checking the suspiciously cheap Samsung listing

## AI image tools  (1 actions, 0 live)

- [STALE 2026-03-03] Generate per-fruit bilingual A4 poster set (Thai style vs natural style) for the ~10 main fruits

## ansible repo (GitHub)  (1 actions, 0 live)

- [STALE 2026-03-03] Add repo description, detailed agent-first README, and flip visibility to public once private data removed

## Signal Studio backlog  (1 actions, 0 live)

- [STALE 2026-03-03] Angela to exercise the app and log desired changes as separate line items

## ansible / machine docs  (1 actions, 0 live)

- [STALE 2026-03-03] Document HyperX QuadCast mic gain/input/angle config for the M4 Mini creator machine

## brains/ecamm-audio-setup  (1 actions, 0 live)

- [STALE 2026-03-03] Document final HyperX QuadCast gain/input-volume settings

## video editing (C18)  (1 actions, 0 live)

- [STALE 2026-03-03] Fix C18 intro to start on-camera per brand style and research pattern-break timing formulas

## FliHub workflow engine docs  (1 actions, 0 live)

- [STALE 2026-03-03] Document how textarea/grower sizing is determined in workflow docs

## Claude Code agent conventions  (1 actions, 0 live)

- [STALE 2026-03-03] Always include absolute filesystem paths in agent responses

## DeckHand / agentic OS  (1 actions, 0 live)

- [STALE 2026-03-03] Add app launch/position automations (WhatsApp, Finder, VS Code, Chrome, iTerm, Zoom, Ecamm) to button deck and integrate into agentic OS

## RADAR skill  (1 actions, 0 live)

- [STALE 2026-03-03] Add today.md contents plus brief summary output option to RADAR

## dtv  (1 actions, 0 live)

- [STALE 2026-03-04] Book the paid Chong Chom border-run service (transport + paperwork, ~2,000 baht plus fee)

## brains/openclaw  (1 actions, 0 live)

- [STALE 2026-03-04] Process OpenClaw meetup material into the inbox from the agentic-OS perspective

## brains/ecamm  (1 actions, 0 live)

- [STALE 2026-03-04] Map the full Ecamm Live playlist plist schema and figure out how to add Ecamm actions to it

## OMI transcript pipeline  (1 actions, 0 live)

- [STALE 2026-03-04] Create a new recipe for OMI transcript handling in the API generation system

## Ecamm API recipe  (1 actions, 0 live)

- [STALE 2026-03-04] Define requirements for a 100% complete API endpoint recipe with listable entities and Swagger-style testable APIs

## lab video project  (1 actions, 0 live)

- [STALE 2026-03-04] Show two lab video samples and walk through them with colleague tomorrow

## travel/DTV  (1 actions, 0 live)

- [STALE 2026-03-04] Book visa run as today's most critical task

## todo / video ideas  (1 actions, 0 live)

- [STALE 2026-03-05] Capture the five-plus video concepts (FliHub competition video, YouTube Shop to Miser) into a video-ideas home

## team video production  (1 actions, 0 live)

- [STALE 2026-03-05] Fix team video issues (sizing/contrast for mobile, ffmpeg --version, add Skool community CTA to every video) and build Kai/FAL image-to-video skills as foundations

## supportsignal-v2-planning  (1 actions, 0 live)

- [STALE 2026-03-05] Run folder-level gap analysis across supportsignal-v2-planning, .support-signal, incident workflow YAML, AWB, and Signal Studio; produce an eight-feature plan; set up a worktree, commit and push

## FliDeck  (1 actions, 0 live)

- [STALE 2026-03-05] Plan FliDeck handover: new capability to turn a batch of NotebookLM-generated images into a presentation (possibly via the iframe system); download and sequentially label the CDN images now

## video edit pipeline  (1 actions, 0 live)

- [STALE 2026-03-05] Shift audio alignment in the C20 video by five or six frames, then commit and push

## outgoing content batch  (1 actions, 0 live)

- [STALE 2026-03-05] Add this Loom to today's outgoing content batch, with more videos to follow

## AppyStack repo  (1 actions, 0 live)

- [STALE 2026-03-05] Commit and push the current code changes

## agentic OS docs  (1 actions, 0 live)

- [STALE 2026-03-05] Document how another app calls MLX Whisper from CLI or Python for social-media workflows

## upstream repos / agentic-os brain  (1 actions, 0 live)

- [STALE 2026-03-06] Clone NanoBot, NanoClaw, Pocket Hermes, and PicoClaw upstream repos and register them as agentic-OS research areas

## til / google-ai brain  (1 actions, 0 live)

- [STALE 2026-03-06] Research the Google Whisk + Flow merger and send David a summary

## active app session  (1 actions, 0 live)

- [STALE 2026-03-06] List all recently shipped changes and the steps to test them; fix Finder-open and clipboard-copy of folders

## macOS scripts / Stream Deck  (1 actions, 0 live)

- [STALE 2026-03-06] Create a scripts folder and an SC screen-capture command launchable by hotkey or Stream Deck instead of a terminal

## dev tooling  (1 actions, 0 live)

- [STALE 2026-03-06] Investigate the recurring port issue and define a reliable way to find the port

## Paperclip research  (1 actions, 0 live)

- [STALE 2026-03-06] Download MOTUS and compare its structure against Paperclip AI

## dtv brain + todo  (1 actions, 0 live)

- [STALE 2026-03-06] Research TDAC and Laos border-trip requirements, register learnings in DTV border-crossing area, and add lead-time tasks to the todo backlog

## team weekend discussion  (1 actions, 0 live)

- [STALE 2026-03-06] Jan to show the agent-first Loom video to Mary and discuss the agentic-first North Star over the weekend

## booking review  (1 actions, 0 live)

- [STALE 2026-03-06] Review the pending booking details for errors before payment

## voz agent workspace  (1 actions, 0 live)

- [STALE 2026-03-06] Voz+Jan complete Byron brand-strategist project-level definition and create overview.md listing studio agents from the Kip interview on Sunday

## kie.ai / fal.ai  (1 actions, 0 live)

- [STALE 2026-03-06] Voz sets up Kai (kie.ai) and FAL accounts with shared email+password auth, funded pay-per-use ($20-50)

## Wise / hardware procurement  (1 actions, 0 live)

- [STALE 2026-03-06] Voz wires US$2,500 to David via Wise; Jan surveys Manila pricing for two M4 Mac minis (512GB/16GB) plus 27-inch monitors for Jan and Mary

## streaming studio setup  (1 actions, 0 live)

- [STALE 2026-03-07] Hang existing spring-loaded screen as green screen (hook/bar, tension, low-temp iron) with backlight for separation

## ralphy skill (appydave plugin)  (1 actions, 0 live)

- [STALE 2026-03-07] Rename ralphy's numbered modes to descriptive labels: requirements / plan / build / extend

## image diff viewer / slide UAT pipeline  (1 actions, 0 live)

- [STALE 2026-03-07] Add top-level JSON manifest covering every image comparison with metric and perfect/has-issues status

## AppyDave YouTube content  (1 actions, 0 live)

- [STALE 2026-03-07] Record 4 videos: iframe-vs-web-component diff, image-renaming skill, AppyStack stat viewer, Ecamm Live skill

## juice shop operations  (1 actions, 0 live)

- [STALE 2026-03-07] Write nightly two-bag cash split (700+300 THB denominations) with 7-Eleven change replenishment; 60k THB target by March 30

## home video studio  (1 actions, 0 live)

- [STALE 2026-03-07] Joy to review existing lighting gear and buy bright white (not yellow) floor/wall lights via TikTok Shop

## knowledge-harvest / upstream tubescripts  (1 actions, 0 live)

- [STALE 2026-03-08] Re-search Dynamous community for member-only livestreams worth transcribing

## calendar / client-lars  (1 actions, 0 live)

- [STALE 2026-03-08] Schedule Wednesday 14:00 (David's time) follow-up call with Lars on second-brain setup

## agentic_os_ansible repo  (1 actions, 0 live)

- [STALE 2026-03-08] Add TODO in Ansible CLAUDE.md describing a starter/fork repo that mirrors the main system instead of giving clients write access

## agentic_os_ansible client template  (1 actions, 0 live)

- [STALE 2026-03-08] Separate David's personal macOS defaults from the client template playbook (locale EN-DK, light mode, scroll direction)

## brains / cole-medin  (1 actions, 0 live)

- [STALE 2026-03-08] Locate original Cole Medin/Dynamous git repo and verify current local system has all its materials

## DeckHand/AppyStack  (1 actions, 0 live)

- [STALE 2026-03-09] Commit clean app folder then build install-into-existing-directory with unit tests

## AppyStack/create-appystack  (1 actions, 0 live)

- [STALE 2026-03-09] Assess and design AppyStack installer refactor for install-into-existing-folder

## AppyStack docs/brain  (1 actions, 0 live)

- [STALE 2026-03-09] Write a detailed ElevenLabs integration recipe for AppyStack micro apps

## AppyStack docs  (1 actions, 0 live)

- [STALE 2026-03-09] Infer and document app naming rules from DeckHand/AppyStack/ThumbRack/FliVideo patterns

## AI-TLDR brand storage  (1 actions, 0 live)

- [STALE 2026-03-09] Mary to consolidate all AI-TLDR brand and affiliate materials into a new brand-AITLDR cloud folder

## AI-TLDR affiliate program  (1 actions, 0 live)

- [STALE 2026-03-09] Mary to read the Higgsfield contract concept doc and summarize key points for David

## ecamm/workspace brain  (1 actions, 0 live)

- [STALE 2026-03-09] Record the confirmed camera/lighting settings (25fps, 50Hz, Blackmagic 4K HDMI, 6500K bulb) in the appropriate reference location

## client-voz  (1 actions, 0 live)

- [STALE 2026-03-09] Jan to tell/help Vasilios install Wispr Flow before the next meeting

## AppyDave YouTube  (1 actions, 0 live)

- [STALE 2026-03-09] Record skills video and Stream Deck/DeckHand video today

## Joy Juice menu series  (1 actions, 0 live)

- [STALE 2026-03-10] Refine menu data complexity and deliver structured JSON on Friday

## team  (1 actions, 0 live)

- [STALE 2026-03-10] Send Loom video with transcript as the detailed brief

## Ecamm Live integration  (1 actions, 0 live)

- [STALE 2026-03-11] Have Claude go deeper on Bitfocus Companion as an Ecamm integration path

## jump-system lab repo  (1 actions, 0 live)

- [STALE 2026-03-11] Write a requirements document for reimplementing the jump system as a Claude skill rather than shell tooling

## SupportSignal operations docs  (1 actions, 0 live)

- [STALE 2026-03-11] Design a paired operations.provenance document recording the source files and prompts operations.md was built from

## vOz client call  (1 actions, 0 live)

- [STALE 2026-03-12] Ask Foz on tomorrow's call whether to prioritize a new agent or the kid-podcast project, then hand over via Loom transcript

## team-ops / phone  (1 actions, 0 live)

- [STALE 2026-03-12] Call Jan: Power Mac arrives tomorrow — can the Voss meeting move to Saturday morning; take the day off otherwise

## 4C room booking  (1 actions, 0 live)

- [STALE 2026-03-12] Book the 4C room as a recurring weekly event for Clauding Lab sessions

## fleet sync  (1 actions, 0 live)

- [STALE 2026-03-12] Complete MBP↔M4 Mini sync: locations.json gap analysis, agreed folder moves/copies/deletes, global skills sync; M4 Mini is source of truth

## new observability app  (1 actions, 0 live)

- [STALE 2026-03-12] Propose 10 names for the new observability app using the stack naming conventions document

## agentic OS skills  (1 actions, 0 live)

- [STALE 2026-03-12] Run a background task to plan the 'What do I have' system-state skill

## Chiang Mai AI Community event page  (1 actions, 0 live)

- [STALE 2026-03-12] Jan to share any working image-generation skill progress and help design the Claude event page visual

## CLAUDE.md  (1 actions, 0 live)

- [STALE 2026-03-12] Update CLAUDE.md and templates to document new Claude commands (loop, by-the-way, summary) and surface them proactively

## current app UI  (1 actions, 0 live)

- [STALE 2026-03-12] Fix the page UI so multiple pages can be added, deleted, and clicked

## team admin  (1 actions, 0 live)

- [STALE 2026-03-13] Email photos of all purchase receipts to David

## fleet provisioning  (1 actions, 0 live)

- [STALE 2026-03-13] Schedule and run Ansible-first setup of the new Mac with screencasting (weekend or Monday)

## Joy Juice menu app  (1 actions, 0 live)

- [STALE 2026-03-13] Build and maintain the bilingual English/Thai drinks JSON document plus the hover-toggle HTML menu page with category tabs

## Joy Juice shop ops  (1 actions, 0 live)

- [STALE 2026-03-13] Run the daily ~4pm testing protocol: two drinks, 28 sample shots given away outside 7-Eleven, feedback recorded via OMI for AI analysis

## Joy Juice research  (1 actions, 0 live)

- [STALE 2026-03-13] Visit competitor juice bars (Juiced in Nimman, Khun Kai Juice) for research

## appydave brains port registry  (1 actions, 0 live)

- [STALE 2026-03-13] Register correct SupportSignal client ports and choose+register distinct ports for the new AWB instance (old vs new AWB both active)

## Agent Workflow Builder prompts  (1 actions, 0 live)

- [STALE 2026-03-13] Apply Alex's prompt-review feedback in a background task and report back changes

## Agent Workflow Builder / POEM workflows  (1 actions, 0 live)

- [STALE 2026-03-13] Draft Moments That Matter prompts and schemas (Penny) and the YAML workflow with batch-mode flag (Alex) following the new-incident analysis-row pattern

## Agent Workflow Builder / Signal Studio  (1 actions, 0 live)

- [STALE 2026-03-13] Build AWB intake so Moments That Matter appears as a third selectable workflow and Signal Studio can push moments and incidents into it

## fleet-infra todo  (1 actions, 0 live)

- [STALE 2026-03-14] Test remote-control access to the other computers on the network

## AppyDave content pipeline  (1 actions, 0 live)

- [STALE 2026-03-14] Include the South Park-style self-documents idea in upcoming video content

## FliVideo repo  (1 actions, 0 live)

- [STALE 2026-03-14] Persist session outputs as actions, commit all changes, and verify no uncommitted files remain

## smoothie menu image set  (1 actions, 0 live)

- [STALE 2026-03-16] Generate the mango-with-three-blends menu image and prompts for the other eleven fruit concepts

## SyncThing / relay system  (1 actions, 0 live)

- [STALE 2026-03-16] Jan to research SyncThing configuration overnight and reconvene early tomorrow to finish the relay sync test

## Claude Code / requirements doc  (1 actions, 0 live)

- [STALE 2026-03-16] Apply David's non-functional requirement changes and check what the previous session already did before proposing next steps

## appydave-plugins ralphy skill  (1 actions, 0 live)

- [STALE 2026-03-16] Decide whether code/test/architecture audits become standard callings in Ralphy's autonomous loop for all AppyStack apps

## ralph-loop plugin  (1 actions, 0 live)

- [STALE 2026-03-16] Verify the three consultant skills target the intended consultants, not Codex-style external agents

## appydave-tools jump  (1 actions, 0 live)

- [STALE 2026-03-16] Add a jump alias for the new app in /apps/ and verify location + port registry docs are current

## Joy's business  (1 actions, 0 live)

- [STALE 2026-03-16] Send invite message and schedule the Friday collaborative review with both trial employees

## SupportSignal repos  (1 actions, 0 live)

- [STALE 2026-03-16] Delete the mislocated WAV 18 data-infrastructure and Signal Studio wave-22 artifacts

## SupportSignal docs  (1 actions, 0 live)

- [STALE 2026-03-16] Update documentation to reference legacy.supportsignal.com.au instead of app.supportsignal.com.au

## vOz studio repo  (1 actions, 0 live)

- [STALE 2026-03-16] Build the storyboard artist agent from David's Loom transcript and add the transcript to the Vos docs

## vOz docs  (1 actions, 0 live)

- [STALE 2026-03-16] Commit and persist the KDD skill handover doc explaining what problem it solves for Vos and Jan

## David-Jan relay  (1 actions, 0 live)

- [STALE 2026-03-17] Jan to create QR codes for MailerLite signup and Skool community into shared sync folder

## team-video-pipeline  (1 actions, 0 live)

- [STALE 2026-03-17] Jan takes over video editing backlog (14 days of Claude-mas etc.) using Gling; Mary joins Skool

## brains/summits  (1 actions, 0 live)

- [STALE 2026-03-17] Create summits brain with digital-stage-2026 subfolder and log all summit Looms there

## digital-stage-summit brain  (1 actions, 0 live)

- [STALE 2026-03-17] Inventory all agentic apps, CLI tools, plugins, and BMAD v6 agents for the presentation

## dtv/visa-admin  (1 actions, 0 live)

- [STALE 2026-03-18] File TM30 form after returning to Thailand

## appydave.com redesign  (1 actions, 0 live)

- [STALE 2026-03-20] Deep research websites that dynamically generate structured content pages from videos and run monetized contact flows

## brains/brand-dave  (1 actions, 0 live)

- [STALE 2026-03-20] Extract branding/content-pillar information from the second brain to drive site design

## juice bar micro-apps  (1 actions, 0 live)

- [STALE 2026-03-21] Define ingredient/recipe schemas and bilingual Thai data-entry forms persisting to the file system

## upstream  (1 actions, 0 live)

- [STALE 2026-03-28] Commit and push repos.jsonl in Upstream with the new entry

## Claude Code statusline  (1 actions, 0 live)

- [STALE 2026-03-28] Investigate statusline bug showing 5% instead of 75% for seven-day usage

## brains/fleet docs  (1 actions, 0 live)

- [STALE 2026-03-28] Document fallback mechanism, affinity groups registry, and tagging scheme; commit, push, and hand over

## M4 Pro / Ollama  (1 actions, 0 live)

- [STALE 2026-03-28] Run Ollama as a background service bound to 0.0.0.0 so the M4 Mini can reach it over Tailscale after reboot

## model playbook  (1 actions, 0 live)

- [STALE 2026-03-28] Update the model playbook, decide on appydave-to-answerwell rename, and list OpenRouter-blocked models

## BMAD blog pipeline  (1 actions, 0 live)

- [STALE 2026-03-28] Automate David's blog-creation workflow using BMAD Module Builder as the teaching example for Lars

## brains/angeleye  (1 actions, 0 live)

- [STALE 2026-03-28] Write a handover of the visualization work for the AngelEye brain

## appydave-desktop  (1 actions, 0 live)

- [STALE 2026-03-30] Gap analysis between my-v-appydave and the YouTube published folder

## model preview  (1 actions, 0 live)

- [STALE 2026-03-30] Apply for the Swanning model preview

## backups  (1 actions, 0 live)

- [STALE 2026-03-30] Set up offline S3 backups of live project files to free disk space

## Lars infrastructure  (1 actions, 0 live)

- [STALE 2026-03-31] Verify Tailscale and SyncThing relay/peer-to-peer folders working on Lars's machines

## Codex session  (1 actions, 0 live)

- [STALE 2026-03-31] Update the other Codex session's shared document with current learnings and provide a concise handover

## Lars engagement  (1 actions, 0 live)

- [STALE 2026-03-31] Plan week one for Lars: daily 30-minute component sessions plus one long BMAD agent session

## Claude Code accounts  (1 actions, 0 live)

- [STALE 2026-03-31] Investigate why epic 0.7 was missing from the epics folder (account/usage configuration)

## Syncthing  (1 actions, 0 live)

- [STALE 2026-03-31] Verify Syncthing skill loading and document configuration path

## Paperclip  (1 actions, 0 live)

- [STALE 2026-03-31] Set up new Claude account for use with Paperclip

## brains machine-control docs  (1 actions, 0 live)

- [STALE 2026-04-01] Update second-machine documentation with new session learnings

## invoicing  (1 actions, 0 live)

- [STALE 2026-04-01] Lars to send invoice payment after the call

## Dropbox relay  (1 actions, 0 live)

- [STALE 2026-04-01] Set up the Dropbox-based external agent communication folder today

## BMAD story workflow  (1 actions, 0 live)

- [STALE 2026-04-01] Verify whether Bob's validation findings should have been implemented and whether Amelia addressed them

## agent lifecycle UI  (1 actions, 0 live)

- [STALE 2026-04-01] Show lifecycle chain only at top of loading message with current-agent arrow

## agentic-os relay system  (1 actions, 0 live)

- [STALE 2026-04-01] Design unified relay concept adding a Dropbox external relay for external parties/clients

## agent prompts  (1 actions, 0 live)

- [STALE 2026-04-01] Configure every agent to list all future agents to be called at least once per session

## fleet accounts  (1 actions, 0 live)

- [STALE 2026-04-01] Set up secondary $20 Codex and Anthropic accounts on a second machine, consider upgrading to $100

## Hermes runtime  (1 actions, 0 live)

- [STALE 2026-04-01] Complete manual Hermes installation including git submodules and get it running

## ai-research  (1 actions, 0 live)

- [STALE 2026-04-01] Research and compare the best unified model-agnostic harness systems including Hermes and Paperclip

## local harness setup  (1 actions, 0 live)

- [STALE 2026-04-01] Update to the latest system version and configure it before the comparison

## Lars agent relay  (1 actions, 0 live)

- [STALE 2026-04-02] Implement one-minute-loop instruction file (JSONL/CSV) with completion check-off and handling metadata for Lars's agent

## relay/shared-memory system  (1 actions, 0 live)

- [STALE 2026-04-02] Jan to hold an investigation session with David on peer-to-peer shared memories

## Lars machines  (1 actions, 0 live)

- [STALE 2026-04-02] Set up a plist-style scheduled task system for Lars

## jump skill  (1 actions, 0 live)

- [STALE 2026-04-06] Refactor the jump skill to use the provided CLI tooling instead of working around it

## ghosty  (1 actions, 0 live)

- [STALE 2026-04-06] Get ghosty working and run a BMAD 6.7 workflow to completion via a multi-agent swarm

## Kybernesis memory system  (1 actions, 0 live)

- [RECENT 2026-06-05] Build retrieval benchmark harness (quality/query-time/failure-note scoring) before writing the phased memory improvement spec

## fleet/brains  (1 actions, 0 live)

- [RECENT 2026-06-12] Consolidate documentation and machine-local memories into one aligned file set, commit, and delegate Fable 5 task runs to the M4 Mini

## dtv brain / travel files  (1 actions, 0 live)

- [RECENT 2026-06-12] Save Dad's latest travel information into a file

## Gmail integration  (1 actions, 0 live)

- [RECENT 2026-06-12] Confirm whether Claude has access to David's email

## KDD / brains documentation  (1 actions, 0 live)

- [RECENT 2026-06-12] Keep a provenance chain so the work can be redone at the two-week re-look

## fleet/git  (1 actions, 0 live)

- [RECENT 2026-06-12] Verify repos, brains, and related files are synchronized both ways between M4 Pro and M4 Mini and report gaps

## client research / brains  (1 actions, 0 live)

- [RECENT 2026-06-12] Research Australian data residency for Claude on Amazon Bedrock as it applies to NDIS participant data

## Kyber Extension SDK specs  (1 actions, 0 live)

- [RECENT 2026-06-12] Prepare Osmani-style specs for Cortex Core / Brain Core

## Kyber Extension SDK / portable brain  (1 actions, 0 live)

- [RECENT 2026-06-12] Background task: review all portable-brain packages and propose a better architecture for the reconcile/diff responsibility

## KyberAgent core / Cortex core  (1 actions, 0 live)

- [RECENT 2026-06-12] Design a diffing tool shared by KAD, KBDE, and iKANA clients (duplicate vs centralize decision)

## session handover  (1 actions, 0 live)

- [RECENT 2026-06-12] Prepare a detailed handover document before compaction (session at 69%)

## release process  (1 actions, 0 live)

- [RECENT 2026-06-12] Determine whether the release can proceed after the merger completes

## git / coding workflow  (1 actions, 0 live)

- [RECENT 2026-06-12] Commit the requested files and wave one with audit trails confirmed

## Cortex system  (1 actions, 0 live)

- [RECENT 2026-06-12] Research whether Spec B is also relevant for the Cortex system and drop the idea note into cortex

## KyberBot Desktop Enterprise  (1 actions, 0 live)

- [RECENT 2026-06-12] Add reconcile button to KDB/KBDE/KD when Portable Brain is integrated

## Capsule Video  (1 actions, 0 live)

- [RECENT 2026-06-12] Await vendor reply on extending the expired Capsule Video founding-creator coupon before purchasing

## KyberBot brain audit  (1 actions, 0 live)

- [RECENT 2026-06-12] Document current session metrics and persist audit data before closing

## Cortex agent  (1 actions, 0 live)

- [RECENT 2026-06-12] Write handover prompt referencing the spec in Osmani-skill-compatible form for a Cortex agent

## KyberAgent Desktop Enterprise  (1 actions, 0 live)

- [RECENT 2026-06-12] Review recent commits to find why the watch-folders fix regressed in Kyber Agent Desktop Enterprise

## vOz capsules project  (1 actions, 0 live)

- [RECENT 2026-06-12] Get list of the eight capsule stories with details and the first one to work on

## OMI brain  (1 actions, 0 live)

- [RECENT 2026-06-13] Record ideas B and C as documented future concepts, not current work

## Claude Code / appydave skills  (1 actions, 0 live)

- [RECENT 2026-06-13] Compare Anthropic built-in code review output against the delivery-review skill for redundancy vs complementarity

## video-as-code brain  (1 actions, 0 live)

- [RECENT 2026-06-13] Run a gap analysis between Remotion and Hyperframes

## video pipeline  (1 actions, 0 live)

- [RECENT 2026-06-13] Investigate a background-agent POC turning the four slides into a video

## Dark Factory / brains repo  (1 actions, 0 live)

- [RECENT 2026-06-13] Route loop-engineering learnings into dark-factory + brains and commit/push the hyperframes brain updates

## AppyRadar  (1 actions, 0 live)

- [RECENT 2026-06-13] Verify which copy of AppyRadar central received the changes and reconcile with the relocated repo

## Anthropic  (1 actions, 0 live)

- [RECENT 2026-06-13] Partner to apply for the Anthropic Leaders program as an NDIS domain lead

## brains/video-as-code  (1 actions, 0 live)

- [RECENT 2026-06-14] Document all Hyperframes subsystems in the brain before deciding which skills to install

## AI-TLDR video catalogue  (1 actions, 0 live)

- [RECENT 2026-06-14] Track down and document the AI-TLDR YouTube video download/catalogue workflow so it can be repeated for AppyDave

## Kybernesis tracker  (1 actions, 0 live)

- [RECENT 2026-06-14] Update ticket statuses and execute KYB-84A, with delivery review if appropriate

## Angela sideline app  (1 actions, 0 live)

- [RECENT 2026-06-14] Build the small sideline application for Angela of Supporting Potential (due same day)

## website  (1 actions, 1 live)

- [LIVE 2026-06-24] Develop concepts for a new social intro video for the website and present to David

## ai-meetups notes  (1 actions, 1 live)

- [LIVE 2026-06-27] Review the Shopify head-of-engineering AI strategy video from the Cursor event

## dev machine  (1 actions, 1 live)

- [LIVE 2026-06-29] Install and test latest AionUI and T3 as candidate third-party extension hosts

## thumbnail generator  (1 actions, 1 live)

- [LIVE 2026-06-30] Define thumbnail generator fields and per-brand rules starting with AppyDave

## recipe skill  (1 actions, 1 live)

- [LIVE 2026-06-30] Research David's past recipe-development conversations and external examples, then build the generalized self-improving recipe skill

## WatchTower/Switchboard  (1 actions, 1 live)

- [LIVE 2026-07-03] Document the WatchTower and Switchboard communication flow

## gling-automation  (1 actions, 1 live)

- [LIVE 2026-07-04] Research safe open-source agentic alternatives to Gling and Descript for video cutting, vetting code quality and injection/exfiltration risk

## kyber-extension-sdk  (1 actions, 1 live)

- [LIVE 2026-07-05] Write ticket for Kyber Extension SDK capabilities: scheduled tasks/cron plus host-provided chat conversation access for extensions, filed in KyberAgent docs or Dark Factory

## appydave-plugins omi-fetch  (1 actions, 1 live)

- [LIVE 2026-07-05] Unify OMI and Plaud fetch under one provider-agnostic ingestion concept and rename omi-fetch accordingly

## claude-code  (1 actions, 1 live)

- [LIVE 2026-07-06] Establish how to communicate with the KyberAgent system from Claude Code

## client-challenge-dv  (1 actions, 1 live)

- [LIVE 2026-07-07] Send Linda a set of engagement/pricing options (weekly 90-min sessions + monthly retainer + tool-building)

## brains/gling  (1 actions, 1 live)

- [LIVE 2026-07-11] Review the existing gling brain notes before building anything new
