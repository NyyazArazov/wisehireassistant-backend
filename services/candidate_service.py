import json
import os
from mongoengine import connect
from gridfs import GridFS
from model.candidate import DynamicCandidate, Experience

connect(host=os.environ.get('MONGO_URI'))

# Create a GridFS instance
fs = GridFS(DynamicCandidate._get_db())


# Function that saves candidate
def save_candidate(candidate_json):
    # Load JSON data
    candidate_data = json.loads(candidate_json)
    name = candidate_data.get('name', '')
    university = candidate_data.get('university', '')
    degree = candidate_data.get('degree', '')
    skills = candidate_data.get('skills', [])
    experiences_data = candidate_data.get('experience', [])

    experiences = []
    for exp_data in experiences_data:
        title = exp_data.get('title', '')
        company = exp_data.get('company', '')
        experience = Experience(title=title, company=company)
        experiences.append(experience)

    # Create candidate document
    candidate = DynamicCandidate(
        name=name,
        university=university,
        degree=degree,
        skills=skills,
        experience=experiences
    )

    # Save candidate to MongoDB
    candidate.save()

    return True


# Funtion that gets candidate
def get_candidate(candidate_id):
    candidate = DynamicCandidate.objects.get(id=candidate_id)
    candidate_obj = fs.get(candidate.id)

    return candidate_obj
