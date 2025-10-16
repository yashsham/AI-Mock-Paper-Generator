# tools.py

from crewai.tools import tool
import json

@tool("Exam Pattern Tool")
def get_exam_pattern_tool(exam_name: str) -> str:
    """
    Fetches the exam pattern for a specified government exam.
    - exam_name: The name of the exam (e.g., 'SSC CGL Tier 1').
    """
    try:
        with open('mcp_server/exam_patterns.json', 'r') as f:
            all_patterns = json.load(f)
        
        pattern = all_patterns.get(exam_name)
        
        if pattern:
            return json.dumps(pattern)
        else:
            return f"Error: Exam pattern for '{exam_name}' not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"