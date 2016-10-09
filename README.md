# zhwikipedia
## Description of Files
* ```zhwiki-20061208-pages-meta-history.xml```: original xml file from Wikimedia including the entire editing history of the Chinese Wikipedia up to 2006/12/08.


## Prepare Data
### 01 Parse zhwikipedia
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

