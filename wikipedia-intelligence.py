import os 
import openai
import time
import requests
from bs4 import BeautifulSoup
import sys

from dotenv import load_dotenv
from datetime import datetime

from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper

# import env variables
load_dotenv(override=True)

openai.api_key = os.getenv("OPENAI_API_KEY")
zapier_nla_api_key = os.getenv("ZAPIER_NLA_API_KEY")
wiki_url = os.getenv("WIKI_URL")
email_recepient = os.getenv("EMAIL_RECEPIENT")

# Main application
def main(): 

    response = requests.get(wiki_url)
    soup = BeautifulSoup(response.content, "html.parser")  
    previous_revision_list = None
    llm = OpenAI(temperature=0)
    zapier = ZapierNLAWrapper()
    toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
    agent = initialize_agent(toolkit.get_tools(), llm, agent="zero-shot-react-description", verbose=False)

    while True:

        revisions_list = soup.find_all("ul", class_="mw-contributions-list")

        try:

            if revisions_list:
                if revisions_list != previous_revision_list:
                    previous_revision_list = revisions_list
                    last_revision = revisions_list[0].find("a", class_="mw-changeslist-date").text
                    editor_info = revisions_list[0].find("a", class_="mw-userlink").text
                    comment = revisions_list[0].find("span", class_="autocomment").text
                    change = 'User: ' + editor_info + ' made a change to ' + wiki_url + ' on ' + last_revision + '. The change was: ' + comment

                    agent_instructions = 'Send an Email to ' + email_recepient + ' via gmail informing them that changes have been made to the Wikipedia page being tracked and the changes are: ' + change
                    agent.run(agent_instructions)
            else:
                print("No revisions found, check for a bad Wikipedia URL.")
                sys.exit()

            time.sleep(600)  # Wait for 10 minutes before checking again

        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, exiting...")
            sys.exit()

## execute main
if __name__ == "__main__":
    main()