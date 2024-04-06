import os
from flask import jsonify
from mongoengine import connect
from gridfs import GridFS
from model.position import Position

connect(host=os.environ.get('MONGO_URI'))

# Create a GridFS instance
fs = GridFS(Position._get_db())

# Funtion that saves position
def save_position(position_info):
    try:
        # Creates new position
        position = Position(
            companyName=position_info.get('companyName'),
            jobTitle=position_info.get('jobTitle'),
            salary=position_info.get('salary'),
            jobDescription=position_info.get('jobDescription')
        )
        # Inserts position
        position.save()
        
        return {'success': True, 'message': 'Position has saved successfully.'}
    except Exception as e:
        return {'success': False, 'message': f'An error occurred while saving the position: {str(e)}'}

# Funtion that gets position      
def get_position(position_id):
    position = Position.objects.get(id=position_id)
    position_obj = fs.get(position.id)

    return position_obj

# Funtion that deletes position  
def delete_position(position_id):
    try:
        # Deletes position of given id
        position = Position.objects.get(id=position_id)
        position.delete()

        return {'success': True, 'message': 'Position has deleted successfully.'}
    except Position.DoesNotExist:
        return {'success': False, 'message': 'Position has not found.'}
    except Exception as e:
        return {'success': False, 'message': f'An error occurred while deleting the position: {str(e)}'}

# Funtion that gets all position of db
def get_all_positions():
    try:
        # Gets all positions of db
        positions = Position.objects.all()
        positions_json = []
        for position in positions:
            position_json = {
                'id': str(position.id),  
                'companyName': position.companyName,
                'jobTitle': position.jobTitle,
                'salary': position.salary,
                'jobDescription': position.jobDescription,
            }
            if fs.exists(position.id):
                position_obj = fs.get(position.id)
                position_json['file'] = position_obj.read()  
            positions_json.append(position_json)
        
        return jsonify({'success': True, 'positions': positions_json})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500