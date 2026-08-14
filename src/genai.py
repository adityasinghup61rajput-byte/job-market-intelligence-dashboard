from src.config import GENAI_API_KEY, GENAI_MODEL

def generate_insight(summary):
    total = summary.get("total_jobs", 0)
    avg_salary = summary.get("avg_salary", 0)
    return (f"The dataset contains {total} job postings with an average listed salary "
            f"of approximately ₹{avg_salary:,.0f}. Analyze location, title and skill "
            f"trends to identify strong hiring segments.")

def llm_configured():
    return bool(GENAI_API_KEY and GENAI_MODEL)
