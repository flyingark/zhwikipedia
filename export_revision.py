import sys
import csv
import codecs
import datetime
from lxml import etree

import zhwiki_schema
from zhwiki_schema import *
from zhwiki_parse import *

def main( dumpfilepath, outfilepath, logfilepath ):
    # open output file
    fo_id = codecs.open( outfilepath, 'wb', 'utf-8' )

    # open error file
    fe_id = codecs.open( logfilepath, 'wb', 'utf-8' )
  
    # parse xml file iteratively
    for event, elem in etree.iterparse( dumpfilepath, tag = '{http://www.mediawiki.org/xml/export-0.3/}page' ):
        page = get_page_info( elem )
        previd = 0
        prevtext = ""
        for child in elem.iter( '{http://www.mediawiki.org/xml/export-0.3/}revision' ):
            revision = get_revision_info( child, page, previd, prevtext )
            export_revision_info( revision, fo_id, fe_id )
            previd = revision.id
            prevtext = revision.currtext
            print( str( page.id ) + '\t' + str( revision.id ) )
            child.clear()
        elem.clear()

    # close output file
    fo_id.close()
    fe_id.close()

if __name__ == "__main__":
    main( sys.argv[1], sys.argv[2], sys.argv[3] )
