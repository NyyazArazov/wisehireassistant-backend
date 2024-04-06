import os
from mongoengine import connect
from gridfs import GridFS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from model.candidate import DynamicCandidate
from model.position import Position
from model.similarity_score import SimilarityScore

connect(host=os.environ.get('MONGO_URI'))

# Creates a GridFS instance
fs = GridFS(DynamicCandidate._get_db())

# Funtion that saves similarity_score
def save_similarity_score(similarity_score, candidate_id, position_id):
    try:
        # Creates new similarity_score
        similarity_score = SimilarityScore(
            candidate_id=candidate_id,
            position_id=position_id,
            similarity_score=similarity_score,
        )        
        # Inserts similarity_score
        similarity_score.save()
        
        return {'success': True, 'message': 'Similarity score has saved successfully.'}
    except Exception as e:
        return {'success': False, 'message': f'An error occurred while saving the similarity score: {str(e)}'}

# Funtion that gets similarity_score    
def get_similarity_score(similarity_score_id):
    similarity_score = SimilarityScore.objects.get(id=similarity_score_id)
    similarity_score_obj = fs.get(similarity_score.id)

    return similarity_score_obj

# Funtion that calculates similarity_score    
def calculate_similarity_score(candidate_id, position_id):    
    candidate = DynamicCandidate.objects(id=candidate_id).first()
    position = Position.objects(id=position_id).first()
    texts = [candidate.to_json(), position.to_json()]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return cosine_sim[0][0], None 
