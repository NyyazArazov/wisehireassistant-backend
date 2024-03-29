import json
import os
from mongoengine import connect
from gridfs import GridFS
from model.candidate import DynamicCandidate, Education, Experience, Skills

connect(host=os.environ.get('MONGO_URI'))

# Create a GridFS instance
fs = GridFS(DynamicCandidate._get_db())

# Funtion that saves candidate
def save_candidate(candidate_info):
    if not isinstance(candidate_info, dict):
        candidate_data = json.loads(candidate_info)
    else:
        candidate_data = candidate_info
    candidate_name = candidate_data.get('Name')
    if not candidate_name:
        raise ValueError("Candidate name has not specified.")
    candidate = DynamicCandidate(Name=candidate_name)    
    # Experience
    for exp in candidate_data.get('Experience', []):
        experience = Experience(
            Company=exp.get('Company', ''),
            Location=exp.get('Location', ''),
            Position=exp.get('Position', 'Bilinmiyor'),
            Duration=exp.get('Duration', 'Bilinmiyor'),
            Responsibilities=exp.get('Responsibilities', [])
        )
        candidate.Experience.append(experience)  # Listeye ekle
    # Education
    for ed in candidate_data.get('Education', []):
        education = Education(
            University=ed.get('University', ''),
            Location=ed.get('Location', ''),
            Degree=ed.get('Degree', 'Bilinmiyor'),
            Duration=ed.get('Duration', 'Bilinmiyor'),
            GPA=ed.get('GPA', 'Bilinmiyor')
        )
        candidate.Education.append(education)  # Listeye ekle
    # Skills
    skills_data = candidate_data.get('Skills', {})
    skills = Skills(
        Programming_Languages=skills_data.get('Programming Languages', []) if isinstance(skills_data.get('Programming Languages'), list) else [],
        Frontend_Technologies=skills_data.get('Frontend Technologies', []) if isinstance(skills_data.get('Frontend Technologies'), list) else [],
        Backend_Technologies=skills_data.get('Backend Technologies', []) if isinstance(skills_data.get('Backend Technologies'), list) else [],
        Operating_Systems=skills_data.get('Operating Systems', []) if isinstance(skills_data.get('Operating Systems'), list) else [],
        Databases=skills_data.get('Databases', []) if isinstance(skills_data.get('Databases'), list) else [],
        Other=skills_data.get('Other', []) if isinstance(skills_data.get('Other'), list) else [],
    )
    candidate.Skills = skills
    # Inserts candidate
    candidate.save()

    return True

# Funtion that gets candidate
def get_candidate(candidate_id):
    candidate = DynamicCandidate.objects.get(id=candidate_id)
    candidate_obj = fs.get(candidate.id)

    return candidate_obj
