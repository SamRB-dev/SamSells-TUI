# -*- coding: utf-8 -*-
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.prompt import Prompt
from xml.dom import minidom
import xml.etree.ElementTree as ET
import os
import platform
import sys
import datetime

'''
	Features:
		1. Inventories > Add items > show items > search.
		3. make sales
'''
class SamSells:
	def __init__(self):
		'''
		[bright_green]Github[/bright_green]:
		'''
		self.console = Console()
		self.OS = platform.system()
		self.XML = "Inventory.xml"
		self.GITHUB = "https://github.com/SamRB-dev/SamSells-TUI"
		self.XMLWrite = ET.parse(self.XML)
		self.Cross = ":cross_mark:"
		self.CheckMark = ":white_check_mark:"
		self.Info = ":information:"
		self.banner = f"""		                    
_____           _____     _ _     
    |   __|___ _____|   __|___| | |___ 
    |__   | .'|     |__   | -_| | |_ -|
    |_____|__,|_|_|_|_____|___|_|_|___|
"""
		self.ID = None

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
		self.console.print(Panel(menu,title="Menu",subtitle=self.GITHUB))
		
	def __InventoryMenu(self) -> None:
		menu = f"""
			[blue][1][/blue] [dark_violet]Products[/dark_violet]
			[blue][2][/blue] [dark_violet]New Stocks[/dark_violet]
			[blue][3][/blue] [dark_violet]Remove Stocks[/dark_violet] 
			[blue][4][/blue] [dark_violet]Search Items[/dark_violet]
		"""
		self.__ScrnClear()
		self.__Banner()
		self.console.print(Panel(menu,title='Inventory',subtitle=self.GITHUB))
	
	def __ShowInventory(self):
		# Variables
		menu = f"""
[blue][1][/blue] [dark_violet]Products[/dark_violet] [red] * [/red] 
[blue][2][/blue] [dark_violet]New Stocks[/dark_violet]
[blue][3][/blue] [dark_violet]Remove Stocks[/dark_violet]


[dark_violet]DB[/dark_violet]: [blue]Inventory.xml[/blue]
[dark_violet]Time[/dark_violet]: [blue]{datetime.datetime.now()}[/blue]
		"""

		# Creating the objects
		table = Table(title="Products",highlight=True,expand=True)
		layout = Layout()
		
		# Creating the column
		table.add_column("id",style='blue',justify='center')
		table.add_column("Product",style='blue',justify='center')
		table.add_column("Category",justify='center')
		table.add_column("In Stock",justify='center')
		table.add_column("Price",justify='center',style='#af00d7 bold')

		# Creating the rows
		xml = minidom.parse(self.XML)
		products = xml.getElementsByTagName('product')
		for product in products:
			proid = product.attributes['id'].value
			self.ID = proid
			category = product.attributes['category'].value
			name = product.attributes['name'].value
			quantity = product.attributes['quantity'].value
			price = f"{product.attributes['price'].value} tk"
			table.add_row(proid,name,category,quantity,price)

		# Creating layout
		layout.split_column(
			Layout(Panel(self.banner,subtitle=self.GITHUB),size=10),
			Layout(name='Main'),
		)

		layout['Main'].split_row(
				Layout(Panel(menu,title='Menu'),name='Menu',size=35), 
				Layout(table),
		)
		self.console.print(layout,justify='center')

	def __AddItem(self):
		self.console.print(Panel(self.banner),justify='center')
		category = Prompt.ask("Category",default="unkown").lower()
		name = Prompt.ask("Product Name").lower()
		quantity = Prompt.ask("Stock")
		price = Prompt.ask("Price")

		# Adding to the xml
		root = self.XMLWrite.getroot() # XML function
		node = ET.SubElement(root,"product") # For Adding Subnode
		node.set("id",str(int(self.ID)+1)) # Setting the id attribute
		node.set("category",category) # Setting the attribute
		node.set("name",name) # Setting the attribute
		node.set("quantity",str(quantity)) # Setting the attribute
		node.set("price",str(price)) # Setting the attribute
		ET.ElementTree(root).write(self.XML) # For Saving the subnode in xml
		self.console.print(f"{self.CheckMark} [blue]Item Has Been Stocked[/blue]")

	def __Change(self,n): #Greedy
		changes = [1,2,5,10,20,50,100,200,500,1000]
		size = len(changes)
		notes = []
		i = size - 1
		while (i >= 0):
			while(n >= changes[i]):
				n -= changes[i]
				notes.append(changes[i])
			i -= 1
		self.console.print(f"{self.CheckMark} [blue]Notes[/blue]: [dark_violet]{notes}[/dark_violet]")

	def __SearchItems(self):
		self.console.print(self.banner,justify='center')
		category = Prompt.ask("Search Category",default='notebook')

		# Creating table
		table = Table(title=f'{category.capitalize()}',highlight=True,expand=True)
		table.add_column("id",style='blue',justify='center')
		table.add_column("Name",style='blue',justify='center')
		table.add_column("In Stock",style='blue',justify='center')
		table.add_column("Price",style='blue',justify='center')
		
		# Iterating over the Product instances
		root = self.XMLWrite.getroot()
		for item in root.iter('product'):
			itemct = item.get('category')
			if (itemct == category):
				proid = item.get("id")
				name = item.get("name")
				stock = item.get("quantity")
				price = item.get("price")
				table.add_row(proid,name,stock,price)
		self.console.print(table)

	def __Sells(self):
		total = 0
		root = self.XMLWrite.getroot()

		# Table
		table = Table(title='Products',highlight=True,expand=True)
		table.add_column("id",style='blue',justify='center')
		table.add_column("Product",style='blue',justify='center')
		table.add_column("Category",justify='center')
		table.add_column("In Stock",justify='center')
		table.add_column("Price",justify='center',style='#af00d7 bold')

		# Products
		root = self.XMLWrite.getroot()
		for item in root.iter('product'):
			itemct = item.get('category')
			proid = item.get("id")
			name = item.get("name")
			stock = item.get("quantity")
			price = item.get("price")
			table.add_row(proid,name,itemct,stock,price)
		self.console.print(table)

		# Main calc
		items = Prompt.ask(f"{self.Info} Total Items")
		for i in range(int(items)):
			pid = Prompt.ask(f"{self.Info} Product ID")
			for itm in root.iter('product'):
				itmid = itm.get("id")
				if itmid == pid:
					self.console.print(f"{self.CheckMark} [dark_violet]Item Found[/dark_violet]")
					price = itm.get("price")
					total += int(price)
				else:
					continue
		# Print
		self.console.print(f"[dark_violet]Total Price[/dark_violet]: [blue]{total}[/blue]")
		amount = int(Prompt.ask(f"{self.Info} Amount Given"))
		change = total - amount if (total > amount) else (amount - total)
		self.console.print(f"{self.Info} Change: [dark_violet]{change}[/dark_violet]")
		self.__Change(change)

	def __RemoveItems(self):
		root = self.XMLWrite.getroot()
		# Table
		table = Table(title='Products',highlight=True,expand=True)
		table.add_column("id",style='blue',justify='center')
		table.add_column("Product",style='blue',justify='center')
		table.add_column("Category",justify='center')
		table.add_column("In Stock",justify='center')
		table.add_column("Price",justify='center',style='#af00d7 bold')
		# Products
		root = self.XMLWrite.getroot()
		for item in root.iter('product'):
			itemct = item.get('category')
			proid = item.get("id")
			name = item.get("name")
			stock = item.get("quantity")
			price = item.get("price")
			table.add_row(proid,name,itemct,stock,price)
		self.console.print(table)

		# Deleting the node from XML
		pid = Prompt.ask("Product ID")
		for item in root.iter('product'):
			# Matching if the pid == xpid
			xpid = item.get("id")
			if (pid == xpid):
				root.remove(item)
				ET.ElementTree(root).write(self.XML)
				self.console.print("[dark_violet]ITEM HAS BEEN DELETED[/dark_violet]")
				break

	def App(self):
		while True:
			try:
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
						cntnue = Prompt.ask("Continue ?",choices=['yes','no'],default='yes')
						if cntnue == 'no':
							break
					elif optinv == 2: 
						self.__ScrnClear()
						self.__AddItem()
						cntnue = Prompt.ask("Continue ?",choices=['yes','no'],default='yes')
						if cntnue == 'no':
							break
					elif optinv == 3:
						self.__ScrnClear()
						self.__RemoveItems()
						cntnue = Prompt.ask("Continue ?",choices=['yes','no'],default='yes')
						if cntnue == 'no':
							break
					elif optinv == 4:
						self.__ScrnClear()
						self.__SearchItems()
						cntnue = Prompt.ask("Continue ?",choices=['yes','no'],default='yes')
						if cntnue == 'no':
							break
				elif opt == 3:
					self.__ScrnClear()
					self.__Banner()
					self.__Sells()
					cntnue = Prompt.ask("Continue ?",choices=['yes','no'],default='yes')
					if cntnue == 'no':
						break
				else:
					sys.exit(0)
			except Exception as err:
				self.console.print(f"[red]{self.Cross}[/red] [blue]{err}[/blue]")
				cntnue = Prompt.ask("Continue ?",choices=['yes','no'],default='yes')
				if cntnue == 'no':
					break

if __name__ == '__main__':
	shop = SamSells()
	shop.App()
	
