#!/usr/bin/env node
/**
 * MCP Blackboard server — file-backed key-value store with CHANNELS.
 *
 * Tools exposed (via MCP):
 *   bb_set      — write a value at a key (any JSON-serializable value)
 *   bb_get      — read a value at a key (returns null if missing)
 *   bb_list     — list keys, optionally filtered by prefix
 *   bb_delete   — delete a key
 *   bb_channel  — register/resolve a channel's storage path (repo-local opt-in)
 *   bb_drop     — retire a whole channel (deletes its file + registry entry)
 *   bb_channels — list known channels + key counts
 *
 * CHANNELS (v2):
 *   Every op takes an optional `channel` (string). It selects which store file is used:
 *     - omitted / "default"        → the original global store (back-compat: ~/.claude/blackboard/store.json)
 *     - a registered channel       → its registered path (see bb_channel — e.g. a repo-local .blackboard/<ch>.json)
 *     - an unregistered channel    → ~/.claude/blackboard/<channel>.json (global, auto)
 *   Channels give three things at once: separation (two collaborations never interleave),
 *   storage routing (where the file lives is a per-channel choice), and lifecycle (bb_drop).
 *   Writes are serialized by this single server process, so two sessions never clobber a file.
 *
 * Storage: one JSON object per channel file. Atomic-ish: full-file rewrite per set/delete.
 *   File-locking not implemented (single-machine; the single server process serializes writes).
 *
 * Run:  node server.mjs   (speaks JSON-RPC over stdio)
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync, readdirSync } from "node:fs";
import { dirname, isAbsolute, resolve as resolvePath, basename } from "node:path";
import { homedir } from "node:os";

// ─── Channel → path resolution ────────────────────────────────────────────────

// The DEFAULT channel keeps the original path (back-compat, incl. BLACKBOARD_STORE_PATH override).
const DEFAULT_STORE = process.env.BLACKBOARD_STORE_PATH
  ?? `${homedir()}/.claude/blackboard/store.json`;
const BASE_DIR = dirname(DEFAULT_STORE);
const REGISTRY_PATH = `${BASE_DIR}/channels.json`;
const RESERVED = new Set(["store", "channels"]); // file basenames that aren't channels

function ensureDir(p) {
  const dir = dirname(p);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
}

function loadJson(path, fallback) {
  if (!existsSync(path)) return fallback;
  try { return JSON.parse(readFileSync(path, "utf8")); }
  catch { return fallback; }
}

function saveJson(path, obj) {
  ensureDir(path);
  writeFileSync(path, JSON.stringify(obj, null, 2), "utf8");
}

function loadRegistry() { return loadJson(REGISTRY_PATH, {}); }

function normalizeChannel(channel) {
  if (channel === undefined || channel === null || channel === "" || channel === "default") return "default";
  if (typeof channel !== "string") throw new Error("channel must be a string");
  if (!/^[A-Za-z0-9._-]+$/.test(channel)) throw new Error("channel may only contain letters, digits, . _ -");
  return channel;
}

// Resolve a channel to its store file path.
function channelPath(channel) {
  const ch = normalizeChannel(channel);
  if (ch === "default") return DEFAULT_STORE;
  const reg = loadRegistry();
  if (reg[ch]) return reg[ch];
  return `${BASE_DIR}/${ch}.json`;
}

function loadStore(channel) { return loadJson(channelPath(channel), {}); }
function saveStore(channel, store) { saveJson(channelPath(channel), store); }

// ─── Tool implementations ─────────────────────────────────────────────────────

function bbSet({ key, value, channel }) {
  if (typeof key !== "string" || !key.length) throw new Error("key must be a non-empty string");
  const store = loadStore(channel);
  store[key] = value;
  saveStore(channel, store);
  return { ok: true, key, channel: normalizeChannel(channel) };
}

function bbGet({ key, channel }) {
  if (typeof key !== "string" || !key.length) throw new Error("key must be a non-empty string");
  const store = loadStore(channel);
  return { key, value: store[key] ?? null, found: key in store, channel: normalizeChannel(channel) };
}

function bbList({ prefix, channel } = {}) {
  const store = loadStore(channel);
  const keys = Object.keys(store);
  const filtered = prefix ? keys.filter(k => k.startsWith(prefix)) : keys;
  return { keys: filtered, count: filtered.length, channel: normalizeChannel(channel) };
}

function bbDelete({ key, channel }) {
  if (typeof key !== "string" || !key.length) throw new Error("key must be a non-empty string");
  const store = loadStore(channel);
  const existed = key in store;
  delete store[key];
  saveStore(channel, store);
  return { ok: true, key, existed, channel: normalizeChannel(channel) };
}

// Register (with path) or resolve (without) a channel's storage location.
// `path` may be a file (…/foo.json) or a directory (a /foo.json is appended). Absolute recommended.
function bbChannel({ channel, path }) {
  const ch = normalizeChannel(channel);
  if (ch === "default") {
    if (path) throw new Error("cannot relocate the 'default' channel");
    return { channel: ch, path: DEFAULT_STORE, registered: false };
  }
  if (path === undefined) {
    const reg = loadRegistry();
    return { channel: ch, path: channelPath(ch), registered: ch in reg };
  }
  let target = isAbsolute(path) ? path : resolvePath(path);
  if (!target.endsWith(".json")) target = `${target}/${ch}.json`;
  const reg = loadRegistry();
  reg[ch] = target;
  saveJson(REGISTRY_PATH, reg);
  ensureDir(target);
  return { channel: ch, path: target, registered: true };
}

function bbDrop({ channel }) {
  const ch = normalizeChannel(channel);
  if (ch === "default") throw new Error("refusing to drop the 'default' channel");
  const path = channelPath(ch);
  const existed = existsSync(path);
  if (existed) unlinkSync(path);
  const reg = loadRegistry();
  const wasRegistered = ch in reg;
  if (wasRegistered) { delete reg[ch]; saveJson(REGISTRY_PATH, reg); }
  return { ok: true, channel: ch, fileDeleted: existed, unregistered: wasRegistered };
}

function bbChannels() {
  const reg = loadRegistry();
  const known = new Map(); // channel → path
  // default
  known.set("default", DEFAULT_STORE);
  // registered
  for (const [ch, p] of Object.entries(reg)) known.set(ch, p);
  // auto global files in BASE_DIR
  if (existsSync(BASE_DIR)) {
    for (const f of readdirSync(BASE_DIR)) {
      if (!f.endsWith(".json")) continue;
      const name = basename(f, ".json");
      if (RESERVED.has(name)) continue;
      if (!known.has(name)) known.set(name, `${BASE_DIR}/${f}`);
    }
  }
  const channels = [...known.entries()].map(([channel, path]) => {
    const store = loadJson(path, {});
    return { channel, path, keys: Object.keys(store).length, registered: channel in reg };
  });
  return { channels, count: channels.length };
}

// ─── MCP protocol (JSON-RPC over stdio) ──────────────────────────────────────

const channelProp = { type: "string", description: "Optional channel id (separate store file). Omit for the default global store." };

const TOOLS = {
  bb_set: {
    description: "Set a key in the blackboard to any JSON-serializable value. Overwrites if the key exists. Optional `channel` selects a separate store.",
    inputSchema: {
      type: "object", required: ["key", "value"],
      properties: {
        key: { type: "string", description: "Blackboard key (any string)" },
        value: { description: "Any JSON-serializable value to store at this key" },
        channel: channelProp
      }
    },
    handler: bbSet
  },
  bb_get: {
    description: "Read the value at a blackboard key. Returns { key, value, found, channel }. value is null if the key does not exist.",
    inputSchema: { type: "object", required: ["key"], properties: { key: { type: "string" }, channel: channelProp } },
    handler: bbGet
  },
  bb_list: {
    description: "List keys in a channel, optionally filtered by prefix. Returns { keys, count, channel }.",
    inputSchema: { type: "object", properties: { prefix: { type: "string", description: "Optional prefix filter" }, channel: channelProp } },
    handler: bbList
  },
  bb_delete: {
    description: "Delete a key from a channel. Returns { ok, key, existed, channel }.",
    inputSchema: { type: "object", required: ["key"], properties: { key: { type: "string" }, channel: channelProp } },
    handler: bbDelete
  },
  bb_channel: {
    description: "Register a channel's storage path (e.g. a repo-local .blackboard/<channel>.json), or resolve it if `path` is omitted. Returns { channel, path, registered }.",
    inputSchema: {
      type: "object", required: ["channel"],
      properties: {
        channel: { type: "string", description: "Channel id" },
        path: { type: "string", description: "Absolute file or directory for this channel's store. Omit to just resolve the current path." }
      }
    },
    handler: bbChannel
  },
  bb_drop: {
    description: "Retire a whole channel — delete its store file and registry entry. Refuses the 'default' channel. Returns { ok, channel, fileDeleted, unregistered }.",
    inputSchema: { type: "object", required: ["channel"], properties: { channel: { type: "string" } } },
    handler: bbDrop
  },
  bb_channels: {
    description: "List known channels (default + registered + auto global files) with key counts. Returns { channels, count }.",
    inputSchema: { type: "object", properties: {} },
    handler: bbChannels
  }
};

function makeResponse(id, result) { return { jsonrpc: "2.0", id, result }; }
function makeError(id, code, message, data) { return { jsonrpc: "2.0", id, error: { code, message, ...(data ? { data } : {}) } }; }

function handleRequest(req) {
  const { id, method, params } = req;

  if (method === "initialize") {
    return makeResponse(id, {
      protocolVersion: "2024-11-05",
      capabilities: { tools: {} },
      serverInfo: { name: "blackboard-mcp", version: "0.2.0" }
    });
  }

  if (method === "tools/list") {
    return makeResponse(id, {
      tools: Object.entries(TOOLS).map(([name, def]) => ({ name, description: def.description, inputSchema: def.inputSchema }))
    });
  }

  if (method === "tools/call") {
    const { name, arguments: args } = params ?? {};
    const def = TOOLS[name];
    if (!def) return makeError(id, -32601, `unknown tool: ${name}`);
    try {
      const result = def.handler(args ?? {});
      return makeResponse(id, { content: [{ type: "text", text: JSON.stringify(result) }] });
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

process.stderr.write(`[blackboard-mcp] ready (v0.2.0, channels), default store at ${DEFAULT_STORE}\n`);
