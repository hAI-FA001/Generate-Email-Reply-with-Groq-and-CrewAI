from crewai import Crew, Process
from EmailReply.agents import EmailAgents
from EmailReply.tasks import EmailTasks
from EmailReply import EMAIL


if __name__ == "__main__":
    agents = EmailAgents()
    tasks = EmailTasks()

    categorizer_agent = agents.make_categorizer_agent()
    researcher_agent = agents.make_researcher_agent()
    email_writer_agent = agents.make_email_writer_agent()

    categorize_email_task = tasks.categorize_email(categorizer_agent)
    research_info_task = tasks.research_info_for_email(researcher_agent, categorize_email_task)
    draft_email_task = tasks.draft_email(email_writer_agent, categorize_email_task, research_info_task)

    crew = Crew(
        agents=[categorizer_agent, researcher_agent, email_writer_agent],
        tasks=[categorize_email_task, research_info_task, draft_email_task],
        verbose=True,
        process=Process.sequential,
        full_output=True,
        share_crew=False,
    )

    results = crew.kickoff(inputs={"email_content": EMAIL})
    print(f"\n\n\nCrewAI Results: {results}")
    print(f"Usage Metrics: {crew.usage_metrics}")