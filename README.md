# Project Genesis: Universal AI Core

*Read this in other languages: [English](README.md),[Русский](README_RU.md).*

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-State-blue.svg)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-blue.svg)
![Status](https://img.shields.io/badge/Status-Prototyping-orange.svg)

> ⚠️ **PROJECT STATUS: PROTOTYPING & ARCHITECTURE DESIGN**
> *Currently, all files in this repository are structural stubs (placeholders). The project is in the active phase of architectural alignment and foundational setup according to the 10-week roadmap.*

## 🧠 About The Project
**Project Genesis** is a production-ready, domain-agnostic AI Core Infrastructure. It is designed not as a toy script, but as a scalable MLOps asset. 

The system implements a **deterministic multi-agent orchestration pattern** ("controlled emergence"). 
* **The Intelligence** is distributed across stateless, specialized LLM agents.
* **The Power** (execution flow, limits, memory, and retries) is strictly controlled by a deterministic routing layer written in Python.

This is an engineering approach to AI: no "AutoGPT-style" hallucinations, no infinite loops. Just predictable, monitorable, and robust AI pipelines.

---

## 🏗 The 7 Architectural Layers

The core is strictly divided into 7 abstract layers. Tools may change, but the abstractions remain.

1. **Execution / Runtime Layer**
   * *Where the system lives.* Ensures isolation, reproducibility, and portability.
   * *Implementation:* Docker, Docker Compose.
2. **Data & State Layer**
   * *The memory of the system.* Divided into Persistent Facts (PostgreSQL), Semantic Memory (Qdrant Vector DB), and Operational Context (JSON/Redis).
3. **Ingestion & Transformation Layer**
   * *How the outside world gets in.* ETL pipelines, data cleaning, chunking, and embedding generation. 80% of the system's quality is built here.
4. **Intelligence Units (Agents)**
   * *Who thinks.* Independent, specialized executors (Analyst, Critic, Researcher). They are stateless and have no global context.
5. **Orchestration & Control Layer**
   * *Who manages.* The deterministic brain of the system (Not ML). Handles task routing, agent invocation order, and limits.
6. **Feedback & Evaluation Layer**
   * *The immune system.* Evaluates agent outputs. Includes the Critic agent, reject/retry logic, and sanity checks to prevent hallucinations from reaching the user.
7. **Interface & Integration Layer**
   * *Contact with the outside world.* API (FastAPI), CLI, or Telegram Bots. The interface contains zero business logic.

---

## 🚧 Core Boundaries (What is OUT of scope)

To keep the core universal and maintainable, the following are strictly excluded from the base architecture:
* ❌ **Specific Business Logic:** The core doesn't know what a "VR Club" or "E-commerce" is. Business rules are applied via YAML configuration skins.
* ❌ **UI / UX:** The core is a backend engine. Interfaces are just adapters.
* ❌ **AGI / Full Autonomy:** Agents cannot set their own ultimate goals. Everything is bounded by the Orchestrator.
* ❌ **Training LLMs from scratch:** We orchestrate intelligence (Inference/API), we do not train foundational models.

---

## 🗺 10-Week Roadmap

We are currently executing the following build plan:

* **Week 1:** Execution Foundation (Docker, DBs, Repo setup)
* **Week 2:** Data & State (Schemas, Agent state tracking)
* **Week 3:** Ingestion Pipeline (Parsing, Chunking, Embedding)
* **Week 4:** Single Agent Unit (Base classes, strict I/O contracts)
* **Week 5:** Multi-Agent Interaction (Analyst -> Critic flow)
* **Week 6:** Orchestration Core (FSM, Router, Limits)
* **Week 7:** Feedback & Evaluation (Immune system, retry logic)
* **Week 8:** Interface Layer (FastAPI / Bot adapters)
* **Week 9:** Scenario Packaging (Applying the first business "Skin")
* **Week 10:** Stabilization & Documentation (MVP Release)

---

## 📂 Repository Structure

```text
project_genesis/
├── docker-compose.yml          # Layer 1: Services orchestration
├── Dockerfile                  # Layer 1: App container build
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── README.md                   # English documentation
├── README_RU.md                # Russian documentation
├── configs/                    # Configuration Layer (Domain-agnostic & Skins)
│   ├── core_config.yaml        # Base system limits, model parameters
│   ├── agents_config.yaml      # Agent roles, prompts, and contracts
│   └── scenarios/              
│       └── vr_club_skin.yaml   # Demo Skin: Business rules for VR Club
├── src/                        # Source Code
│   ├── main.py                 # Application entry point
│   ├── interface/              # Layer 7: Interface & Integration
│   ├── orchestration/          # Layer 5: Orchestration & Control
│   ├── agents/                 # Layer 4: Intelligence Units
│   ├── evaluation/             # Layer 6: Feedback & Evaluation
│   ├── ingestion/              # Layer 3: Ingestion & Transformation
│   ├── memory/                 # Layer 2: Data & State (Semantic)
│   └── storage/                # Layer 2: Data & State (Persistent)
└── tests/                      # Test Suite
```

## 🚀 Getting Started (For Developers)
1. Copy `.env.example` to `.env` and fill in your API keys.
2. Run `docker-compose up --build -d`.
3. Access the API documentation at `http://localhost:8000/docs`.