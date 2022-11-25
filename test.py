# from xml.dom import minidom
# xml = minidom.parse('Inventory.xml')
# products = xml.getElementsByTagName('product')
# for product in products:
# 	category = product.attributes['category'].value
# 	name = product.attributes['name'].value
# 	quantity = product.attributes['quantity'].value
# 	price = product.attributes['price'].value
# 	print(f"{name} {category} {quantity} ${price}")
from rich import print
from rich.console import Group
from rich.panel import Panel

panel_group = Group(
    Panel("Hello", style="on blue"),
    Panel("World", style="on red"),
)
print(Panel(panel_group))