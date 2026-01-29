


### Fields

Of the original TTP exports by zooma; 

 - BatchUuid: ID of the batch (currently 5 distinct ones) 
 - BatchPhase: all same value ("Fase 1")
 - BatchName: three, roughly equally prevalent values ("Subject tags (1)", "Photo tags (1)", "Photo Tags (3)")
 - BatchType: either "Scene" or "Object" (former twice as common); distinguishes the two annotation tasks
 - annotation: may always contain a reason why no tags was provided; for BatchType "Object" this field contains the bounding box as four coordinates (if provided)
 - objectSourceIdentifier: name of the image holder; either "Tropenmuseum" or "Bronbeek" (7.5%)
 - objectIdentifier: the handle.net URI of the corresponding collection record (in less than 8% of cases the object number of the record; (probably Bronbeek due to lack of handle.net URIs))
 - termSourceIdentifier: ID of the source of terms, namely the thesaurus of NMvW (as a WikiData entry, entity Q112184776)
 - termIdentifier: ID of the tagged term, as the handle.net URI into the NMvW thesaurus
 - label: label of the tagged term; this is the label visible to the annotator, while the termIdentifier is the ID of the term itself
 - skipped: has value "1" in 9.5% percent of cases, other simply missing
 - remarks: remarks, present for one percent
 - sensitive: value "1" in 18 cases
 - datetime: date and time of the annotation (BUT NOT IN DATETIME FORMAT)
 - annotationUuid: uuid of the annotation
 - annotationType: "Label" (85%), "Skipped", "Remark", etc (for scene annotations; similar for object annotations)
 - checkedStatus: "Valid" (56%; 75% if only considering scene tagging) or "Invalid"
 - autoChecked: "0" (56%) or "1"
 - matchedAnnotationUuid: only relevant for object bounding boxes (and even then only present for 6%) (refers to the annotation for which intersecition-over-union overlap has been computed)
 - matchedIOU: intersecition-over-union overlap
 - BatchPhotoStatus: "Done" (89%), "Dropped" or "Skipped too many times"
 - BatchPhotoDroppedReason: only 2%; values such as "Skipped too many times", "No valid annotations"
 - AnnotatorUuid: the Uuid of the annotator 


