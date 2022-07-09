# HLBoost
SYDE 361 Web App for HLBoost Medium Fidelity Prototype

## Requirements
- Python3
- Flask
- Pandas
- Numpy
- Plotly
- Kaleidos

## How to Run
Once all the correct packages and libraries are downloaded, run this command to startup the server:

```shell
flask run
```

and head over to this website in your browser: http://127.0.0.1:5000/

## Folder Descriptions
- CSV/: Contains test csv files based on data we collected
- DV_Option_1,2,3/: These folders contain the python functions used to generate the plots each design option
- Electronics/: Contains Teensyduino code for hardware component
- static/: Plots for Design 1 and 2 are saved as a PNG here
- templates/: HTML / Jinja2 code for each webpage
- WebAppDemoImages/: Contains images for the web app (homepage, questionaire, design options etc.)