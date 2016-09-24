# parse the xml file for the datadump

import codecs
import csv
import datetime
from lxml import etree
import mafan

import zhwiki_schema
from zhwiki_schema import *
import traditionalzh

def extract_text( elem ):
    try:
        return elem.text.replace( "\"", "-" )
    except:
        return "NaN"

def extract_id( elem ):
    try:
        return int( elem.text )
    except:
        return -1

def extract_time( elem ):
    try:
        return datetime.datetime.strptime( elem.text, "%Y-%m-%dT%H:%M:%SZ" )
    except:
        return datetime.datetime( 9999, 12, 31, 23, 59, 59 )

def extract_namespace( elem ):
    nsdict = {
        "Media": -2,
        "Special": -1,
        "": 0,
        "Talk": 1,
        "User": 2,
        "User talk": 3,
        "Wikipedia": 4,
        "Wikipedia talk": 5,
        "Image": 6,
        "Image talk": 7,
        "MediaWiki": 8,
        "MediaWiki talk": 9,
        "Template": 10,
        "Template talk": 11,
        "Help": 12,
        "Help talk": 13,
        "Category": 14,
        "Category talk": 15,
        "Portal": 100,
        "Portal": 101 }
    try:
        ns = elem.text.split( ":" )
        return nsdict[ns[0]]
    except:
        return 0

def get_text_size( text ):
    """return bytesize of the text and the number of characters in the text"""
    try:
        return ( len( text.encode( 'utf-8' ) ), len( text ) )
    except:
        return "NaN", "NaN"

def get_editor_info( elem ):
    """read a contributor element and return an editor instance"""
    try:
        id = extract_id( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}id' ) )
        name = extract_text( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}username' ) )
        ipaddr = extract_text( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}ip' ) )
        return Editor( id = id, name = name, ipaddr = ipaddr )
    except:
        return Editor()

def get_page_info( elem ):
    """read a page element and return an page instance"""
    try:
        id = extract_id( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}id' ) )
        name = extract_text( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}title' ) )
        ns = extract_namespace( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}title' ) )
        return Page( id = id, name = name, ns = ns )
    except:
        return Page()

def get_revision_info( elem, page, previd, prevtext ):
    """read a revision element and return an revision instance""" 
    try:
        id = extract_id( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}id' ) )
        timestamp = extract_time( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}timestamp' ) )
        editor = get_editor_info( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}contributor' ) )
        minor = 1 if elem.find( '{http://www.mediawiki.org/xml/export-0.3/}minor' ) != None else 0
        comment = extract_text( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}comment' ) )
        currtext = extract_text( elem.find( '{http://www.mediawiki.org/xml/export-0.3/}text' ) )
        currtextbytesize, currtextcharsize = get_text_size( currtext )
        prevtextbytesize, prevtextcharsize = get_text_size( prevtext )
        addcharsize, addtradcharsize = traditionalzh.add_traditional( prevtext, currtext )
        traditional = False
        try:
            revbytesize = currtextbytesize - prevtextbytesize
        except:
            revbytesize = "NaN"
        try:
            revcharsize = currtextcharsize - prevtextcharsize
        except:
            revcharsize = "NaN"
        return Revision( 
            id = id,
            page = page,
            timestamp = timestamp,
            editor = editor,
            comment = comment,
            currtext = currtext,
            currtextbytesize = currtextbytesize,
            currtextcharsize = currtextcharsize,
            revbytesize = revbytesize,
            revcharsize = revcharsize,
            previd = previd,
            minor = minor,
            addcharsize = addcharsize,
            addtradcharsize = addtradcharsize )
    except:
        return Revision()

def export_revision_info( revision, fo_id, fe_id ):
    """export revision into output file"""
    fe_id.write( str( revision.page.id ) + '\t' + str( revision.id ) + ":" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.id ) + '\",' )
    except:
        fo_id.write( '\"' + str( -1 ) + '\",' )
        fe_id.write( "0" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.page.id ) + '\",' )
    except:
        fo_id.writer( '\"' + str( -1 ) + '\",' )
        fe_id.write( "1" + '\t' )
    try:
        fo_id.write( '\"' + revision.page.name + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + '\",' )
        fe_id.write( "2" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.page.ns ) + '\",' )
    except:
        fo_id.write( '\"' + str( 0 ) + '\",' )
        fe_id.write( "3" + '\t' )
    try:
        fo_id.write( '\"' + revision.timestamp.isoformat() + '\",' )
    except:
        fo_id.write( '\"' + datetime.datetime( 9999, 12, 31, 23, 59, 59 ).isoformat() + '\",' )
        fe_id.write( "4" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.editor.id ) + '\",' )
    except:
        fo_id.write( '\"' + str( -1 ) + '\",' )
        fe_id.write( "5" + '\t' )
    try:
        fo_id.write( '\"' + revision.editor.name + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + '\",' )
        fe_id.write( "6" + '\t' )
    try:
        fo_id.write( '\"' + revision.editor.ipaddr + '\",' )
    except:
        fo_id.write( '\"' + "0.0.0.0" + '\",' )
        fe_id.write( "7" + '\t' )
    try:
        fo_id.write( '\"' + revision.comment + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + "\"," )
        fe_id.write( "8" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.currtextbytesize ) + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + '\",' )
        fe_id.write( "9" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.currtextcharsize ) + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + '\",' )
        fe_id.write( "10" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.revbytesize ) + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + "\"," )
        fe_id.write( "11" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.revcharsize ) + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + '\",' )
        fe_id.write( "12" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.previd ) + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + '\",' )
        fe_id.write( "13" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.minor ) + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + '\",' )
        fe_id.write( "14" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.addcharsize ) + '\",' )
    except:
        fo_id.write( '\"' + "NaN" + '\",' )
        fe_id.write( "15" + '\t' )
    try:
        fo_id.write( '\"' + str( revision.addtradcharsize ) + '\"' )
    except:
        fo_id.write( '\"' + "NaN" + '\"' )
        fe_id.write( "16" + '\t' )
    fo_id.write( '\n' )
    fe_id.write( '\n' )
