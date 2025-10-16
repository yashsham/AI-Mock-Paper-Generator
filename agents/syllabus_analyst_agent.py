# agents/syllabus_analyst_agent.py

from crewai import Agent, Task
# Import the new tool
from tools import get_exam_pattern_tool

class SyllabusAnalystAgents:
    def make_analyst_agent(self, llm):
        return Agent(
            role='Expert Exam Syllabus Analyst',
            goal='Use the tools on the MCP server to retrieve the specific pattern and syllabus for a given government exam.',
            backstory=(
                "You are an expert on government exam structures. You use a specialized "
                "MCP server to access a knowledge base of exam patterns, ensuring you always "
                "provide accurate and up-to-date information."
            ),
            verbose=True,
            allow_delegation=False,
            llm=llm,
            # Give the agent its tool
            tools=[get_exam_pattern_tool]
        )

    def make_analysis_task(self, agent, exam_name):
        return Task(
            description=f'Fetch the complete exam pattern for the exam named: {exam_name}.',
            expected_output='A JSON string containing the detailed pattern for the specified exam, including all subjects and question distribution.',
            agent=agent,
            # Also specify the tool for the task
            tools=[get_exam_pattern_tool]
        )