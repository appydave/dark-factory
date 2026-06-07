#!/usr/bin/env node
// selfcheck-promote — asserts buildPromoteTicket() produces a well-formed queue
// ticket and that the JSON round-trips when written to a TEMP dir. Touches no
// servers, no real engine dirs. Run: node experiments/watchtower-board/selfcheck-promote.mjs
import { buildPromoteTicket, slugify } from './server.mjs';
import { writeFile, readFile, mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import assert from 'node:assert/strict';

const now = Date.now();
const { queue_id, ticket } = buildPromoteTicket('Floor↔Lanes bridge / promote!!', 'execution', now);

// queue_id is safe: prefix, ms timestamp, sanitized slug — no slash, no dotdot.
assert.match(queue_id, /^q-\d+-promoted-[a-z0-9-]+$/, 'queue_id shape');
assert.ok(!queue_id.includes('/') && !queue_id.includes('..'), 'queue_id sanitized');
assert.equal(slugify('a/b/../c'), 'a-b-c', 'slug strips path chars');

// ticket shape matches existing instruction tickets in done/
assert.equal(ticket.queue_id, queue_id);
assert.equal(ticket.kind, 'instruction');
assert.equal(ticket.experiment_id, 'exp-promoted');
assert.equal(ticket.requested_by, 'watchtower-board');
assert.deepEqual(ticket.args, { from: 'lanes-board', lane: 'execution' });
assert.ok(ticket.prompt.includes('Elaborate this concept') && ticket.prompt.includes('(lane: execution)'));
assert.equal(ticket.requested_at, new Date(now).toISOString(), 'timestamp from OS clock');

// round-trip through a TEMP file (not the real queue) — proves a valid file would be produced
const dir = await mkdtemp(join(tmpdir(), 'promote-'));
const fp = join(dir, queue_id + '.json');
await writeFile(fp, JSON.stringify(ticket, null, 2));
const back = JSON.parse(await readFile(fp, 'utf8'));
assert.deepEqual(back, ticket, 'JSON round-trips');

console.log('OK selfcheck-promote: well-formed ticket', queue_id, '→', fp);
