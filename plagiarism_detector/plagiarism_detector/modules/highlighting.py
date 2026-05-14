from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def highlight_sentences(text1, text2):
    sentences1 = text1.split('.')
    sentences2 = text2.split('.')

    matches = []

    for s1 in sentences1:
        for s2 in sentences2:
            if s1.strip() and s2.strip():

                vectorizer = TfidfVectorizer(ngram_range=(1,2))
                vectors = vectorizer.fit_transform([s1, s2])

                score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

                if score > 0.3:
                    matches.append((s1.strip(), s2.strip(), round(score, 2)))

    return matches