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

## Test Transcript
{
  "transcript": "Investment Banking Strategic Advisory Meeting\n\nParticipants:\n\nSarah Chen (SC) – Managing Director, Investment Banking\nMichael Ross (MR) – Vice President, Investment Banking\nDavid Kapoor (DK) – CEO, NovaTech Solutions\nLisa Patel (LP) – CFO, NovaTech Solutions\n\nSC: Thanks everyone for joining. David, Lisa, we're excited to discuss your fundraising and growth plans.\n\nDK: Thanks, Sarah. Our primary objective is expanding into Southeast Asia over the next 18 months. We've seen strong inbound demand and believe the market timing is favorable.\n\nLP: To support that expansion, we're evaluating a growth capital raise and assessing strategic partnership opportunities.\n\nMR: Based on our preliminary review, the business is performing well. Revenue growth and customer retention metrics are attractive from an investor perspective.\n\nDK: What valuation range do you believe the market would support today?\n\nMR: Based on comparable transactions, we estimate a valuation between $180 million and $220 million, assuming current growth rates continue.\n\nLP: That's broadly in line with our expectations.\n\nSC: One concern investors may raise is scalability. They will want confidence that your operational infrastructure can support international growth without compressing margins.\n\nDK: That's fair. We're currently investing in customer success and regional hiring, but there is still uncertainty around regulatory compliance costs.\n\nLP: We are also evaluating how customer acquisition costs may change as we enter new markets.\n\nMR: Those are exactly the questions investors will focus on during diligence.\n\nDK: If we moved forward with a fundraising process next month, what timeline would you expect?\n\nMR: We'd recommend four to six weeks of preparation followed by an active process lasting eight to ten weeks.\n\nSC: Another important consideration is capital sizing. How much are you currently planning to raise?\n\nLP: Our original target was $40 million.\n\nDK: However, after reviewing our latest forecasts, we believe $25 million to $30 million may be sufficient.\n\nSC: Investors generally appreciate disciplined capital planning. Raising the minimum amount required often creates a stronger narrative.\n\nMR: Agreed. It demonstrates management confidence and efficient capital allocation.\n\nDK: What are the pros and cons of strategic investors versus traditional financial investors?\n\nMR: Strategic investors can provide distribution channels and market access, but they typically move more slowly and may request governance rights.\n\nSC: Any governance provisions would need careful negotiation to preserve flexibility for future transactions.\n\nLP: Understood.\n\nMR: As next steps, I will prepare valuation benchmarks and a target investor list by Friday.\n\nSC: I will circulate a preliminary market assessment and schedule a follow-up meeting for next week.\n\nDK: Perfect. We appreciate the guidance.\n\nLP: Thank you everyone.\n\nSC: Looking forward to continuing the discussion.\n\n[Meeting Ends]"
}
