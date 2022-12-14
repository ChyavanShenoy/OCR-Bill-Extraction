from http import client
from os import environ
# from pydantic import BaseModel, Field
from fastapi import FastAPI, Body
import utils.fileops as fileops
import prediction_machine as pm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# on startup event delet files inside temp_files folder


@app.on_event("startup")
async def startup_event():
    fileops.delete_files()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/bill")
# def detect_bill(image_location: ImgLoc = Body(embed=True)):
def detect_bill(image_data: str = Body(..., embed=True)):
    print("-----------------")
    print(image_data)
    print("-----------------")
    image = fileops.base64_to_image(image_data)
    file_name = fileops.write_image_to_file(image)
    result, synth_image = pm.predict(file_name)
    synth_image_base64 = fileops.image_to_base64(synth_image)
    return {
        "synth_image": synth_image_base64,
        "result": result,
    }


def main():
    import uvicorn
    # use uvicorn to run the app at env:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # use uvicorn to run the app at environment port
    # port=environ.get("PORT", 8080)
    # print("port: ", port)


if __name__ == "__main__":
    main()
