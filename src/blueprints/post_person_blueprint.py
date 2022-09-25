import json
from quart import Blueprint, Response, request
from shered.models.person_model import PersonModel

post_person_blueprint = Blueprint('post_person', __name__,)


def data_validation(data: dict, signature: dict) -> dict:
    errors = []

    for prop in signature.keys():
        if prop not in data.keys():
            errors.append('Has not ' + prop+'!')
        elif type(data[prop]) != signature[prop]:
            errors.append('Bad type for ' + prop)
        elif type(data[prop]) == str and len(data[prop]) > 255:
            errors.append('Max len of ' + prop + ' is 255!')

    if len(data) > len(signature):
        errors.append('To much data!')

    return {'error'+str(i): error for i, error in enumerate(errors)}


@post_person_blueprint.route('/api/v1/persons', methods=['POST'])
async def post_person() -> Response:
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
            person = PersonModel.create(
                person_name=person_data['name'],
                person_age=person_data['age'],
                person_address=person_data['address'],
                person_work=person_data['work']

            )
        except Exception as e:
            person = None
            errors = {'error': 'BD is dead'}

        if person is not None:
            return Response(
                status=201,
                headers={
                    'Content-Type': 'application/json',
                    'Location': '/person/' + str(person.person_id)
                },
            )

    return Response(
        status=400,
        content_type='application/json',
        response=json.dumps({
            'message': 'Error',
            'errors': errors
        })
    )