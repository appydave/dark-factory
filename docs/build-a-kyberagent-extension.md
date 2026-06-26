# Dark Factory → build a KyberAgent (KBDE) extension

> **Purpose.** Hand Dark Factory the authoring kit so a *ticket / idea* → a *built bundled extension*
> in KyberAgent Enterprise. This is a **pointer**, not a copy — the canonical knowledge lives in the
> `extension-sdk` skill and the live reference plugins; read those, don't transcribe them.

## The mental model (read this first)

- An **extension** is a bundled unit identified by a `pluginId` (e.g. `plugin.seam-probe`). It lives in
  `packages/daemon/src/bundled-plugins/<name>/` as **two files**: `kbde.extension.ts` (the SDK-authored
  seam contributions) and `kbde.plugin.ts` (the outer plugin/manifest wrapper). **You author the
  `kbde.extension.ts`.**
- An extension **contributes** things over the seam. Each contribution has a **contributionId** shaped
  `<kind>.<extension>[.<resource>]`:
  - **kind** — *what sort of thing it is*: `surface` (a UI mount), `data` (a queryable data endpoint),
    `composer` (a composer capability), `settings`, `contextualAction`, `sidecar`, `bridge`, …
  - **extension** — *whose it is* (the invariant; every contribution of one extension shares it).
  - **resource** — *which one*, when the extension has several of that kind (e.g. `data.brain-lens.graph`
    vs `data.brain-lens.brain`).
- **You no longer hand-type the id.** Supply typed fields and the SDK derives it (SPEC 2):
  `defineSurface({ ext: 'my-thing' })` → `surface.my-thing`;
  `defineDataEndpoint({ ext: 'my-thing', name: 'rows' })` → `data.my-thing.rows`.

## The kit (where the real knowledge is)

1. **The skill** — `.claude/skills/extension-sdk/`. Start at `references/scaffold.md` (archetype → working,
   gate-correct surface), then `references/capability-model.md` (what each channel MEANS — esp. Brain is a
   host-owned capability, not the extension's data) and `references/trust-invariants.md` (the four security
   rules — never ship a latent hole).
2. **The scaffolder** — `scripts/extensions/scaffold-extension.ts` (deterministic generator; "name an
   archetype → get a working surface"). Don't hand-write the skeleton.
3. **The live reference to COPY (never transcribe)** —
   `packages/daemon/src/bundled-plugins/seam-probe/` — the canonical two-mount extension: surfaces, a data
   endpoint, a brain read, host-context/host-command, the `web/app.js` channel registry. It now uses the
   **typed `{ ext, name }`** authoring form — copy that shape.
4. **The generated truth** — `packages/extension-sdk/extension-capabilities.json` (the real SDK surface +
   channels + gates; CI fails on drift). Regenerate with `pnpm extensions:capabilities`.

## The four archetypes (pick one)
`in-proc-web-surface` · `sandboxed-iframe-surface` · `two-mount-surface` · `data-only`. The scaffolder
decides the mount + gate per archetype. Sandboxed-iframe for untrusted/third-party; in-proc for first-party.

## Trust invariants (non-negotiable — see `references/trust-invariants.md`)
Gate before grant · frame identity is host-attested (never trust a renderer claim) · an extension is a
*gated consumer* of host capabilities (brain, host-context), never their owner · deny-twin every new gate.

## Verify a built extension (no human clicking)
`pnpm -F @kyberagent/daemon typecheck` · `pnpm extensions:check` (manifests valid) ·
`pnpm extensions:capabilities` (drift) · `pnpm uat:seam` (the seam end-to-end) ·
`pnpm uat:extensions` (the bundled baseline). For a visible surface, the `uat:seam-iframe` lane drives real
Electron.

## ⚠️ The one case that does NOT fit the model — external connectors / routers (e.g. Composio)
`composio-runtime` contributes `gmail.search` / `gmail.send` — composer capabilities whose **ids are the
external provider's own ids** (`<provider>.<tool>`), NOT `<kind>.<ext>.<name>`. They are kept by declaration
(the user-facing `$gmail.search` syntax + the Composio mapping) and must **never be renamed or migrated** to
the typed form. This is a recognised **third ownership category — externally-owned connector tools — that the
`<kind>.<ext>.<name>` convention does not yet model.** A *router* like Composio (potentially hundreds of
tools) should NOT mint hundreds of static contributionIds; that needs a **dynamic/proxy capability** design
that is still an **open question**. If a DF ticket is "wrap an external router," flag it as out-of-pattern —
do not invent static external ids.
