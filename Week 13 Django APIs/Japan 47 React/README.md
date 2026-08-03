# Japan 47

Japan 47 is an API-first community travel guide to Japan’s 9 regions and 47 prefectures. Django is the reusable backend for the React web application and future native clients such as SwiftUI.

## Architecture

```text
Browser / SwiftUI
        │ JSON + multipart + JWT
        ▼
Nginx ──┬── /, React Router fallback → built React frontend
        ├── /api/, /admin/           → Django + Gunicorn
        ├── /media/                  → persistent uploads
        └── /static/                 → collected Django admin/static assets
                                         │
                                         ├── PostgreSQL (production data)
                                         └── Redis (shared cache)
```

The copied SQLite database and all existing uploads remain in `backend/`. Production uses an explicit, backed-up Django fixture cutover described in `POSTGRES_MIGRATION.md`; container restarts never import data. The public UI lives exclusively in React, while Django exposes JSON APIs and the internal Django admin.

## Prerequisites

- Python 3.12 or newer (the migrated copy was verified with 3.14.0)
- Node 20.19+ or 22.12+ (verified with 24.18.0)
- npm (verified with 11.16.0)
- Docker with Compose for the production-style stack

PostgreSQL is supplied by Docker; local development defaults to the preserved SQLite database.

## Local development

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp backend/.env.example backend/.env
cd backend
python manage.py migrate
python manage.py check
python manage.py runserver
```

In another terminal:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api`, `/media`, and `/static` to Django at `http://localhost:8000`; frontend code never hardcodes that host.

Admin: `http://localhost:8000/admin/`  
OpenAPI schema: `http://localhost:8000/api/schema/`  
Swagger UI: `http://localhost:8000/api/docs/`

## Environment variables

Copy `.env.example` for Docker or `backend/.env.example` for local Django. Never commit a real `.env`.

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Required secret; production refuses the development placeholder |
| `DJANGO_DEBUG` | Development debug toggle; production settings force `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated accepted hosts |
| `DATABASE_URL` | SQLite or PostgreSQL URL |
| `CORS_ALLOWED_ORIGINS` | Comma-separated browser origins |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for admin/session tools |
| `FRONTEND_URL` | Public React origin used for frontend-owned asset URLs |
| `VITE_PUBLIC_URL` | Public origin compiled into `sitemap.xml` and `robots.txt` |
| `JWT_ACCESS_MINUTES` / `JWT_REFRESH_DAYS` | JWT lifetimes |
| `API_ANON_THROTTLE` / `API_USER_THROTTLE` | General API rates |
| `AUTH_THROTTLE` | Sensitive authentication endpoint rate |
| `REDIS_URL` / `CACHE_DEFAULT_TIMEOUT` | Shared production cache and default lifetime |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Docker PostgreSQL credentials |
| `VITE_API_BASE_URL` | Browser API prefix, normally `/api/v1` |
| `EMAIL_*`, `ADMIN_EMAILS` | SMTP delivery and recipients for server-error alerts |

Generate a development secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## Database and existing data

Local commands operate on `backend/db.sqlite3`, preserving all original records and migration history:

```bash
cd backend
../.venv/bin/python manage.py showmigrations
../.venv/bin/python manage.py migrate
```

Follow [POSTGRES_MIGRATION.md](POSTGRES_MIGRATION.md) for the guarded `dumpdata`/`loaddata` cutover, model-count verification, media copy, backup, and rollback commands. PostgreSQL, Redis, static files, and media use separate named volumes.

## Media and images

- Django owns image metadata and multipart upload validation.
- Files up to 8 MB are accepted; MIME type and pixel count are validated, EXIF orientation is removed, and large images are constrained to 1200 px.
- Non-JPEG/WebP uploads are converted to WebP, and gallery images receive separate 480×320 WebP thumbnails.
- Profile images are EXIF-corrected, square-cropped, converted to JPEG, and limited to 512 px.
- API serializers return absolute media URLs using the request host, so React and SwiftUI receive usable URLs.
- Django serves media only in development. Nginx serves `/media/` in production.

Do not rename or remove `backend/media/`. To test an upload, log in, open a prefecture, choose **Suggest a place**, and submit an image.

## Authentication

The API uses short-lived JWT access tokens plus rotating refresh tokens with blacklist support:

1. Register at `POST /api/v1/auth/register/`.
2. Obtain tokens at `POST /api/v1/auth/login/`.
3. Send `Authorization: Bearer <access>`.
4. Refresh at `POST /api/v1/auth/refresh/`.
5. Revoke the refresh token at `POST /api/v1/auth/logout/`.

The React client stores tokens locally for this portfolio deployment and automatically attempts one refresh after a 401. For a hardened public web deployment, consider keeping the refresh token in an HttpOnly secure same-site cookie. Native SwiftUI should store tokens in Keychain.

Example:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"your-user","password":"your-password"}'

curl http://localhost:8000/api/v1/profile/ \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

Validation failures use one stable envelope:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Please correct the highlighted fields.",
    "fields": { "email": ["Enter a valid email address."] }
  }
}
```

