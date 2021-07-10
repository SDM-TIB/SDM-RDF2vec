# SDM-RDF2vec

## Setup

You must install the required libraries with pip:

`pip install -r requirements.txt`

(from src folder)

and then just executing the server as follows:

`python app.py`

### Note
For wikidata, the support of pyrdf2vec needs to be fixed, you can do this
replacing the `connectors.py` of the pyrdf2vec library you've installed
with `src/custom/connectors.py`, it will adapt the url for the endpoint
as you can see if you diff the files.

## Setup with Docker-compose

You can also use `docker-compose` to create a docker container for the 
server in an easier way:

`docker-compose up`

You don't have to care about the replacement of the `connectors.py` file
in this case, the Dockerfile will take care of it.

## Usage

You can use the `/api/class_embeddings` endpoint to obtain embeddings of 
entities from the class you want. You should also specify certain query 
parameters for the request in order to get the desired set of embeddings:

- `source`: external source to use, it will be mapped to the corresponding 
endpoint in the `EmbeddingsService.py`. Example: `dbpedia` -> `https://dbpedia.org/sparql`
- `class`: the class of the entities you are interested in. Example: `http://dbpedia.org/ontology/Organisation`
- `sg`: interger to specify if the RDF2Vec algorithm to use, use `1` for Skip-Gram Algorithm, in any
other case it will use CBOW (Continuous Bag of Words).
- `walk_strategy`: walk strategy to create the paths. Example: `rw` for `RandomWalk`.
- `v_size`: integer with vector size for each set of embeddings.
- `depth`: depth for the walks.
- `n_walks`: integer for the number of walks per graph.
- `limit`: number of entities you want to obtain that belong to the specified `class`.

### Example

With curl:
```bash
curl --request GET \
  --url 'http://localhost:5000/api/class_embeddings?source=dbpedia&class=http%3A%2F%2Fdbpedia.org%2Fontology%2FOrganisation&sg=1&walk_strategy=rw&depth=4&v_size=100&n_walks=25&limit=5'
```

In this `curl` request it will use `dbpedia` as source, will search for 5 entities belonging
to the `http://dbpedia.org/ontology/Organisation` class, will produce embeddings of size `100`
for each entity, and the Embeddings will be generated using SG algorithm, `RandomWalk` as 
walking strategy with depth `4` and `25` walks per graph.

## Supported Sources:

- `wikidata`: `https://query.wikidata.org/sparql`
- `dbpedia`: `https://dbpedia.org/sparql`
- `tib-dbpedia`: `http://node1.research.tib.eu:4001/sparql`
- `tib-wikidata`: `http://node3.research.tib.eu:4010/sparql`

## Supported Walk Strategies

- `an`: AnonymousWalk
- `ha`: HALK Walk
- `ng`: NGram Walk
- `rw`: Random Walk
- `wa`: Walklet Walk

