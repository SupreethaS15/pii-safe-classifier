from models import SBERT_SVM_Classifier

model = SBERT_SVM_Classifier()
model.train("combined_emails_with_natural_pii.csv")
model.save()
