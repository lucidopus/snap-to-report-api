from langchain_core.tools import Tool

from utils.prompts import CAPTION_IMAGE_TOOL_PROMPT, GET_CATEGORY_TOOL_PROMPT, QUERY_IMAGE_TOOL_PROMPT, DETECT_OBJECTS_TOOL_PROMPT
from utils.helper import get_category, get_image_caption, query_image, detect_objects

tools = [
    Tool(
        name="Get image caption",
        func=get_image_caption,
        description=CAPTION_IMAGE_TOOL_PROMPT,
        return_direct=False
    ),

    Tool(
        name="Ask queries regarding the image context",
        func=query_image,
        description=QUERY_IMAGE_TOOL_PROMPT,
        return_direct=False
    ),

    Tool(
        name="Detect objects in the image",
        func=detect_objects,
        description=DETECT_OBJECTS_TOOL_PROMPT,
        return_direct=False
    ),
    
    Tool(
        name="Get category of the image",
        func=get_category,
        description=GET_CATEGORY_TOOL_PROMPT,
        return_direct=False
    ),
]
