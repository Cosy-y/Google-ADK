from data_insight_agent.agent import analyze_csv_data, identify_top_student
from feedback_generator_agent.agent import generate_feedback
from report_writer_agent.agent import write_csv_report

def generate_comprehensive_report(csv_content: str) -> dict:
    """Generates a complete report with all analyses combined."""
    try:
        output = []
        
        # 1. Basic Analysis
        analysis = analyze_csv_data(csv_content)
        if analysis["status"] == "success":
            output.append("### 📊 Data Overview")
            output.append(analysis["report"])
            
        # 2. Top Student Analysis
        top_student = identify_top_student(csv_content)
        if top_student["status"] == "success":
            output.append("\n### 🏆 Top Performance")
            output.append(f"Top Student: {top_student['report']['top_student']}")
            output.append(f"Total Score: {top_student['report']['total_score']}")
            
        # 3. Student Feedback
        feedback = generate_feedback(csv_content)
        if feedback["status"] == "success":
            output.append("\n" + feedback["report"])
            
        # 4. Visual Report
        report = write_csv_report(csv_content)
        if report["status"] == "success":
            output.append("\n" + report["output"])
            
        return {
            "status": "success",
            "output": "\n".join(output)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error generating comprehensive report: {str(e)}"
        }

def route_to_analysis(csv_content: str) -> dict:
    """Runs CSV through data insight analysis tools."""
    # If it's a general analysis request, generate comprehensive report
    return generate_comprehensive_report(csv_content)

def route_to_feedback(csv_content: str) -> dict:
    """Routes to feedback generator agent."""
    result = generate_feedback(csv_content)
    return {
        "status": result["status"],
        "output": result.get("report", result.get("error_message", "No feedback available."))
    }

def route_to_report(csv_content: str) -> dict:
    """Routes to the report writer agent that generates Markdown + chart."""
    return write_csv_report(csv_content)