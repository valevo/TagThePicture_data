from time import sleep
from tqdm import tqdm
import requests as rq
from datetime import datetime

import os
endpoint_url = "https://collectie.wereldmuseum.nl/ccrdf/ccrdf.py"
from src.helpers import *



indonesia_photography = "and(objecttrefwoord=Foto*;termmasterid=10061190)"
n = 150000 # total number of objects expected
def dump_endpoint(n, output_dir="../../data/nmvw_dumps", k=1000, internal_query=indonesia_photography):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    
    
    endpoint_params = dict(command="search",
                  query=internal_query,
                  fields="*",
                  range=""
                 )


    with open(f"./{output_dir}/META.txt", "w") as handle:
        handle.write(f"""
DUMP OF THE NMVW LINKEDART ENDPOINT

URL: {endpoint_url}
PARAMS: {endpoint_params}
DATE: {datetime.today()}
"""
        )
    
    failed = []
    for i in tqdm(range(0, n, k)):
        endpoint_params["range"] = f"{i}-{i+k}"
        try:
            cur = rq.get(endpoint_url, params=params)
            cur.raise_for_status()
            if len(cur.text) < 50:
                print(f"range {endpoint_params['range']} yielded no results... continuing")
                continue
    
            with open(f"./{output_dir}/{i:06}-{(i+k):06}.xml", "w") as handle:
                handle.write(cur.text)
            
            sleep(0.3)
        except (rq.exceptions.ConnectionError, rq.exceptions.Timeout, 
                rq.exceptions.HTTPError, rq.exceptions.RequestException) as e:
            failed.append((endpoint_params["range"], e))
    return failed



def get_objects(G):
    q = """
    SELECT DISTINCT 
        ?handle_link
        ?object_number

        
    WHERE {
        ?handle_link a crm:E22_Human-Made_Object .
        ?handle_link crm:P1_is_identified_by [  a crm:E42_Identifier; 
                                                crm:P2_has_type aat:300312355; 
                                                crm:P190_has_symbolic_content ?object_number ] .

    }
    """

    objects = DataFrame_from_Graph(G, q)
    return objects


def get_object_tags(G):
    q = """
    SELECT DISTINCT 
        ?handle_link
        ?object_number

        # ?type_thesaurus
        # ?type_label

        ?culture
        ?function_context_tag


    WHERE {
        # ?handle_link <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o .
        ?handle_link a crm:E22_Human-Made_Object .
        ?handle_link crm:P1_is_identified_by [  a crm:E42_Identifier;
                                                crm:P2_has_type aat:300312355;
                                                crm:P190_has_symbolic_content ?object_number ] .
        # # ?handle_link crm:P2_has_type ?type_thesaurus .
        # # ?handle_link crm:P2_has_type [a crm:E55_Type; rdfs:label ?type_label] . # slow
        # # FILTER (strstarts(str(?type_thesaurus), str(handle:))).


        # # ?handle_link crm:P32_used_general_technique [a crm:E55_Type; rdfs:label ?technique ] . # doesn't work

        ?handle_link crm:P67i_is_referred_to_by [ a crm:E33_Linguistic_Object; crm:P2_has_type ?culture ] .
        FILTER (strstarts(str(?culture), str(handle:))).


        ?handle_link crm:P65_shows_visual_item [ crm:P2_has_type ?function_context_tag ] .

    }
    """

    tags = DataFrame_from_Graph(G, q)
    return tags



