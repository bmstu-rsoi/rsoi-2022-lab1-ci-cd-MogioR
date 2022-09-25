import json
from quart import Blueprint, Response
from shered.models.person_model import PersonModel

get_persons_blueprint = Blueprint('get_persons', __name__,)


@get_persons_blueprint.route('/api/v1/persons', methods=['GET'])
async def get_persons() -> Response:
    query = PersonModel.select()
    persons = [q.as_dict() for q in query]

    return Response(
        status=200,
        content_type='application/json',
        response=json.dumps(persons)
    )
