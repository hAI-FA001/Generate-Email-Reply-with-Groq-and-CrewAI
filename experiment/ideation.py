from crewai import Crew, Agent, Task, Process
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun

from dotenv import load_dotenv
import os


load_dotenv()

GROQ_LLM = ChatGroq(model=os.environ['LLM_MODEL'])
search_tool = DuckDuckGoSearchRun()


class EmailAgents():
    def make_categorizer_agent(self):
        return Agent(
            role='Email Categorizer Agent',
            goal="""Take an email to our company and categorize it into one of the following:
            price_enquiry - when someone asks for info about pricing
            customer_complaint - when someone complains about something
            product_enquiry - when someone asks for info about a product feature, benefit or other
            customer_feedback - when someone gives feedback about a product
            off_topic - when it doesn't fit in any other category""",
            backstory="You are a master at understanding what a customer wants in an email",
            llm=GROQ_LLM,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            memory=True,
        )
    
    def make_researcher_agent(self):
        return Agent(
            role='Info Researcher Agent',
            goal="""Take an email to our company along with email category and decide what info you need to search to reply to the email in a thoughtful and helpful way.
            If you don't think a search will help, reply "NO SEARCH NEEDED".
            If you don't find any useful info, reply "NO USEFUL RESEARCH FOUND".
            Otherwise, reply with the info you found that is useful for the email writer""",
            backstory="You are a master at understanding what info our email writer needs to write a reply that will help the customer",
            llm=GROQ_LLM,
            verbose=True,
            max_iter=5,
            allow_delegation=False,
            memory=True,
            tools=[search_tool],
        )
    
    def make_email_writer_agent(self):
        return Agent(
            role='Email Writer Agent',
            goal="""Take an email to our company, the email's category and info from the research agent and write a helpful email in a thoughtful and friendly way.
            
            If the email's category is 'off_topic', ask them questions for more info.
            If the email's category is 'customer_complaint', assure we value them and we're addressing their issues.
            If the email's category is 'customer_feedback', assure we value their feedback and will consider it for our products.
            If the email's category is 'product_enquiry', give them the info from the researcher agent in a succint and friendly way.
            If the email's category is 'price_enquiry', give them the pricing info they requested.
            
            Never make up any information that's not provided by the researcher or in the email.
            Always sign off the emails in an appropriate manner and from the Resident Manager.
            """,
            backstory="You are a master at writing a helpful email that addresses the customer's issues and provides them with helpful info",
            llm=GROQ_LLM,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            memory=True
        )

class EmailTasks():
    def categorize_email(self, agent):
        return Task(
            description="""Conduct a comprehensive analysis of the email and categorize into one of the following categories:
            price_enquiry - when someone asks for info about pricing
            customer_complaint - when someone complains about something
            product_enquiry - when someone asks for info about a product feature, benefit or other
            customer_feedback - when someone gives feedback about a product
            off_topic - when it doesn't fit in any other category
            
            EMAIL_START:
            
            {email_content}
            
            EMAIL_END
            Output a single category only.""",
            expected_output="A single category from ('price_enquiry, 'customer_complaint', 'product_enquiry', 'customer_feedback', 'off_topic')",
            output_file="email_category.txt",
            agent=agent
        )
    
    def research_info_for_email(self, agent, categorize_email_task):
        return Task(
            description="""Conduct a comprehensive analysis of the provided email and the email's category, and search the web to find info needed to respond to the email
            
            EMAIL_START:
            
            {email_content}
            
            EMAIL_END
            Only provide the necessary info, DON'T write the reply, only give the info.""",
            expected_output="Either a set of bullet points of useful info for the email writer, or clear instructions that no useful material was found",
            context=[categorize_email_task],
            output_file="research_info.txt",
            agent=agent
        )
    
    def draft_email(self, agent, categorize_email_task, research_info_for_email_task):
        return Task(
            description="""Conduct a comprehensive analysis of the provided email, category and info from the research specialist to write an email.
            Write a simple, polite and to the point email in response to the provided email.
            
            If you find the research specialist's info useful, use that info in the email.
            If you don't find the research specialist's info useful, then answer politely but don't make up any info.
            
            Here's the provided email:
            EMAIL_START:
            
            {email_content}
            
            EMAIL_END
            """,
            expected_output="A well-crafted email for the customer to address their issues and concerns",
            context=[categorize_email_task, research_info_for_email_task],
            output_file="draft_email.txt",
            agent=agent
        )

