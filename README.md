# AI Receptionist — Conversational AI Workflow for Dental Clinics

AI Receptionist is a stateful conversational AI system built to automate dental clinic front-desk operations through WhatsApp.

The system handles:

* appointment scheduling
* FAQ retrieval
* emergency escalation
* multi-turn conversations
* real-time slot booking

using LangGraph orchestration, RAG pipelines, Cal.com APIs, and Twilio messaging.

---

# Problem

Most clinic front desks still rely on:

* manual appointment handling
* repetitive FAQ answering
* fragmented communication workflows
* delayed patient responses
* overloaded reception staff

Traditional chatbots fail because they:

* lose conversational context
* hallucinate structured data
* cannot handle multi-step workflows
* break during real scheduling operations

---

# Solution

AI Receptionist combines deterministic backend workflows with LLM-driven conversational orchestration.

The system can:

✅ Answer clinic-specific questions using RAG

✅ Maintain conversational memory across multiple messages

✅ Check real-time appointment availability

✅ Schedule appointments through Cal.com APIs

✅ Escalate urgent dental cases automatically

✅ Operate directly through WhatsApp

---

# Core Architecture

```text
WhatsApp User
      ↓
Twilio Webhook
      ↓
Django Ninja API
      ↓
LangGraph Workflow
      ↓
Intent Router
 ┌───────────────┬───────────────┬───────────────┐
 ↓               ↓               ↓
FAQ Node     Booking Node   Emergency Node
 ↓               ↓               ↓
RAG Search    Cal.com API    Resend API
      ↓
Final Response Generator
      ↓
WhatsApp Response
```

---

# Technical Stack

## Backend

* Django
* Django Ninja Extra
* LangGraph
* LangChain

## AI Stack

* Llama 3.1 8B via Cerebras
* Gemini Embeddings
* Voyage AI Reranker
* Structured LLM Outputs

## Database & Retrieval

* PostgreSQL
* pgvector
* Hybrid Search
* SearchVector

## Infrastructure

* Celery
* Redis
* Docker

## APIs

* Cal.com
* Twilio WhatsApp
* Resend Email API

---

# Key Engineering Concepts

* Stateful conversational systems
* Retrieval-Augmented Generation (RAG)
* Hybrid vector + keyword search
* Multi-turn workflow orchestration
* Conversational memory persistence
* Structured extraction pipelines
* Deterministic validation around LLMs
* Real-world API integrations
* WhatsApp webhook handling
* Timezone normalization

---

# Current MVP Capabilities

* Conversational dental appointment booking
* WhatsApp-based AI receptionist
* Real-time slot checking
* Persistent conversation memory
* FAQ retrieval from clinic documents
* Emergency escalation workflows
* Multi-turn scheduling flows

---

# Future Improvements

* Dynamic nearest-slot recommendations
* Voice-call integrations
* Multi-language support
* Admin dashboard
* Better scheduling recovery flows
* Multi-clinic support
* Production-grade deployment

---

# Author

Built by Aman.

Focused on building practical AI systems involving:

* conversational workflows
* backend orchestration
* workflow automation
* LLM-powered applications

GitHub:
[https://github.com/batman00723](https://github.com/batman00723)
