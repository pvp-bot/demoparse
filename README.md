coh demo parser for team arena matches

[example](https://datastudio.google.com/u/0/reporting/c64893fe-7f45-4dd0-b6cd-dd68b6a4fd80/)

message me (xhiggy) on discord if you have questions on how stuff works or is calculated. if you find errors let me know or feel free to submit a pull request.

## foreword

This program is made for the standard structure of team arena matches: 8 vs 8, 10 minute area matches based around calling targets with multiple people attacking. The further you deviate from the usual structure the less useful this script becomes (though some parameters could be changed to make it work for different match types). 

This was made to provide a useful breakdown of matches and weights certain info more, but I've tried to include most of what I can to where you can find info if you look for it. Some of the parameters in the reporting are based around calibration of my matches along side my own vods, so there are a few numbers that are somewhat subjective. 

There are some limitations with demorecords where you may get some missing information. It will only record info within render range from your character (note this is different from perception range) so on larger maps you can miss some data, especially when you respawn away from the fight. Some powers don't have effects, difficult to isolate effects, or share the same effects with other powers which makes some things difficult to code for. Since spikes are based on certain actions in-game there will be a few false positives here and there but I've found the script to be pretty reliable in practice.

## notes

Quick how-to use for people. These instructions will assume a small amount of familiarity with Python and command line stuff. I've made some bash scripts for my own ease of use, if you don't have bash they're probably straight forward enough that you could rewrite them in python or as a Windows batch file. If you're on Windows you can use the _Window Subsystem for Linux_ as an easy way to access a Linux shell.

## setup

### program setup

If you haven't already, clone the repo somewhere (or use your favourite git client)
`git clone https://github.com/pvp-bot/demoparse.git`

If cloned it previously, pull to get the latest updates (from the repo folder)  
`git pull`

Python (v3+) requirements: numpy, google-cloud-bigquery

To record a demo file in-game use the `/demorecord nameofdemohere` in the buff phase of a match after you've loaded onto the map. Use the `/demostop` command after the match ends (the demo will also stop when you load out of the map). Demos are saved under the `client_demos` folder in your City of Heroes folder. Default configuration is for 10 minute match time. If you use the same name when recording a demo it will overwrite the existing demo. Note: the demo takes a few seconds to populate with data after you stop it, so don't try to parse it or move the file immediately.

### folder setup

I'd recommend storing your demo files in a similar way to me: a top level folder for all your demos and in it a subfolder for each night of matches. E.g. the `~/Documents/demos` folder houses things like `~/Documents/demos/200930_kickball/` and in that you have the several demo files such as `~/Documents/demos/200930_kickball/match1_skyway.cohdemo`. I name demos just single numbers based on the order they're played (e.g. `1.cohdemo` is the first match of the night), but any name should work with a few changes in the report.

## usage

### parsing the demos

From the repo folder you have a few options on how to run it.
Running the `parsedemo.py` on a .cohdemo file will generate a parsed .csv file of that demo with the same name as well as spit out some high level stats from that match.  
`python parsedemo.py /path/to/demofile/skywayexample.cohdemo`

`upload_bq.py` will upload a parsed .csv file to your Google Big Query cloud account as a query table if you have it configured. Typically you want to run this on a merged csv file (i.e. not just a single match) so that you can view multiple matches from within the same Datastudio report.  
`python upload_bq.py /path/to/demofile/skywayexample.csv`

Instead of running the python scripts directly, I recommend running the shell script `parsefolder.sh` on an entire folder. Run this script by giving it an input `-i` folder and it will run the `parsedemo.py` script on every demo file in that folder, append all the .csvs to a single one, then upload the final .csv to your Big Query project under a table with the same name as your folder. e.g.


`sh ./parsefolder.sh -i /path/to/demofolder/`  


Adding a `-s` parameter to the command will 'skip' the parsing step and only append+upload the final .csv (in case you've already run the parsedemo.py individually and don't want to rerun it on all files). Rerunning the script will overwrite the existing Big Query table of the same name if it exists. A `-u` parameter will skip the upload and only parse and append the .csvs.

### Datastudio storage method

If you want to use Big Query as your data storage method you will need
- a Google Cloud account and a project with Big Query enabled
- a dataset created in your Big Query project where you'll be uploading your tables
- a Google service account with Big Query job acccess to the dataset you're using
- a Google credentials .json file for that service account stored in the data folder of the demoparse project (**important:** do not share this .json file with anyone if you do not understand what you're sharing access to)
- rename the `secrets_example.py` to `secrets.py` and open it to edit it
  - change the `GOOGLE_APPLICATION_CREDENTIALS` parameter to the name of your .json credentials file
  - change the project name and dataset name to the names you've created in your Google Cloud project
  
Alternatively, you _can_ use Google Sheets to store the .csv data however I don't recommend this for a few reasons. Queries with Sheets is noticably slower than Big Query, my Big Query parse and upload method is mostly automated for saving time, and it will require you to relink all data fields and conditional formatting in the Datastudio report (and will miss further template updates from me unless you go through the relinking process again).

I can maybe set you up on my cloud storage if you can't get it to work.

### creating the Datastudio report
Find a recent report with copying enabled (see top of the README for a recent one) and hit the _Make a copy of this report_ button in the top right, then go _New Data Source>Create New Source>Big Query>My Projects>Your Project>Your Dataset_ then select the data table corresponding to the demo folder you've just uploaded.

Update the 2 names of the report in the top left and whatever other adjustments you want to make. Update the share permissions to allow others to view if you want to share it.

## overrides
The demorecord will miss some things in the match occasionally, especially on larger maps when you can get out of render range (note: perception range is irrelevant). You can manually add override lines to the start of the demofile (using any text editor) to adjust the final match score, player team assignment, player powersets, or swap red and blue sides. See `data/override.py` for examples.

## issues
There was an issue with numpy on Windows when I ran it last which required downgrading to an older version. The error message included a URL which had instructions on which version to downgrade to. Not sure if numpy has been updated to fix this yet.