from pydantic import BaseModel, Field
from fastapi import FastAPI, Body
import utils.fileops as fileops
import prediction_machine as pm
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImgLoc(BaseModel):
    # image_data: str = Field(description="Path to the image")
    image_data: str

    # def __getitem__(self, item):
    #     return getattr(self, item)


# on startup event delet files inside temp_files folder
@app.on_event("startup")
async def startup_event():
    fileops.delete_files()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/bill")
def detect_bill(image_location: ImgLoc = Body(embed=True)):
    image = fileops.base64_to_image(image_location.image_data)
    file_name = fileops.write_image_to_file(image)
    result, synth_image = pm.predict(file_name)
    synth_image_base64 = fileops.image_to_base64(synth_image)
    return {
        "synth_image": synth_image_base64,
        "result": result,
    }
