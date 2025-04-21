# 🧠 PII-Safe Email Classifier API

A FastAPI backend that classifies support emails using `SBERT + SVM`, while safely masking and restoring personally identifiable information (PII) using `regex` and `SpaCy` NER.

---

## 🔧 Tech Stack

- **FastAPI** – Lightweight REST API backend
- **SBERT (MiniLM-L6-v2)** – Sentence embeddings
- **Linear SVM** – Email classification
- **Regex + SpaCy** – PII detection & masking
- **Joblib** – Model persistence
- **Uvicorn** – ASGI server

---

## ⚙️ How It Works

1. Accepts raw email text (`email_body`)
2. Detects and masks PII using regex and NER
3. Classifies the masked email into 1 of 4 categories:
   - `Incident`, `Request`, `Problem`, `Change`
4. Gives the position of the entity like email position,full_name position etc.
5. Demasks PII for final response
6. Returns output in strict JSON schema

---

## ⚙️ How to work(Using Swagger UI)
1. Use this url "https://supreetha15-pii-safe-classifier.hf.space/docs"
2. This will redirect to Swagger UI.
3. Use POST and the route by default will be /classify.
4. Check on Try Out to to evaluate the API bu giving a raw email text in email_body
5. Click execute to run the API and fetch the result.

## Other Evaluation methods
1. Use this url "https://supreetha15-pii-safe-classifier.hf.space/classify"
2. Go to POSTMAN and set request to POST
3. In body select raw and type as JSON and provide a raw email text as {"email_body":"string"}
4. Send the request in order to get the API response
5. Other Equivalent method can be using curl.
