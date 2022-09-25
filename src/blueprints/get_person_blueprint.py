import json
from quart import Blueprint, Response
from shered.models.person_model import PersonModel

get_person_blueprint = Blueprint('get_person', __name__,)


@get_person_blueprint.route('/api/v1/persons/<int:person_id>', methods=['GET'])
async def get_person(person_id: int) -> Response:
    try:
        person = PersonModel.select().where(PersonModel.person_id == person_id).get()
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
