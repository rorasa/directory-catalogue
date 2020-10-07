import sys
import os
import shutil

if len(sys.argv) < 3:
    catalogue_name = "Directory Catalogue"
else:
    catalogue_name = sys.argv[2]

if len(sys.argv) < 2:
    print("no input directory given")
    sys.exit(-1)

root_directory = os.path.abspath(sys.argv[1])
print("Creating catalogue for {}".format(root_directory))


created_pages = []

path = os.walk(root_directory)

for root, directories, files in path:
    if root == root_directory:
        slug = "home"
        title = "Home"
    else:
        slug = os.path.basename(root).lower().replace(' ','-')
        title = os.path.basename(root)

    # create a new page
    page = '<div class="page" id="{}">\n'.format(slug)
    
    # add titile
    page += '<h1>{}</h1>\n'.format(title)

    # add subpage links
    if len(directories)>0:
        directories.sort()
        page += '<h2>Subpages</h2>\n'
        page += '<ul>\n' 
        for directory in directories:
            directory_slug = directory.lower().replace(' ','-')
            page += """<li><a href="#" onclick="goToPage($('#{}'))">{}</a></li>\n""".format(directory_slug, directory)
        page += '</ul>\n' 

    # add file list
    if len(files)>0:
        page += '<h2>File list</h2>\n'
        page += '<ul>\n'
        for f in files:
            page += """<li>{}</li>\n""".format(f)
        page += '</ul>\n'

    # close the page
    page += '</div>\n'

    created_pages.append(page)
    
    if "info.toml" in files:
        pass

    # 1. create new page for root
    # 2. create a link for each directory
    # 3. create a list of files
    # 4. if root contain info.toml, use them to update the infomation in the page
    # 5. generate tags page containing the list of all pages with a tag
    # 6. generate a favorite page

if os.path.exists('public'):
    shutil.rmtree('public')
os.mkdir('public')
shutil.copy('template/default.css', 'public/default.css')
shutil.copy('template/zepto.min.js', 'public/zepto.min.js')

with open('public/catalogue.html', 'w') as output:
    with open('template/base.html') as template:
        base_file = template.read()
        base_file = base_file.replace("{{title}}", catalogue_name)
        base_file = base_file.replace("{{body}}", "\n".join(created_pages))
        output.write(base_file)

print("Finished building catalogue at {}".format('public/'))
    