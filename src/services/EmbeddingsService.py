from typing import List, Sequence

from pyrdf2vec import RDF2VecTransformer
from pyrdf2vec.embedders import Word2Vec
from pyrdf2vec.graphs import KG
from pyrdf2vec.samplers import PageRankSampler, UniformSampler
from pyrdf2vec.walkers import AnonymousWalker, Walker, CommunityWalker, \
    HALKWalker, NGramWalker, RandomWalker, WalkletWalker
import rdflib

from components.Logger import Logger

logger = Logger('EmbeddingsService')


class EmbeddingsService:

    # To add support to more endpoints, add here:
    endpoints = {
            'wikidata': 'https://query.wikidata.org/sparql',
            'dbpedia': 'https://dbpedia.org/sparql',
            'tib-dbpedia': 'http://node1.research.tib.eu:4001/sparql',
            'tib-wikidata': 'http://node3.research.tib.eu:4010/sparql',
        }

    walkers = ['an', 'ha', 'ng', 'rw', 'wa']

    @staticmethod
    def get_walker(sampler_id, walk_strategy, depth, walks_per_graph):
        sampler = None
        if sampler_id == 'uniform':
            sampler = UniformSampler()

        walkers = None
        if walk_strategy == 'an':
            walkers = [AnonymousWalker(depth, walks_per_graph, sampler)]
        elif walk_strategy == 'ha':
            walkers = [HALKWalker(depth, walks_per_graph, sampler)]
        elif walk_strategy == 'ng':
            walkers = [NGramWalker(depth, walks_per_graph, sampler)]
        elif walk_strategy == 'rw':
            walkers = [RandomWalker(depth, walks_per_graph, sampler)]
        elif walk_strategy == 'wa':
            walkers = [WalkletWalker(depth, walks_per_graph, sampler)]

        return walkers

    @staticmethod
    def create_embeddings(
            kg: KG,
            entities: List[rdflib.URIRef],
            walkers: Sequence[Walker],
            sg: int = 1,
            v_size: int = 100
    ) -> List[str]:
        """Creates embeddings for a list of entities according to a knowledge
        graphs and a walking strategy.
        Args:
            kg: The knowledge graph.
                The graph from which the neighborhoods are extracted for the
                provided instances.
            entities: The train and test instances to create the embedding.
            walkers: The list of walkers strategies.
            sg: The training algorithm. 1 for skip-gram; otherwise CBOW.
                Defaults to 1.
            v_size: feature vector size for the embedding
        Returns:
            The embeddings of the provided instances.
        """
        transformer = RDF2VecTransformer(Word2Vec(sg=sg, vector_size=v_size), walkers=walkers)
        logger.log('Fitting model...')
        return transformer.fit_transform(kg, entities)

    @classmethod
    def gen_embeddings(cls, source, entities, sg=1,
                       walk_strategy='rw', sampler='uniform',
                       v_size=100, depth=4, walks_per_graph=25):
        endpoint = cls.endpoints[source]
        logger.log('Endpoint selected: %s' % endpoint)
        entities_uris = [rdflib.URIRef(entity) for entity in entities]
        kg = KG(endpoint,
                is_remote=True,
                literals=[
                        [
                            "http://dbpedia.org/ontology/wikiPageWikiLink",
                            "http://www.w3.org/2004/02/skos/core#prefLabel",
                            "http://www.w3.org/2000/01/rdf-schema#label"
                        ],
                        ["http://dbpedia.org/ontology/humanDevelopmentIndex"],
                ])
        walkers = cls.get_walker(sampler, walk_strategy, depth, walks_per_graph)
        sg = sg
        embeddings = cls.create_embeddings(kg, entities_uris, walkers, sg=sg, v_size=v_size)
        embeddings = embeddings[0]
        embeddings = [embedding.tolist() if not isinstance(embedding, list) else embedding for embedding in embeddings]
        return embeddings
