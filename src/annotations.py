import os
import pandas as pd
from datetime import datetime


DATA_DIR = "./data"

ANNOTATION_FILE = os.path.join(DATA_DIR,
                               "20250326-Alle-annotaties-Fotos1Onderwerpen1Fotos2Onderwerpen2Fotos3_20250326102326-kopieHAICU.csv")

RELEVANT_FIELDS = ['annotationUuid',
                     'objectSourceIdentifier',
                     'objectIdentifier',
                     'AnnotatorUuid',
                     'datetime',
                     'termIdentifier',
                     'label',
                     'annotationType',
                     'skipped',
                     'sensitive',
                     'checkedStatus',
                     'autoChecked',
                     'annotation',
                     'BatchPhotoDroppedReason']


simple_replace = {"https://hdl.handle.net/20.500.11840/termmaster25127": 
                                      "https://hdl.handle.net/20.500.11840/termmaster10049794",
                  "https://hdl.handle.net/20.500.11840/termmaster10066458X":
                                      "https://hdl.handle.net/20.500.11840/termmaster10066895",
                  "https://hdl.handle.net/20.500.11840/termmaster10066952X":
                                      "https://hdl.handle.net/20.500.11840/termmaster10066952",
                  "https://hdl.handle.net/20.500.11840/termmaster10066833X":
                                      "https://hdl.handle.net/20.500.11840/termmaster10066833",
                 }

ambiguous = {"https://hdl.handle.net/20.500.11840/termmaster10066346":
                                    "https://hdl.handle.net/20.500.11840/termmaster10066335",
            "https://hdl.handle.net/20.500.11840/termmaster10066470": 
                                     "https://hdl.handle.net/20.500.11840/termmaster10049906",
             "https://hdl.handle.net/20.500.11840/termmaster10066893":
                                     "https://hdl.handle.net/20.500.11840/termmaster10079410"
            }
additional_notion = {"https://hdl.handle.net/20.500.11840/termmaster10066895":"https://hdl.handle.net/20.500.11840/termmaster10067195",
                     "https://hdl.handle.net/20.500.11840/termmaster10066952":"https://hdl.handle.net/20.500.11840/termmaster10067195",
                    "https://hdl.handle.net/20.500.11840/termmaster10066833":"https://hdl.handle.net/20.500.11840/termmaster10067195"
                    }
             
             


def get_annotations(only_scene_tags=True):
    anns = pd.read_csv(ANNOTATION_FILE, sep=';')

    if only_scene_tags:
        anns = anns[anns.BatchType == "Scene"]
    
    anns = anns.dropna(subset="termIdentifier")
    anns["datetime"] = pd.to_datetime(anns.datetime, format="%d-%m-%Y %H:%M")

    
    for k, v in simple_replace.items():
        cur_indexer = (anns.termIdentifier == k)
        anns.loc[cur_indexer, "termIdentifier"] = v
        anns.loc[cur_indexer, "label"]  = None
        
    for k, v in ambiguous.items():
        cur_indexer = (anns.termIdentifier == k)
        anns.loc[cur_indexer, "termIdentifier_alternative"] = v

    for k, v in additional_notion.items():
        cur_indexer = (anns.termIdentifier == k)
        anns.loc[cur_indexer, "termIdentifier_modifier"] = v


    return anns[RELEVANT_FIELDS]



