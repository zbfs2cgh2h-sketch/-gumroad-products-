# Category 8: API Development & Integration (10 Prompts)

---

## Prompt #73 — REST API Endpoint Generator

```
Generate a complete REST API endpoint with all the production details people forget.

Resource: [e.g., "users", "orders", "products"]
Operations: [CRUD, or specific ones — e.g., "create and list only"]
Framework: [Express / FastAPI / Django REST / Spring Boot / Gin / etc.]

For each endpoint, include:
1. Route definition with proper HTTP methods
2. Request validation (schema validation, not just "trust the input")
3. Authentication middleware
4. Authorization check (can this user do this action?)
5. Business logic (or a clear placeholder)
6. Error handling (specific errors, not just 500)
7. Response formatting (consistent shape: { data, error, metadata })
8. Pagination (cursor-based, not offset — explain why)
9. Rate limiting
10. Logging (request ID, user ID, duration)
11. OpenAPI/Swagger annotations if framework supports it

Also generate: request/response types, validation schema, and a test for each endpoint.
```

---

## Prompt #74 — Third-Party API Integration

```
Write a robust integration with this third-party API.

API: [name — e.g., Stripe, Twilio, GitHub, OpenAI]
Documentation: [URL]
Operations I need: [list specific API calls]
Language: [Python / JavaScript / etc.]

Build a client class/module with:
1. **Authentication** (API key, OAuth, whatever the API uses)
2. **Retry logic** (exponential backoff, configurable max retries)
3. **Timeout handling** (connect timeout + read timeout, both configurable)
4. **Rate limit handling** (respect rate limit headers, queue/delay requests)
5. **Error handling** (parse API error responses, throw typed exceptions)
6. **Logging** (request/response at debug level, errors at error level — NEVER log secrets)
7. **Response typing** (parse JSON into typed objects, not raw dicts)
8. **Testing** (mock responses for unit tests, record/replay for integration tests)
9. **Circuit breaker** (stop calling if the API is consistently failing)

Don't use the official SDK unless I ask for it — I want to understand the API contract.
Show the client code + usage example + test with mocked responses.
```

---

## Prompt #75 — Webhook Handler

```
Build a production-ready webhook handler.

Webhook source: [e.g., Stripe, GitHub, Shopify, or custom]
Events to handle: [list event types]
Framework: [Express / FastAPI / etc.]

Include:
1. **Signature verification** (verify the webhook is really from [source])
   - Show the exact verification algorithm
2. **Idempotency** (handle duplicate deliveries — same event sent twice)
   - Store event IDs, check before processing
3. **Async processing** (respond 200 immediately, process in background)
   - Don't make the webhook source wait for your business logic
4. **Event routing** (map event type to handler function)
5. **Error handling** (if processing fails, don't lose the event)
   - Dead letter queue or retry table
6. **Logging** (every event received, processed, or failed — with event ID)
7. **Timeout protection** (what if your handler takes too long?)

Also provide:
- Local testing setup (how to receive webhooks locally — ngrok, etc.)
- Integration test that sends a test webhook
```

---

## Prompt #76 — GraphQL Schema & Resolvers

```
Design a GraphQL schema and resolvers for this domain.

Domain entities:
[describe your data model — e.g., "Users have Orders, Orders have LineItems, LineItems reference Products"]

Operations needed:
- Queries: [list — e.g., "get user by ID", "list orders with filters"]
- Mutations: [list — e.g., "create order", "update user profile"]
- Subscriptions: [list if needed — e.g., "order status changes"]

Framework: [Apollo Server / Strawberry / Graphene / etc.]

Build:
1. **Schema** (SDL format — types, queries, mutations, inputs)
2. **Resolvers** with:
   - N+1 prevention (DataLoader / batch loading)
   - Input validation
   - Authorization per field/type
   - Error handling (user errors vs system errors)
3. **Pagination** (Relay cursor-based connection pattern)
4. **Filtering/sorting** (flexible input types)
5. **Depth/complexity limiting** (prevent abusive queries)

Include: example queries that clients would actually send.
```

---

## Prompt #77 — API Error Response Standard

```
Design a consistent error response format for my API.

Current problem:
[describe — e.g., "each endpoint returns errors differently", "frontend can't parse errors reliably"]

Requirements:
- Support: validation errors (multiple fields), auth errors, not found, rate limits, server errors
- Machine-readable (status codes + error codes for programmatic handling)
- Human-readable (message text for displaying to users)
- Debuggable (request ID, timestamp for support tickets)

Design:
1. Error response schema (JSON structure used by EVERY endpoint)
2. Error code registry (enum/constants: VALIDATION_ERROR, AUTH_EXPIRED, etc.)
3. Validation error format (which field, what's wrong, what's expected)
4. Error middleware/handler (centralized, no per-endpoint error formatting)
5. Client-side error handling example (how the frontend should parse this)
6. Error logging (what to log server-side for each error)

Show: the schema, 5+ example error responses, and the middleware code.

Reference standards: [RFC 7807 Problem Details / custom / don't care]
```

