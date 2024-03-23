from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(file1_path, file2_path):
    
    # Reads files
    with open(file1_path, 'r', encoding='utf-8') as file:
        text1 = file.read()
    with open(file2_path, 'r', encoding='utf-8') as file:
        text2 = file.read()

    # Creates TF-IDF vectors
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([text1, text2])

    # Calculates cosine similarity 
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return cosine_sim[0][0]

# Indicates file paths
file1_path = 'file1.txt'
file2_path = 'file2.txt'

# Calculates similarity score and prints 
similarity_score = calculate_similarity(file1_path, file2_path)
print("Cosine Similarity Score:", similarity_score)