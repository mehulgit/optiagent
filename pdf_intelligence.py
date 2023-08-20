import os
import time
import sys

from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper

# import env variables
load_dotenv(override=True)

llm = OpenAI(model='text-davinci-003', temperature=0)
zapier = ZapierNLAWrapper()
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
agent = initialize_agent(toolkit.get_tools(), llm, agent="zero-shot-react-description", verbose=False)
text_splitter = CharacterTextSplitter()

def summarize_pdf(pdf_file_path):
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load_and_split()
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)   
    return summary

def main():
    # assign directory

    input_directory = 'unprocessed_pdfs'
    processed_directory = 'processed_pdfs'

    while True:
        try:
            # iterate over pdf files in directory

            for filename in os.listdir(input_directory):
                f = os.path.join(input_directory, filename)

                # checking if it is a file

                if os.path.isfile(f):
                    if f.endswith('.pdf'):
                        summary = summarize_pdf(f)
                        category = llm.predict('Catagorize the following as either a finance or sales category: ' + summary)
                        # Remove new lines and other characters in the GPT output
                        category = category.strip(' \t\n\r')
                        agent_instructions = 'Send a slack message to slack workspace lablab-hackathron and slack channel ' + category + ' and message' + summary
                        agent.run(agent_instructions)
                        os.rename(f, processed_directory + '/' + filename)

            time.sleep(600)  # Wait for 10 minutes before checking again
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, exiting...")
            sys.exit()


if __name__ == "__main__":
    main()