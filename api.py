# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import SBERT_SVM_Classifier
from utils import mask_pii, demask
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="PII-Safe Email Classifier",
    version="1.0",
    description="An API that masks PII, classifies emails, and returns demasked results."
)

# Load trained classifier
classifier = SBERT_SVM_Classifier()
classifier.load("sbert_linear_model.joblib")


class EmailRequest(BaseModel):
    """
    Request schema: expects raw email body.
    """
    email_body: str


@app.post("/classify")
def classify_email(request: EmailRequest):
    """
    API endpoint: Mask PII, classify masked email,
    then return demasked result in strict format.
    """
    try:
        raw_email = request.email_body

        # Step 1: Mask PII
        masked_email, entities = mask_pii(raw_email)

        # Step 2: Classify masked content
        predicted_category = classifier.predict([masked_email])[0]

        # Step 3: Demask to restore PII
        demasked_email = demask(masked_email, entities)

        # Step 4: Return strict JSON format
        return {
            "input_email_body": raw_email,
            "list_of_masked_entities": entities,
            "masked_email": masked_email,
            "category_of_the_email": predicted_category
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#  Run locally: uvicorn api:app --reload
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
