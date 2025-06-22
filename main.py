import uvicorn
from fastapi import FastAPI, Request, Depends, Security, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException

from utils.config import API_NAME, API_KEY
from utils.models import S2RRequest, S2RResponse
from pipelines import assistant_pipeline

app = FastAPI(
    title=API_NAME,
    description="Get auto-generated reports from images.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="static")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key"
    )

@app.get("/robots.txt", include_in_schema=False)
async def get_robots_txt():
    return FileResponse("static/robots.txt", media_type="text/plain")

@app.get("/", tags=["Index"], response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ping", tags=["Health"])
def ping():
    return {"message": f"{API_NAME} is alive!"}

@app.post("/generate-report", tags=["Pipeline"], response_model=S2RResponse)
async def process(
    file: str = Form(..., description="The image file to process"),
    latitude: float = Form(..., description="The latitude of the location"),
    longitude: float = Form(..., description="The longitude of the location"),
    api_key: str = Depends(get_api_key)
):
    request = S2RRequest(file=file, latitude=latitude, longitude=longitude)

    report = assistant_pipeline(request)

    return S2RResponse(report=report)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)