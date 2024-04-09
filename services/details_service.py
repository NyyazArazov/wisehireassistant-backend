import os
from flask import jsonify
from mongoengine import connect
from gridfs import GridFS
from model.details import Details

connect(host=os.environ.get('MONGO_URI'))

# Create a GridFS instance
fs = GridFS(Details._get_db())

# Funtion that saves details
def save_details(resume_json, position_id, similarityResponse):
    try:
        # Creates new details
        details = Details(
            name = resume_json.get('name'),
            rank = str(similarityResponse.get('similarity_score')),
            consistency = resume_json.get('consistency'),
            position_id = position_id
        )
        # Inserts details
        details.save()
        
        return {'success': True, 'message': 'Details has saved successfully.'}
    except Exception as e:
        return {'success': False, 'message': f'An error occurred while saving the details: {str(e)}'}

# Funtion that gets details      
def get_details_byPositionId(position_id):
    details = Details.objects.get(position_id=position_id)
    details_obj = fs.get(position_id)

    return details_obj

# Funtion that gets all details of db of given position_id
def get_all_details(position_id):
    try:
        # Gets all details from the database
        details_list = Details.objects.filter(position_id=position_id)
        print(details_list)
        details_json = []

        # Check if details_list is empty
        if not details_list:
            # If details_list is empty, append a default object with "empty" strings
            details_json.append({
                'name': "empty",
                'rank': "empty",
                'consistency': "empty",
                'position_id': "empty",
                'file': "empty"
            })
        else:
            for details in details_list:
                detail = {
                    'name': details.name if details.name else "empty",
                    'rank': str(details.rank) if details.rank else "empty",
                    'consistency': details.consistency if details.consistency else "empty",
                    'position_id': position_id
                }
                # Assuming fs is a file storage system you've set up
                if fs.exists(position_id):
                    details_obj = fs.get(position_id)
                    detail['file'] = details_obj.read() if details_obj.read() else "empty"
                details_json.append(detail)

        return jsonify({'success': True, 'details': details_json})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500