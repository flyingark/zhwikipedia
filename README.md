# zhwikipedia

## 01 Parse zhwikipedia
- parse data dump of Chinese Wikipedia data/zhwiki-20061208-pages-meta-history.xml
- export to data/revisions.csv
- ```python export_revision.py data/zhwiki-20061208-pages-meta-history.xml data/revisions.csv```

## 02 Identify Reverts
read revisions.csv and identify revisions that are reverted and reverting
```python identify_revert.py data/revisions.csv data/revisions_reverts.csv```
