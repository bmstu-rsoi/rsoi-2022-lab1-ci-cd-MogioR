import os

from quart import Quart
from blueprints.get_persons_blueprint import get_persons_blueprint
from blueprints.get_person_blueprint import get_person_blueprint
from blueprints.post_person_blueprint import post_person_blueprint
from blueprints.delete_person_blueprint import delete_person_blueprint
from blueprints.patch_person_blueprint import patch_person_blueprint

app = Quart(__name__)
app.register_blueprint(get_persons_blueprint)
app.register_blueprint(get_person_blueprint)
app.register_blueprint(post_person_blueprint)
app.register_blueprint(delete_person_blueprint)
app.register_blueprint(delete_person_blueprint)
app.register_blueprint(patch_person_blueprint)

port = os.environ.get('PORT')
if port is None:
    port = 8080

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))
