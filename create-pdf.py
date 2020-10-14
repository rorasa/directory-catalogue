from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import toml
import sys
import os
import platform

if len(sys.argv) < 3:
    catalogue_name = "Directory Catalogue"
else:
    catalogue_name = sys.argv[2]

if len(sys.argv) < 2:
    print("no input directory given")
    sys.exit(-1)

if platform.system() == "Windows":
    PATH_SEPARATOR = "\\"
else:
    PATH_SEPARATOR = '/'

PAGE_MARGIN_TOP = 1
PAGE_MARGIN_LEFT = 1

class Document:
    def __init__(self, doc):
        self.doc = doc
        self.origin_x = PAGE_MARGIN_LEFT*inch
        self.origin_y = (11.75-PAGE_MARGIN_TOP)*inch
        self.doc.translate(self.origin_x,self.origin_y)
        self.last_line = 0

    def newPage(self):
        self.doc.showPage()
        self.doc.translate(self.origin_x,self.origin_y)
        self.last_line = 0

    def addBookmark(self, key):
        self.doc.bookmarkPage(key)

    def text(self, text, x, y):
        self.last_line += y
        self.doc.drawString(x*inch,-self.last_line*inch,text)

    def link(self, text, x, y, destination):
        self.text(text, x, y)        
        self.doc.linkRect(text, destination, (0,
            -self.last_line*inch, 
            (8.25-2*PAGE_MARGIN_LEFT)*inch, 
            -(self.last_line*inch) + 15),
        thickness=2, 
        Border='[1 1 1]')

    def title(self, text, x, y):
        self.doc.saveState()
        self.doc.setFont("Helvetica", 16)
        self.text(text, x, y)
        self.doc.restoreState()
        
    def save(self):
        self.doc.save()

def createTagPages(document, tag_list):
    # create tag list page
    document.title("Tag List", 0, 0)
    document.addBookmark("tag_list")

    key_list = list(tag_list)
    key_list.sort()
    for i in range(0, len(key_list)):
        key = key_list[i]
        document.link(key, 0, 0.3, key)

        if (i+1)%20 == 0:
            document.newPage()
        i += 1
        
    document.newPage()

    # create tag pages
    for key in key_list:
        document.title("TAG: {}".format(key), 0, 0)
        document.addBookmark(key)

        item_list = tag_list[key]
        item_list.sort()
        for i in range(0, len(item_list)):
            item_path = item_list[i]
            document.link(os.path.basename(item_path), 0, 0.3, item_path)

            if (i+1)%20 == 0:
                document.newPage()
            i+=1

        document.newPage()
        
        # add title
        # document.title("TAG: {}".format(key), 0, 0)
        # document.addBookmark()


def createDirectoryPages(document, created_outline):
    for key in created_outline:
        created_outline[key].sort()

        # for each directory
        for path in created_outline[key]:
            print("level {}: {}".format(key, path))

            # add title
            document.title("DIR: {}".format(os.path.basename(path)),0,0)
            document.addBookmark(path)
            
            # add directory listing
            document.text("Directory list:",0,0.5)
            
            items = os.listdir(path)
            for i in range(0, len(items)):
                item = items[i]
                item_path = os.path.join(path, item)
               
                # add subpage links
                if os.path.isdir(item_path):
                    document.link("DIR: {}".format(item_path),0,0.3, item_path)

                # add file list
                if os.path.isfile(item_path):
                    document.text("FILE: {}".format(item_path),0,0.3)
                
                if (i+1)%20 == 0:
                    document.newPage()
                
                i += 1

            # add info
            # info from toml file goes here
            if "info.toml" in items:
                doc.text("Metadata",0,0.5)
            
            # close the page
            doc.newPage()

if __name__ == "__main__":
    root_directory = os.path.abspath(sys.argv[1])
    print("Creating catalogue for {}".format(root_directory))
  
    # analyse directory
    created_outline = {}
    tag_list = {}
    fav_list = []

    path = os.walk(root_directory)
    for root, directories, files in path:
        relative_path = root.replace(root_directory,"")
        path_level = relative_path.count(PATH_SEPARATOR)
        if not path_level in created_outline:
            created_outline[path_level] = []
        created_outline[path_level].append(root)

        if "info.toml" in files:
            with open(os.path.join(root,"info.toml")) as meta_file:
                metadata = toml.loads(meta_file.read())

            tags = metadata['tag']
            for tag in tags:
                if not tag in tag_list:
                    tag_list[tag] = []
                tag_list[tag].append(root)

            if metadata['favourite']:
                fav_list.append(root)

    # create empty document
    doc = Document(canvas.Canvas("{}.pdf".format(os.path.basename(root_directory))))
       
    # add entry page
    doc.title(catalogue_name,0,0)
    doc.text("Favourite list", 0, 0.5)
    doc.link("Tag list",0,0.5, "tag_list")
    doc.link("Directory tree",0,0.5, root_directory)
    doc.newPage()

    # creat tag pages
    createTagPages(doc, tag_list)

    # create directory pages
    createDirectoryPages(doc, created_outline)
    
    # save output file
    doc.save()
