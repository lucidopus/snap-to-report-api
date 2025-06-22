import ast
import random
import datetime
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq

from utils.config import GROQ_API_KEY, GROQ_MODEL, TABLE_NAME
from utils.database import supabase_client
from utils.helper import get_address, extract_category, extract_annotated_image
from utils.models import ReportOutput, S2RRequest, ReportObject
from utils.tools import tools
from utils.prompts import ASSISTANT_PROMPT


def assistant_pipeline(request: S2RRequest):

    image = request.file
    latitude = request.latitude
    longitude = request.longitude
    mainid = random.randint(100000, 999999)

    address = get_address(latitude, longitude)

    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
    )

    tool_names = [tool.name for tool in tools]

    report_parser = PydanticOutputParser(pydantic_object=ReportOutput)

    format_instructions = report_parser.get_format_instructions()

    agent_prompt = PromptTemplate(
        input_variables=["agent_scratchpad", "input"],
        template=ASSISTANT_PROMPT,
        partial_variables={
            "tool_names": tool_names,
            "location": address,
            "format_instructions": format_instructions,
        },
    )

    agent = create_react_agent(llm, tools, agent_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
        early_stopping_method="generate",
    )

    response = agent_executor.invoke(
        {
            "image_url": image,
        }
    )

    report = response["output"]

    supabase_client.table(TABLE_NAME).insert(
        {
            "report": report,
            "mainid": mainid,
            "image_url": request.file,
            "timestamp": datetime.datetime.now().isoformat(),
            "category": extract_category(response['intermediate_steps']),
            "latitude": latitude,
            "longitude": longitude,
            "annotated_image_url": extract_annotated_image(response['intermediate_steps']),
            "address": address,
        }
    ).execute()

    return response['output']
