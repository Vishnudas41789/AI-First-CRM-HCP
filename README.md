# AI-First CRM HCP Module

## Overview

AI-First CRM HCP Module is a healthcare interaction management system that enables pharmaceutical field representatives to log Healthcare Professional (HCP) interactions using natural language through an AI assistant.

The application uses **LangGraph** and **Groq LLM** to understand user requests, execute AI tools, automatically populate the interaction form, edit existing interactions, and generate intelligent follow-up suggestions.

---

## Tech Stack

### Frontend
- React
- Redux Toolkit
- Vite
- Axios

### Backend
- FastAPI
- Python
- SQLAlchemy

### AI
- LangGraph
- LangChain
- Groq LLM (Llama 3.3 70B Versatile)

### Database
- PostgreSQL

---

## Features

- AI-powered interaction logging
- Automatic form filling from chat
- Edit interaction using natural language
- Summarize interaction
- Suggest follow-up actions
- Recommend next best action
- PostgreSQL database integration
- FastAPI REST API
- LangGraph workflow

---

## LangGraph Tools

### 1. Log Interaction
Creates a new HCP interaction from natural language.

Example:
> Today I met Dr. Smith. Discussed Product X. Positive sentiment. Shared brochure.

---

### 2. Edit Interaction
Updates previously logged interaction fields.

Example:
> Change the sentiment to negative.

---

### 3. Summarize Interaction
Generates a concise summary of the discussion.

---

### 4. Suggest Follow-up
Suggests appropriate follow-up activities for the HCP.

---

### 5. Next Best Action
Recommends the next sales action based on previous interaction details.

---

## Project Structure

```
AI-First-CRM-HCP
│
├── frontend
├── backend
├── README.md
└── requirements.txt
```

---

## Running the Project

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## AI Workflow

User Chat

↓

LangGraph Agent

↓

Groq LLM

↓

Tool Selection

↓

Tool Execution

↓

PostgreSQL

↓

Response to React UI

---

## Author

**Vishnu Das DS**

B.Tech Computer Science & Engineering (AI)

2026 Graduate