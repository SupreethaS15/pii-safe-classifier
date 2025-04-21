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

## 🔌 API Overview
**Framework**: FastAPI
**Main file**: api.py
**Model**: SBERT encoder + Linear SVM loaded via models.py
**PII masking**: Done in utils.py using regex & SpaCy
**Entry point**: app.py (used for Hugging Face Spaces or Docker)

---
## ☁️ Hugging Face Spaces Deployment
1.Create a Space and choose Docker as the SDK.
2.Upload all project files:
   `app.py, api.py, models.py, utils.py`
   `requirements.txt`
   `Dockerfile`
   `README.md`
   `sbert_linear_model.joblib`
Space will build automatically and give the following link:
https://<space-name>.hf.space/docs
Use Swagger UI or curl to test live requests.

---
## 📚 Module Documentation
Module | Purpose
1.`app.py` | Hugging Face Spaces entry point; exposes FastAPI app instance from api.py.
2.`api.py` | FastAPI route /classify for processing incoming emails: masks PII, classifies, and demasks.
3.`models.py` | Contains SBERT_SVM_Classifier class: training, saving, loading, and predicting using SBERT + SVM.
4.`utils.py` | Implements mask_pii() and demask() using advanced regex and SpaCy for secure entity handling.
5.`requirements.txt` | Python dependencies required to run the application (locally or in Hugging Face Space).
6.`Dockerfile` | Containerization file to deploy the API using Hugging Face's Docker SDK or locally with Docker.
7.`README.md` | Complete setup guide, documentation, deployment steps, and test instructions.
8.`sbert_linear_model.joblib` | Serialized classifier model file (must be pre-trained and included for prediction).

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
3. In body select raw JSON and provide a raw email text as {"email_body":"string"}
4. Send the request in order to get the API response
5. Other Equivalent method can be using curl.
