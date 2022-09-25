from quart import Blueprint, Response
from shered.models.person_model import PersonModel

delete_person_blueprint = Blueprint('delete_person', __name__,)


@delete_person_blueprint.route('/api/v1/persons/<int:person_id>', methods=['DELETE'])
async def delete_person(person_id: int) -> Response:
    try:
        PersonModel.get(PersonModel.person_id == person_id).delete_instance()
    except PersonModel.DoesNotExist:
        pass

    return Response(
        status=204
        # content_type='application/json',
        # response=json.dumps({
        #     'message': 'Not found Person for ID'
        # })
    )