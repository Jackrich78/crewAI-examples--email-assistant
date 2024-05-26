import os
import time
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.search import GmailSearch
from tenacity import retry, wait_fixed, stop_after_attempt  # Import retry and timeout handling
import logging  # Import logging for better traceability

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Nodes():
    def __init__(self):
        self.gmail = GmailToolkit()

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(5))  # Retry up to 5 times with a 2-second wait between attempts
    def check_email(self, state):
        logging.info("Checking for new emails")  # Log the beginning of the email check process
        search = GmailSearch(api_resource=self.gmail.api_resource)
        emails = search('after:newer_than:1d')
        checked_emails = state['checked_emails_ids'] if state['checked_emails_ids'] else []
        thread = []
        new_emails = []
        for email in emails:
            if (email['id'] not in checked_emails) and (email['threadId'] not in thread) and (os.environ['MY_EMAIL'] not in email['sender']):
                thread.append(email['threadId'])
                new_emails.append(
                    {
                        "id": email['id'],
                        "threadId": email['threadId'],
                        "snippet": email['snippet'],
                        "sender": email["sender"]
                    }
                )
        checked_emails.extend([email['id'] for email in emails])
        return {
            **state,
            "emails": new_emails,
            "checked_emails_ids": checked_emails
        }

    def wait_next_run(self, state):
        logging.info("Waiting for 30 seconds")  # Log the waiting period (originally 180 seconds)
        time.sleep(30)
        return state

    def new_emails(self, state):
        if len(state['emails']) == 0:
            logging.info("No new emails")  # Log when no new emails are found
            return "end"
        else:
            logging.info("New emails found")  # Log when new emails are found
            return "continue"
