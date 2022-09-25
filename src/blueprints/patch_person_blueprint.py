import json
from quart import Blueprint, Response, request
from shered.models.person_model import PersonModel

patch_person_blueprint = Blueprint('patch_person', __name__,)


def data_validation(data: dict, signature: dict) -> dict:
    errors = []

    for prop in signature.keys():
        if prop in data.keys():
            if type(data[prop]) != signature[prop]:
                errors.append('Bad type for ' + prop)
            elif type(data[prop]) == str and len(data[prop]) > 255:
                errors.append('Max len of ' + prop + ' is 255!')

    if len(data) > len(signature):
        errors.append('To much data!')

    return {'error'+str(i): error for i, error in enumerate(errors)}


@patch_person_blueprint.route('/api/v1/persons/<int:person_id>', methods=['PATCH'])
async def patch_person_person(person_id: int) -> Response:
    if request.is_json:
        person_data = await request.get_json()
        try:
            errors = data_validation(person_data, PersonModel.get_signature())
        except:
            errors = {
                'error': 'Bad JSON'
            }
    else:
        errors = {
            'error': 'Bad JSON'
        }

    if len(errors) == 0:
        try:
            person = PersonModel.select().where(PersonModel.person_id == person_id).get()
            if 'name' in person_data.keys():
                person.person_name = person_data['name']
            if 'age' in person_data.keys():
                person.person_age = person_data['age']
            if 'address' in person_data.keys():
                person.person_address = person_data['address']
            if 'work' in person_data.keys():
                person.person_work = person_data['work']
            person.save()
        except PersonModel.DoesNotExist:
            person = None

        if person is not None:
            return Response(
                status=200,
                content_type='application/json',
                response=json.dumps(person.as_dict())
            )
        else:
            return Response(
                status=404,
                content_type='application/json',
                response=json.dumps({
                    'message': 'Not found Person for ID'
                })
            )

    return Response(
        status=400,
        content_type='application/json',
        response=json.dumps({
            'message': 'Error',
            'errors': errors
        })
    )