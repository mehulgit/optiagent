import os 
import openai
import tempfile
import time
import sys

from dotenv import load_dotenv
from datetime import datetime
from moviepy.editor import *
from pytube import YouTube
from urllib.parse import urlparse, parse_qs

from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ReduceDocumentsChain, MapReduceDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.document_loaders import UnstructuredFileLoader
from googleapiclient.discovery import build
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper

# import env variables
load_dotenv(override=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

api_service_name = 'youtube'
api_version = 'v3'
DEVELOPER_KEY = os.getenv("GOOGLE_API_KEY")

zapier_nla_api_key = os.getenv("ZAPIER_NLA_API_KEY")

channel_id = os.getenv("CHANNEL_ID")
channel_name = os.getenv("CHANNEL_NAME")
email_recepient = os.getenv("EMAIL_RECEPIENT")

youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

def get_latest_video(channel_id):
    response = youtube.search().list(
        channelId=channel_id,
        order='date',
        maxResults=1,
        part='snippet,id'
    ).execute()

    if 'items' in response:
        return response['items'][0]
    else:
        return None

# Transcripe MP3 Audio function
def transscribe_audio(file_path):
    file_size = os.path.getsize(file_path)
    file_size_in_mb = file_size / (1024 * 1024)
    if file_size_in_mb < 25:
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file, verbose= False, logger=None)

        return transcript
    else:
        print("Please provide a smaller audio file (max 25).")

def get_latest_video(channel_id):
    response = youtube.search().list(
        channelId=channel_id,
        order='date',
        maxResults=20,
        type='video',
        part='snippet'
    ).execute()

    if 'items' in response:
        return response['items'][0]
    else:
        return None

def process_video(video_url):
    # Extract the video ID from the url
    query = urlparse(video_url).query
    params = parse_qs(query)
    video_id = params["v"][0]

    with tempfile.TemporaryDirectory() as temp_dir:
        
        # Download video audio
        yt = YouTube(video_url)

        # Get the first available audio stream and download this stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=temp_dir)

        # Convert the audio file to MP3
        audio_path = os.path.join(temp_dir, audio_stream.default_filename)
        audio_clip = AudioFileClip(audio_path)
        audio_clip.write_audiofile(os.path.join(temp_dir, f"{video_id}.mp3"), logger=None)

        # Keep the path of the audio file
        audio_path = f"{temp_dir}/{video_id}.mp3"

        # Transscripe the MP3 audio to text
        transcript = transscribe_audio(audio_path)
        
        # Delete the original audio file
        os.remove(audio_path)
            
    # save the transcript to a text file

    timestr = time.strftime("%Y%m%d-%H%M%S")
    try:
        os.makedirs('./transcripts')
    except OSError:
        pass # already exists
    filename = './transcripts/youtube-video' + timestr + '.txt'

    with open(filename, 'w') as f:
         f.write(transcript.text)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    loader = UnstructuredFileLoader(filename)
    doc = loader.load()

    # Map
    map_template = """The following is a video transcript
    {doc}
    Based on this video transcript, please identify the main themes and summarize them in a few sentences.
    Helpful Answer:"""
    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt)

    # Reduce
    reduce_template = """The following is set of summaries:
    {doc_summary}
    Take these and distill it into a final, consolidated summaries of the main theme. 
    Helpful Answer:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

# Takes a list of documents, combines them into a single string, and passes this to an LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="doc_summary"
    )

# Combines and iteravely reduces the mapped documents
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=4000,
    )

    # Combining documents by mapping a chain over them, then combining results
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="doc",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
    )

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    split_text = text_splitter.split_documents(doc)

    summary = (map_reduce_chain.run(split_text))

    llm = OpenAI(temperature=0)
    zapier = ZapierNLAWrapper()
    toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
    agent = initialize_agent(toolkit.get_tools(), llm, agent="zero-shot-react-description", verbose=False)

    date_string = f'{datetime.now():%Y-%m-%d-%H:%M:%S%z}'

    agent_instructions = 'Send an Email to ' + email_recepient + 'via gmail informing them that a new video has been posted and the summary of the video transcript is: ' + summary + 'Also add one row with the value Column1: ' + str(date_string) + ' Column2: ' +  str(video_url) + ', Column3: ' + channel_name + ' to the youtube-videos google sheet' 
    agent.run(agent_instructions)

# Main application
def main(): 
    # Get the channel Id of a youtube channnel from here: https://commentpicker.com/youtube-channel-id.php

    global channel_name 
    latest_video = None

    while True:
        try:
            new_video = get_latest_video(channel_id)

            if new_video and new_video != latest_video:
                latest_video = new_video
                video_id = latest_video['id']['videoId']
                video_url = f'https://www.youtube.com/watch?v={video_id}'

                # Process the video
                process_video(video_url)
            time.sleep(600)  # Wait for 10 minutes before checking again
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, exiting...")
            sys.exit()

## execute main
if __name__ == "__main__":
    main()