# zhwikipedia
## Prepare Data
### 01 Parse zhwikipedia
- parse data dump of Chinese Wikipedia data/zhwiki-20061208-pages-meta-history.xml
- export to data/revisions.csv
- ```python export_revision.py data/zhwiki-20061208-pages-meta-history.xml data/revisions.csv```

### 02 Identify Reverts
- identify revisions from data/revisions.csv
- add two columns for reverteds and revertings
- export to data/revisions_reverts.csv
- ```python identify_revert.py data/revisions.csv data/revisions_reverts.csv```

### 03 Create Editors File
- calculate proportion of simplified and traditional Chinese used by editors
- determine if editors ever contributed in any block
- export to data/editors.csv