## API v1 summary

| Endpoint | Access and purpose |
|---|---|
| `GET /api/v1/health/` | Public health check |
| `GET /api/v1/home/` | Latest, ranked, and contributor homepage data |
| `GET /api/v1/regions/`, `/{name}/` | Region list/detail with computed ratings |
| `GET /api/v1/prefectures/`, `/{name}/` | Search/filter/order and detail previews |
| `/api/v1/places/`, `/{id}/` | Public reads; authenticated create; owner/staff mutation |
| `GET /api/v1/places/trending/` | Places with the most review activity in the last 30 days |
| `POST /api/v1/places/{id}/images/` | Owner/staff gallery upload with generated thumbnail |
| `GET /api/v1/places/?search=&prefecture=&region=&min_rating=&ordering=&page=` | Filtered, ordered, paginated discovery |
| `/api/v1/reviews/`, `/{id}/` | Public reads; authenticated owner-scoped writes |
| `GET/PATCH /api/v1/profile/` | Current private profile and multipart update |
| `GET /api/v1/contributors/{user_id}/` | Public profile without email/login identifier |
| `GET /api/v1/badges/` | Badge thresholds and assets |
| `GET /api/v1/search/?q=` | Unified published-content search |
| `/api/v1/favorites/`, `/visited-places/` | Authenticated personal travel tracking |
| `/api/v1/collections/`, `/itineraries/` | Personal collections and itinerary planning |
| `POST/DELETE /api/v1/places/{id}/favorite/`, `/visited/` | Toggle personal place state |
| `POST/DELETE /api/v1/reviews/{id}/helpful/` | Helpful review voting |
| `/api/v1/reports/` | Authenticated moderation reports |
| `/api/v1/auth/...` | Register, login, refresh, logout |

Place writes accept JSON or multipart fields: `prefecture_id`, `name`, `description`, `image`, `city`, `google_maps_url`, `official_website`, `travel_tips`, `best_season`, `latitude`, and `longitude`. New submissions are pending. A non-staff edit to published content returns it to moderation.

## Tests and quality checks

```bash
# Backend
cd backend
DJANGO_SETTINGS_MODULE=config.settings.test ../.venv/bin/python manage.py check
../.venv/bin/python manage.py test
../.venv/bin/python manage.py spectacular --file /tmp/japan47-schema.yml --validate

# Frontend
cd ../frontend
npm run lint
npm test
npm run build
```

The backend suite covers serializers through endpoint behavior, auth, permissions, moderation visibility, CRUD, duplicate review validation, field errors, uploads, and absolute media URLs. Frontend tests cover route rendering, loading, API errors, and login submission/navigation.

## Docker production-style stack

```bash
cp .env.example .env
# Replace every placeholder and use the real HTTPS domain in .env
docker compose config
docker compose up --build
```

Open `http://localhost` (or the configured `HTTP_PORT`). Useful commands:

```bash
docker compose ps
docker compose logs -f backend nginx
docker compose exec backend python manage.py check --deploy
docker compose exec backend python manage.py test
docker compose exec backend python manage.py createsuperuser
docker compose exec db pg_dump -U japan47 -d japan47 -Fc -f /tmp/japan47.dump
docker compose down
```

`docker compose down` preserves named volumes. `docker compose down -v` destroys PostgreSQL and persistent media and should only be used intentionally after a backup.

For HTTPS, place a TLS-aware load balancer in front or add certificate/listen configuration to Nginx, then set `DJANGO_SECURE_SSL_REDIRECT=True`, `DJANGO_SECURE_COOKIES=True`, use HTTPS origins, and enable secure deployment hosts. The Compose example defaults secure cookies off only so Django admin can be tested over local HTTP; production settings default them on when the variable is omitted.

