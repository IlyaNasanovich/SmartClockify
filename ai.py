from os import environ
from langchain_openai import ChatOpenAI
from openai import OpenAI
from config import OPENAI_KEY
from track_time_model import TrackTimeResponse


environ["OPENAI_API_KEY"] = OPENAI_KEY

openai_client = OpenAI()
langchain_model = ChatOpenAI(model='gpt-4o-mini')
structured_output_model = langchain_model.with_structured_output(TrackTimeResponse, method='json_schema')
