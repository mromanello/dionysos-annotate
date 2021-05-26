# shs-website

This project is a website created for the class HUM-452-Mythes de la méditerranée ancienne
at EPFL.  
The final aim is to study ancient Greek plays by 3D rendering them using Unity.  
This project comes as a pre-processing step of the play. It reads XML from the Perseids project (https://www.perseids.org/)
and detects where certain actions should be performed by the characters of the play. An example of this
is when a character is imploring the Gods and has to have his hands up towards the sky.
The website also allows adding metadata about the play, which will be used by the Unity app.
And to add translation for each portion of text that requires a character to move.
A final JSON file is created and will serve as input to the Unity app.


## How to deploy the app
Disclaimer: the website is meant for local use, and is not fit for deployment on a full-fledged
server, due to security issues.

2 options are available:
### Using pip virtual environments
- clone the environment
- `cd shs-website`
- run the script: `./boot.sh`
- you may need to first make the script executable : `chmod +x boot.sh`
- access `localhost:5000`

### Using Docker
- Build the image : `make build_image`
- run the website: `make website`
- access `localhost:5000`

## Code
The app structure is fairly simple,
the **app** folder contains all the code and is organized as follows:
- **app/patterns**: contains all code for searching for certains patterns in words, these
translate into gestures taken by the characters.
- **app/templates**: contains HTML and CSS. Uses Bootstrap 5 and Jinja2.
- **app/static**: Contains some Javascript code used by the website.
- **__init__.py**: Initializes the Flask app. Follows most Flask apps structure.
- **config.py**: Contains a Config class which holds and Configuration constants
for the app.
- **logic.py**: Contains all Database operations and main logic of the app.
- **models.py**: Contains the Database tables declarations, in SQLAlchemy fashion.
- **perseids_search.py**: contains all code which is related to parsing XML obtained from
the Perseids project.
- **routes.py**: answers HTTP requests from the front-end.
**migrations** contains Database migrations info (Alembic)
Disclaimer 2.0: the code can be improved in certain parts. However, it should be well documented/commented.  

