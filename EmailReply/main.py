from crewai import Crew, Process
from EmailReply.agents import EmailAgents
from EmailReply.tasks import EmailTasks
from EmailReply import EMAIL


if __name__ == "__main__":
    categorizer_agent = EmailAgents.make_categorizer_agent()
    researcher_agent = EmailAgents.make_researcher_agent()
    email_writer_agent = EmailAgents.make_email_writer_agent()

    categorize_email_task = EmailTasks.categorize_email(categorizer_agent)
    research_info_task = EmailTasks.research_info_for_email(researcher_agent, categorize_email_task)
    draft_email_task = EmailTasks.draft_email(email_writer_agent, categorize_email_task, research_info_task)

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
    print(f"\n\nUsage Metrics: {crew.usage_metrics}")