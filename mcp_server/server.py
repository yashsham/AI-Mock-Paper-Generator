# mcp_server/server.py

from fastmcp import FastMCP
from crewai.tools import tool
import json

# 1. Create an instance of the MCP server
mcp = FastMCP("mock_paper_generator_mcp")

# 2. Define the tool to get exam patterns
@tool("Exam Pattern Tool")
def get_exam_pattern_tool(exam_name: str) -> str:
    """
    Fetches the exam pattern, including subjects and question distribution,
    for a specified government exam.
    - exam_name: The name of the exam (e.g., 'SSC CGL Tier 1').
    """
    try:
        with open('mcp_server/exam_patterns.json', 'r') as f:
            all_patterns = json.load(f)
        
        # Find the specific pattern for the requested exam
        pattern = all_patterns.get(exam_name)
        
        if pattern:
            return json.dumps(pattern) # Return the pattern as a string
        else:
            return f"Error: Exam pattern for '{exam_name}' not found."
    except Exception as e:
        return f"An error occurred while reading the exam patterns file: {str(e)}"

# 3. Add a line to make the server runnable
if __name__ == "__main__":
    mcp.run(transport="stdio")