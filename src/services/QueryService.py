from flask import abort
import json
import requests
from components.Logger import Logger

logger = Logger('QueryService')


class QueryService:
    # To add support to more endpoints, add here:
    endpoints = {
        'wikidata': 'https://query.wikidata.org/sparql',
        'dbpedia': 'https://dbpedia.org/sparql',
        'tib-dbpedia': 'http://node1.research.tib.eu:4001/sparql',
        'tib-wikidata': 'http://node3.research.tib.eu:4010/sparql',
    }

    @classmethod
    def get_class_entities_query(cls, source, class_, limit=None):
        limit_str = 'LIMIT %s' % limit if limit else ''
        if 'dbpedia' in source:
            return """
            SELECT DISTINCT ?entity
            WHERE {
              ?entity rdf:type ?type.
              ?type rdfs:subClassOf* <%s>.
            } %s
            """ % (class_, limit_str)
        elif 'wikidata' in source:
            return """
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>


            SELECT distinct ?entity WHERE {
                ?entity  wdt:P31*/wdt:P279* <%s>.
            } %s
            """ % (class_, limit_str)

    @classmethod
    def get_class_enttities(cls, source, class_, limit):

        endpoint = cls.endpoints[source]
        query = cls.get_class_entities_query(source, class_, limit)

        s = requests.Session()

        headers = {
            'Accept': 'application/json'
        }
        data = {'query': query}
        s.headers.update(headers)

        response = s.post(endpoint, data=data, headers=headers)

        if response.status_code != 200:
            logger.log('Query to endpoint %s, returned code %s' % (endpoint, response.status_code))
            logger.log(response.text)
            abort(400, response.text)

        content = json.loads(response.text)

        if 'results' not in content or 'bindings' not in content['results']:
            logger.log('Query for class %s returned not entities' % class_)
            abort(400)

        results = content['results']['bindings']

        entities_uris = [result['entity']['value'] for result in results]

        return entities_uris



