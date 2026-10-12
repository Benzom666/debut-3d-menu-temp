# Reservation service (local build)

This is a replacement for the original site's reservation endpoint. It is **not deployed or connected to the public booking page**. The current booking page continues to use phone and email.

The service is intended for a public Sites Worker project with a D1 database. It must run behind Sites dispatch, which supplies the trusted `oai-authenticated-user-id` and `oai-authenticated-user-email` headers after ChatGPT sign-in. Do not deploy this Worker to a generic host that accepts those headers from visitors.

## Routes

| Route | Access | Purpose |
| --- | --- | --- |
| `POST /api/reservations` | Public, rate limited | Submit a request; returns only an ID and `pending` status. |
| `GET /api/reservations` | Nobody | Returns 405. Guest records are never public. |
| `GET /admin` | Signed-in, allowlisted staff | Branded reservation dashboard. |
| `GET /api/admin/reservations` | Signed-in, allowlisted staff | Up to 100 recent requests. |
| `PATCH /api/admin/reservations/:id` | Signed-in, allowlisted staff | Set pending, confirmed, or cancelled. |

The guest request is **not** a confirmed table. Staff must contact the guest. There is no automated notification or email provider yet, so the public form must stay offline until staff can reliably monitor the dashboard and receive alerts.

## Required hosted configuration

- `DB`: D1 binding with `schema.sql` applied as a migration.
- `ADMIN_EMAILS`: Comma-separated staff email allowlist. Empty or absent means nobody can access admin records.
- `RATE_LIMIT_SECRET`: A private random value of at least 32 characters. Missing or short values disable public submissions.
- `PUBLIC_ORIGINS`: Exact, comma-separated public frontend origins allowed to submit from a browser. Set to the temporary GitHub Pages origin and current Sites origin when enabling the form. No wildcard.

No guest details, staff emails, or secret values belong in source control. The service limits each network address to five submissions per hour, using an HMAC of the address in storage. It validates dates, disallows Tuesdays, caps party size and request length, uses parameterized SQL, and denies public reads. A production launch also needs a notification path, a retention policy, live identity tests, and a review of the original site's exposed endpoint.

## Local verification

```sh
node --test reservation-api/worker.test.mjs
```

The tests use an in-memory SQLite database to execute the real schema and SQL queries. They do not establish that the Sites identity headers, D1 binding, or live email workflow are configured.
