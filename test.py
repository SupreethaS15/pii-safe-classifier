# test_model.py
from models import SBERT_SVM_Classifier
from utils import mask_pii, demask
import json

# Load trained model
model = SBERT_SVM_Classifier()
model.load("sbert_linear_model.joblib")


def classify_email(raw_email: str) -> dict:
    # 1. Mask PII
    masked_email, entities = mask_pii(raw_email)

    # 2. Predict category using masked email
    predicted_category = model.predict([masked_email])[0]

    # 3. Demask to restore original
    demasked_email = demask(masked_email, entities)

    # 4. Return formatted output
    return {
        "input_email_body": raw_email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": predicted_category
    }


# 🔬 Test sample
if __name__ == "__main__":
    email_text = "Subject: John Doe's Aadhar number is 1234-5678-9012 and email is johnd@example.com. Need access to billing portal."
    result = classify_email(email_text)
    print(json.dumps(result, indent=2))
