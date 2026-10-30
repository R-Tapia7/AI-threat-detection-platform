# Security Log Analyzer & AI Threat Detection

A hybrid microservices architecture for automated cybersecurity threat detection, combining real-time log generation, intelligent rule-based analysis, and AI-powered incident reporting.

**Author:** Rodrigo Tapia  
**GitHub:** [R-Tapia7](https://github.com/R-Tapia7)  
**LinkedIn:** [rodrigo-tapia-a058a138a](https://www.linkedin.com/in/rodrigo-tapia-a058a138a/)

---

## Overview

This platform simulates a corporate Security Operations Center (SOC) by generating realistic audit logs, detecting suspicious patterns, and producing natural-language threat reports using a local LLM — all in real time.

```
[ Java / Spring Boot ] ──→ [ Python / FastAPI ] ──→ [ PostgreSQL ]
  Generates audit logs       Pandas rule engine         Persistent storage
  Simulates attacks          Responds immediately             ▲
                                      │                       │ attaches AI report
                                      ▼                       │
                              [ In-memory queue ] ──→ [ AI worker thread ] ──→ [ Llama 3.2 / Ollama ]

[ React Dashboard ] ←── polls /analyze/results every 3 s
```

Detection and AI reporting are **decoupled**: the rule engine never waits for the LLM, so a slow or unavailable model cannot delay or lose threat detection.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Log Generator | Java 21, Spring Boot 3, Maven |
| Analyzer API | Python 3.12, FastAPI, Pandas, SQLAlchemy |
| AI Engine | Llama 3.2 via Ollama (local, free) |
| Database | PostgreSQL 16 |
| Dashboard | React 18, Vite, Axios |
| DevOps | Docker, Docker Compose, Alembic |

---

## Features

- **Real-time log generation** — Spring Boot scheduler generates audit events every 5 seconds: login attempts, file downloads, admin access, config changes, and more
- **Rule-based threat detection** — Pandas pipeline evaluates 5 detection rules across rolling time windows:
  - Brute force: >10 failed logins from the same IP in 5 minutes
  - Sensitive resource access: successful access to `/admin/panel` or `/config/secrets`
  - Mass download: >5 file downloads by the same user in 5 minutes
  - Off-hours access: activity outside working hours (before 7am or after 10pm)
  - High error rate: >50% failure ratio system-wide in 5 minutes
- **Asynchronous AI threat analysis** — suspicious events are placed in a queue and processed by a background worker that calls Llama 3.2 locally via Ollama, generating structured incident reports (risk level, MITRE ATT&CK technique, mitigation steps). Reports are attached to the stored event when ready. If Ollama is slow or down, detection keeps working and the event is marked as `AI report unavailable`
- **Persistent storage** — all analyzed events stored in PostgreSQL with both event timestamp and processing timestamp, enabling latency analysis
- **Live dashboard** — React frontend polls the API every 3 seconds showing metrics and a color-coded log table. Selecting an event shows its AI report, or a "Generating AI report..." state until the worker finishes
- **Attack simulation** — dedicated endpoint to trigger brute force scenarios for testing detection rules

---

## Project Structure

```
/
├── log-generator/              # Java Spring Boot microservice
│   ├── src/main/java/com/security/log_generator/
│   │   ├── config/             # RestClient bean with timeout config
│   │   ├── controller/         # REST endpoints including attack simulation
│   │   ├── model/              # SecurityLog data model
│   │   ├── scheduler/          # Scheduled log generation and forwarding
│   │   └── service/            # Log generation logic
│   └── Dockerfile
│
├── security-analyzer/          # Python FastAPI microservice
│   ├── app/
│   │   ├── db/                 # SQLAlchemy models and database connection
│   │   ├── models/             # Pydantic schemas
│   │   ├── routers/            # API endpoints
│   │   ├── services/           # Analyzer, threat rules, AI reporter, background AI worker
│   │   └── store.py            # In-memory cache and AI job queue
│   ├── alembic/                # Database migrations
│   └── Dockerfile
│
├── security-dashboard/         # React frontend
│   ├── src/
│   │   ├── api/                # Axios API client
│   │   └── components/         # MetricsBar, LogsTable, ThreatReport
│   └── Dockerfile
│
└── docker-compose.yml
```

---

## Getting Started

### Prerequisites

- Java 21
- Maven 3.9+
- Python 3.12+
- Node.js 20+
- PostgreSQL 16
- [Ollama](https://ollama.com) with Llama 3.2

### 1. Pull the AI model

```bash
ollama pull llama3.2
```

### 2. Set up the Python environment

```bash
cd security-analyzer
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

Create `security-analyzer/.env`:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/security_platform
```

Create the database in PostgreSQL:

```sql
CREATE DATABASE security_platform;
```

Run migrations:

```bash
alembic upgrade head
```

### 4. Start all services

Open three terminals:

```bash
# Terminal 1 — Java log generator
cd log-generator
mvn spring-boot:run (PowerShell: .\mvnw spring-boot:run)

# Terminal 2 — Python analyzer
cd security-analyzer
uvicorn app.main:app --reload --port 8001

# Terminal 3 — React dashboard
cd security-dashboard
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) to see the dashboard.

---

## Docker (Alternative)

Requires Docker Desktop running.

Create a `.env` file in the project root:

```
DB_PASSWORD=your_postgres_password
```

Then:

```bash
docker compose up --build
```

Open [http://localhost:3000](http://localhost:3000) for the dashboard.

To stop:

```bash
docker compose down
```

### Database Access in Docker
To prevent port conflicts with any local PostgreSQL installations, the Dockerized database is exposed on port **5433** instead of the default 5432. 

To inspect the logs using pgAdmin or DBeaver while Docker is running, use these connection details:
- **Host:** `localhost`
- **Port:** `5433`
- **Database:** `security_platform`
- **Username:** `postgres`
- **Password:** (The password you set in your `.env` file)

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/logs` | Get a batch of generated logs |
| `GET` | `/api/logs/single` | Get a single log |
| `POST` | `/api/logs/attack/brute-force` | Simulate a brute force attack |
| `POST` | `/analyze/` | Analyze a batch of logs |
| `GET` | `/analyze/results` | Get the last 200 analyzed results |
| `GET` | `/analyze/health` | Health check |

Interactive API docs available at [http://localhost:8001/docs](http://localhost:8001/docs).

---

## Detection Rules

| Rule | Trigger | Threat Level |
|---|---|---|
| Brute Force | >10 failed logins from same IP in 5 min | CRITICAL |
| Sensitive Resource (admin action) | `ADMIN_ACCESS` or `CONFIG_ACCESS` on critical resource | CRITICAL |
| Sensitive Resource (other action) | Any other action on critical resource | SUSPICIOUS |
| Mass Download | >5 downloads by same user in 5 min | SUSPICIOUS |
| Off Hours | Access before 7am or after 10pm | SUSPICIOUS |
| High Error Rate | >50% failure ratio system-wide in 5 min | SUSPICIOUS |

---

## Simulating an Attack
To trigger a brute force detection and see the AI in action, we use the built-in Swagger UI (this avoids terminal JSON formatting issues across different operating systems):

1. Open your browser and navigate to [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)
2. Expand the `POST /api/logs/attack/brute-force` endpoint and click **"Try it out"**.
3. In the Request body, change the default `"string"` to a realistic IP address (e.g., `"45.33.32.156"`).
4. Click **"Execute"**.

This immediately generates a burst of failed login attempts from the target IP. Within seconds, the React dashboard will light up with CRITICAL alerts. The AI incident reports follow shortly after, as the background worker generates them with the local Ollama instance and attaches them to each event.

---

## Architecture Decisions

**Why Java for log generation?** Spring Boot's `@Scheduled` makes periodic tasks trivial, and the strong typing of Java models ensures consistent log structure when serialized to JSON.

**Why Python for analysis?** Pandas is the industry standard for tabular data processing. The rolling time-window aggregations that power the brute force and mass download rules are a single line of Pandas code.
In addition, Pandas rolling windows use the same logic as statistical processing and algorithmic trading, which are widely used in many fields, including finance and data science.

**Why a local LLM instead of a cloud API?** Ollama with Llama 3.2 runs entirely on your machine — no API costs, no data leaving your network, no rate limits. This mirrors the privacy requirements of a real corporate SOC where security logs cannot be sent to third-party services.

**Why is the AI decoupled from detection?** LLM inference on CPU takes tens of seconds and competes for resources with the rest of the system. If detection waited for it, a saturated or crashed model would block the Java generator, delay the dashboard and lose events. Instead, the rule engine stores every event immediately and enqueues suspicious ones. A single background worker consumes the queue, calls the model and updates each stored event with its report. Alerts are therefore near-instant, while reports are enrichment that arrives later, which is how real SOC pipelines treat detection versus enrichment. Events are enqueued only after they have been saved, so the worker can always find the record it needs to update.

**Why polling instead of WebSockets?** For a dashboard that updates every 3 seconds, polling is simpler, more reliable, and sufficient. WebSockets would add complexity without a meaningful user experience improvement at this update frequency.

---

## Known Limitations & Future Work

- **Single AI worker:** reports are generated one at a time. This is deliberate, since parallel LLM calls on CPU only worsen saturation, but under heavy suspicious traffic the report queue grows and reports are delayed. The queue is bounded (100 items); beyond that, reports are skipped while detection continues.
- **In-memory queue:** pending reports are lost if the analyzer restarts (the events themselves are already persisted). A production deployment would use a broker such as Redis, RabbitMQ or Kafka.
- **In-memory history window:** rolling detection rules use the last 500 events held in memory. A larger deployment would query a time-series store instead.
- **Application-layer telemetry only:** rules cover audit logs, not network traffic (ports, destinations, protocols). Network-level detection would require additional data sources and fields.

---

## License

MIT