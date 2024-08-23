from crewai import Agent
from EmailReply import GROQ_LLM, search_tool


class EmailAgents:
    @staticmethod
    def make_categorizer_agent():
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
    
    @staticmethod
    def make_researcher_agent():
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
    
    @staticmethod
    def make_email_writer_agent():
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
