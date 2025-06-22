from pydantic import BaseModel, Field

class S2RResponse(BaseModel):
    report: str = Field(..., description="The generated report")
    
class S2RRequest(BaseModel):
    file: str = Field(..., description="The image file to process")
    latitude: float = Field(..., description="The latitude of the location")
    longitude: float = Field(..., description="The longitude of the location")

class ReportOutput(BaseModel):
    title: str = Field(..., description="A short title for the report")
    category: str = Field(..., description="The category returned by the Get Category Tool")
    location: str = Field(..., description="The location where the issue was observed.")
    description: str = Field(..., description="A detailed description of the issue")
    impact: str = Field(..., description="A few sentences identifying the most likely direct effects on residents, pedestrians, or city services. Focus on realistic, immediate concerns rather than hypothetical worst-case scenarios")

class ReportObject(BaseModel):
    latitude: float = Field(..., description="The latitude of the location")
    longitude: float = Field(..., description="The longitude of the location")
    address: str = Field(..., description="The address of the location")
    category: str = Field(..., description="The category of the location")
    caption: str = Field(..., description="The caption of the location")
    annotated_image_url: str = Field(..., description="The annotated image url")
