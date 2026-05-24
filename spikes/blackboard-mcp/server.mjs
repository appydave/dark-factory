#!/usr/bin/env node
/**
 * Minimal MCP Blackboard server — file-backed key-value store.
 *
 * Tools exposed (via MCP):
 *   bb_set    — write a value at a key (any JSON-serializable value)
 *   bb_get    — read a value at a key (returns null if missing)
 *   bb_list   — list all keys, optionally filtered by prefix
 *   bb_delete — delete a key
 *
 * Storage: single JSON file at ~/.claude/blackboard/store.json
 *   - Simple object: { "<key>": <value>, ... }
 *   - Atomic-ish: full-file rewrite on every set/delete
 *   - File-locking not implemented (single-machine v1; add for multi-writer)
 *
 * Spec: github.com/modelcontextprotocol/specification
 * Run:  node server.mjs   (speaks JSON-RPC over stdio)
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { homedir } from "node:os";

// ─── Storage ─────────────────────────────────────────────────────────────────

const STORE_PATH = process.env.BLACKBOARD_STORE_PATH
  ?? `${homedir()}/.claude/blackboard/store.json`;

function ensureStore() {
  const dir = dirname(STORE_PATH);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  if (!existsSync(STORE_PATH)) writeFileSync(STORE_PATH, "{}", "utf8");
}

function loadStore() {
  ensureStore();
  try { return JSON.parse(readFileSync(STORE_PATH, "utf8")); }
  catch { return {}; }
}

function saveStore(store) {
  ensureStore();
  writeFileSync(STORE_PATH, JSON.stringify(store, null, 2), "utf8");
}

// ─── Tool implementations ─────────────────────────────────────────────────────

function bbSet({ key, value }) {
  if (typeof key !== "string" || !key.length) throw new Error("key must be a non-empty string");
  const store = loadStore();
  store[key] = value;
  saveStore(store);
  return { ok: true, key };
}

function bbGet({ key }) {
  if (typeof key !== "string" || !key.length) throw new Error("key must be a non-empty string");
  const store = loadStore();
  return { key, value: store[key] ?? null, found: key in store };
}

function bbList({ prefix } = {}) {
  const store = loadStore();
  const keys = Object.keys(store);
  const filtered = prefix ? keys.filter(k => k.startsWith(prefix)) : keys;
  return { keys: filtered, count: filtered.length };
}

function bbDelete({ key }) {
  if (typeof key !== "string" || !key.length) throw new Error("key must be a non-empty string");
  const store = loadStore();
  const existed = key in store;
  delete store[key];
  saveStore(store);
  return { ok: true, key, existed };
}

// ─── MCP protocol (JSON-RPC over stdio) ──────────────────────────────────────
// Implements the minimum subset of MCP needed for tool exposure.

const TOOLS = {
  bb_set: {
    description: "Set a key in the blackboard to any JSON-serializable value. Overwrites if the key exists.",
    inputSchema: {
      type: "object",
      required: ["key", "value"],
      properties: {
        key: { type: "string", description: "Blackboard key (any string)" },
        value: { description: "Any JSON-serializable value to store at this key" }
      }
    },
    handler: bbSet
  },
  bb_get: {
    description: "Read the value at a blackboard key. Returns { key, value, found }. value is null if the key does not exist.",
    inputSchema: {
      type: "object",
      required: ["key"],
      properties: { key: { type: "string" } }
    },
    handler: bbGet
  },
  bb_list: {
    description: "List all keys in the blackboard, optionally filtered by prefix. Returns { keys, count }.",
    inputSchema: {
      type: "object",
      properties: { prefix: { type: "string", description: "Optional prefix filter" } }
    },
    handler: bbList
  },
  bb_delete: {
    description: "Delete a key from the blackboard. Returns { ok, key, existed }.",
    inputSchema: {
      type: "object",
      required: ["key"],
      properties: { key: { type: "string" } }
    },
    handler: bbDelete
  }
};

function makeResponse(id, result) {
  return { jsonrpc: "2.0", id, result };
}

function makeError(id, code, message, data) {
  return { jsonrpc: "2.0", id, error: { code, message, ...(data ? { data } : {}) } };
}

function handleRequest(req) {
  const { id, method, params } = req;

  if (method === "initialize") {
    return makeResponse(id, {
      protocolVersion: "2024-11-05",
      capabilities: { tools: {} },
      serverInfo: { name: "blackboard-mcp", version: "0.1.0" }
    });
  }

  if (method === "tools/list") {
    return makeResponse(id, {
      tools: Object.entries(TOOLS).map(([name, def]) => ({
        name,
        description: def.description,
        inputSchema: def.inputSchema
      }))
    });
  }

  if (method === "tools/call") {
    const { name, arguments: args } = params ?? {};
    const def = TOOLS[name];
    if (!def) return makeError(id, -32601, `unknown tool: ${name}`);
    try {
      const result = def.handler(args ?? {});
      return makeResponse(id, {
        content: [{ type: "text", text: JSON.stringify(result) }]
      });
    } catch (err) {
      return makeError(id, -32000, err.message);
    }
  }

  if (method === "notifications/initialized") return null; // notification — no response

  return makeError(id, -32601, `method not found: ${method}`);
}

// ─── stdio loop ──────────────────────────────────────────────────────────────

let buffer = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", chunk => {
  buffer += chunk;
  let idx;
  while ((idx = buffer.indexOf("\n")) !== -1) {
    const line = buffer.slice(0, idx).trim();
    buffer = buffer.slice(idx + 1);
    if (!line) continue;
    try {
      const req = JSON.parse(line);
      const resp = handleRequest(req);
      if (resp !== null) process.stdout.write(JSON.stringify(resp) + "\n");
    } catch (err) {
      process.stderr.write(`[blackboard-mcp] parse error: ${err.message}\n`);
    }
  }
});

process.stderr.write(`[blackboard-mcp] ready, store at ${STORE_PATH}\n`);
