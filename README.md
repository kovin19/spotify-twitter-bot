# Spotify Random Mexican Song
The purpose of this project is to generate an image of a random song from Mexico's top songs playlist. As this playlist changes constantly, so do the recommendations.

## Python version
This project was built using **Python 3.12**. 

Python 3.10+ is required to run this project.

## How to run
To run this project, you must follow these steps:

1. Rename the **.env.example** file to **.env** and specify your own Spotify credentials from Spotify's Development Dashboard.
2. Create a virtual environment and install the packages from the **requirements.txt** file
    2.1 Create virtual environment
    ### Linux
    > python3 -m venv [VENV NAME]

        Example
        python3 -m venv venv
    ### Windows
    > py -m venv [VENV NAME]

        Example
        py -m venv venv

    2.2 Install required libraries
    > pip install -r requirements.txt

3. Run the **main.py** file from your terminal

    Example
    >py main.py