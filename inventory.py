
#========The beginning of the class==========

class Shoe:
    def __init__(self, country, code, product, cost, quantity):
          #  Class constructor method with prescribed instance variables, including default attribute settings.
          self.country = country
          self.code = code 
          self.product = product 
          self.cost = cost 
          self.quantity = quantity 

    def get_cost(self):
      #  Returns cost of object.
        return self.cost

    def get_quantity(self):
      #  Returns quantity of object.
        return self.quantity

    def set_quantity(self, units):
        #  Sets new quanitiy of units for object.
        self.quantity = units + "\n"
      
    def __str__(self):
        #  Returns a string representation of object.
        output =   "\n▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\n\n"
        output +=  f"Country: \033[94m{self.country}\033[0m\n"
        output +=  f"Code: \033[94m{self.code}\033[0m\n"
        output +=  f"Product: \033[94m{self.product}\033[0m\n"
        output +=  f"Cost: \033[94m{self.cost}\033[0m\n"
        output +=  f"Quantity: \033[94m{self.quantity}\033[0m\n"
        output +=  "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\n"
        return output

      
#==========Functions outside the class==============
      
def read_shoes_data():
#  Reads shoe data from file.
  global shoe_list, tbl_list  #  Allows variable to be used in other functions.
  shoe_list = []
  tbl_list = []
  try:  #  Executes block if file exists and data valid.
    with open('inventory.txt', 'r+') as f:
      for count, line in enumerate(f):
        fdata = line.split(',')  #  Splits line data into list elements.
        tbl_list.append(fdata)  #  Appends list used to display data.
        #  List comprehension to convert 'fdata' list elements into initialised 'Shoe' object attribute values.
        shoe_list += [Shoe(country, code, product, cost, quantity) for country, code, product, cost, quantity in [(fdata[0], fdata[1], fdata[2], fdata[3], fdata[4])]]
  except Exception:  #  If no file or data invalid, error message displayed.
    print("No file data or file data corrupt...")


def capture_shoes():
#  Captures item details and updates object list.
  with open('inventory.txt', 'a') as f:
    f.write(f"\n")  #  Initially sets file pointer on a new line at end of file.
  f.close()
  while True:
    try:
      print("Please enter shoe item details: \n")
      #  User promted to enter corresponding variable values.
      country = input("Enter country: ")
      code = input("Enter code: ")
      product = input("Enter product: ")
      cost = int(input("Enter cost: "))
      quantity = int(input("Enter quantity: "))
      shoe_list.append(Shoe(country, code, product, str(cost), str(quantity)))  #  Adds new object to list.
      with open('inventory.txt', 'a') as f:
        f.write(f"{country},{code},{product},{str(cost)},{str(quantity)}")  #  Writes update to file.
      f.close()
      print("\n\033[92mItem added...\033[0m\n")
      break
    except Exception:
      print("\nPlease enter a number for cost and quantity...\n")
    

def view_all():
  #  Uses tabulate function to display shoe information in a table.
  print(tabulate(tbl_list, headers="firstrow", showindex='always', tablefmt=""))
  

def re_stock():
  #  Finds shoe with lowest units and gives user option to restock.
  qty_list = []
  tbl_list.pop(0)  #  Removes string value passed on from file.
  for num, value in enumerate(tbl_list):
    qty_list.append(int(tbl_list[num][4]))  #  Appends integer vlaues for each shoe quantity.
  #  Finds lowest quantity with 'min' function and uses 'index' function to find corresponding 'shoe_list' object.
  item = (qty_list.index(min(qty_list)) + 1)  
  print("\033[92mThe following item is running low in stock...\033[0m")
  print(shoe_list[item].__str__())
  while True:
    user_choice = str(input("\nWould you like to restock y/n:  "))
    if user_choice.lower() == 'y':
      try:  #  Tests for integer input.
        units = int(input("\nHow many units would you like to add: "))
        units += int(shoe_list[item].quantity)  #  Calculates total units after restock.
        shoe_list[item].set_quantity(str(units))  #  Sets new quantity value for 'shoe_list' object.
        print(shoe_list[item].__str__())
        update_file()
        break
      except Exception:
        print("\nPlease enter a number...")
    elif user_choice.lower() == 'n':
      break
    else:
      print("\nPlease enter 'y' or 'n': ")

      
def search_shoe():
  #  Finds and displays shoe with matching search code.
  user_choice = input("Please enter SKU code to search item: ")
  for item, obj in enumerate(shoe_list):
    if user_choice in obj.code:
      print(shoe_list[item].__str__())
      
    
def value_per_item():
  #  Calculates and displays the total value for each item.
  value_list = []
  for item in range(1, len(shoe_list)):  
    total_value = int(shoe_list[item].get_cost()) * int(shoe_list[item].get_quantity()) 
    value_data = (shoe_list[item].product, shoe_list[item].code, str(total_value))  
    value_list.append(value_data)
  print(tabulate(value_list, headers=["Product", "Code", "Value"], showindex='always', tablefmt=""))
    

def highest_qty():
  #  Finds shoe with highest quantity and displays it as on sale.
  qty_list = []
  tbl_list.pop(0)  #  Removes string value passed on from file.
  for num, value in enumerate(tbl_list):
    qty_list.append(int(tbl_list[num][4]))  #  Appends integer vlaues for each shoe quantity.
    #  Finds highest quantity with 'max' function and uses 'index' function to find corresponding 'shoe_list' object.
  item = (qty_list.index(max(qty_list)) + 1)  
  print("\033[92mThe following item is on sale this week...\033[0m")
  print(shoe_list[item].__str__())


def update_file():
#  Writes updated object list to file.
  with open('inventory.txt', 'w') as f:
    for obj in shoe_list:
      f.write(obj.country + ',' + obj.code + ',' + obj.product + ',' + obj.cost + ',' + obj.quantity)
  f.close()
  print("\n\033[92mFile updated...\033[0m\n")
  
  

#==========Main Menu=============
import os 
from tabulate import tabulate
menu_select = ""
while True:
  os.system('clear')
  read_shoes_data()
  print("\033[92m============================= WELCOME TO THE NIKE STORE ================================\n\033[0m")
  menu_select = input("""====================================== MAIN MENU =======================================
  
  1 - capture item
  2 - view all
  3 - restock item
  4 - search item
  5 - item stock value
  6 - sale item
  q - quit
  
  Please select an option:
  \033[94m» \033[0m""")
  
  if menu_select == '1':
    os.system('clear')
    capture_shoes()
    
  elif menu_select == '2':
    os.system('clear')
    view_all()
    hold = input("""\n                    ---------- press any key ----------""")
  
  elif menu_select == '3':
    os.system('clear')
    re_stock()
    hold = input("""\n                    ---------- press any key ----------""")

  elif menu_select == '4':
    os.system('clear')
    search_shoe()
    hold = input("""\n                    ---------- press any key ----------""")
  
  elif menu_select == '5':
    os.system('clear')
    value_per_item()
    update_file()
    hold = input("""\n                    ---------- press any key ----------""")
  
  elif menu_select == '6':
    os.system('clear')
    highest_qty()
    hold = input("""\n                    ---------- press any key ----------""")

  elif menu_select == 'q':
    os.system('clear')
    print("\n\033[92mLive long and prosper...\033[0m")
    break
    
  else: 
    print("\n\033[92mPlease enter a valid selection...\033[0m")
    hold = input("""\n                    ---------- press any key ----------""")
  
