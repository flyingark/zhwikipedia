import datetime

class Editor:
    def __init__( self, id = -1, name = "NaN", ipaddr = "0.0.0.0", simple = True, withinblock = False ):
        self.id = id
        self.name = name
        self.ipaddr = ipaddr
        self.simple = simple
        self.withinblock = withinblock

class Page:
    def __init__( self, id = -1, name = "NaN", ns = 0 ):
        self.id = id
        self.name = name
        self.ns = ns

class Revision:
    def __init__( 
        self, 
        id = -1, 
        page = Page(), 
        timestamp = datetime.datetime( 9999, 12, 31, 23, 59, 59 ), 
        editor = Editor(), 
        comment = "NaN", 
        currtext = "NaN", 
        currtextbytesize = "NaN", 
        currtextcharsize = "NaN", 
        revbytesize = "NaN", 
        revcharsize = "NaN", 
        previd = -1, 
        minor = 0,
        reverted = "NaN",
        reverting = "NaN",
        addcharsize = "NaN",
        addtradcharsize = "NaN" ):
        self.id = id
        self.page = page
        self.timestamp = timestamp
        self.editor = editor
        self.comment = comment
        self.currtext = currtext
        self.currtextbytesize = currtextbytesize
        self.currtextcharsize = currtextcharsize
        self.revbytesize = revbytesize
        self.revcharsize = revcharsize
        self.previd = previd
        self.minor = 0
        self.reverted = reverted
        self.reverting = reverting
        self.addcharsize = addcharsize
        self.addtradcharsize = addtradcharsize
