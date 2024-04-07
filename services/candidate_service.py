import json
import os
from mongoengine import connect
from gridfs import GridFS
from model.candidate import DynamicCandidate, Education, Experience, Skills

connect(host=os.environ.get('MONGO_URI'))

# Create a GridFS instance
fs = GridFS(DynamicCandidate._get_db())


# Function that saves candidate
def save_candidate(candidate_info):
    if not isinstance(candidate_info, dict):
        candidate_data = json.loads(candidate_info)
    else:
        candidate_data = candidate_info
    candidate_name = candidate_data.get('name')
    if not candidate_name:
        raise ValueError("Candidate name has not specified.")
    candidate = DynamicCandidate(name=candidate_name)
    # Experience
    for exp in candidate_data.get('experience', []):
        experience = Experience(
            company=exp.get('company', ''),
            location=exp.get('location', ''),
            position=exp.get('position', 'Bilinmiyor'),
            duration=exp.get('duration', 'Bilinmiyor'),
            responsibilities=exp.get('responsibilities', [])
        )
        candidate.experience.append(experience)  # Listeye ekle
    # Education
    for ed in candidate_data.get('education', []):
        education = Education(
            university=ed.get('university', ''),
            location=ed.get('location', ''),
            degree=ed.get('degree', 'Bilinmiyor'),
            duration=ed.get('duration', 'Bilinmiyor'),
            GPA=ed.get('GPA', 'Bilinmiyor')
        )
        candidate.education.append(education)  # Listeye ekle

    # Skills
    skills_data = candidate_data.get('skills', None)
    if isinstance(skills_data, list):
        skills = Skills(
            skills=skills_data,
            other=[]
        )
    elif isinstance(skills_data, dict):
        skills = Skills(
            skills=skills_data.get('skills', []),
            other=skills_data.get('other', [])
        )
    else:
        # Handle other cases accordingly, such as raising an error or setting default values
        skills = Skills(skills=[], other=[])

    candidate.Skills = skills
    # Inserts candidate
    candidate.save()

    return True


# Funtion that gets candidate
def get_candidate(candidate_id):
    candidate = DynamicCandidate.objects.get(id=candidate_id)
    candidate_obj = fs.get(candidate.id)

    return candidate_obj
