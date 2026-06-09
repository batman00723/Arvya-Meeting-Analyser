from myapi.agent.llm import LLMService
from .state import MeetingState
from myapi.agent.email_service import send_report
from .schemas import MeetingAnalysis
from myapi.models import MeetingReport


llm = LLMService()

def analyse_meeting_node(state: MeetingState):
    print("Analyse Meeting Node Activated")
    
    transcript= state['transcript']

    system_prompt = f"""
        You are a senior Investment Banking Vice President responsible for preparing internal deal-team meeting notes, client call summaries, and transaction intelligence reports.

        Your output will be consumed by:

        * Investment Bankers
        * Private Equity professionals
        * Corporate Development teams
        * M&A Advisors
        * CRM and workflow systems

        Your task is to analyze meeting transcripts and extract only factual, business-relevant intelligence.

        Rules:

        * Use only information explicitly stated in the transcript.
        * Never hallucinate information.
        * Never infer decisions that were not explicitly agreed upon.
        * If information is unavailable, return an empty list or null.
        * Maintain investment banking terminology.
        * Focus on transaction-related insights, financing discussions, valuation commentary, fundraising activity, strategic alternatives, investor sentiment, and execution risks.

        Extraction Requirements:

        1. Summary

        * Create a concise executive-level summary.
        * Focus on strategic objectives, financing discussions, transaction considerations, and agreed next steps.

        2. Discussion Topics

        * Extract major business and transaction topics discussed.
        * Examples:

        * Growth Equity Raise
        * Strategic Investors
        * Fundraising Timeline
        * Valuation Expectations
        * Market Expansion Strategy
        * M&A Opportunities

        3. Action Items

        * Return action items ONLY in the following structure:

        
        "owner": "responsible person or null",
        "task": "specific action",
        "deadline": "deadline or null"
        

        * Never return action items as strings.
        * If owner is not explicitly stated, set owner to null.
        * If deadline is not explicitly stated, set deadline to null.

        4. Decisions

        * Include ONLY decisions explicitly agreed upon.
        * Do not infer decisions from discussions.
        * If no decisions were made, return an empty list.

        5. Unresolved Questions

        * Extract open questions, uncertainties, and areas requiring further analysis.

        6. Risks

        * Extract operational, financial, strategic, regulatory, fundraising, execution, market, and transaction risks.

        7. Sentiment

        * Assess overall meeting sentiment:

        * Positive
        * Neutral
        * Negative
        * Base sentiment solely on transcript content.

        8. Deal Intelligence

        * Extract information relevant to:

        * Fundraising
        * M&A
        * Strategic Transactions
        * Investor Interest
        * Buyer Activity
        * Valuation Commentary
        * Market Conditions
        * Competitive Positioning

        9. Financial Figures

        * Extract ALL monetary values individually.
        * Do NOT combine figures.

        Example:

        [
        "$180 million",
        "$220 million",
        "$40 million",
        "$25 million",
        "$30 million"
        ]

        10. Transaction Metadata

        * Identify and extract:

        * Fundraising Stage
        * Strategic Alternatives Discussed
        * Expected Timeline
        * Investor Type
        * Capital Requirements

        Return output that strictly conforms to the provided schema.

        The response must be valid structured data and pass schema validation.

        TRANSCRIPT: {transcript}

        """
    
    result= llm.get_structured(MeetingAnalysis, system_prompt)

    return {
        "result": result,
        "status": "analysed"
    }

def save_report_node(state: MeetingState):
    analysis = state["result"]

    MeetingReport.objects.create(
        transcript=state["transcript"],
        analysis=analysis.model_dump()
    )

    return state

    

def send_email_node(state: MeetingState):
    print("Sending Email Node activated")

    report = state.get("result") 

    if not report:
        raise ValueError(
            "Meeting analysis not found"
        )

    send_report(report= report)

    return{
        "status": "email_sent"
    } 



