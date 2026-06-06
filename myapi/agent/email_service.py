
# This is just for prototype in production real life settings phone call will and an emergency alert wil be 
# send to supervisor for human escalation for critical matters

import resend
from backend.config import settings

resend.api_key= settings.resend_api_key.get_secret_value()


def build_report_html(report):

    action_items_html = "".join(
        f"""
        <tr>
            <td>{item.owner or "N/A"}</td>
            <td>{item.task}</td>
            <td>{item.deadline or "N/A"}</td>
        </tr>
        """
        for item in report.action_items
    )

    discussion_topics_html = "".join(
        f"<li>{topic}</li>"
        for topic in report.discussion_topics
    )

    risks_html = "".join(
        f"<li>{risk}</li>"
        for risk in report.risks
    )

    return f"""
    <html>
    <body>

        <h1>Investment Banking Meeting Report</h1>

        <h2>Executive Summary</h2>
        <p>{report.summary}</p>

        <h2>Discussion Topics</h2>
        <ul>
            {discussion_topics_html}
        </ul>

        <h2>Action Items</h2>

        <table border="1" cellpadding="8">
            <tr>
                <th>Owner</th>
                <th>Task</th>
                <th>Deadline</th>
            </tr>
            {action_items_html}
        </table>

        <h2>Risks</h2>
        <ul>
            {risks_html}
        </ul>

        <h2>Financial Figures</h2>
        <ul>
            {''.join(f"<li>{x}</li>" for x in report.financial_figures)}
        </ul>

        <h2>Deal Intelligence</h2>
        <ul>
            {''.join(f"<li>{x}</li>" for x in report.deal_intelligence)}
        </ul>

    </body>
    </html>
    """

def send_report(report):
    try:
        html = build_report_html(report)
        params = {
            "from": "onboarding@resend.dev",
            "to": ["batmanmishra23@gmail.com"],  
            "subject": "Investment Banking Meeting Report",
            "html": html,
        }

        response = resend.Emails.send(params)
        print(f"Sent Report to Sir: {response}")
        return response
    except Exception as e:
        print({f"Error sending email: {e}"})
        return None


