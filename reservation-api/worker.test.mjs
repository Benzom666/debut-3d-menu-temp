import assert from 'node:assert/strict';
import test from 'node:test';
import { readFileSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { createHandler } from './worker.mjs';

const reservation = {
  name: 'Test Guest',
  email: 'guest@example.com',
  phone: '705-555-0100',
  date: '2026-10-15',
  time: '19:00',
  guests: 2,
  message: 'Window seat if available',
};

function fakeDB() {
  const calls = [];
  return {
    calls,
    prepare(sql) {
      const call = { sql, values: [] };
      calls.push(call);
      return {
        bind(...values) { call.values = values; return this; },
        async first() { return { count: 1 }; },
        async run() { return { success: true, meta: { changes: 1 } }; },
        async all() { return { results: [{ id: 'r1', name: 'Test Guest', status: 'pending' }] }; },
      };
    },
  };
}

function makeEnv(db = fakeDB()) {
  return { DB: db, ADMIN_EMAILS: 'owner@example.com,manager@example.com', RATE_LIMIT_SECRET: 'local-test-secret-that-is-long-enough-123' };
}

const handle = createHandler(() => new Date('2026-10-12T18:00:00Z'));
const request = (path, method = 'GET', body, headers = {}) => new Request(`https://example.com${path}`, {
  method,
  headers: { 'content-type': 'application/json', 'cf-connecting-ip': '203.0.113.10', ...headers },
  body: body === undefined ? undefined : JSON.stringify(body),
});

test('the public endpoint never returns reservation records', async () => {
  const response = await handle(request('/api/reservations'), makeEnv());
  assert.equal(response.status, 405);
});

test('admin records require a signed-in allowlisted staff identity', async () => {
  const db = fakeDB();
  const env = makeEnv(db);
  assert.equal((await handle(request('/api/admin/reservations'), env)).status, 401);
  assert.equal((await handle(request('/api/admin/reservations', 'GET', undefined, {
    'oai-authenticated-user-email': 'visitor@example.com',
    'oai-authenticated-user-id': 'visitor-id',
  }), env)).status, 403);
  assert.equal((await handle(request('/api/admin/reservations', 'GET', undefined, {
    'oai-authenticated-user-email': 'owner@example.com',
  }), env)).status, 401);
  assert.equal(db.calls.length, 0);
  const allowed = await handle(request('/api/admin/reservations', 'GET', undefined, {
    'oai-authenticated-user-email': 'OWNER@example.com',
    'oai-authenticated-user-id': 'owner-id',
  }), env);
  assert.equal(allowed.status, 200);
  assert.equal((await allowed.json()).reservations.length, 1);
});

test('admin stays closed when staff allowlist is unconfigured', async () => {
  const env = makeEnv();
  delete env.ADMIN_EMAILS;
  const response = await handle(request('/api/admin/reservations', 'GET', undefined, {
    'oai-authenticated-user-email': 'owner@example.com',
    'oai-authenticated-user-id': 'owner-id',
  }), env);
  assert.equal(response.status, 403);
});

test('admin dashboard requires sign-in and staff authorization before serving HTML', async () => {
  const env = makeEnv();
  const anonymous = await handle(request('/admin'), env);
  assert.equal(anonymous.status, 302);
  assert.equal(anonymous.headers.get('location'), '/signin-with-chatgpt?return_to=%2Fadmin');
  const visitor = await handle(request('/admin', 'GET', undefined, {
    'oai-authenticated-user-id': 'visitor-id',
    'oai-authenticated-user-email': 'visitor@example.com',
  }), env);
  assert.equal(visitor.status, 403);
  const staff = await handle(request('/admin', 'GET', undefined, {
    'oai-authenticated-user-id': 'owner-id',
    'oai-authenticated-user-email': 'owner@example.com',
  }), env);
  assert.equal(staff.status, 200);
  assert.match(staff.headers.get('content-type'), /text\/html/);
  const html = await staff.text();
  assert.match(html, /Reservations/);
  assert.match(html, /\/api\/admin\/reservations/);
});

test('valid reservation is persisted and returns only a receipt', async () => {
  const db = fakeDB();
  const response = await handle(request('/api/reservations', 'POST', reservation), makeEnv(db));
  const result = await response.json();
  assert.equal(response.status, 201);
  assert.equal(result.status, 'pending');
  assert.ok(result.id);
  assert.equal(result.email, undefined);
  assert.ok(db.calls.some(call => call.sql.includes('INSERT INTO reservations')));
});

test('public writes stay closed without a strong rate-limit secret', async () => {
  const env = makeEnv();
  env.RATE_LIMIT_SECRET = 'weak';
  const response = await handle(request('/api/reservations', 'POST', reservation), env);
  assert.equal(response.status, 503);
  assert.equal(env.DB.calls.length, 0);
});

test('past dates, Tuesdays, and malformed details do not write records', async () => {
  const db = fakeDB();
  for (const invalid of [
    { ...reservation, date: '2026-10-11' },
    { ...reservation, date: '2026-10-13' },
    { ...reservation, email: 'not-an-email' },
    { ...reservation, guests: 0 },
  ]) {
    const response = await handle(request('/api/reservations', 'POST', invalid), makeEnv(db));
    assert.equal(response.status, 400);
  }
  assert.equal(db.calls.length, 0);
});

test('only staff can update status, and updates are restricted to known values', async () => {
  const env = makeEnv();
  const path = '/api/admin/reservations/r1';
  assert.equal((await handle(request(path, 'PATCH', { status: 'confirmed' }), env)).status, 401);
  assert.equal((await handle(request(path, 'PATCH', { status: 'deleted' }, {
    'oai-authenticated-user-email': 'owner@example.com',
    'oai-authenticated-user-id': 'owner-id',
  }), env)).status, 400);
  assert.equal((await handle(request(path, 'PATCH', { status: 'confirmed' }, {
    'oai-authenticated-user-email': 'owner@example.com',
    'oai-authenticated-user-id': 'owner-id',
  }), env)).status, 200);
});

test('SQLite storage enforces private reads, status updates, and rate limits end to end', async () => {
  const sqlite = new DatabaseSync(':memory:');
  sqlite.exec(readFileSync(new URL('./schema.sql', import.meta.url), 'utf8'));
  const db = {
    prepare(sql) {
      const statement = sqlite.prepare(sql);
      let values = [];
      return {
        bind(...next) { values = next; return this; },
        async first() { return statement.get(...values); },
        async all() { return { results: statement.all(...values) }; },
        async run() { return { meta: { changes: statement.run(...values).changes } }; },
      };
    },
  };
  const env = makeEnv(db);
  const posted = await handle(request('/api/reservations', 'POST', reservation), env);
  assert.equal(posted.status, 201);
  const { id } = await posted.json();
  assert.equal((await handle(request('/api/reservations'), env)).status, 405);
  const headers = { 'oai-authenticated-user-email': 'owner@example.com', 'oai-authenticated-user-id': 'owner-id' };
  const before = await handle(request('/api/admin/reservations', 'GET', undefined, headers), env);
  assert.equal((await before.json()).reservations[0].email, reservation.email);
  const updated = await handle(request(`/api/admin/reservations/${id}`, 'PATCH', { status: 'confirmed' }, headers), env);
  assert.equal(updated.status, 200);
  assert.equal(sqlite.prepare('SELECT status, updated_by FROM reservations WHERE id = ?').get(id).status, 'confirmed');
  for (let i = 0; i < 4; i++) {
    assert.equal((await handle(request('/api/reservations', 'POST', reservation), env)).status, 201);
  }
  assert.equal((await handle(request('/api/reservations', 'POST', reservation), env)).status, 429);
  sqlite.close();
});
