# Arvya Meeting Analyser

A meeting intelligence system that converts raw meeting recordings into structured investment banking and private equity insights using SST, workflow orchestration, and LLM based information extraction.

The system automates the post-meeting workflow of transcription, analysis, persistence, and report generation and delivery.

---

# Problem

Investment banking and private equity teams spend significant time manually reviewing meeting notes, extracting key decisions, identifying risks, tracking action items, and documenting deal discussions.

This project automates that workflow by transforming unstructured meeting conversations into structured reports.

---

# System Architecture

```text
Meeting Recording
       │
       ▼
 Audio Upload API
       │
       ▼
Temporary Storage
       │
       ▼
 Groq Whisper STT
       │
       ▼
   Transcript
       │
       ▼
LangGraph Workflow
       │
       ▼
┌───────────────────────┐
│ Analyse Meeting Node  │
└───────────────────────┘
            │
            ▼
┌───────────────────────┐
│ Save Report Node      │
└───────────────────────┘
            │
            ▼
┌───────────────────────┐
│ Email Report Node     │
└───────────────────────┘
            │
            ▼
PostgreSQL
```

---

# Core Design Principle

The report generation layer is centralised.

Different ingestion sources can reuse the same processing pipeline.

```text
Audio Upload
       │
       ▼
    file_path
       │
       ▼
process_audio()
       │
       ▼
process_transcript()
```

Future integrations such as:

* Google Drive
* Google Meet
* Zoom Cloud Recordings
* S3 Buckets

can reuse the existing pipeline without modifying the analysis layer.

---

# Processing Pipeline

## Stage 1 — Audio Ingestion

Accepted formats:

* mp3
* wav
* m4a

Files are stored temporarily and removed after processing.

To prevent filename collisions, uploaded files are assigned UUID-based names.

Example:

```text
recordings/
 └── 8c5f2f1d-xxx_meeting.m4a
```

---

## Stage 2 — Speech To Text

Transcription is performed using:

```text
Groq Whisper
```

The transcription layer converts raw audio into plain text.

Output:

```text
Audio
    ↓
Transcript
```

---

## Stage 3 — Workflow Orchestration

The analysis workflow is done using LangGraph.

Current workflow:

```text
Analyse
   ↓
Save
   ↓
Email
```

Although the current workflow could be implemented using sequential function calls, LangGraph was chosen to support future expansion, including:

* Human approval steps
* Compliance review nodes
* CRM integrations
* Branching workflows
* Retry mechanisms
* Multiple domain-specific agents

---

## Stage 4 — Structured Intelligence Extraction

LLM outputs are constrained using structured schemas.

Extracted entities include:

<p align="center">
  <img src="Screenshot 2026-06-06 215846.png" width="600" title="Email test ss">
</p>---

## Stage 5 — Persistence

Reports are stored in PostgreSQL.

---

## Stage 6 — Delivery

After successful persistence, reports are distributed through email.

This guarantees that report generation and persistence occur before external delivery.

---

# Technology Stack

## Backend

* Django
* Django Ninja Extra

## Workflow Engine

* LangGraph

## LLM Layer

* Groq
* Qwen3 32B

## Database

* PostgreSQL
* Supabase

## Email

* Bravo

## Deployment

* Render

---

## File Handling

Uploaded audio files are stored temporarily using UUID-prefixed filenames
to prevent collisions when multiple uploads contain identical names.
Files are automatically removed after processing using a try/finally cleanup pattern.

## Engineering Decisions and Tradeoffs

- UUID-prefixed filenames are used to avoid collisions between uploaded audio files.
- Audio files are deleted after transcription using a try/finally cleanup pattern.
- Both the transcript and the structured report are persisted to allow future reprocessing.
- Recipients are delivered through BCC to preserve subscriber privacy.
- LangGraph is used to model the workflow as composable processing nodes.

# Future Work

* Founder Meeting Intelligence Agent
* CRM Integrations
* Multi-Meeting Analytics
* Google Meet Integration
* Zoom Cloud Recording Integration
* Role Aware Insight Generation
* Human-In-The-Loop Approval Nodes

---

# Deployment

```text
https://arvya-meeting-analyser.onrender.com/api_v1/docs
```


## Test Transcript (for transcription to report api endpoint)
{
  "transcript": "Investment Banking Strategic Advisory Meeting\n\nParticipants:\n\nSarah Chen (SC) – Managing Director, Investment Banking\nMichael Ross (MR) – Vice President, Investment Banking\nDavid Kapoor (DK) – CEO, NovaTech Solutions\nLisa Patel (LP) – CFO, NovaTech Solutions\n\nSC: Thanks everyone for joining. David, Lisa, we're excited to discuss your fundraising and growth plans.\n\nDK: Thanks, Sarah. Our primary objective is expanding into Southeast Asia over the next 18 months. We've seen strong inbound demand and believe the market timing is favorable.\n\nLP: To support that expansion, we're evaluating a growth capital raise and assessing strategic partnership opportunities.\n\nMR: Based on our preliminary review, the business is performing well. Revenue growth and customer retention metrics are attractive from an investor perspective.\n\nDK: What valuation range do you believe the market would support today?\n\nMR: Based on comparable transactions, we estimate a valuation between $180 million and $220 million, assuming current growth rates continue.\n\nLP: That's broadly in line with our expectations.\n\nSC: One concern investors may raise is scalability. They will want confidence that your operational infrastructure can support international growth without compressing margins.\n\nDK: That's fair. We're currently investing in customer success and regional hiring, but there is still uncertainty around regulatory compliance costs.\n\nLP: We are also evaluating how customer acquisition costs may change as we enter new markets.\n\nMR: Those are exactly the questions investors will focus on during diligence.\n\nDK: If we moved forward with a fundraising process next month, what timeline would you expect?\n\nMR: We'd recommend four to six weeks of preparation followed by an active process lasting eight to ten weeks.\n\nSC: Another important consideration is capital sizing. How much are you currently planning to raise?\n\nLP: Our original target was $40 million.\n\nDK: However, after reviewing our latest forecasts, we believe $25 million to $30 million may be sufficient.\n\nSC: Investors generally appreciate disciplined capital planning. Raising the minimum amount required often creates a stronger narrative.\n\nMR: Agreed. It demonstrates management confidence and efficient capital allocation.\n\nDK: What are the pros and cons of strategic investors versus traditional financial investors?\n\nMR: Strategic investors can provide distribution channels and market access, but they typically move more slowly and may request governance rights.\n\nSC: Any governance provisions would need careful negotiation to preserve flexibility for future transactions.\n\nLP: Understood.\n\nMR: As next steps, I will prepare valuation benchmarks and a target investor list by Friday.\n\nSC: I will circulate a preliminary market assessment and schedule a follow-up meeting for next week.\n\nDK: Perfect. We appreciate the guidance.\n\nLP: Thank you everyone.\n\nSC: Looking forward to continuing the discussion.\n\n[Meeting Ends]"
}
