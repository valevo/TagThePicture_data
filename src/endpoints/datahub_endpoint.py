from tqdm import tqdm
from time import sleep

# from src.helpers import replace_prefix, reverse_prefix, PREFIXES, DataFrame_from_SPARQL
from src.helpers import *


nmvw_endpoint = "https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql"
thesaurus_endpoint = "https://api.colonialcollections.nl/datasets/nmvw/thesaurus/sparql"

# not needed, this is specifically about the NMvW -- careful about the /services/kg/ subdomain!
# datahub_endpoint = "https://api.colonialcollections.nl/datasets/data-hub/knowledge-graph/services/kg/sparql"


def _get_object_tags(handle_links):
    wanted = " ".join(map(replace_prefix, handle_links))
    
    object_thes_query = PREFIXES + f"""
        SELECT DISTINCT
            ?objectURI
            ?material

            ?objecttype
            ?objecttype_alternative
            
            ?depicts

            
        WHERE {{
            ## The object
            ?objectURI a crm:E22_Human-Made_Object .
    
            OPTIONAL {{ ?objectURI crm:P45_consists_of ?material . }}
            OPTIONAL {{ ?objectURI crm:P2_has_type ?objecttype . }}

            OPTIONAL {{ ?objectURI crm:P103_was_intended_for [ crm:P190_has_symbolic_content ?objecttype_alternative ] .}}

            OPTIONAL {{ ?objectURI crm:P65_shows_visual_item [ crm:P138_represents ?depicts ] . }}

    
            VALUES ?wanted {{ {wanted} }}
            FILTER( ?objectURI = ?wanted )
        }}
    """
    
    tags = DataFrame_from_SPARQL(nmvw_endpoint, object_thes_query)
    # thes["objectURI"] = thes.objectURI.apply(reverse_prefix)
    if len(tags) < 1:
        return None
    tags = tags.fillna("").map(reverse_prefix)
    return tags.set_index("objectURI")

def get_object_tags(handle_links):
    if len(handle_links) <= 50:
        return _get_object_tags(handle_links)
    else:
        n = 50
        dfs = []
        for i in tqdm(range(0, len(handle_links), n), desc="querying for object tags"):
            cur = _get_object_tags(handle_links[i:i + n])
            if cur is not None:
                dfs.append(cur)
            sleep(0.3)
        return pd.concat(dfs, axis=0)



def _get_thesaurus(handle_links):

    wanted = " ".join(map(replace_prefix, handle_links))
    
    q = PREFIXES + f"""
        SELECT DISTINCT
            ?conceptURI
            ?prefLabel
            ( lang(?prefLabel) AS ?prefLabelLanguage )

            ?altLabel # English or Dutch alternative
            ( lang(?altLabel) AS ?altLabelLanguage )

    
            ?note # note on how to use the term
            # ?notation # notation from the OVM 
            # ?inScheme # always handle:conceptscheme4
            ?exactMatch # corresponding AAT or geonames.org entry
    
        WHERE {{
            ?conceptURI a skos:Concept .
            ?conceptURI skos:prefLabel ?prefLabel .
            ?conceptURI skos:altLabel ?altLabel .
            OPTIONAL {{ ?conceptURI skos:note ?note . }}
            OPTIONAL {{ ?conceptURI skos:notation ?notation . }}
            OPTIONAL {{ ?conceptURI skos:inScheme ?inScheme . }}
            OPTIONAL {{ ?conceptURI skos:exactMatch ?exactMatch . }} 
            
            # ?conceptURI skos:broader ?broader .
            # ?conceptURI skos:narrower ?narrower .
            
            
            VALUES ?wanted {{ {wanted} }}
            FILTER ( ?conceptURI = ?wanted )
    
        }}
    """

    recs = DataFrame_from_SPARQL(thesaurus_endpoint, q)
    recs["conceptURI"] = recs.conceptURI.apply(reverse_prefix)
    return recs.set_index("conceptURI")



def get_thesaurus(handle_links):
    if len(handle_links) <= 50:
        thes = _get_thesaurus(handle_links)
    else:
        n = 50
        dfs = []
        for i in tqdm(range(0, len(handle_links), n), desc="querying for thesaurus"):
            dfs.append(_get_thesaurus(handle_links[i:i + n]))
            sleep(0.3)
        thes = pd.concat(dfs, axis=0)
    thes.altLabelLanguage = thes.altLabelLanguage.apply(lambda l: l if l else "nl")
    thes.prefLabelLanguage = thes.prefLabelLanguage.apply(lambda l: l if l else "nl")
    return thes


def _get_hierarchy(handle_links):

    wanted = " ".join(map(replace_prefix, handle_links))
    
    q = PREFIXES + f"""
        SELECT DISTINCT
            ?conceptURI
            ?broader
            ?narrower
        WHERE {{
            ?conceptURI a skos:Concept .
            
            OPTIONAL {{ ?conceptURI skos:broader ?broader . }}
            OPTIONAL {{ ?conceptURI skos:narrower ?narrower . }}
            
            
            VALUES ?wanted {{ {wanted} }}
            FILTER ( ?conceptURI = ?wanted )
    
        }}
    """

    recs = DataFrame_from_SPARQL(thesaurus_endpoint, q)
    if len(recs) < 1: print(handle_links)
    recs["conceptURI"] = recs.conceptURI.apply(reverse_prefix)
    return recs.set_index("conceptURI")



def get_hierarchy(handle_links):
    if len(handle_links) <= 50:
        thes = _get_hierarchy(handle_links)
    else:
        n = 50
        dfs = []
        for i in tqdm(range(0, len(handle_links), n), desc="querying for thesaurus"):
            dfs.append(_get_hierarchy(handle_links[i:i + n]))
            sleep(0.3)
        thes = pd.concat(dfs, axis=0)
    return thes

