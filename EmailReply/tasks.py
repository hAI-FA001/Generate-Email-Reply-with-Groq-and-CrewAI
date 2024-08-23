from crewai import Task


class EmailTasks:
    @staticmethod
    def categorize_email(agent):
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
    
    @staticmethod
    def research_info_for_email(agent, categorize_email_task):
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
    
    @staticmethod
    def draft_email(agent, categorize_email_task, research_info_for_email_task):
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
