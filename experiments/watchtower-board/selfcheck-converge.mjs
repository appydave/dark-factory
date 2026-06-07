#!/usr/bin/env node
// selfcheck-converge — asserts buildConvergeTicket() produces ONE well-formed queue
// ticket from a CLUSTER of concepts and that the JSON round-trips when written to a
// TEMP dir. Touches no servers, no real engine dirs.
// Run: node experiments/watchtower-board/selfcheck-converge.mjs
import { buildConvergeTicket, slugify } from './server.mjs';
import { writeFile, readFile, mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import assert from 'node:assert/strict';

const now = Date.now();
const items = [
  { concept: 'Floor↔Lanes bridge / converge!!', lane: 'execution' },
  { concept: 'Standing reaper for stranded runs', lane: 'infra' },
  { concept: 'Terse handback return-leg', lane: 'comms' },
];
const { queue_id, ticket } = buildConvergeTicket(items, now);

// queue_id is safe: prefix, ms timestamp, sanitized slug — no slash, no dotdot.
assert.match(queue_id, /^q-\d+-converge-[a-z0-9-]+$/, 'queue_id shape');
assert.ok(!queue_id.includes('/') && !queue_id.includes('..'), 'queue_id sanitized');
assert.equal(slugify('a/b/../c'), 'a-b-c', 'slug strips path chars');

// ticket shape matches the spec for exp-converge instruction tickets
assert.equal(ticket.queue_id, queue_id);
assert.equal(ticket.kind, 'instruction');
assert.equal(ticket.experiment_id, 'exp-converge');
assert.equal(ticket.requested_by, 'watchtower-board');
assert.deepEqual(ticket.args, { from: 'lanes-converge', count: 3 });
assert.equal(ticket.requested_at, new Date(now).toISOString(), 'timestamp from OS clock');

// prompt: ONE synthesis brief covering all N concepts, numbered + lane-tagged
assert.ok(ticket.prompt.startsWith('Converge these 3 related concepts into ONE cohesive brief.'));
assert.ok(ticket.prompt.includes('1) execution: Floor↔Lanes bridge / converge!!'));
assert.ok(ticket.prompt.includes('2) infra: Standing reaper for stranded runs'));
assert.ok(ticket.prompt.includes('3) comms: Terse handback return-leg'));
assert.ok(ticket.prompt.includes('docs/watchtower/converged-briefs/'), 'names the brief output path');

// guard: <1 concept throws (the bar enforces >=2; the pure fn enforces >=1)
assert.throws(() => buildConvergeTicket([], now), /at least one concept/, 'empty cluster rejected');

// round-trip through a TEMP file (not the real queue) — proves a valid file would be produced
const dir = await mkdtemp(join(tmpdir(), 'converge-'));
const fp = join(dir, queue_id + '.json');
await writeFile(fp, JSON.stringify(ticket, null, 2));
const back = JSON.parse(await readFile(fp, 'utf8'));
assert.deepEqual(back, ticket, 'JSON round-trips');

console.log('OK selfcheck-converge: well-formed ONE-brief ticket', queue_id, '→', fp);
