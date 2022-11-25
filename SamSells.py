# -*- coding: utf-8 -*-
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from xml.dom import minidom
import os
import platform
import sys

'''
	Features:
		1. Inventories > Add items > show items > delete items.
		2. Sales history
		3. make sales
		4. Export Sales History
'''
class SamSells:
	def __init__(self):
		self.console = Console()
		self.OS = platform.system()
		self.XML = "Inventory.xml"
		self.banner = """		                    
_____           _____     _ _     
    |   __|___ _____|   __|___| | |___ 
    |__   | .'|     |__   | -_| | |_ -|
    |_____|__,|_|_|_|_____|___|_|_|___|
	[bright_green]TUI[/bright_green] By [dark_violet]Sadim Rahman Badhan[/dark_violet]
"""

	def __Banner(self) -> None:
		self.console.print(self.banner,style='blue',justify='center')
		
	def __ScrnClear(self):
		command = "clear" if self.OS == 'Linux' else 'cls'
		os.system(command)

	def __Menu(self) -> None:
		menu = """
			[blue][1][/blue] [dark_violet]Inventory[/dark_violet]
			[blue][2][/blue] [dark_violet]Sales History[/dark_violet]
			[blue][3][/blue] [dark_violet]Sells[/dark_violet]
			[blue][4][/blue] [dark_violet]Exit[/dark_violet]
		"""
		self.console.print(Panel(menu,title="Menu"))
		
	def __InventoryMenu(self) -> None:
		menu = """
			[blue][1][/blue] [dark_violet]Products[/dark_violet]
			[blue][2][/blue] [dark_violet]New Stocks[/dark_violet]
			[blue][3][/blue] [dark_violet]Remove Stocks[/dark_violet]
		"""
		self.__ScrnClear()
		self.__Banner()
		self.console.print(Panel(menu,title='Inventory'))
	
	def __ShowInventory(self):
		# Variables
		menu = """
[blue][1][/blue] [dark_violet]Products[/dark_violet] [red] * [/red] 
[blue][2][/blue] [dark_violet]New Stocks[/dark_violet]
[blue][3][/blue] [dark_violet]Remove Stocks[/dark_violet]


[dark_violet]DB[/dark_violet]: [blue]Inventory.xml[/blue]
		"""

		# Creating the objects
		table = Table(title="Products",highlight=True,expand=True)
		layout = Layout()
		
		# Creating the column
		table.add_column("Product",style='blue',justify='center')
		table.add_column("Category",justify='center')
		table.add_column("In Stock",justify='center')
		table.add_column("Price",justify='center',style='#af00d7 bold')

		# Creating the rows
		xml = minidom.parse(self.XML)
		products = xml.getElementsByTagName('product')
		for product in products:
			category = product.attributes['category'].value
			name = product.attributes['name'].value
			quantity = product.attributes['quantity'].value
			price = f"{product.attributes['price'].value}tk"
			table.add_row(name,category,quantity,price)

		# Creating layout
		layout.split_column(
			Layout(Panel(self.banner),size=10),
			Layout(name='Main'),
		)

		layout['Main'].split_row(
				Layout(Panel(menu,title='Menu'),name='Menu',size=35), 
				Layout(table),
		)
		self.console.print(layout,justify='center')

	def App(self):
		self.__ScrnClear()
		self.__Banner()
		self.__Menu()
		opt = int(input("\t\t\t\t >>> "))
		if opt == 1:
			self.__InventoryMenu()
			optinv = int(input("\t\t\t >>> "))
			if optinv == 1:
				self.__ScrnClear()
				self.__ShowInventory()
		else:
			sys.exit(0)
		

if __name__ == '__main__':
	shop = SamSells()
	shop.App()
	
