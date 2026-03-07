# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
**Project:** Universal AI Core with deterministic multi-agent orchestration (Project Genesis)  
**Role:** AI Infrastructure Engineer / MLOps Engineer  
**Document Status:** Approved (Baseline 10-week plan)  

---

## 1. General System Information
### 1.1. System Purpose
Development of a production-ready infrastructure AI Core (AI Pipeline + Agent Swarm) designed for business process automation, data analytics, and decision-making. The system is built on the principle of "controlled emergence": intellectual work is performed by isolated LLM agents, while the execution flow (routing) is strictly managed by deterministic code.

### 1.2. Business Context & Scalability
The core is **domain-agnostic**. 
For the MVP (Proof-of-Value), the "VR Club / Arena Management" vertical will be implemented (workload analysis, anomaly detection in admin behavior, churn prediction). Business logic is implemented exclusively at the configuration file level (skins) and is never hardcoded into the core.

---

## 2. Architectural Pattern & Tech Stack
The system implements a hybrid pattern: **Workflow-Oriented Core + Agent-Oriented Processing**.

**Abstraction to Implementation Mapping (MVP Stack):**
*   **Compute (Execution Environment):** Python 3.10+ (async).
*   **Execution / Runtime (Isolation):** Docker, Docker Compose.
*   **State Storage (Operational state & facts):** PostgreSQL (via psycopg3).
*   **Semantic Memory (Long-term memory):** Vector DB (Qdrant / FAISS).
*   **Orchestration (Flow control):** Custom Python router (FSM - Finite State Machine).
*   **Boundaries (Interfaces):** REST API (FastAPI), Telegram Bot API.

---

## 3. Logical Core Architecture (7 Layers)

### Layer 1: Execution / Runtime Layer
*   **Function:** Ensures system reproducibility, isolation, and portability.
*   **Requirement:** The architecture must not change when switching the execution environment (local -> server -> cloud).

### Layer 2: Data & State Layer
*   **Function:** Context storage. Divided into 3 circuits:
    1.  *Persistent State:* Facts and event logs (PostgreSQL).
    2.  *Semantic Memory:* Vector knowledge base (RAG pattern).
    3.  *Operational State:* Short-term context of the current task (JSON/Redis).

### Layer 3: Ingestion & Transformation Layer
*   **Function:** Ingesting data from the outside world (files, APIs), cleaning, normalization, chunking, and vectorization (embedding).

### Layer 4: Intelligence Units (Agent Layer)
*   **Function:** Execution of highly specialized tasks.
*   **Requirement:** Agents (Analyst, Critic, Researcher, Executor) have no global context. Each agent is an isolated function (stateless) that takes an input and returns an output based on a prompt. There is no single "Self" in the system.

### Layer 5: Orchestration & Control Layer
*   **Function:** Deterministic task routing.
*   **Requirement:** Hardcoded logic (Not ML). Defines the order of agent invocation, limits, loops, and stop criteria. Intelligence resides in the agents; power resides in the orchestrator.

### Layer 6: Feedback & Evaluation Layer (Immune System)
*   **Function:** Quality assessment of outputs (Self-reflection / Self-improvement).
*   **Requirement:** Presence of a Critic Agent and validation rules. The system must be able to reject hallucinations and initiate retries until the result meets quality thresholds.

### Layer 7: Interface & Integration Layer
*   **Function:** Entry/Exit points.
*   **Requirement:** Interfaces (UI/Bot/API) must contain zero business logic.

---

## 4. Functional Requirements (FR)
1.  **FR-1 (Ingestion):** The system must ingest raw data (Excel, PDF, text), clean it, and store it in the Vector DB.
2.  **FR-2 (Orchestration):** The system must route tasks between agents based on a configuration file (YAML/JSON).
3.  **FR-3 (Evaluation):** The system must automatically verify the executor agent's output and, if it fails quality metrics, send the task back for revision.
4.  **FR-4 (Memory):** The system must retrieve relevant context from long-term memory (Vector DB) before passing a task to an agent.
5.  **FR-5 (Configuration):** Changing agent roles, prompts, and behavioral scenarios must be done via config files without recompiling or rewriting the core code.

---

## 5. Non-Functional Requirements (NFR)
1.  **NFR-1 (Determinism):** Infinite loops are strictly prohibited. The orchestrator must have hard limits on iterations (`max_retries`).
2.  **NFR-2 (Observability):** All state transitions and agent decisions must be logged to ensure debuggability.
3.  **NFR-3 (Security):** Agents have no direct, unreviewed access to external resources (code execution, deployment) without passing the Evaluation layer.

---

## 6. System Boundaries (Out of Scope)
The following elements are **excluded** from the current core development scope:
1.  **Hardcoded Business Logic:** The core does not know about "clubs" or "VR arenas". This is applied via configs (skins).
2.  **UI / UX:** Frontend, dashboards, and complex designs are not developed. Interfaces are utilitarian (API / CLI / Telegram).
3.  **Highload / Kubernetes:** Auto-scaling and SRE practices are not implemented at the MVP stage.
4.  **AGI / Full Autonomy:** Free goal-setting by agents (AutoGPT style) is prohibited.
5.  **Model Training (Pretraining):** The system uses pre-trained LLMs (via API or local inference). Training foundational models from scratch is out of scope.

---

## 7. Implementation Roadmap (10 Weeks)

| Phase | Timeline | Deliverables | Architectural Layer |
| :--- | :--- | :--- | :--- |
| **Milestone 1** | Week 1 | Environment setup: Docker, docker-compose, PostgreSQL, Qdrant. Basic read/write script. | Execution Layer |
| **Milestone 2** | Week 2 | DB schema design (facts, events). Agent state tracking implementation (`agent_state.json`). | Data & State Layer |
| **Milestone 3** | Week 3 | ETL pipeline development: file parsing, cleaning, chunking, embedding generation. | Ingestion Layer |
| **Milestone 4** | Week 4 | Base Agent class creation. LLM integration, strict I/O contracts setup. | Intelligence Units |
| **Milestone 5** | Week 5 | Multi-agent interaction (Analyst -> Critic). Context passing. | Intelligence Units |
| **Milestone 6** | Week 6 | Orchestrator (Router) development. FSM implementation for flow control. | Orchestration Layer |
| **Milestone 7** | Week 7 | Immune system setup: confidence metrics, reject/retry logic. | Evaluation Layer |
| **Milestone 8** | Week 8 | Adapter development: Telegram Bot / FastAPI endpoints integration. | Interface Layer |
| **Milestone 9** | Week 9 | Scenario packaging (Config-driven). Applying the "Club Analytics" business skin. E2E testing. | Configuration Layer |
| **Milestone 10**| Week 10| Stabilization. Refactoring. Technical documentation (README, architecture diagrams). | Release MVP |

---

## 8. Post-MVP Scaling Vector
After locking the core (Week 10), scaling is done exclusively via **extensions** that do not break the core's integrity:
*   *Inference Extensions:* Connecting local ML models.
*   *Action Agents:* Adding tool-using agents under strict supervisor control.
*   *External Integrations:* Connecting payment gateways, CRMs.
*   *DevOps:* Migration to Kubernetes, CI/CD pipeline setup.