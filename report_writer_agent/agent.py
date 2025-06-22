import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.agents import Agent
from common.data_utils import load_csv, get_top_student, get_subject_averages

def write_csv_report(csv_content: str, is_file: bool = False, filetype: str = "csv") -> dict:
    """Generates a human-readable report in Markdown format from a CSV dataset."""
    try:
        df = load_csv(csv_content, is_file=is_file, filetype=filetype)
        top_student, total_score = get_top_student(df)
        averages = get_subject_averages(df)

        report = f"### 📊 Student Performance Report\n\n"
        report += f"**Top Student:** {top_student} with a total score of {total_score}\n\n"
        report += f"**Subject Averages:**\n"
        for subject, avg in averages.items():
            report += f"- {subject}: {avg}\n"
        report += "\n✅ This report summarizes overall performance using basic statistics."

        return {
            "status": "success",
            "report": report
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error generating report: {str(e)}"
        }

root_agent = Agent(
    name="report_writer_agent",
    model="gemini-2.0-flash",
    description="Agent to generate human-readable performance reports from a CSV dataset.",
    instruction="""
You are a Markdown-savvy reporting assistant. When given a CSV containing student scores:
1. Identify the top-performing student.
2. Calculate average scores for each subject.
3. Generate a readable report in Markdown format.

Always include bullet points and summary insights that help readers understand the data easily.
""",
    tools=[write_csv_report]
)
