# read csv file of revision and export the aggregate use of traditional Chinese for each editor

import sys
import csv
import datetime
from lxml import etree
import mafan

import zhwiki_schema
from zhwiki_schema import *
from zhwiki_parse import *

def main( infilepath, outfilepath ):
    # open input file
    fi_id = open( infilepath, 'rb' )
    fi_reader = csv.reader( fi_id, doublequote = True )

    # open error file
    fo_id = open( outfilepath, 'wb' )
    fo_writer = csv.writer( fo_id, doublequote = True )

    # decare list of editors
    editor_list = []

    # go through input file and get editors revision data
    for line in fi_reader:
        print line[0] + '\t' + line[1] + '\t' + line[5] + '\t' + line[6] + '\t' + line[15] + '\t' + line[16]
        editor_found = False
        if int( line[5] ) != -1:
            revision = Revision( 
                editor = Editor( id = int( line[5] ), name = line[6] ), 
                addcharsize = int( line[15] ), 
                addtradcharsize = int( line[16] ) )
            for item in editor_list:
                if item[0] == revision.editor.id:
                    editor_found = True
                    item[2] = item[2] + revision.addcharsize
                    item[3] = item[3] + revision.addtradcharsize
                    import pdb; pdb.set_trace()
                    break
            if editor_found == False:
                editor_list.append( [int( line[5] ), line[6], int( line[15] ), int( line[16] )] )

    # export
    for item in editor_list:
        fo_writer.writerow( [item[0]] + [item[1]] + [item[2]] + [item[3]] )

    # close files
    fi_id.close()
    fo_id.close()

if __name__ == "__main__":
    main( sys.argv[1], sys.argv[2] )
