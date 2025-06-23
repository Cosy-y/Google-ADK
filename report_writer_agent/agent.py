import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.agents import Agent
from common.data_utils import (
    load_csv,
    get_subject_columns,
    get_top_student,
    get_top_3_students,
    get_subject_averages,
    generate_bar_chart
)
import google.generativeai as genai
import os

# Always configure Gemini, regardless of Vertex setting
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Optional: Read VERTEXAI flag if you need it for branching logic
use_vertexai = os.getenv("VERTEXAI", "False").lower() == "true"

if use_vertexai:
    # (Your Vertex code — likely not used)
    pass
else:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Generate a report...")



def write_csv_report(csv_content: str) -> dict:
    """Generates a human-readable report and saves chart as PNG."""
    try:
        df = load_csv(csv_content)

        # Get top student info
        top_student, top_score = get_top_student(df)

        # Get top 3 students
        top_3 = get_top_3_students(df)

        # Calculate subject averages
        subject_averages = get_subject_averages(df)

        # Generate chart
        chart_message = generate_bar_chart(
            data=subject_averages,
            title="Subject-wise Average Scores"
        )

        # Compose report
        full_report = (
            f"### 📝 Student Performance Report\n\n"
            f"🏆 **Top Student:** {top_student} with a total score of {top_score}\n\n"
            f"🥇 **Top 3 Students:**\n"
        )

        for i, (name, total) in enumerate(top_3, 1):
            full_report += f"{i}. {name} — {total:.0f} points\n"

        full_report += "\n📈 **Subject Averages:**\n"
        for subject, avg in subject_averages.items():
            full_report += f"- {subject}: {avg:.2f}\n"

        full_report += f"\n{chart_message}"

        return {
            "status": "success",
            "output": full_report
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
1. Identify the top-performing student
2. List the top 3 students by total marks
3. Calculate average scores for each subject
4. Generate a readable report in Markdown format
5. Include a bar chart showing subject-wise averages

Always include bullet points, visuals, and summary insights that help readers understand the data easily.
""",
    tools=[write_csv_report]
)
