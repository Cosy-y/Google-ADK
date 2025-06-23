import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.agents import Agent
from common.data_utils import load_csv, get_top_student, get_subject_columns, detect_missing_values


def analyze_csv_data(csv_content: str, is_file: bool = False, filetype: str = "csv") -> dict:
    """Basic summary and sample of the dataset."""
    try:
        df = load_csv(csv_content, is_file=is_file, filetype=filetype)

        # Create a readable summary string
        summary = (
            f"Total Rows: {len(df)}\n"
            f"Columns: {', '.join(list(df.columns))}\n\n"
            f"Sample Data (first 5 rows):\n"
        )

        # Add sample data in a readable format
        for idx, row in df.head(5).iterrows():
            summary += f"Row {idx + 1}: {dict(row)}\n"

        return {
            "status": "success",
            "report": summary
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error analyzing CSV: {str(e)}"
        }

def detect_missing_data(csv_content: str, is_file: bool = False, filetype: str = "csv") -> dict:
    """Reports missing values per column."""
    try:
        df = load_csv(csv_content, is_file=is_file, filetype=filetype)
        report = detect_missing_values(df)
        return {
            "status": "success",
            "report": report
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error analyzing missing data: {str(e)}"
        }

def identify_top_student(csv_content: str, is_file: bool = False, filetype: str = "csv") -> dict:
    """Finds the top-scoring student."""
    try:
        df = load_csv(csv_content, is_file=is_file, filetype=filetype)
        name, total = get_top_student(df)
        return {
            "status": "success",
            "report": {
                "top_student": name,
                "total_score": total
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error finding top student: {str(e)}"
        }

root_agent = Agent(
    name="data_insights_assistant",
    model="models/gemini-1.5-flash",
    description="Agent to analyze CSV data and provide insights about the dataset.",
    instruction="""
You are a helpful data analysis assistant who can:
1. Analyze CSV files and provide basic insights
2. Detect and report missing data patterns
3. Identify the top-performing student based on total scores

When a user asks who scored highest, who the best student is, or anything about top performance, you should call the top student analysis tool. Always explain your output in a human-friendly format.
""",
    tools=[analyze_csv_data, detect_missing_data, identify_top_student]
)
