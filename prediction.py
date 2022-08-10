import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


class Predictor:
    def __init__(self):
        self.data = pd.read_csv("data/intents.csv")
        self.train()

    def train(self):
        X_train, y_train = self.data["intent"], self.data["response"]
        self.count_vect = CountVectorizer()
        X_train_counts = self.count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        self.clf = MultinomialNB().fit(X_train_tfidf, y_train)

    def predict(self, text):
        return self.clf.predict(self.count_vect.transform([text]))[0]


if __name__ == "__main__":
    print("started...")
    predictor = Predictor()

    while True:
        resp = predictor.predict(input(">>>>>\t"))
        print(resp)
