# NASA Space Apps 2020 by Hacker's Tribe Foundation

Steps to ensure while uploading your project:

- Create the main directory with your team name inside your location's directory
    - [Delhi](Delhi)
    - [Noida](Noida)
    - [Gurugram](Gurugram)
    - [Jodhpur](Jodhpur)

- Inside this main directory should be 3 things:
    - Source Code and/or Link to hosted implementation
    - README.md file (Format can be copied from README-Team.md file)
    - Presentation (Powerpoint or Google Slides) or Video

[How to create a Pull Request](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github)

**NOTE** - Use Github Desktop if using Windows to upload the files

## RESOURCES
### Procedure for installing Jupyter Notebook and Python via Anaconda
- Download Anaconda
    - [Linux](https://www.anaconda.com/download/#linux)
    - [MacOS](https://www.anaconda.com/download/#macos)
    - [Windows](https://www.anaconda.com/download/#windows)
- Install version of Anaconda which you downloaded, following the instructions on the download page
- Congratulations, you have installed Jupyter Notebook!
- You can start the notebook server from the command line (using Terminal on Mac/Linux, Command Prompt on Windows) by running - jupyter notebook

### Importing and Loading the dataset

import pandas as pd

read_file = pd.read_csv('filename.csv')

### Certificate Signing Bot
- Download UIPath from [here](https://docs.uipath.com/installation-and-upgrade/docs/studio-install-studio)
- Download [CertificateBot](https://github.com/hackerstribefoundation/nasaspaceapps2020/tree/main/CertificateBot)
- Place the Exported Sheet in the same directory as CertificateBot and double click the CertificateBot.xaml file.
- Click on Design tab and select Run File
- If all goes well, you'll have a notification pop up asking for Canva Link that points to the certificate you want to use and then another one asking for path to the Exported Sheet
- In the end you'll have a Mischied Managed Notification Pop Up and have certificates downloaded similar to ![this](CertificateBot/FNAME%20LNAME.jpg)
NOTE - Here both the Name of Person and File Name are "FNAME LNAME". In your case it'll be obviously mentioning the participants names and saved by the same file name. 