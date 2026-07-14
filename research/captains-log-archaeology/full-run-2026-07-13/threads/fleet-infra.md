# Thread: fleet-infra

**Purpose**: Six-month narrative timeline of David's fleet-infrastructure captures — how the multi-Mac agentic fleet went from a Stream Deck question to a five-machine, three-country provisioned network.

**For Agents**:
- Use this to understand how fleet decisions were reached (and which were superseded)
- Records: 114, spanning 2026-01-11 → 2026-06-13
- Part of the captains-log archaeology full run 2026-07-13

---

## Shape of the thread

```
Jan ─ hardware curiosity (Stream Deck)
Feb ─ naming (Project Theodore) → 2-machine drift pain → CRISIS (MBP screen death)
Mar ─ rebuild + blueprint → provisioning (Ansible) → team fleet (Jan/Mary) → relay layer
Apr ─ relay conventions settle → security cleanup → scheduled-task manager idea
     ── DORMANT ~10 weeks ──
Jun ─ single re-emergence (AppyRadar wrong-repo)
```

This thread is really three braided strands that repeatedly split and merge: **(a) physical fleet & remote control**, **(b) provisioning-as-code (Ansible)**, and **(c) the agentic OS layer riding on top (Project Theodore)**. A fourth strand — **file/data transport (relay)** — buds off in mid-March and settles in April.

---

## 2026-01-11 — STARTED: hardware, not infrastructure

The thread opens deceptively small: a mall crawl comparing hardware controllers (Stream Deck Neo/Plus/XL/Studio, RODE Streamer X, Logitech MX Creator Console). Decision: **Stream Deck Plus has the best plugin SDK; buy a Neo now, order the Plus**. A companion research question is logged — why Stream Decks fail through USB hubs and only work direct into USB-C.

Nothing here says "fleet" yet, but this is the seed of the programmable-controls / DeckHand strand that later gets folded into the agentic OS.

## 2026-02-02 — Naming and intent: Project Theodore

Three weeks later the ambition appears. David names his personal agentic OS **"Project Theodore"** (from the film *Her*), with **Samantha** as the executive-assistant persona. Early design ideas: brain-stored North-Star guidance, and connectivity options weighed — **ngrok tunnels vs a communication bus vs direct Supabase** (this question stays open for a month; Supabase wins by March).

## 2026-02-12 / 02-20 — First remote-control itch

After losing two closed AI conversations, David asks what the brain already holds on SSH/remote computer control. On 02-20, after Cole Medin's second-brain workshop, he directs that **Slack be added as a channel to Ansible and the agentic OS** (a direction that never resurfaces in this thread — quietly dropped; Telegram/Discord win in the March architecture).

## 2026-02-22 — The big burst: two machines that won't match

A single marathon day generates ~15 captures. The pain is concrete: **M2 and M4 don't match despite Ansible-installed SSH/settings/plugins** ("remote machine environment drift"), screen-sharing clipboard won't copy, Tailscale won't install because Chrome never arrived, the "air/airspool" workflow over SSH is untrusted and hangs the remote Mac, and ~550–650GB of disk usage is unexplained.

Out of the frustration comes structure:

