# agents/paper_formatter_agent.py

from crewai import Agent, Task

class PaperFormatterAgents:
    def make_formatter_agent(self, llm):
        return Agent(
            role='Expert Document Formatter',
            goal='Format a collection of questions and subjects into a professional, well-structured mock exam paper in Markdown format.',
            backstory=(
                "You are a meticulous editor with a talent for organizing information. "
                "You specialize in creating clean, professional, and easy-to-read "
                "educational documents from raw text."
            ),
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    def make_formatting_task(self, agent, context):
        return Task(
            description=(
                'Take the generated questions and format them into a complete mock exam paper. '
                'The final output must be a single Markdown document that includes:\n'
                '1. A main title for the exam.\n'
                '2. Clear headings for each subject/section.\n'
                '3. All questions listed neatly under their respective headings.'
            ),
            expected_output='A single, complete mock exam paper formatted in clean Markdown.',
            agent=agent,
            context=context
        )