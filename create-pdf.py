from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import sys
import os
import platform

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

    def drawString(self, text, x, y):
        self.last_line += y
        self.doc.drawString(x*inch,-self.last_line*inch,text)
       
    def save(self):
        self.doc.save()

if __name__ == "__main__":
    root_directory = os.path.abspath(sys.argv[1])
    print("Creating catalogue for {}".format(root_directory))
  
    # create leveled outline of directory
    created_outline = {}
    path = os.walk(root_directory)
    for root, directories, files in path:
        relative_path = root.replace(root_directory,"")
        path_level = relative_path.count(PATH_SEPARATOR)
        if not path_level in created_outline:
            created_outline[path_level] = []
        created_outline[path_level].append(root)

    # create empty document
    doc = Document(canvas.Canvas("{}.pdf".format(os.path.basename(root_directory))))
       
    # create content pages
    for key in created_outline:
        created_outline[key].sort()

        # for each directory
        for path in created_outline[key]:
            print("level {}: {}".format(key, path))

            # add titile
            doc.drawString(os.path.basename(path),0,0)
            
            # add directory listing
            doc.drawString("Directory list:",0,0.5)
            
            items = os.listdir(path)
            for i in range(0, len(items)):
                item = items[i]
                item_path = os.path.join(path, item)
               
                # add subpage links
                if os.path.isdir(item_path):
                    doc.drawString("DIR: {}".format(item_path),0,0.3)

                # add file list
                if os.path.isfile(item_path):
                    doc.drawString("FILE: {}".format(item_path),0,0.3)

                # add info
                
                if i == 20:
                    doc.newPage()
                
                i += 1
            
            # close the page
            doc.newPage()

    doc.save()
    
# c = canvas.Canvas("hello.pdf")
# c.drawString(72,72,"Page 1")
# c.showPage()
# c.drawString(72,72,"Page 2")
# c.showPage()

# createInfoPage(c)

# c.doForm("InfoPageForm")
# c.showPage()
# c.doForm("InfoPageForm")
# c.showPage()

# c.save()