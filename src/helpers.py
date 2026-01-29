from tqdm import tqdm
from glob import glob

import requests as rq

from SPARQLWrapper import SPARQLWrapper, JSON

import rdflib
from rdflib import Graph

import pandas as pd

prefixes_map = dict(
    crm="http://www.cidoc-crm.org/cidoc-crm/",
    rdfs="http://www.w3.org/2000/01/rdf-schema#",
    la="https://linked.art/ns/terms/",
    dc="http://purl.org/dc/terms/",
    handle="https://hdl.handle.net/20.500.11840/",
    skos="http://www.w3.org/2004/02/skos/core#",
    aat="http://vocab.getty.edu/aat/"
)


PREFIXES = "\n".join(f"PREFIX {name}: <{uri}>" for name, uri in prefixes_map.items())


def reverse_prefix(x):
    pref, *rest = x.split(":", maxsplit=1)
    if pref in prefixes_map:
        return prefixes_map[pref] + rest[0]
    return x

def replace_prefix(x):
    for name, uri in prefixes_map.items():
        if x.startswith(uri):
            return f"{name}:{x.replace(uri, '')}"
    return x


def DataFrame_from_SPARQL(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    results = sparql.query().convert()
    result_df = pd.DataFrame.from_records(
        [{k: replace_prefix(v["value"]) for k, v in rec.items()} for rec in results["results"]["bindings"]] #, f"{k}_type": v["type"]
    )
    return result_df



def Graph_from_url(url, url_query_params, G=None):
    if G is None:
        G = Graph()

    try:
        cur = rq.get(endpoint_url, params=url_query_params)
        cur.raise_for_status()
        G.parse(data=cur.text, format='xml')
        return G

    except (rq.exceptions.ConnectionError, rq.exceptions.Timeout, 
                rq.exceptions.HTTPError, rq.exceptions.RequestException) as e:
        raise


def Graph_from_dump(dump_dir, G=None):
    if G is None:
        G = Graph(store="Oxigraph")

    files = sorted(glob(dump_dir+"/*.xml"))
    for f in tqdm(files):
        try:
            G.parse(f)
        except ValueError:
            print(f"{f} failed!")
    return G

def DataFrame_from_Graph(G, sparql_query, query_has_prefixes=False, reverse_prefixes=True):
    """
    Export results from an rdflib SPARQL query into a `pandas.DataFrame`,
    using Python types. See https://github.com/RDFLib/rdflib/issues/1179.
    """
    if not query_has_prefixes:
        sparql_query = PREFIXES + "\n\n" + sparql_query
    qres = G.query(sparql_query)
    
    df = pd.DataFrame(
        data=([None if x is None else x.toPython() for x in row] for row in qres),
        columns=[str(x) for x in qres.vars],
    )
    if reverse_prefixes:
        df = df.map(reverse_prefix)
    return df


