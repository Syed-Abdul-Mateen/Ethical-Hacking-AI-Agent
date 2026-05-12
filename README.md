# Ethical Hacking AI Agent: Autonomous Security Operations Framework

![Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-2.0.0-blue)
![Architecture](https://img.shields.io/badge/Architecture-Distributed-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## Abstract

The Ethical Hacking AI Agent is an advanced, autonomous Security Operation Center (SOC) and Dynamic Application Security Testing (DAST) framework. Engineered to orchestrate complex vulnerability assessments, the platform automates the entire threat lifecycle, from reconnaissance and payload injection to AI-driven vulnerability analysis and remediation generation. 

Designed for seamless integration into modern DevSecOps pipelines, the system leverages an asynchronous execution engine and real-time telemetry streaming to deliver high-fidelity security intelligence with minimal latency.

## System Architecture

The platform operates on a distributed, microservices-inspired architecture to ensure non-blocking execution during intensive penetration testing workloads.

| Component | Description | Technologies Utilized |
| :--- | :--- | :--- |
| **Control Plane (Backend)** | Asynchronous API layer responsible for scan orchestration, payload dispatching, and state management. | FastAPI, Python 3.10+, Uvicorn |
| **Telemetry Engine** | High-throughput WebSocket bridge for real-time streaming of scan diagnostics and threat intelligence. | Socket.IO, ASGI |
| **Data Persistence** | Asynchronous relational database mapped to an Object-Relational Model (ORM) for audit logging. | SQLAlchemy (Async), SQLite |
| **Mission Control (Frontend)** | High-performance, reactive user interface for live monitoring and executive dashboarding. | Next.js 16, React, Tailwind CSS |
| **Intelligence Node** | Analytical engine that correlates findings and generates actionable remediation code using AI heuristic models. | Python, Custom Logic Modules |

## Core Capabilities

- **Concurrent Threat Orchestration:** Implements an asynchronous worker queue to execute reconnaissance, analysis, and active exploitation phases concurrently, preventing main-thread starvation.
- **Live Telemetry & Diagnostics:** Establishes a persistent WebSocket connection to broadcast operational logs, phase transitions, and vulnerability discoveries in real-time.
- **Contextual AI Remediation:** Parses raw vulnerability data through an intelligence module to generate specific, code-level remediation strategies and business impact assessments.
- **Enterprise Reporting & Compliance:** Automatically compiles execution data into executive-ready PDF audits and standard SARIF (Static Analysis Results Interchange Format) logs for immediate CI/CD ingestion.

## Deployment Topologies

The framework supports multiple deployment strategies to accommodate varying infrastructural requirements.

### Primary Deployment: Docker Orchestration (Enterprise)

The entire platform (Next.js Frontend, FastAPI Backend, and PostgreSQL Database) has been fully containerized. This is the recommended approach for production deployments on AWS, DigitalOcean, or Azure.

**1. Configure the Environment**
Create a `.env` file in the root directory:
```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/ai_hacker_db

# Security & AI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
SECRET_KEY=super_secret_enterprise_key_change_in_prod
```

**2. Deploy the Platform**
Run the following command to build and launch all microservices securely:
```bash
docker-compose up --build -d
```

**3. Authenticate**
Access Mission Control via `http://localhost:3000`. The platform is secured by JWT Authentication. Use the default operator credentials:
* **Operator ID:** `admin`
* **Passcode:** `admin123`

### Secondary Deployment: Local Distributed Architecture

If you prefer to run the applications locally without Docker:

**1. Provision the Control Plane (Backend)**
Ensure Python 3.10+ is installed. Ensure your local `.env` points to a local PostgreSQL instance.
```bash
pip install -r requirements.txt
python -m uvicorn backend.main:socket_app --reload --port 8000
```

**2. Provision Mission Control (Frontend)**
Ensure Node.js 18.0+ is installed.
```bash
cd frontend
npm install
npm run dev
```

### Fallback Deployment: Standalone Architecture

For constrained environments lacking Node.js runtimes, the platform maintains a monolithic Flask application. This topology utilizes standard HTTP polling rather than a persistent WebSocket connection.

**1. Initialize the Standalone Server**
```bash
pip install -r requirements.txt
python run_web.py
```

**2. System Verification**
Access the standalone interface via `http://127.0.0.1:5000`.

## Continuous Integration (CI/CD) Output

Upon successful completion of an audit, the framework automatically generates compliance artifacts in the `data/scans/<operation-id>/` directory:
- **Executive Audit (`report.pdf`):** A comprehensive summary of threat profiles, attack vectors, and remediation steps.
- **Pipeline Data (`report.sarif.json`):** A machine-readable format designed for native ingestion into platforms such as GitHub Advanced Security, GitLab CI, and SonarQube.

## Legal Authorization & Compliance Disclaimer

This framework constitutes a rigorous security testing tool. It is strictly authorized for internal infrastructure auditing, authorized penetration testing engagements, and academic research. Operators bear sole responsibility for obtaining explicit, documented authorization prior to directing the agent against any target network, domain, or application. The authors and maintainers disclaim all liability for unauthorized deployment, service disruption, or data compromise resulting from the misuse of this software.
