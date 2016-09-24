#!/usr/bin/python
# -*- coding: utf-8

# identify reverts in revision. return a csv file called revision_withreverts.

import sys
import codecs
import csv
import datetime

import zhwiki_schema
from zhwiki_schema import *

def find_revert( rev_list ):
    for idx, revision in reversed( list( enumerate( rev_list ) ) ):
        if ( ( "恢复到" in rev_list[idx][8] and "的最后一次编辑" in rev_list[idx][8] ) or 
            ( "恢復到" in rev_list[idx][8] and "的最後一次編輯" in rev_list[idx][8] ) or
            ( "回降到" in rev_list[idx][8] and "的最後一次編輯" in rev_list[idx][8]) or
            ( "reverted to last edit by" in rev_list[idx][8] ) ):
            rev_list[idx][16] = "revert"
            for i in reversed( range( idx ) ):
                # go back the revision list to find the revision that is reverted to
                editorname = rev_list[i][6]
                editoripaddr = rev_list[i][7]
                
                if ( editorname in rev_list[idx][8] or editoripaddr in rev_list[idx][8] ):
                    # if the revision that is reverted to is found, mark all revisions being reverted.
                    for j in range( i + 1, idx ):
                        rev_list[j][15] = revision[0]
                    break
                
                
def main( infilepath, outfilepath ):
    # open input file
    fi_id = open( infilepath, 'rb' )
    fi_reader = csv.reader( fi_id, doublequote = True )

    # open output file
    fo_id = open( outfilepath, 'wb' )

    # declare list of revision for a page
    pageid = 0
    rev_list = []

    # go through the file and identify revert
    for line in fi_reader:
        if int( line[1] ) != pageid:
            # identify revert
            find_revert( rev_list )
            
            # export revision records with reverts
            for revision in rev_list:
                fo_id.write( "\"" + revision[0] + "\"," )
                fo_id.write( "\"" + revision[1] + "\"," )
                fo_id.write( "\"" + revision[2] + "\"," ) 
                fo_id.write( "\"" + revision[3] + "\"," ) 
                fo_id.write( "\"" + revision[4] + "\"," ) 
                fo_id.write( "\"" + revision[5] + "\"," ) 
                fo_id.write( "\"" + revision[6] + "\"," ) 
                fo_id.write( "\"" + revision[7] + "\"," ) 
                fo_id.write( "\"" + revision[8] + "\"," ) 
                fo_id.write( "\"" + revision[9] + "\"," ) 
                fo_id.write( "\"" + revision[10] + "\"," ) 
                fo_id.write( "\"" + revision[11] + "\"," ) 
                fo_id.write( "\"" + revision[12] + "\"," ) 
                fo_id.write( "\"" + revision[13] + "\"," )
                fo_id.write( "\"" + revision[14] + "\"," )
                fo_id.write( "\"" + revision[15] + "\"," ) 
                fo_id.write( "\"" + revision[16] + "\"" )
                fo_id.write( '\n' )
            
            # update rev_list
            pageid = int( line[1] )
            rev_list = [] 
        
        # append revision to include the revision id that reverts it
        line.append( "NaN" )
        line.append( "NaN" )
        rev_list.append( line )

    fi_id.close()
    fo_id.close()

if __name__ == "__main__":
    main( sys.argv[1], sys.argv[2] )

