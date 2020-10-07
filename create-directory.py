import sys
import os

if len(sys.argv) < 2:
    print("no input directory given")
    sys.exit(-1)

root_directory = os.path.abspath(sys.argv[1])
print("Creating catalogue for {}".format(root_directory))

path = os.walk(root_directory)
for root, directories, files in path:
    print(root)
    # print(directories)
    # print(files)
    if "info.toml" in files:
        print("This is a leaf page")

    # 1. create new page for root
    # 2. create a link for each directory
    # 3. create a list of files
    # 4. if root contain info.toml, use them to update the infomation in the page
    # 5. generate tags page containing the list of all pages with a tag
    # 6. generate a favorite page