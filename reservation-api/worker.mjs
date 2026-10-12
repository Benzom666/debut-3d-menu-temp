import { adminPage } from './admin-page.mjs';

const JSON_HEADERS = { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' };
const STATUSES = new Set(['pending', 'confirmed', 'cancelled']);

function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), { status, headers: { ...JSON_HEADERS, ...headers } });
}

function allowedOrigin(request, env) {
  const origin = request.headers.get('origin');
  if (!origin) return null;
  const allowed = new Set([new URL(request.url).origin, ...(env.PUBLIC_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean)]);
  return allowed.has(origin) ? origin : false;
}

function corsHeaders(origin) {
  return origin ? {
    'access-control-allow-origin': origin,
    'access-control-allow-methods': 'POST, OPTIONS',
    'access-control-allow-headers': 'content-type',
    'vary': 'Origin',
  } : {};
}

function staffAccess(request, env) {
  const userId = request.headers.get('oai-authenticated-user-id')?.trim();
  const email = request.headers.get('oai-authenticated-user-email')?.trim().toLowerCase();
  if (!userId || !email) return { status: 401 };
  const staff = new Set((env.ADMIN_EMAILS || '').split(',').map(s => s.trim().toLowerCase()).filter(Boolean));
  return staff.has(email) ? { email } : { status: 403 };
}

function torontoToday(now) {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Toronto', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(now);
  const value = Object.fromEntries(parts.map(part => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}`;
}

function validateReservation(value, now) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return null;
  const name = typeof value.name === 'string' ? value.name.trim() : '';
  const email = typeof value.email === 'string' ? value.email.trim().toLowerCase() : '';
  const phone = typeof value.phone === 'string' ? value.phone.trim() : '';
  const date = typeof value.date === 'string' ? value.date : '';
  const time = typeof value.time === 'string' ? value.time : '';
  const guests = value.guests;
  const message = typeof value.message === 'string' ? value.message.trim() : '';
  if (name.length < 2 || name.length > 100 || /[<>]/.test(name)) return null;
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return null;
  if (phone.length > 30 || phone.replace(/\D/g, '').length < 7 || /[<>]/.test(phone)) return null;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || date < torontoToday(now)) return null;
  const day = new Date(`${date}T12:00:00Z`);
  if (Number.isNaN(day.getTime()) || day.toISOString().slice(0, 10) !== date || day.getUTCDay() === 2) return null;
  if (day.getTime() > now.getTime() + 180 * 86400000) return null;
  if (!/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(time)) return null;
  if (!Number.isInteger(guests) || guests < 1 || guests > 20) return null;
  if (message.length > 1000 || /[<>]/.test(message)) return null;
  return { name, email, phone, date, time, guests, message };
}

async function parseBody(request) {
  if (!request.headers.get('content-type')?.toLowerCase().startsWith('application/json')) return null;
  if (Number(request.headers.get('content-length') || 0) > 8192) return null;
  const text = await request.text();
  if (text.length > 8192) return null;
  try { return JSON.parse(text); } catch { return null; }
}

async function rateLimit(env, request, now) {
  const ip = request.headers.get('cf-connecting-ip');
  if (!ip || typeof env.RATE_LIMIT_SECRET !== 'string' || env.RATE_LIMIT_SECRET.length < 32) {
    return { unavailable: true };
  }
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(env.RATE_LIMIT_SECRET),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const bytes = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(ip));
  const hash = Array.from(new Uint8Array(bytes), byte => byte.toString(16).padStart(2, '0')).join('');
  const window = Math.floor(now.getTime() / 3600000);
  const row = await env.DB.prepare(`INSERT INTO reservation_rate_limits (client_hash, window_hour, count)
    VALUES (?, ?, 1) ON CONFLICT (client_hash, window_hour) DO UPDATE SET count = count + 1
    RETURNING count`).bind(hash, window).first();
  return { limited: !row || row.count > 5 };
}

export function createHandler(clock = () => new Date()) {
  return async function handle(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/$/, '') || '/';
    const origin = allowedOrigin(request, env);
    if (origin === false && request.method !== 'GET') return json({ error: 'Origin not allowed' }, 403);
    if (path === '/admin' && request.method === 'GET') {
      const access = staffAccess(request, env);
      if (access.status === 401) return new Response(null, {
        status: 302, headers: { location: '/signin-with-chatgpt?return_to=%2Fadmin', 'cache-control': 'no-store' },
      });
      if (access.status) return new Response('Access denied', { status: 403, headers: { 'cache-control': 'no-store' } });
      return new Response(adminPage, { headers: {
        'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store',
        'x-content-type-options': 'nosniff', 'referrer-policy': 'no-referrer',
      } });
    }
    if (path === '/api/reservations') {
      if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders(origin) });
      if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405);
      if (!env.DB) return json({ error: 'Reservations unavailable' }, 503, corsHeaders(origin));
      const reservation = validateReservation(await parseBody(request), clock());
      if (!reservation) return json({ error: 'Check your reservation details' }, 400, corsHeaders(origin));
      const limit = await rateLimit(env, request, clock());
      if (limit.unavailable) return json({ error: 'Reservations unavailable' }, 503, corsHeaders(origin));
      if (limit.limited) return json({ error: 'Too many requests. Please call the restaurant.' }, 429, corsHeaders(origin));
      const id = crypto.randomUUID();
      const stamp = clock().toISOString();
      await env.DB.prepare(`INSERT INTO reservations
        (id, name, email, phone, reservation_date, reservation_time, guests, message, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)`)
        .bind(id, reservation.name, reservation.email, reservation.phone, reservation.date,
          reservation.time, reservation.guests, reservation.message, stamp, stamp).run();
      return json({ id, status: 'pending' }, 201, corsHeaders(origin));
    }
    if (path === '/api/admin/reservations' || path.startsWith('/api/admin/reservations/')) {
      const access = staffAccess(request, env);
      if (access.status) return json({ error: access.status === 401 ? 'Sign in required' : 'Access denied' }, access.status);
      if (!env.DB) return json({ error: 'Reservations unavailable' }, 503);
      if (path === '/api/admin/reservations' && request.method === 'GET') {
        const rows = await env.DB.prepare(`SELECT id, name, email, phone, reservation_date, reservation_time,
          guests, message, status, created_at, updated_at, updated_by FROM reservations
          ORDER BY reservation_date DESC, created_at DESC LIMIT 100`).all();
        return json({ reservations: rows.results });
      }
      if (path.startsWith('/api/admin/reservations/') && request.method === 'PATCH') {
        const id = path.slice('/api/admin/reservations/'.length);
        const body = await parseBody(request);
        if (!/^[a-zA-Z0-9-]{1,64}$/.test(id) || !body || !STATUSES.has(body.status)) {
          return json({ error: 'Invalid reservation status' }, 400);
        }
        const result = await env.DB.prepare(`UPDATE reservations SET status = ?, updated_at = ?, updated_by = ? WHERE id = ?`)
          .bind(body.status, clock().toISOString(), access.email, id).run();
        if (!result.meta?.changes) return json({ error: 'Reservation not found' }, 404);
        return json({ id, status: body.status });
      }
      return json({ error: 'Method not allowed' }, 405);
    }
    return json({ error: 'Not found' }, 404);
  };
}

export default { fetch: createHandler() };

