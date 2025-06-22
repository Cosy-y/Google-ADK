
# 📊 Student Insights Assistant (Google ADK Hackathon)

This project is a multi-agent educational assistant built entirely on the [Google Agent Development Kit (ADK)](https://github.com/google/agent-development-kit). It runs on the built-in ADK web interface (`adk web`), requiring no custom frontend.

> 🧠 Core directory: `multi-control/` — contains the controller and all agents  
> 🌐 Use entirely through: `adk web`

---

## 🧠 Features

This multi-agent setup allows users to upload student performance data (CSV/Excel) and get:

- 📑 A complete markdown performance report with charts
- 📈 Subject-wise average visualizations
- 🗣️ Personalized student feedback
- 🥇 Ranked list of top 3 students

All processing is routed through a controller agent that delegates tasks to specialized agents:

| Agent                     | Description                                           |
|--------------------------|-------------------------------------------------------|
| `report_writer_agent`    | Generates full performance reports with chart        |
| `feedback_generator_agent` | Provides individual feedback per student            |
| `top_student_agent`      | Lists top performers and total scores                |

---

## 🚀 How to Run (Web-Only ADK Interface)

1. **Clone the repository**
```bash
git clone https://github.com/Cosy-y/Google-ADK.git
cd Google-ADK/multi-control
```

2. **Install dependencies**
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. **Start ADK Web App**
```bash
adk web
```

4. **Use the web interface to upload `.csv` or `.xlsx` files**
Example CSV format:
```
Name,Math,English,Science
Alice,80,70,90
Bob,75,85,78
Charlie,90,92,88
```

---

## 🧭 Directory Overview

```
multi-control/
├── agents/                 # All agent definitions
├── common/                 # Shared utilities (CSV parsing, charting, etc.)
├── main.py                 # Multi-agent controller (entry point)
└── ...
```

All business logic is shared via `common/data_utils.py`. Agents are modular and registered in `main.py`.

---

 🧪 Try These Prompts

    Generate a performance report from this student scores CSV.

    Can you give me a breakdown of subject averages and top 3 students?

    Please create a summary with a chart from the uploaded Excel file.

🧑‍🏫 Feedback Generator Agent

    Give personalized feedback to all students in this CSV.

    How did Ethan perform compared to the class average?

    Can you suggest improvement areas for each student?

📈 Data Insights Agent

    Tell me which subject had the highest average.

    Are there any missing values in this dataset?

    Which student scored the lowest overall?

🧠 Multi-Agent Controller (via ADK Web)

    Upload a student marksheet CSV and ask: "Can I get a summary report and feedback for all students?"

    Ask: "Which student has the best total marks, and how did others rank?"

    Query: "Generate feedback and visual report for this Excel file."

---

## 📄 License

MIT License — use and modify freely.