- **Fleet plan articulated for the first time**: five computers, lowercase-dashed hostnames via `scutil`, **Tailscale mesh** (learned: it's a mesh VPN), Ansible-style deployment from the main Mac, future machines for Jan and Mary in the Philippines, creator-machine vs network-machine separation (Ecamm only on the creator box).
- **Remote-control layering sorted**: Screen Sharing/VNC for visual control, SSH for agent-driven automation; Whisper voice must be piped over SSH.
- **Decision (SUPERSEDED)**: "remote access should be visual remote desktop rather than SSH." Within 48 hours the Feb-24 orchestrator work makes SSH the primary agent channel; the lasting model is *both layers, different jobs* (VNC for humans, SSH for agents).
- zsh alias architecture questioned and partly settled (dedicated alias files); a **dev-folder exclude-from-copy registry** idea logged (prefigures the migration tooling needed six days later).
- Decision to keep the M4 and rerun Ansible playbook checks on both machines from within Claude.

## 2026-02-24 — Claude Code becomes the orchestrator

David records a YouTube demo of **Claude Code as cross-machine orchestrator** — SSH into the M4 Mini, remote clone of the 1,491-file brains repo — and lays out the 5-machine/3-location plan with per-machine identities, OpenCore on one machine, KyberBot memory on the main one, Samantha voice on top.

Hard evidence of the drift problem lands: Claude over SSH to the M2 falsely claims tmux and Homebrew are missing — **the remote SSH shell environment isn't loading correctly**. The Ansible playbook run for dotfiles/aliases also fails to apply. Two process gaps are logged: session resume/tracking procedure, and frustration that the agent asks him to run SSH/tmux steps it could execute itself.

## 2026-02-28 — CRISIS: MacBook Pro screen death → emergency migration

The forcing function. Mid-Signal-Studio work, the MBP's screen dies (hardware fault — interlacing, black line, blackout; externals still work). David declares an emergency and decides to **migrate everything off the laptop to the M4 over SSH**.

The migration is run agentically and generates its own sub-system:

- Transfer priority set (video projects first, then dev in order), background agents one at a time, secrets/env configs moved early.
- **Decision**: maintain a copied-vs-uncopied tracking file + machine-readable twin for folder-level gap analysis.
- Repo triage: copy the live repos, delete dead projects, push uncommitted/no-remote repos to GitHub.
- A **repo-audit tool** is born out of necessity (with corrected scope: locate repos, rerunnable, no last-updated reporting) — the earliest ancestor of the later locations.json / repo-audit tooling.
- Warranty strand opens: is Bangkok really the only Apple repair option from Chiang Mai?

Everything the Feb-22 burst had worried about abstractly (drift, sync, what lives where) got stress-tested for real.

## 2026-03-01 — Rebuild day becomes blueprint day

A new **M4 Mini** comes online as disaster recovery (Time Machine, Tailscale mesh to the M4 Pro), and instead of just restoring, David writes the plan:

- **Project Theodore 3-month roadmap**: five-Mac Tailscale mesh (3 Chiang Mai + Jan/Mary M4s in the Philippines), AppyStack micro-apps, Ralphie loop, Lisa-curated brains, **Ansible provisioning, Supabase data bus** (the Feb-02 open question resolved), Samantha/ElevenLabs voice, automated morning briefing.
- **Vertical/horizontal stack model defined**: per-agent vertical stack (brain → memory → Claude SDK harness → Cowork → chat → voice) × horizontal Tailscale mesh.
- **Decision**: rename AppyDeck → **DeckHand**, rebuild on AppyStack instead of Electron (merging the January Stream Deck strand into the OS).
- **Decision (supersedes same-day note)**: package managers settled as **Bun primary, pnpm optional** — an earlier capture that day had asked to store a PNPM preference; the Bun-primary recommendation is what got adopted.
- "Standard machine provisioning" named explicitly as the goal — the seed statement of the Ansible fleet approach.
- Application registry commissioned (name/description/location/port with priorities) — ancestor of `locations.json` + `apps.json`.
- Documentation directive: rich-data-first, then NotebookLM package for diagrams.
- Recurring parity question crystallises: **should every machine-level change (displays, monitors, Rust install) update the Ansible config so infra-as-code stays in sync?**

## 2026-03-02 → 03-05 — Friction list + the Ansible video

Small persistent pains logged: Claude forgets SSH/hostname details every session (→ later fixed by memory files + `remote-machines` skill), the Ansible coding profile's hated three-profile selector, Moom going buggy (→ lean Hammerspoon).

Then the provisioning strand goes public: **the Ansible agentic-OS video** is produced over 03-05 — discovery playbook + `--check` dry-run on the M4 Mini surfacing four real diffs and fixing them live, the per-agent vertical stack + five-machine horizontal mesh explained (heavy M4 creator, Rover field laptop, headless M2 at Joy's business, MJ/Mary Philippines minis), framed as a perspective piece not a tutorial. Skool named as main monetisation with Dent-style consulting (Lars first client). MLX Whisper local transcription gets installed on the M4 Mini as part of the same push.

## 2026-03-10 → 03-17 — Fleet goes multi-person; relay strand buds

- 03-10: **Supabase as shared memory for everything** — each entity concept gets a table (memory-bus idea matured).
- 03-12: **AngelEye added as the observability layer** of the agentic OS; the **repaired MacBook Pro returns** and is resynced from the M4 Mini as source of truth (Ansible discovery, locations.json gap analysis, case-by-case folder migrations, public GitHub remotes for DeckHand/AngelEye/AppyStack). Tailscale personal plan (3 users/100 devices) chosen for the future Jan+Mary fleet. A durable question logged: why does every tool invent its own config location — want **centralized machine config** (answered months later by `~/.config/appydave/` with a private git remote).
- 03-16: **The team fleet becomes real.** Two Mac Mini M4s + monitors bought (~$2.5k, Voz approved). **Jan's Mac fully provisioned remotely** — Homebrew bootstrap, Tailscale auth key, SSH with David's GitHub keys, then the standard Ansible toolchain. Decisions: **split Ansible inventory into public/private sibling repos**; **policy: team tools go through Ansible, never manual installs**; **SyncThing 'relay' folder** named as the peer-to-peer AI-to-AI file channel over Tailscale. Mary's setup scheduled next.
- 03-17: Narrative reframed for the Digital Stage Summit — away from port minutiae toward *why machine-to-machine communication matters*; a "level 4" capability tier proposed (observability, self-improvement, workflow tooling).

## 2026-03-28 — Local LLM layer

The fleet gains inference: **Ollama on the M4 Pro exposed over Tailscale** (`OLLAMA_HOST=0.0.0.0`, reboot-surviving service), models pulled (Phi-4, Gemma 3, Llama 3, Qwen 2.5), fallback mechanism + affinity-groups registry demanded, benchmarking plan across five brains. Open question: rename the 'appydave' model alias to 'answerwell'.

## 2026-03-31 → 04-02 — Breakage, recovery, and the relay layer settles

A rough patch: Paperclip cross-machine access fails ('invalid claim' over Tailscale), and **Claude Code breaks on the MacBook Pro** — a messy uninstall/reinstall saga (incomplete cleanout proven by launching it; orphaned shells; both paid accounts hitting usage limits → anonymised support case for Anthropic). **Decision**: post-mortem written to brains, back up `~/.claude` rather than wipe, reinstall on the appydave account (not ideasman). 04-01 continues with a corrupted-Claude recovery on the ideasmen machine, and a **security-focused cleanup** direction (verify downloaded repos against sources of truth, audit for exfiltration/prompt-injection).

Meanwhile the relay strand matures from idea to convention:

- Requirements session for a **SyncThing relay skill** (REST API on 8384 vs filesystem, remote-access choices, staging before build).
- Hands-on run surfaces gaps (no open command, no folder listing, unsafe on existing folders).
- Key operational learning: SyncThing folders must be explicitly registered and shares disabled everywhere before renames/moves, or the mesh resyncs and corrupts data — unlike Dropbox.
- **Decision (settled convention)**: `relay/{type}/{name}` with app/project/people types, `to-<agent>` naming for harness targets, `david-jan`/`david-mary`/`david-lars` people folders, **Syncthing internal / Dropbox external** (Lars).

04-02 closes the active period with an idea that points at the future: a **distributed scheduled-task manager micro-app** — central source of truth for task rules/ownership across plist and agent-based schedulers, Lars as first client, OMI fetch as first job.

## 2026-04-02 → 06-13 — DORMANT (~10 weeks)

No fleet-infra captures for two and a half months. The infrastructure had reached "working": fleet provisioned, relay conventions set, video shipped. (Ambient evidence elsewhere shows the work moved to consuming the fleet — AppyRadar telemetry, k-agent fleet, appydave-config — rather than building it.)

## 2026-06-13 — RE-EMERGED (one blip)

A single capture: David suspects **Claude applied changes to an outdated copy of AppyRadar central** because the repo's home had moved. Classic late-stage fleet problem — not "does the fleet work" but "do the agents know where things live now" — i.e. the 03-12 centralized-config question resurfacing in new clothes.

---

## Superseded decisions (explicit)

| When | Decision | Superseded by |
|------|----------|---------------|
| 2026-02-20 | Slack as messaging channel for Ansible/agentic OS | Never implemented; Mar-01/05 architecture uses Telegram/Discord + Samantha voice |
| 2026-02-22 | Remote access = visual remote desktop **rather than** SSH | Feb-24 onward: SSH is the primary agent channel; VNC retained for human/visual only |
| 2026-03-01 (am) | Store PNPM as package-manager preference | Same day: **Bun primary, pnpm optional** adopted into the agentic OS |
| 2026-03-01 | AppyDeck (Electron) | Renamed **DeckHand**, rebuilt on AppyStack |
| 2026-02-02 | ngrok vs bus vs Supabase (open) | Mar-01/10: **Supabase data bus / shared memory** chosen |
| pre-03-16 | Ad-hoc/manual installs on team machines | 03-16 policy: **all team tooling via Ansible** |
| 2026-03-31 | Initial single Syncthing relay concept | 04-01 unified model: **Syncthing internal + Dropbox external**, `relay/{type}/{name}` |

## Current status (as of 2026-07-13)

**Mature and in maintenance mode.** The five-machine Tailscale fleet exists and is provisioned via Ansible (public/private inventory split); Jan's machine is live, relay conventions are settled and in use (Lars on Dropbox external), local LLM hosting runs on the mesh, and the Stream Deck strand lives on as DeckHand. Open residue: the Jun-13 stale-repo-location problem (agents acting on moved repos), the centralized machine-config push (since partially answered by the private `appydave-config` remote), the distributed scheduled-task manager (idea only), and Mary's machine setup (in progress as of the Mar-16 captures, not confirmed complete inside this thread).
