import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.agents import Agent
from common.controller_utils import (
    route_to_analysis,
    route_to_feedback,
    route_to_report
)


def smart_dispatch(csv_content: str, query: str) -> dict:
    """
    Multi-agent controller that intelligently routes queries to the correct sub-agent.
    """
    query_lower = query.lower()

    try:
        # Keywords for each route
        analysis_keywords = [
            "analyze", "summary", "overview", "columns", "rows", "structure", "data inside", "what's in", "contents"
        ]
        feedback_keywords = [
            "feedback", "comment", "suggestion", "advise", "advice", "recommend", "improve", "per student"
        ]
        report_keywords = [
            "report", "performance", "top", "topper", "rank", "best", "highest",
            "score", "average", "chart", "graph", "result", "visual", "visualize", "plot"
        ]



        # Smart routing
        if any(kw in query_lower for kw in analysis_keywords):
            return route_to_analysis(csv_content)

        elif any(kw in query_lower for kw in feedback_keywords):
            return route_to_feedback(csv_content)

        elif any(kw in query_lower for kw in report_keywords):
            return route_to_report(csv_content)

        else:
            return {
                "status": "uncertain",
                "message": (
                    "I couldn't understand the task. Please clarify if you want:\n"
                    "- a summary of the data\n"
                    "- personalized student feedback\n"
                    "- a performance report with charts"
                )
            }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error during multi-agent dispatch: {str(e)}"
        }



root_agent = Agent(
    name="multi_agent_controller",
    model="models/gemini-1.5-flash",
    description="An agent that routes CSV-based questions to the best suited sub-agent.",
    instruction="""
You are a multi-agent orchestrator. When given a CSV file and a user query, decide whether to:

- Analyze the dataset (column names, row counts, structure)
- Generate feedback per student (based on average scores)
- Generate a report (topper, averages, chart)

Call the correct sub-agent accordingly.
""",
    tools=[smart_dispatch]
)
