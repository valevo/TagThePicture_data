# TagThePicture_data

_UNDER CONSTRUCTION_

Simple codebase to gather data stemming from and related to the TagThePicture (TTP) crowd-sourcing project (see https://tagthepicture.nl/home) carried out by the Wereldmuseum (WM). The overall aim of the project is to increase the level of documentation for the photography collections of the Wereldmuseum -- beginning with the Indonesia parts of that collection -- and to thereby increase searchability and eventually accessibility.

This repository's function is to extract, pre-process and conveniently expose information (data) to allow for data-scientific interrogations and AI experiments. To this end, the repository is a codebase with methods to dump data from different sources (see below)


## Components

There are four primary sources of information:

### Annotations

The annotations themselves, produced by the crowd workers on the platform itself. This data is exported from the platform's CMS by scripts from Zooma, the company responsible for the user-facing annotation platform. Because there is (as of now) no API or endpoint for this data, the source file for annotation data is placed manually in this repository. 

See [here](./READMEs/annotations.md) for details about the annotation data, the meaning of individual fields and functionality offered to retrieve and use it.


### Object Records

Since the images (photographs) on the TTP platform are part of the Wereldmuseum's (WM) collection, they of course have records in the museum's catalogue (where they are "object records", just like everything else in the museum's catalogue).

In this context, object records primarily consist of textual information about a photograph -- title, descriptions and other notes -- and links into the thesaurus. The latter are organised into several categories (sometimes, but not always governed by the thesaurus itself), such as assigned culture, assigned geography, cultural or social functions and context, and what is depcited.

The WM provides an endpoint to expose object records (and other entities from its catalogue) in RDF, specifically modeled as [LinkedArt](linked.art). This repository retrieves all relevant and available information about objects from this endpoint, the way in which the endpoint is accessed and how information is extracted from it is described in a [separate README](./READMEs/objects.md). This README also contains more detailed information about the contents of the extracted data about objects exposed in this repository.

### Thesaurus Data

The [Wereldmuseum Thesaurus](https://collectie.wereldmuseum.nl/thesaurus) is the reference resource for tags both in the TTP annotations and the object records. As is typical, the thesaurus is organised into a hierarchy of broader and narrower concepts which have one or more labels. The thesaurus' default language for labels is Dutch but translations into English exist. Concepts come with descriptions, notes on their use (scope) and, wherever applicable, refer to their [AAT](vocab.getty.edu) or [geonames](geonames.org) equivalent.

Similar to records of objects, the WM's endpoint delivers the thesaurus in RDF, modeled in SKOS, see the [relevant README](./READMEs/thesaurus.md).

### Images

The same endpoints which deliver information about objects also deliver URIs to the server of the WM which delivers images (referred to as an "imageproxy" server). This way, the image data itself isn't stored here or elsewhere, only the way to get the data is.

Of course, images in the collection are subject to different licenses and, in some cases, copyright restrictions. Copyright-restricted images are not publicly accessible and hence not exposed here. Publicly available images come with license information.


