import os
import joblib
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

MODEL_PATH = os.path.join(os.path.dirname(__file__), "sentiment_model.joblib")

def train_and_save_model():
    print("Loading IMDB dataset...")
    # Using IMDB reviews dataset
    dataset = load_dataset("stanfordnlp/imdb")
    
    # We will use the training set
    train_texts = dataset['train']['text']
    train_labels = dataset['train']['label'] # 0 for neg, 1 for pos
    
    # To save time and memory for this demonstration, we can use a subset or the full dataset
    # We'll just use the full train split for decent accuracy
    
    print("Training TF-IDF + Logistic Regression pipeline...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=10000, stop_words='english')),
        ('clf', LogisticRegression(max_iter=1000))
    ])
    
    pipeline.fit(train_texts, train_labels)
    
    # Evaluate on test set
    print("Evaluating model...")
    test_texts = dataset['test']['text']
    test_labels = dataset['test']['label']
    predictions = pipeline.predict(test_texts)
    
    print(f"Accuracy: {accuracy_score(test_labels, predictions)}")
    print(classification_report(test_labels, predictions))
    
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(pipeline, MODEL_PATH)
    print("Done!")

if __name__ == "__main__":
    train_and_save_model()
