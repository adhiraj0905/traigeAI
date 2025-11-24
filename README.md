# TriageAI: Automated Support Orchestrator

**Track:** Enterprise Agents
**Model:** Gemini 1.5 Flash
**Status:** Prototype

## 📖 Overview
TriageAI is a multi-agent system designed to reduce customer support response times by 40%. It autonomously categorizes incoming emails, executes database lookups for order status, and drafts policy-compliant responses for human review.

## ⚙️ Architecture
The system utilizes a **Sequential Multi-Agent Architecture**:
1.  **Manager Agent:** Analyzes sentiment and intent; extracts entities (Order IDs).
2.  **Tooling Layer:** A deterministic Python function that acts as a mock API gateway to retrieve real-time order data.
3.  **Writer Agent:** Synthesizes the initial context + tool data + company policy to generate the final response.

## 🚀 Key Features (Course Concepts)
* **Multi-Agent Orchestration:** Chained workflow where Agent 1's output feeds Agent 2's context.
* **Tool Use:** Custom function calling to simulate retrieving external structured data.
* **Context Engineering:** System instructions inject "TechGadget" company policy to ensure consistent tone and compliance.

## 🛠️ Setup & Usage
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install google-generativeai
    ```
3.  Add your Gemini API Key in `main.py`.
4.  Run the agent:
    ```bash
    python main.py
    ```

## 📄 License
MIT License