from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def bert_similarity(text1, text2):
    try:
        if not text1.strip() or not text2.strip():
            return 0.0

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text1, text2])

        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

        return score

    except Exception as e:
        print("Similarity Error:", e)
        return 0.0