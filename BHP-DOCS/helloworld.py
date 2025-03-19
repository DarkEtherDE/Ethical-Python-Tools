def pySwitch(item, inputVal):
    match inputVal:
        case '1': 
            print('Pizza')
        case '2':
            print('Sandwhich') 
        case _:
            print("Try again")
           
def main():
    menuItems = {'Food':['Pizza', 'Sphagetti'],'Drink':['Sprite','Coke','Diet Pepsi'],'Dessert':['Pie','Ice Cream'] }

    for item in menuItems:
        print(item, menuItems[item])  
    
if __name__ == '__main__':
    main()