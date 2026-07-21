# Polyglot Vulnerable Web Lab

> **Intentionally insecure training repository. Run locally only. Do not deploy to the internet or a shared environment.**

This monorepo is a working website designed for authorized DevSecOps scanner evaluation. It contains intentionally vulnerable code in **Java, JavaScript/TypeScript, COBOL, Python, SQL, C#, and PHP**, plus deliberately misconfigured **Terraform, Bicep, and Kubernetes** files.

## What is included

| Area | Implementation |
|---|---|
| Web UI / gateway | TypeScript + browser JavaScript (`gateway/`) |
| SQL injection + constrained command-injection sink | Python + SQLite (`python-service/`) |
| Broken access control / IDOR | Java (`java-service/`) and C# (`csharp-service/`) |
| Path traversal | PHP (`php-service/`) |
| Legacy report service | COBOL called by a small Python HTTP wrapper (`cobol-service/`) |
| Database schema and intentionally weak data handling | SQL (`sql/`) |
| IaC misconfigurations | Terraform, Bicep, Kubernetes (`iac/`) |
| Dependency / container findings | Old dependency versions and old base images in service manifests and Dockerfiles |
| Fake scanner-detectable secrets | `lab-secrets/` and selected source files |

## Safety design

- Every published port is bound to `127.0.0.1` in `docker-compose.yml`.
- All credentials and tokens are **fake test values**.
- The command-injection demonstration defaults to **simulation mode** (`LAB_UNSAFE_MODE=false`). Static analyzers can still see the unsafe data flow, but arbitrary commands are not executed by default.
- Containers drop Linux capabilities and use `no-new-privileges` where practical.
- IaC is scanner input only. **Do not apply it.**

## Run

Requirements: Docker Desktop or Docker Engine with Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

Open: `http://127.0.0.1:3000`

Run the smoke test after the containers are healthy:

```bash
bash scripts/smoke-test.sh
```

Stop and remove the lab:

```bash
docker compose down -v
```

## Scanner-friendly entry points

- SAST: source files under each service
- SCA: `package.json`, `requirements.txt`, `pom.xml`, `.csproj`, and `composer.json`
- Secrets: `lab-secrets/`, `.env.example`, and hardcoded demo values
- IaC: `iac/terraform`, `iac/bicep`, and `iac/k8s`
- Containers: every `Dockerfile` and `docker-compose.yml`

See [`docs/VULNERABILITY_MAP.md`](docs/VULNERABILITY_MAP.md) for the exact finding locations and safe local test cases.

## Known intentionally old dependencies

The versions are pinned so SCA tools have findings to report. They are not required to be directly exploitable by the UI.

- `org.apache.logging.log4j:log4j-core:2.14.1` — affected by CVE-2021-44228.
- `lodash:4.17.20` — affected by vulnerabilities fixed in later releases.
- `urllib3:1.25.7` — affected by CVE-2020-7212.
- `Newtonsoft.Json:12.0.1` — affected by CVE-2024-21907.
- `guzzlehttp/guzzle:6.5.2` — intentionally old Composer dependency for SCA testing.

## Repository intent

Use this repository only in systems you own or are authorized to test. The project is meant for scanner comparison, pipeline gating, alert review, and remediation exercises—not as an application template.
"# polyglot-vuln-lab" 
