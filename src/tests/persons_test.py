import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import pytest
import json
from main import app
from src.shered.models.person_model import PersonModel


@pytest.mark.asyncio
async def test_post_person():
    app.config['TESTING'] = True
    test_client = app.test_client()

    responce = await test_client.post(
        '/api/v1/persons',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "name": "Homer Simpson",
            "age": 45,
            "address": "animation",
            "work": "Nuclear admin"
        })
    )
    assert responce.status_code == 201
    assert responce.headers['location'][:8] == '/person/'
    assert type(int(responce.headers['location'][8:])) is int
    person = PersonModel.get(PersonModel.person_id == int(responce.headers['location'][8:]))
    assert person.person_age == 45
    assert person.person_name == "Homer Simpson"
    assert person.person_address == "animation"
    assert person.person_work == "Nuclear admin"
    person.delete_instance()

    responce = await test_client.post(
        '/api/v1/persons',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "name": "Homer Simpson",
            "address": "animation",
            "work": "Nuclear admin"
        })
    )
    assert responce.status_code == 400


@pytest.mark.asyncio
async def test_get_person():
    app.config['TESTING'] = True
    test_client = app.test_client()

    homer = PersonModel.create(
        person_id=0,
        person_name="Homer Simpson",
        person_age=45,
        person_address="animation",
        person_work="Nuclear admin"
    )

    responce = await test_client.get(
        '/api/v1/persons/0',
    )
    homer.delete_instance()
    assert responce.status_code == 200
    assert responce.headers['Content-Type'] == 'application/json'

    responce = await test_client.get(
        '/api/v1/persons/0',
    )
    assert responce.status_code == 404


@pytest.mark.asyncio
async def test_delete_person():
    app.config['TESTING'] = True
    test_client = app.test_client()

    homer = PersonModel.create(
        person_id=0,
        person_name="Homer Simpson",
        person_age=45,
        person_address="animation",
        person_work="Nuclear admin"
    )

    responce = await test_client.delete(
        '/api/v1/persons/0',
    )
    assert responce.status_code == 204

    responce = await test_client.delete(
        '/api/v1/persons/0',
    )
    assert responce.status_code == 204


@pytest.mark.asyncio
async def test_patch_person():
    app.config['TESTING'] = True
    test_client = app.test_client()

    homer = PersonModel.create(
        person_id=0,
        person_name="Homer Simpson",
        person_age=45,
        person_address="animation",
        person_work="Nuclear admin"
    )

    responce = await test_client.patch(
        '/api/v1/persons/0',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "name": "Homer Clinton",
        })
    )

    homer.delete_instance()
    assert responce.status_code == 200

    responce = await test_client.patch(
        '/api/v1/persons/0',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "name": "Homer Clinton",
        })
    )
    assert responce.status_code == 404
