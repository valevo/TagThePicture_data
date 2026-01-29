# TagThePicture_data

Simple codebase to gather data related to the TagThePicture (TTP) crowd-sourcing project (see https://tagthepicture.nl/home). 


## Components

There are four primary sources of information related to the TTP data:

### Annotations

The annotations themselves, produced by the crowd workers on the platform itself. This data is exported from the platforms CMS by scripts from Zooma, the company responsible for the platform.

See [here](./READMEs) for details about the annotations.

### Object Records

Since the images (photographs) on the TTP platform are part of the Wereldmuseum's (WM) collection, they of course have records in the museum's catalogue (where they are among all other objects from the museum, hence the name).
The 


### Images

The same endpoints which deliver information about objects also deliver URIs to the server of the WM which delivers images (referred to as an "imageproxy" server).
This way, the image data itself isn't stored here or elsewhere, only the way to get the data.

The license of each image is also 


### Thesaurus Data




