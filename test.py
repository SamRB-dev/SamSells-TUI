import xml.etree.ElementTree as ET

# Add Item
xml = ET.parse("Inventory.xml")
root = xml.getroot()
# new = ET.SubElement(root,"product")
# new.set("id",'4')
# new.set("category","notebook")
# new.set("name","Matador's Notebook")
# new.set("quantity","75")
# new.set("price","200")
# ET.ElementTree(root).write("Inventory.xml")

# Search
for item in root.iter('product'):
    category = item.get("category")
    if category == "notebook":
        print(category.capitalize())