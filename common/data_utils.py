import pandas as pd
from typing import Dict, List, Tuple
from io import StringIO, BytesIO
import base64

import matplotlib
matplotlib.use('Agg')  # This must be before any matplotlib.pyplot import
import matplotlib.pyplot as plt
import os


def generate_bar_chart(data: dict, title: str, save_dir: str = "CHARTS") -> str:
    """Generates a bar chart and saves it in the CHARTS directory by default."""
    try:
        plt.clf()
        plt.close('all')

        fig, ax = plt.subplots(figsize=(10, 6))
        subjects = list(data.keys())
        scores = [float(score) for score in data.values()]

        bars = ax.bar(subjects, scores, color='skyblue')
        ax.set_title(title)
        ax.set_xlabel('Subjects')
        ax.set_ylabel('Average Score')
        ax.set_ylim(0, 100)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')

        plt.tight_layout()

        # Create the folder if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)

        # Define the full path inside CHARTS folder
        output_path = os.path.join(save_dir, "subject_averages.png")
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close('all')

        return f"\n📊 Chart saved to: {output_path}"

    except Exception as e:
        plt.close('all')
        return f"\n⚠️ Could not generate chart: {str(e)}"


def load_csv(content: str, is_file: bool = False, filetype: str = "csv") -> pd.DataFrame:
    """Load CSV or Excel content from string or file.

    Args:
        content (str): Raw CSV text or base64-encoded file
        is_file (bool): If true, content is base64-encoded
        filetype (str): 'csv' or 'excel'

    Returns:
        pd.DataFrame
    """
    try:
        if not is_file:
            return pd.read_csv(StringIO(content)) if filetype == "csv" else pd.read_excel(StringIO(content))
        else:
            decoded = base64.b64decode(content)
            if filetype == "csv":
                return pd.read_csv(BytesIO(decoded))
            elif filetype == "excel":
                return pd.read_excel(BytesIO(decoded))
            else:
                raise ValueError("Unsupported file type")
    except Exception as e:
        raise RuntimeError(f"Error loading file: {str(e)}")


def get_subject_columns(df: pd.DataFrame) -> List[str]:
    """Assumes first column is student name, rest are subjects."""
    return list(df.columns[1:])


def get_top_student(df: pd.DataFrame) -> Tuple[str, int]:
    """Return top student name and total score."""
    subject_cols = get_subject_columns(df)
    df["Total"] = df[subject_cols].sum(axis=1)
    top_row = df.loc[df["Total"].idxmax()]
    return top_row[df.columns[0]], int(top_row["Total"])


def get_top_3_students(df: pd.DataFrame) -> List[Tuple[str, float]]:
    """Return top 3 students as (name, total score)."""
    subject_cols = get_subject_columns(df)
    df["Total"] = df[subject_cols].sum(axis=1)
    top_3 = df.nlargest(3, "Total")
    return [(row[df.columns[0]], row["Total"]) for _, row in top_3.iterrows()]



def get_subject_averages(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate subject-wise averages."""
    subject_cols = get_subject_columns(df)
    return {col: round(df[col].mean(), 2) for col in subject_cols}


def detect_missing_values(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """Return missing count and % for each column."""
    return {
        col: {
            "missing_count": int(df[col].isna().sum()),
            "missing_percentage": round(df[col].isna().sum() / len(df) * 100, 2)
        }
        for col in df.columns
    }


def generate_student_feedback(df: pd.DataFrame) -> Dict[str, str]:
    """Return feedback string for each student."""
    feedback = {}
    subject_cols = get_subject_columns(df)

    for _, row in df.iterrows():
        name = row[0]
        scores = row[subject_cols]
        avg = scores.mean()
        msg = f"{name} scored an average of {avg:.1f}. "

        if avg >= 85:
            msg += "Excellent performance overall."
        elif avg >= 70:
            msg += "Good, but improvement is possible."
        else:
            msg += "Needs focused support in core subjects."

        feedback[name] = msg

    return feedback
