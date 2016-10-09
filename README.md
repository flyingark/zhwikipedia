# Zhwikipedia
## Description of Files
### Data File
* ```zhwiki-20061208-pages-meta-history.xml```: original xml file from Wikimedia including the entire editing history of the Chinese Wikipedia up to 2006/12/08
* ```revision.csv```: containing each revision parsed from the orignal xml file, not including information on reverts or tag for real editor, bot editor or ip editor
* ```revision_withreverts.csv```: adding two columns to ```revision.csv``` indicating reverting
* ```revisions_full.csv```: modifying editor information indicating real editor, bot or ip editor
* ```editors_withinblocked.csv```: indicating whether an editor has ever contributed during the block
* ```editors_tradratio.csv```: indcating the fraction of traditional characters an editor has used
* ```editors_blocked.csv```: indicating whether an editor is blocked or not (defined as have traditional ratio <= 0.2 and never contributed in any block)

### Result File
* ```numrev_2005-06-19T00:00:00_2005-09-19T00:00:00.csv```: including number of revisions, revertings and reverteds in each article between 2005/06/19 and 2005/09/19 (three months before the block)
* ```numrev_2005-09-19T00:00:00_2005-12-19T00:00:00.csv```: including number of revisions, revertings and reverteds in each article between 2005/09/19 and 2005/12/19 (three months after the block)
* ```workload_2005-06-19T00:00:00_2005-09-19T00:00:00.csv```: including workload information in each article between 2005/06/19 and 2005/09/19 (three months before the block)
* ```workload_2005-09-19T00:00:00_2005-12-19T00:00:00.csv```: including workload information in each article between 2005/09/19 and 2005/12/19 (three months after the block)


## Prepare Data
### 01 Parse Zhwikipedia
* parse data dump of Chinese Wikipedia data/zhwiki-20061208-pages-meta-history.xml
* export to data/revisions.csv
* ```python export_revision.py data/zhwiki-20061208-pages-meta-history.xml data/revisions.csv```

### 02 Identify Reverts
* identify revisions from data/revisions.csv
* add two columns for reverteds and revertings
* export to data/revisions_reverts.csv
* ```python identify_revert.py data/revisions.csv data/revisions_reverts.csv```

### 03 Identify Bots and IPs
* distinguish among real editors, bots and ip addresses
* reformat the csv file and generate revision_full.csv
* editor described in columns 5 (editor id, -1 for bot and ip editor), 6 (editor name, ip for ip editor) and 7 (0 for real editor, 1 for bot, 2 for ip editor).
* export to data/revision_full.csv
* ```python identify_bot.py```

### 04 Create Editors File (needs to be repaired)
* calculate proportion of simplified and traditional Chinese used by editors
* determine if editors ever contributed in any block
* export to data/editors.cs

