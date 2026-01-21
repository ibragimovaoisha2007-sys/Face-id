# Hikvision Face Terminal Attendance (Maktab Davomat)

Ushbu loyiha Hikvision Face Terminal qurilmalaridan event/loglarni qabul qilish, DBga yozish, Telegram bot orqali xabar berish va admin panelda ko‘rsatish uchun minimal, productionga yaqin skeleton hisoblanadi.

## 1) ARXITEKTURA

### 1.1 Integratsiya variantlari (push/pull)
- **Push (Webhook):** qurilma eventni serverga HTTP POST qilib yuboradi. `POST /hikvision/event-receiver` endpoint. Ishonchli, real-time.
- **Pull (Periodic Sync):** server qurilmadan ISAPI orqali loglarni olib keladi. `POST /sync/pull-logs` endpointni cron bilan chaqirasiz.

### 1.2 ISAPI vs SDK
- **ISAPI (HTTP API):** qurilma tarmoqda ochiq bo‘lsa, event/loglarni olish, user data olish/yangilash mumkin. Webhook yoki polling uchun mos.
- **SDK:** agar qurilmada ISAPI cheklangan bo‘lsa, yoki kompleks event stream kerak bo‘lsa. SDK ko‘pincha Windows servis yoki local agent talab qiladi.

### 1.3 Event qabul qilish dizayni
- **Webhook endpoint:** `POST /hikvision/event-receiver` — eventni adapter layer orqali normalizatsiya qiladi va DBga yozadi.
- **Sync job:** `POST /sync/pull-logs` — ISAPI/SDK orqali loglarni olib kelib DBga yozadi.

### 1.4 Xavfsizlik
- Qurilma bilan **Basic Auth** yoki **Digest Auth** (Hikvision odatda shuni ishlatadi).
- Webhook endpoint uchun **IP whitelisting**, **token header**, **rate limit**.
- Qurilma ID + secret token bilan imzolash (masalan `X-Device-Token`).

### 1.5 24/7 ishlash
- Katta yuklama bo‘lsa **Redis queue** yoki **RabbitMQ** orqali eventlarni navbatga qo‘yish tavsiya qilinadi.
- Minimal holatda sync/insert to‘g‘ridan-to‘g‘ri DBga yoziladi.

## 2) DATABASE MODEL

### Asosiy jadval va ustunlar (PostgreSQL)
- `students`: o‘quvchi profili, `terminal_user_id` **unique**.
- `parents`: ota-ona profili.
- `student_parents`: bog‘lash jadvali (many-to-many).
- `classes`: sinf ma’lumoti.
- `devices`: terminal ma’lumotlari.
- `attendance_logs`: event loglari, `source_event_id` bilan dedup.
- `users`: admin/teacher account.

## 3) BUSINESS LOGIC
- **Keldi/Ketdi:** bir kunda **birinchi IN = keldi**, **oxirgi OUT = ketdi**.
- **Kechikkanlar:** belgilangan vaqt (masalan 08:05)dan keyin kelganlar.
- **Dedup:** `source_event_id` + `device_id` unique. Event takror kelsa qayta yozilmaydi.
- **Offline:** qurilma interneti uzilsa, keyin pull orqali tarixiy loglar olinadi.

## 4) BACKEND IMPLEMENTATION (FastAPI)
- Stack: **FastAPI + PostgreSQL + Redis (ixtiyoriy)**
- Pydantic schema, SQLAlchemy models, Alembic migration skeleton.
- Endpointlar:
  - `POST /devices/register`
  - `POST /hikvision/event-receiver`
  - `POST /sync/pull-logs`
  - `CRUD /students`
  - `GET /attendance/report?date=YYYY-MM-DD`
  - Adapter layer `GenericHikvisionAdapter` turli payloadlarni `terminalUserId/employeeNo` kabi fieldlar bilan moslaydi.
  - Placeholderlar `.env` ichida: `HIKVISION_ISAPI_BASE_URL`, `HIKVISION_DEVICE_USERNAME`, `HIKVISION_DEVICE_PASSWORD`.

## 5) TELEGRAM BOT
- **python-telegram-bot** ishlatiladi.
- `/start` → ota-ona bog‘lash (admin bergan `link_code`).
- Event kelganda xabar: “Farzandingiz [ism] [vaqt] da keldi/ketdi”.
- Teacher view: “Bugun kelmaganlar”, “Kechikkanlar”.

## 6) ADMIN PANEL
- Minimal **FastAPI + Jinja2**.
- Pages: Students, Devices, Attendance, Reports.
- Role-based: admin/teacher.

## 7) DEPLOYMENT
- Docker compose: app + postgres + redis.
- Nginx reverse proxy + HTTPS (Let’s Encrypt).
- Logging: JSON structured logs.

## 7.1 LOYIHA PAPKA STRUKTURASI (minimal)
```
app/
  main.py
  models.py
  routers/
  services/
  templates/
scripts/
  fake_event_generator.py
deploy/
  nginx.conf
```

## 8) ISHGA TUSHIRISH
```bash
cp .env.example .env
# .env ichida DB/Telegram/Hikvision parametrlari kiritiladi

docker compose up --build
```

## 9) TEST
```bash
python scripts/fake_event_generator.py --url http://localhost:8000/hikvision/event-receiver
```

## 10) 1 HAFTALIK PILOT REJA (MVP)
- **1-kun:** Server setup + DB schema + event receiver.
- **2-kun:** Student CRUD + device register.
- **3-kun:** Telegram bot + xabar jo‘natish.
- **4-kun:** Attendance report + dedup/logic.
- **5-kun:** Admin panel (minimal).
- **6-kun:** Device sync (pull).
- **7-kun:** Test + deployment.

Keyingi bosqichlar:
- Face enroll UI.
- Advanced analytics (dashboard, export).
- Multi-school / multi-tenant.
