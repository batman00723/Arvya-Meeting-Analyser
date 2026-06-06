# Arvya Meeting Analyser

Meeting intelligence system that converts meeting transcripts into structured Financial(IB, PE) insights using LangGraph and LLMs.

## Features

* Transcript analysis using LLMs
* Structured data extraction
* Action item detection
* Risk identification
* Deal intelligence generation
* Financial figure extraction
* PostgreSQL persistence
* Automated email reporting
* REST API interface

## Tech Stack

* Django
* Django Ninja Extra
* LangGraph
* Groq (Qwen 32B)
* PostgreSQL (Supabase)
* Resend
* Render

## Architecture

```text
Transcript
    │
    ▼
Meeting Analysis Node
    │
    ▼
Save Report Node
    │
    ▼
Email Report Node
```

## Email Sccreenshot

<p align="center">
  <img src="Screenshot 2026-06-06 215846.png" width="600" title="Email test ss">
</p>

## Extracted Fields

* Summary
* Discussion Topics
* Action Items
* Decisions
* Unresolved Questions
* Risks
* Sentiment
* Deal Intelligence
* Financial Figures

## Assumptions

* Transcript is available before processing.
* Speaker attribution exists in the transcript.

## Tradeoffs

* One agent workflow for simplicity over multi agent specialisation in single task.
* Structured extraction improves consistency but may require schema optimisation.
* Qwen 32B LLM Model chosen for less latency and less costs.


## Deployment

```text
https://arvya-meeting-analyser.onrender.com/api_v1/docs
```

