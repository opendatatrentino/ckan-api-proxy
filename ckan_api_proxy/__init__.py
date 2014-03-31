import flask

app = flask.Flask(__name__)


@app.route('/dataset')
def get_dataset_list():
    pass


@app.route('/dataset', methods=['POST'])
def post_dataset():
    pass


@app.route('/dataset/<dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    pass


@app.route('/dataset/<dataset_id>', methods=['PUT'])
def put_dataset(dataset_id):
    pass


@app.route('/dataset/<dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    pass


@app.route('/dataset/<dataset_id>/resources', methods=['GET'])
def get_dataset_resources(dataset_id):
    pass


@app.route('/dataset/<dataset_id>/resources', methods=['POST'])
def post_dataset_resources(dataset_id):
    pass
