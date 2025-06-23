import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.agents import Agent
from common.data_utils import load_csv, generate_student_feedback

def generate_feedback(csv_content: str, is_file: bool = False, filetype: str = "csv") -> dict:
    """Generates personalized feedback for each student in a CSV."""
    try:
        df = load_csv(csv_content, is_file=is_file, filetype=filetype)
        feedback = generate_student_feedback(df)

        # Format feedback into readable list
        feedback_lines = [f"- {student}: {message}" for student, message in feedback.items()]
        formatted = "### 🎯 Student Feedback Report\n\n" + "\n".join(feedback_lines)

        return {
            "status": "success",
            "report": formatted
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error generating feedback: {str(e)}"
        }

root_agent = Agent(
    name="feedback_generator_agent",
    model="models/gemini-1.5-flash",
    description="Agent that generates personalized feedback for students based on their scores.",
    instruction="""
You are a student advisor agent. When given a CSV of student scores, return personalized feedback per student.
Use their average score to guide your response:
- Above 85 → Excellent
- 70–85 → Good
- Below 70 → Needs improvement

Present your feedback as a clean, readable Markdown list.
""",
    tools=[generate_feedback]
)
