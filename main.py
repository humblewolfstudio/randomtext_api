from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from generateText import generateText
from fastapi.openapi.utils import get_openapi
from fastapi import status, HTTPException

app = FastAPI()

@app.get("/", response_class=RedirectResponse, include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')

@app.get("/getRandomText", tags=["Main API"], openapi_extra={
    "requestBody": {
        "content": {
            "application/json": {
                "schema": {
                    "required": ["nPhrases", "lan"],
                    "type": "object",
                    "properties": {
                        "nPhrases": {"type": "number"},
                        "lan": {"type": "string"},
                    }
                }
            }
        },
        "required": True,
    }}, 
    responses={200: {"content": {"application/json": {"example": ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla blandit risus vel lorem vulputate, vitae porttitor orci viverra. Fusce vitae consectetur arcu."]}}}, 500:{"content": {"application/json": {"example": {"detail":"Some values are incorrect (nPhrases is a Number and lan is a supported ISO language codes)"}}}}})
def getRandomText(nPhrases: int, lan:str):
    code, response = generateText(nPhrases, lan)
    if(code != 200):
        raise HTTPException(
            status_code=code,
            detail=response
        )
    else:
        return {response}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="RandomTextGenerator",
        version="0.1.0",
        description="Generate a random text (Lorem Ipsum-inspired) in any language supported by the ISO language codes",
        routes=app.routes,
        tags=[{"name": "Main API", "desciprion": "Main functions of this API"}]
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi