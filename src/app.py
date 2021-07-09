import os
import sys

from components.Logger import Logger
from flask import Flask, abort, request, make_response
from services.EmbeddingsService import EmbeddingsService
from services.QueryService import QueryService


app = Flask(__name__)
logger = Logger('app')


@app.route('/api/class_embeddings', methods=['GET'])
def gen_class_entities_embeddings():
    class_ = request.args.get('class')
    source = request.args.get('source')
    sg = int(request.args.get('sg', 1))
    walk_strategy = request.args.get('walk_strategy', 'rw')
    limit = int(request.args.get('limit', None))
    v_size = int(request.args.get('v_size', 100))
    depth = int(request.args.get('depth', 4))
    walks_per_graph = int(request.args.get('n_walks', 25))

    entities = QueryService.get_class_enttities(source, class_, limit)

    embeddings = EmbeddingsService.gen_embeddings(source=source, entities=entities,
                                                  sg=sg, walk_strategy=walk_strategy,
                                                  v_size=v_size, depth=depth,
                                                  walks_per_graph=walks_per_graph)

    return {
        'entities': entities,
        'embeddings': embeddings
    }


@app.route('/api/up', methods=['GET'])
def up():
    return {'msg': 'ok'}


def main(*args):

    if len(args) == 1:
        myhost = args[0]
    else:
        myhost = "0.0.0.0"

    debug = os.environ.get('APP_DEBUG', 'true').lower() == 'true'
    app.run(debug=debug, host=myhost, port=5000)


if __name__ == '__main__':
    main(*sys.argv[1:])