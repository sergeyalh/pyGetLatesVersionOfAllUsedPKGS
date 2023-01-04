import xml.etree.ElementTree as ET
import subprocess

# parse the XML file
tree = ET.parse('example.xml')

# get the root element
root = tree.getroot()

f = open("lastVersJS.txt", "w")
i = 1
# iterate over the <library> elements
for library in root.findall('library'):
  # get the 'name' element
  version = library.find('version').text
  group = library.find('group').text
  occurrences = library.find('occurrences')
  if occurrences is not None:
    products = occurrences.findall('product')
    for product in products:
      proj = product.find('project').text
      # Do something with the product element
      if ("(transitiveDependency)" not in proj):
        try:
          result = subprocess.run(['npm', 'view', group, 'version'], stdout=subprocess.PIPE, check=True)
          result_string = result.stdout.decode("utf-8")
          if (result.returncode == 0):
            lines = result.stdout.splitlines()
            isUpdated = (version.encode() == lines[0])
            if isUpdated:
              print(version.encode(), " ", lines[0], "  But is it equal?!", isUpdated )
            else:
              str = "group:" + group + " " + "in proj:" + proj + " " + "version:" + version + " last Version is: "  + result_string
              f.write(str)
              print(i, " updates needed")
              i = i + 1
        except subprocess.CalledProcessError:
          print("THIS IS JAVA DUDE!")


