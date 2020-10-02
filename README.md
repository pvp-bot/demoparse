coh demo parser for team arena matches  
message me (xhiggy) on discord if you have questions  
I usually find some bugs whenever I use this, so it's an ongoing process of work and fine tuning  

## notes

Quick how-to use for people. These instructions will assume a small amount of familiarity with Python and command line stuff. I've made some bash scripts for my own ease of use, if you don't have bash they're probably straight forward enough that you could rewrite them in python or as a Windows batch file. If you're on Windows you can use the _Window Subsystem for Linux_ as an easy way to access a Linux shell.

This program is made for typical team arena matches. If you're running it for non-standard matches (i.e. smaller than 6v6, more than 10 minutes, more than 2 teams) you'll have to go into the code and change parameters to get actually useful outputs.

## setup

### program setup

If you haven't already, clone the repo somewhere (or use your favourite git gui)
`git clone https://github.com/pvp-bot/demoparse.git`

If cloned it previously, pull to get the latest updates (from the repo folder)  
`git pull`

Python (v3+) requirements: numpy, google-cloud-bigquery

To record a demo file in-game use the `/demorecord nameofdemohere` in the buff phase of a match after you've loaded onto the map. Use the `/demostop` command after the match ends (the demo will also stop when you load out of the map). Demos are saved under the `client_demos` folder in your City of Heroes folder. If you use the same name when recording a demo it will overwrite the existing demo.

### storage method

If you want to use Big Query as your data storage method you will need
- a Google Cloud account and a project with Big Query enabled
- a dataset created in your Big Query project where you'll be uploading your tables
- a Google service account with Big Query job acccess to the dataset you're using
- a Google credentials .json file for that service account stored in the data folder of the demoparse project (**important:** do not share this .json file with anyone if you do not understand what you're sharing access to)
- rename the `secrets_example.py` to `secrets.py` and open it to edit it
  - change the `GOOGLE_APPLICATION_CREDENTIALS` parameter to the name of your .json credentials file
  - change the project name and dataset name to the names you've created in your Google Cloud project
  
Alternatively, you _can_ use Google Sheets to store the .csv data however I don't recommend this for several reasons. The storage is noticably slower than Big Query, my Big Query parse and upload method is mostly automated which means a lot more time spent if not using it, and, more importantly, it will require you to relink all data fields and conditional formatting in the Datastudio report (and will miss further template updates unless you go through the relinking process again).

### folder setup

For ease of use I'd recommend storing your demo files in the same way as I am: a top level folder for all your demos and in it a subfolder for each night of matches. E.g. the `~/Documents/demos` folder houses things like `~/Documents/demos/200930_kickball/` and in that you have the several demo files such as `~/Documents/demos/200930_kickball/match1_skyway.cohdemo`. I name demos just single numbers based on the order they're played (e.g. `1.cohdemo` is the first match of the night), but any name should work.

## use instructions

### parsing the demos

From the repo folder you have a few options on how to run it.
Running the `parsedemo.py` on a .cohdemo file will generate a parsed .csv file of that demo with the same name as well as spit out some high level stats from that match.  
`python parsedemo.py /path/to/demofile/skywayexample.cohdemo`

`upload_bq.py` will upload a parsed .csv file to your Google Big Query cloud account as a query table if you have it configured. Typically you want to run this on a merged csv file (i.e. not just a single match) so that you can view mupltiple matches from within the same Datastudio report.  
`python upload_bq.py /path/to/demofile/skywayexample.csv`

Instead of running the python scripts directly, I recommend running the shell script `parsefolder.sh` on an entire folder. Run this script by giving it an input `-i` folder and it will run the `parsedemo.py` script on every demo file in that folder, append all the .csvs to a single one, then upload the final .csv to your Big Query project under a table with the same name as your folder. e.g.


`./parsefolder.sh -i /path/to/demofolder/`  


Adding a `-s` to the command will 'skip' the parsing step and only append+upload the final .csv (in case you've already run the parsedemo.py individually and don't want to rerun it on all files). Rerunning the script will overwrite the existing Big Query table of the same name if it exists. You may need to make the script executable first, `chmod +x parsefolder.sh`.

### creating the Datastudio report
Find a recent report with copying enabled (either one of your previous version or one of mine if you have it) and hit the _Make a copy of this report_ button in the top right, then go _New Data Source>Create New Source>Big Query>My Projects>Your Project>Your Dataset_ then select the data table corresponding to the demo folder you've just uploaded.

Update the 2 names of the report in the top left and whatever other adjustments you want to make. Update the share permissions to allow others to view if you want to share it.

## other stuff
The demorecord will miss some things in the match occasionally, especially on larger maps when you can get out of render range (note: perception range is irrelevant). You can manually add override lines to the start of the demofile (using any text editor) to change the match score, player team assignment, player powersets, or swap red and blue entirely. See `data/override.py` for examples.
