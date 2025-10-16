# agents/question_generator_agent.py

from crewai import Agent, Task

class QuestionGeneratorAgents:
    # Add a 'tools' parameter here
    def make_generator_agent(self, llm, tools=None):
        return Agent(
            role='Expert Academic Question Creator',
            goal='Generate a set of high-quality, exam-style questions based on a given subject, number of questions, and reference material.',
            backstory=(
                "You are a seasoned educator and subject matter expert, renowned for your ability "
                "to create challenging and relevant exam questions that accurately test a student's knowledge, "
                "often drawing from provided study notes."
            ),
            verbose=True,
            allow_delegation=False,
            llm=llm,
            tools=tools or [] # Use the provided tools
        )

    # The task definition remains the same
    def make_question_task(self, agent, context):
        return Task(
            description=(
                'Based on the provided exam pattern, generate the specified number of questions for EACH subject. '
                'Return all generated questions formatted clearly under their respective subject headings.'
            ),
            expected_output='A well-structured text block containing all the generated questions, neatly organized by subject.',
            agent=agent,
            context=context
        )