---

## Prompt #78 — API Rate Limiter Implementation

```
Implement rate limiting for my API.

Requirements:
- Global limit: [e.g., 1000 requests/minute per API key]
- Per-endpoint limits: [e.g., POST /upload: 10/minute, GET /search: 100/minute]
- Burst handling: [allow brief bursts? Or strict?]
- Response: [429 Too Many Requests with Retry-After header]

Framework: [Express / FastAPI / etc.]
Storage: [Redis / in-memory / database]

Algorithm: [token bucket / sliding window / fixed window / leaky bucket — or recommend one]

Implement:
1. Rate limit middleware (plug into any endpoint)
2. Key extraction (by API key, user ID, IP, or combination)
3. Response headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)
4. 429 response body (clear message about the limit and when to retry)
5. Different limits for different tiers (free/pro/enterprise)
6. Distributed setup (multiple servers sharing the same limit via Redis)
7. Graceful degradation (what if Redis is down — fail open or fail closed?)

Show the code + configuration + test verifying the limit works.
```

---

## Prompt #79 — Request/Response Logging Middleware

```
Build request/response logging middleware for my API.

Framework: [Express / FastAPI / Koa / Django / etc.]

Log this for every request:
1. Request ID (generate UUID, add to response headers)
2. Timestamp
3. HTTP method + path
4. Query parameters
5. Request body (REDACT sensitive fields: password, token, credit card)
6. User/API key (from auth context)
7. Response status code
8. Response time (ms)
9. Response body (optional — only for errors, truncated)

Requirements:
- Structured logging (JSON, not free text)
- Correlation: request ID propagated through entire request lifecycle
- Redaction: NEVER log passwords, tokens, or PII
- Performance: logging shouldn't add >1ms to request time
- Size: truncate large request/response bodies (>10KB)
- Sampling: log 100% of errors, sample success responses at [N]%

Show the middleware, configuration for redaction rules, and example log output.
```

---

## Prompt #80 — API Client SDK Generator

```
Generate a client SDK/wrapper for this API.

API specification:
[paste OpenAPI spec, or list endpoints with request/response shapes]

Language: [Python / TypeScript / Go / etc.]

The SDK should feel native to [language] — not like a thin HTTP wrapper.

Include:
1. **Client class** with configuration (base URL, API key, timeout)
2. **Typed methods** for each endpoint (parameters → typed response)
3. **Error types** (specific exceptions for 400, 401, 404, 429, 500)
4. **Retry logic** (configurable, exponential backoff)
5. **Pagination helpers** (auto-paginate, or convenient iterator)
6. **Request/response logging** (debug level)
7. **Usage examples** for each method
8. **Type definitions** for all request/response objects
9. **Tests** with mocked HTTP responses

Don't use code generation tools — hand-write it for a clean, idiomatic API.
```

---

## Prompt #81 — WebSocket Implementation

```
Implement WebSocket communication for this real-time feature.

Feature: [describe — e.g., "live chat", "real-time notifications", "collaborative editing"]

Server framework: [Express+ws / FastAPI+websockets / Socket.IO / etc.]
Client: [browser / React / mobile / Node service]

Implement:
1. **Connection lifecycle** (connect, authenticate, heartbeat/ping, disconnect)
2. **Authentication** (verify token on connection, not just on upgrade)
3. **Message protocol** (define message types and JSON schema for each)
4. **Rooms/channels** (group connections by topic/user)
5. **Reconnection** (client-side automatic reconnection with backoff)
6. **Message ordering** (handle out-of-order delivery)
7. **Offline queue** (buffer messages when disconnected, send on reconnect)
8. **Scaling** (how to handle WebSockets across multiple server instances — Redis pub/sub?)
9. **Error handling** (malformed messages, server errors mid-connection)
10. **Monitoring** (active connections, message throughput, error rate)

Show: server code, client code, and message protocol documentation.
```

---

## Prompt #82 — API Security Hardening

```
Harden this API against common attacks.

API code:
[paste relevant code — routes, middleware, auth]

Framework: [Express / FastAPI / etc.]
Deployment: [behind reverse proxy? CDN? Direct?]

Check and implement protections for:
1. **Injection**: SQL injection, NoSQL injection, command injection
2. **Authentication**: Brute force protection, credential stuffing
3. **Authorization**: IDOR (insecure direct object references), privilege escalation
4. **Input**: Request body size limits, content-type validation, file upload restrictions
5. **Headers**: CORS configuration, security headers (HSTS, CSP, X-Frame-Options)
6. **Rate limiting**: By IP, by user, by endpoint
7. **Secrets**: Environment variable handling, no secrets in logs/errors
8. **Dependencies**: Known vulnerable packages
9. **SSRF**: If the API fetches URLs, prevent internal network access
10. **Denial of Service**: Regex DoS, large payload, slow loris

For each: show the vulnerability, the fix (code), and how to verify it's fixed.
```
