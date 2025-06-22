import ast
import uuid
import pandas as pd
import numpy as np
from io import BytesIO
import moondream as md
from PIL import Image, ImageDraw
from geopy.geocoders import Nominatim
from langchain_openai import OpenAIEmbeddings
import requests

from utils.config import MOONDREAM_API_KEY, OPENAI_API_KEY


model = md.vl(api_key=MOONDREAM_API_KEY)


def extract_category(intermediate_steps):
    for i, step in enumerate(intermediate_steps):
        if isinstance(step, tuple) and len(step) == 2:
            agent_action, response = step
            if getattr(agent_action, 'tool', '') == "Get category of the image":
                return response 
    return "No matching category found!"

def extract_annotated_image(intermediate_steps):
    for i, step in enumerate(intermediate_steps):
        if isinstance(step, tuple) and len(step) == 2:
            agent_action, response = step
            if getattr(agent_action, 'tool', '') == "Detect objects in the image":
                return response 
    return "No annotations found!"


def get_image_from_url(image: str) -> Image:
    response = requests.get(image)
    image = Image.open(BytesIO(response.content))
    return image


def detect_objects(detection_request: dict):
    detection_request = ast.literal_eval(detection_request)

    image_url = detection_request["image"]
    image = get_image_from_url(image_url)

    objects = detection_request["objects"]
    annotations = model.detect(image, objects)["objects"]

    annotated_image = image.copy()
    draw = ImageDraw.Draw(annotated_image)
    width, height = image.size

    for obj in annotations:
        x_min = int(obj["x_min"] * width)
        y_min = int(obj["y_min"] * height)
        x_max = int(obj["x_max"] * width)
        y_max = int(obj["y_max"] * height)
        draw.rectangle([x_min, y_min, x_max, y_max], outline="lightgreen", width=4)

    # image_bytes = BytesIO()
    # annotated_image.save(image_bytes, format="PNG")
    # image_bytes.seek(0)

    # filename = f"annotated-{uuid.uuid4()}.png"

    # # Upload to Supabase Storage
    # supabase_client.storage.from_(BUCKET_NAME).upload(
    #     path=filename,
    #     file=image_bytes.getvalue(),
    #     file_options={"content-type": "image/png"},
    # )

    # public_url_response = supabase_client.storage.from_(BUCKET_NAME).get_public_url(filename)
    # public_url = public_url_response.get("publicUrl") or public_url_response.get("public_url")

    # print(public_url)

    return "The image has been annotated with the detected objects."


def get_image_caption(image_url: str) -> str:
    image = get_image_from_url(image_url)
    caption = model.caption(image)['caption']
    return caption


def query_image(query_request: dict) -> str:

    query_request = ast.literal_eval(query_request)

    image = query_request['image']
    query = query_request['query']

    image = get_image_from_url(image)
    response = model.query(image=image, question=query)
    return response['answer']


def get_category(raw_category: str) -> str:
    
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-large")

    embedding = embeddings.embed_query(raw_category)

    df = pd.read_csv(
        "data/category_embeddings.csv", converters={"embedding": eval}
    )  

    df["embedding_norm"] = df["embedding"].apply(
        lambda x: np.array(x) / np.linalg.norm(x)
    )

    new_embedding = np.array(embedding)
    new_embedding_norm = new_embedding / np.linalg.norm(new_embedding)

    df["similarity"] = df["embedding_norm"].apply(
        lambda x: np.dot(x, new_embedding_norm)
    )

    best_match = df.loc[df["similarity"].idxmax()]
    return best_match["category"]


def get_address(latitude, longitude):
    """
    Converts latitude and longitude to a human-readable address.

    Args:
      latitude: The latitude of the location.
      longitude: The longitude of the location.

    Returns:
      The full address string, or None if the address could not be found.
    """
    geolocator = Nominatim(user_agent="S2R Agent")
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        return location.address
    except (AttributeError, TypeError, ValueError):
        return None
