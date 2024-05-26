from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.create_draft import GmailCreateDraft
from langchain.tools import tool
from tenacity import retry, wait_fixed, stop_after_attempt  # Import retry and timeout handling

class CreateDraftTool():
    @tool("Create Draft")
    @retry(wait=wait_fixed(2), stop=stop_after_attempt(5))  # Retry up to 5 times with a 2-second wait between attempts
    def create_draft(data):
        """
        Useful to create an email draft.
        The input to this tool should be a pipe (|) separated text
        of length 3 (three), representing who to send the email to,
        the subject of the email and the actual message.
        For example, `lorem@ipsum.com|Nice To Meet You|Hey it was great to meet you.`.
        """
        try:
            email, subject, message = data.split('|')
            gmail = GmailToolkit()
            draft = GmailCreateDraft(api_resource=gmail.api_resource)
            result = draft.invoke({
                'to': [email],
                'subject': subject,
                'message': message
            })
            return f"\nDraft created: {result}\n"
        except Exception as e:
            print(f"Error creating draft: {e}")  # Log any errors encountered during draft creation
            raise