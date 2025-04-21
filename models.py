# models.py

from sentence_transformers import SentenceTransformer
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump, load
import pandas as pd
import re


class SBERT_SVM_Classifier:
    """
    SBERT + Linear SVM classifier for email subject classification.
    """

    def __init__(self, model_name="paraphrase-MiniLM-L6-v2"):
        """
        Initialize sentence transformer and SVM model.
        """
        self.encoder = SentenceTransformer(model_name)
        self.label_encoder = LabelEncoder()
        self.model = LinearSVC(C=1.0)

    def preprocess(self, text):
        """
        Lowercase and clean subject prefix.
        """
        text = text.lower()
        return re.sub(r'^subject:\s*', '', text.strip())

    def train(self, csv_path):
        """
        Train model on email dataset.
        """
        df = pd.read_csv(csv_path)
        df['email'] = df['email'].apply(self.preprocess)

        X = df['email'].tolist()
        y = self.label_encoder.fit_transform(df['type'].tolist())

        print("[*] Generating sentence embeddings...")
        X_embed = self.encoder.encode(
            X,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        print("[*] Training Linear SVM (FAST mode)...")
        self.model.fit(X_embed, y)

        # Optional evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            X_embed, y, test_size=0.2, random_state=42
        )
        y_pred = self.model.predict(X_test)
        print(
            classification_report(
                y_test,
                y_pred,
                target_names=self.label_encoder.classes_
            )
        )

    def predict(self, email_texts):
        """
        Predict category for list of email strings.
        """
        emails = [self.preprocess(e) for e in email_texts]
        X = self.encoder.encode(emails, convert_to_numpy=True)
        y_pred = self.model.predict(X)
        return self.label_encoder.inverse_transform(y_pred)

    def save(self, path="sbert_linear_model.joblib"):
        """
        Save model + label encoder to disk.
        """
        dump((self.model, self.label_encoder), path)

    def load(self, path="sbert_linear_model.joblib"):
        """
        Load model + label encoder from disk.
        """
        self.model, self.label_encoder = load(path)