### Hetzner deployment handoff

1. Create a VPS, restrict SSH to keys, enable a firewall for ports 22, 80, and 443, and install Docker Engine plus its Compose plugin.
2. Point the chosen domain's A/AAAA records at the VPS. The domain name and DNS credentials are intentionally not stored in this repository.
3. Clone the repository, copy `.env.example` to `.env`, replace every placeholder, set all public URLs to the HTTPS domain, and run the PostgreSQL cutover in `POSTGRES_MIGRATION.md`.
4. Put a TLS terminator such as Hetzner Load Balancer, Caddy, or a Certbot-managed Nginx listener in front of this HTTP stack. Only enable Django's secure redirect/cookies after HTTPS is reachable.
5. Run `docker compose up -d --build`, then execute the deploy checks and manual smoke test below.

Back up both database and media. For example, schedule `pg_dump -Fc` to encrypted off-server storage and snapshot the `media_data` volume daily; retain multiple generations and rehearse restoration. Container health checks cover PostgreSQL, Redis, Django, and React. Forward stdout logs and `/api/v1/health/` to the operator's monitoring provider, and configure SMTP variables so uncaught Django request errors reach `ADMIN_EMAILS`.

### Production smoke test

```bash
curl -fsS https://YOUR_DOMAIN/api/v1/health/
curl -fsS https://YOUR_DOMAIN/api/schema/ -o /tmp/japan47-openapi.yml
curl -fsS https://YOUR_DOMAIN/regions -o /dev/null
curl -fsS https://YOUR_DOMAIN/regions/kanto -o /dev/null
curl -fsS https://YOUR_DOMAIN/sitemap.xml -o /dev/null
docker compose exec backend python manage.py check --deploy
docker compose exec backend python manage.py showmigrations --plan
```

Also verify admin login, registration/login/refresh/logout, a direct React-route refresh, filters, review permissions, an existing image, a new cover/gallery upload, generated thumbnails, and persistence after `docker compose restart`. Do not use `docker compose down -v` during verification.

## SwiftUI client guidance

SwiftUI can use the same `/api/v1/` resources without React:

- Generate `Codable` models from `/api/schema/` or model the documented JSON directly.
- Use `URLSession` for JSON and multipart requests.
- Store access and refresh tokens in Keychain; refresh once after a 401.
- Use stable numeric place/user IDs for identity and API writes; display names and slugs are presentation data.
- Render the absolute `image_url` values returned by Django.
- Respect pagination (`count`, `page`, `pages`, `next`, `previous`, `results`) and structured field errors.

The mobile client therefore needs no Django rewrite or React-specific response parsing.

## Repository layout

```text
.
├── backend/
│   ├── config/                 # API settings, URLs, ASGI/WSGI
│   ├── requirements/           # base/development/production pins
│   ├── travel/
│   │   ├── api/                # serializers, responsibility-split views, filters, permissions
│   │   ├── migrations/         # preserved migrations
│   │   ├── tests/              # backend API, service, upload, and admin tests
│   │   ├── templates/admin/    # internal admin dashboard only; no public Django UI
│   │   └── services.py         # ratings, badges, and image processing
│   ├── media/                  # preserved uploads
│   ├── db.sqlite3              # preserved local database (Git-ignored)
│   └── Dockerfile
├── frontend/
│   ├── public/                 # logo, favicon, badge assets
│   ├── src/                    # API, components, layouts, pages, routes, styles
│   ├── Dockerfile
│   └── vite.config.js
├── nginx/nginx.conf
├── docker-compose.yml
├── MIGRATION_CHECKLIST.md
├── POSTGRES_MIGRATION.md
└── .env.example
```

## Known limitations

- Image processing currently uses filesystem paths and the production stack intentionally uses a persistent local media volume. Object storage would require a storage-compatible image processing refactor.
- The legal text remains project-provided informational text; obtain professional legal review before a public commercial launch.
- Docker is not installed on the development machine used for this pass, so Compose config, PostgreSQL volume persistence, Nginx proxy behavior, and live HTTPS must be smoke-tested on the VPS using the commands above.
- Buying/configuring a domain, recording a demo video, taking final deployment screenshots, publishing to a GitHub portfolio, and editing a CV require the owner's accounts and final deployed URL; the repository cannot perform those external actions safely.
