#!/usr/bin/env node
//
// parse-concepts.mjs — turn backlog/concepts.md into structured lanes for the
// Watchtower "Concept Lanes" view (board v2). Pure Node, no dependencies.
//
// Shape:  [{ lane: "<heading>", items: [{ concept, status, pri }] }]
//
// Parsing rules (see ticket q-20260606-board-v2-lanes):
//  - each '## <Title>' heading starts a new lane
//  - within a lane, each markdown table row '| concept | status | pri |' is an item
//  - SKIP the header row ('| Concept | Status | Pri |') and the '|---|' separator
//  - strip markdown bold/asterisks + surrounding whitespace from <concept>
//  - keep the status emoji (💡/📋/🔨/✅) and pri emoji (🔴/🟡/🟢) verbatim
//  - ignore prose / non-table lines
//
// Run directly (node parse-concepts.mjs) → reads ../../backlog/concepts.md
// relative to this file and prints '<N> lanes, <M> items' (the self-test).

import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

// Split a markdown table row into its cells, dropping the leading/trailing empties.
function rowCells(line) {
  const parts = line.split('|');
  return parts.slice(1, parts.length - 1).map((c) => c.trim());
}

const isSeparator = (cells) => cells.length > 0 && cells.every((c) => /^:?-+:?$/.test(c));
const isHeader = (cells) => (cells[0] || '').toLowerCase() === 'concept';
const stripBold = (s) => s.replace(/\*+/g, '').trim();

export function parseConcepts(md) {
  const lanes = [];
  let current = null;
  for (const raw of md.split('\n')) {
    const line = raw.trim();
    if (line.startsWith('## ')) {
      current = { lane: line.slice(3).trim(), items: [] };
      lanes.push(current);
      continue;
    }
    // table row: starts and ends with a pipe
    if (current && line.startsWith('|') && line.endsWith('|')) {
      const cells = rowCells(line);
      if (cells.length < 3) continue;        // malformed / not our 3-col table
      if (isSeparator(cells) || isHeader(cells)) continue;
      current.items.push({
        concept: stripBold(cells[0]),
        status: cells[1],
        pri: cells[2],
      });
    }
  }
  return lanes;
}

// --- self-test when run directly -------------------------------------------
const isMain = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const here = dirname(fileURLToPath(import.meta.url));
  const path = resolve(here, '..', '..', 'backlog', 'concepts.md');
  const md = await readFile(path, 'utf8');
  const lanes = parseConcepts(md);
  const items = lanes.reduce((n, l) => n + l.items.length, 0);
  console.log(`${lanes.length} lanes, ${items} items`);
}
