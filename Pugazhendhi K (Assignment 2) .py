# Pizza delivery management system

import time
from tabulate import tabulate
from datetime import date
global offer, coup, order_id

def user(off, coup):
        global pizza_instock,order_id
        d= {}
        p_name= []
        prod_id= []
        small= []
        medium= []
        large= []
        for i in pizza_instock:
          if pizza_instock[i]['Stock'] > 0:
            p_name.append(i)
            prod_id.append(pizza_instock[i]['Product ID'])
            small.append(pizza_instock[i]['Small'])
            medium.append(pizza_instock[i]['Medium'])
            large.append(pizza_instock[i]['Large'])
        if len(prod_id)== 0:
          print('Sorry, Today\'s sale is over!')
        else:
          print('\n')
          for word in ' MENU '.split('#'):
            print(f'{word:=^88}')
          print()
          d['Product ID']= prod_id
          d['Pizza Name']= p_name
          d['Small (in ₹)']= small
          d['Medium (in ₹)']= medium
          d['Large (in ₹)']= large
          print(tabulate(d, headers= 'keys',tablefmt= 'psql'))
        print()
        print("TODAY'S OFFER")
        print()
        if str(off).split()[0]!='Sorry,':
                  for i in off[0]:
                        print(i)
                  print()
                  op= input('Do you want to go with offer (yes/no) ? ')
                  while True:
                    if op[1]=='e':
                        print('Offer selected')
                        a= 1
                        for i in off[3]:
                          for j in pizza_instock:
                            if i[0][0].lower()== j[0].lower():
                              pizza_instock[j]['Stock']-=i[1]
                        break
                    elif op[1]=='o':
                        a= 0
                        break
                    else:
                        print('INVALID INPUT')
                        op= input('Do you want to go with offer (yes/no) ? ')
        else:
                  a=0
                  print(off)
                  
        print()
        ch= input('Do you want to order anymore (yes/no) ? ')
        while True:
            if ch[1]=='e':
                t_order= []
                sa_order= []
                p_type = pizza_type()
                print()
                ch= input('Do you want to add toppings for your ordered pizzas ? (yes/no)')
                while True:
                  print()
                  if ch[1]=='e':
                    p_topp = pizza_toppings(p_type)
                    break
                  elif ch[1]=='o':
                    for i in p_type:
                      t_order.append(False)
                    p_topp= t_order
                    break
                  else:
                    print('INVALID INPUT')
                    ch= input('Do you want to add toppings for your ordered pizzas ? (yes/no)')

                print()
                ch= input('Do you want to add sauce for your ordered pizzas ? (yes/no)')
                while True:
                  print()
                  if ch[1]=='e':
                    p_sauce = pizza_sauce(p_type)
                    break
                  elif ch[1]=='o':
                    for i in p_type:
                      sa_order.append(False)
                    p_sauce= sa_order
                    break
                  else:
                    print('INVALID INPUT')
                    ch= input('Do you want to add sauce for your ordered pizzas ? (yes/no)')
                p_size = pizza_size(p_type,p_topp,p_sauce)
                break
            elif ch[1]=='o':
                p_size = [False]
                break
            else:
                print('INVALID INPUT')
                ch= input('Do you want to order anymore (yes/no) ? ')
        if a!=0 or p_size!=[False]:
            order_id+=1
            print()
            det= customer_details()
            print()
            amt = total_pay(a,off[1],off[2],det,p_size,order_id,coup)
        elif a== 0 and all(p_size)== False:
            print('Oops! you haven\'t placed any order')
            ch= input('Do you wish to order ? ')
            if ch[1]=='e':
                user(off,coup)
            else:
                print('Thank you and visit again')


def total_pay(a,piz,price,det,p_size,order_id,coup):
  global pizza_instock,cust_det, pizza_toppings
  bill={'Item':[],'Topping':[],'Sauce':[],'Price (in Rs)':[]}
  amt= 0
  if a== 1:
      amt+= price
      bill['Item']= [piz]
      bill['Price (in Rs)'] =[amt]
      bill['Topping']= ['-']
      bill['Sauce']= ['-']
  if p_size != [False] :
    for i in p_size:
        for j in pizza_instock:
          if i[0][0][0].lower() == j[0].lower():
            bill['Item'].append(j)
            if i[0][1] != False:
                bill['Price (in Rs)'].append(pizza_instock[j][p_size[0][1]] + topping[i[0][1]])
                amt+= pizza_instock[j][p_size[0][1]] + topping[i[0][1]]
                bill['Topping'].append(i[0][1])
            else:
                bill['Price (in Rs)'].append(pizza_instock[j][p_size[0][1]])
                amt+= pizza_instock[j][p_size[0][1]]
                bill['Topping'].append('-')
            if i[0][2] != False:
                bill['Sauce'].append(i[0][2])
            else:
                bill['Sauce'].append('-')

  bill['Sauce'].append('------------------')
  bill['Price (in Rs)'].append('---------------')
  bill['Sauce'].append('SubTot :')
  bill['Price (in Rs)'].append(amt)  
  if 500< amt <= 1000:
    disc= '10%'
    dis= 0.01
    bill['Sauce'].append('Discount :')
    bill['Price (in Rs)'].append('10 %')
    amt= amt- amt*dis
  elif 1000< amt <= 1500:
    disc= '20%'
    dis= 0.02
    bill['Sauce'].append('Discount :')
    bill['Price (in Rs)'].append('20 %')
    amt= amt- amt*dis
  elif amt > 1500:
    if coup!= None:
      print('Congrats !!! You have won coupon')
      while True:
        ch= input('Do you want to unlock it ?')
        if ch[1]=='e':
          print('Coupon code : ',coup[0])
          while True:
            c= input('Enter your coupon code : ')
            if c == coup[0]:
              print('You have won a discount of',coup[1],'%')
              bill['Sauce'].append('Discount (Coupon) :')
              bill['Price (in Rs)'].append(str(coup[1])+'%')
              amt= amt-amt*(coup[1]/100)
              break
            else:
              print('INVALID Coupon code')
          break
        elif ch[1]=='o':
          print('Your coupon expired :(')
          break
        else:
          print('INVALID INPUT')
    else:
      disc= '25'
      dis= 0.25
      bill['Sauce'].append('Discount :')

      bill['Price (in Rs)'].append('25 %')
      amt= amt- amt*dis
  CGST= (2.5*amt)/100
  SGST_UTGST = (2.5*amt)/100
  total= amt+ CGST+ SGST_UTGST
  r_total= round(total)
  r= r_total-total
  bill['Sauce'].append('CGST @2.5% :')
  bill['Price (in Rs)'].append(round(CGST,2))
  bill['Sauce'].append('SGST/UTGST @2.5% :')
  bill['Price (in Rs)'].append(round(SGST_UTGST,2))
  bill['Sauce'].append('Rounding off :')
  bill['Price (in Rs)'].append(round(r,2))
  bill['Sauce'].append('------------------')
  bill['Price (in Rs)'].append('---------------')
  bill['Sauce'].append('Grand Total :')
  bill['Price (in Rs)'].append(r_total)
  for word in ' BILL '.split('#'):
    print(f'{word:=^65}')
  print()
  print('ORDER ID :',order_id)
  print()
  print('DATE :',date.today())
  print()
  print(tabulate(bill,headers= 'keys',numalign='left'))
  det['Amount']= r_total
  print()
  print('Please provide your ratings : ')
  print('1 star --> Need to be improved',
        '2 star --> Poor',
        '3 star --> Good',
        '4 star --> Better',
        '5 star --> Best',sep= '\n')
  r= input()
  det['Ratings']= r
  print()
  print('Your each word value a lot for us')
  print('Please provide your feedback : ')
  fb= input()
  f= fb.split('.')
  fe= ''
  for i in f:
      fe+= i+'\n'
  print()
  print('Thank you so much for your feedback')
  det['Feedback']= fe
  cus_det[order_id]= det
  print('Have a wonderful dine with Pizza :)')
  print()
  
def pizza_type() :
  l_order= []
  while True:
    n_piz= int(input('Enter no. of pizzas you want to order : '))
    while n_piz!=0:
        order_pizza= input('Enter the pizza type : ')
        for i in pizza_instock:
            if order_pizza[0].lower() == i[0].lower():
                qty= int(input('Enter the quantity : '))
                pizza_instock[i]['Stock'] -= qty
                for k in range(qty):
                  l_order.append(i)
        n_piz-=qty
    break
  return l_order

def pizza_size(p_type, p_topp, p_sause):
  s_order= []
  print()
  for i in zip(p_type, p_topp, p_sause):
        if i[0] != False:
            print('Pizza name :',i[0])
        else:
            print('Pizza name :',None)
        if i[1] != False:
            print('Topping :',i[1])
        else:
            print('Topping :',None)
        if i[2] != False:
            print('Sauce :',i[2])
        else:
            print('Sauce :',None)
        print()
        o_size= input('Enter the size (Small/Medium/Large): ')
        print()
        if o_size[1]=='m':
          size= 'Small'
        elif o_size[1]=='e':
          size= 'Medium'
        else:
          size= 'Large'
        s_order.append([i,size])
  print('Order placed !!!')
  return s_order

def pizza_toppings(p_type):
  global topping
  t_order= []
  t= {}
  topp= []
  cost= []
  
  for word in ' TOPPING MENU '.split('#'):
    print(f'{word:=^40}')
  print()
  for i in topping:
    topp.append(i)
    cost.append(topping[i])          
  t['Toppings']= topp
  t['Price (in ₹)']= cost
  print(tabulate(t, headers= 'keys',tablefmt= 'psql'))
  for i in p_type:
    while True:
              ch= input('Do you want us to add toppings for '+ i +' ? (yes/no)')
              if ch[1]=='e':
                print('Please enter the topping')
                p_t= input(i + ':' )
                for j in topping:
                  if j[0].lower()==p_t[0].lower():
                    t_order.append(j)
                break
              elif ch[1]=='o':
                print('No topping is selected')
                t_order.append(False)
                break
              else:
                print('INVALID INPUT')
  return t_order

def pizza_sauce(p_type):
  for word in ' SAUCE MENU '.split('#'):
    print(f'{word:=^40}')
  print()
  global sauce
  sa_order= []
  header= ['Sauce']
  print(tabulate(sauce,headers= header,tablefmt= 'psql'))
  for i in p_type :
    while True:
      ch= input('Do you want us to add sauce for '+ i +' ? (yes/no)')
      if ch[1]=='e':
        print('Please enter the sauce you want')
        s= input(i + ':')
        for j in sauce:
          for k in j:
            if k[0].lower() == s[0].lower():
              sa_order.append(k)
        break
      elif ch[1]== 'o':
        print('No sauce is selected')
        sa_order.append(False)
        break
      else:
        print('INVALID INPUT') 
  return sa_order
  
def customer_details():
    name= input('Enter your name : ')
    add= input('Enter your address : ')
    pin= int(input('Enter the pin code : '))
    city= input('Enter your city : ')
    state= input('Enter your state : ')
    ph_no= int(input('Enter your phone number : '))
    return {'Name': name, 'Address': add, 'Pincode': pin, 'City': city, 'State': state,'Phone number': ph_no}
  
def admin():
    global offer, coup
    op= 'yes'
    while op[0]=='y':
        print('1. Update the stocks',
              '2. Current instock',
              '3. Customer report',
              '4. Customer feedback',
              '5. Today\'s offer',
              '6. Change Coupon code',
              '7. Change the price / pizza ',
              '8. Exit',sep= '\n')
        ch= int(input('Enter your choice : '))
        if ch== 1:
            up= update_stocks()
        elif ch== 2:
            rep= stock_data()
        elif ch== 3:
            cus= customer_report()
        elif ch== 4:
            feedback= customer_feedback()
        elif ch== 5:
            offer= today_offer()
        elif ch== 6:
            coup= change_coupon()
        elif ch== 7:
            alt= alter_data()
        elif ch== 8:
            break
        else:
            print('INVALID INPUT')
            continue
        op= input('Do you want to continue ? (yes/no)')
                                  
def update_stocks():
    global pizza_instock
    ch= input('Do you want to update your stock ? (yes/no)') 
    while True:
        if ch[1] =='e':
            pizza_name= input('Enter the pizza name : ')
            if pizza_name not in pizza_instock:
                print('INVALID INPUT')
                
            for i in pizza_instock:
                if i[0]==pizza_name[0]:
                    cur_stock= print('Current stock : ',pizza_instock[i]['Stock'])
                    stock= int(input('How many pizzas to be added ? '))
                    pizza_instock[i]['Stock']+= stock
                    print('Updated successfully !!!')
                    break
            ch= input('Do you want to continue ? ')
            
        elif ch[1]=='o':
            break
        else:
            print('INVALID INPUT')
    print()
    print('UPDATED STOCK LIST')
    d= {}
    p_name= []
    prod_id= []
    stock= []
    for i in pizza_instock:
            p_name.append(i)
            prod_id.append(pizza_instock[i]['Product ID'])
            stock.append(pizza_instock[i]['Stock'])
          
    d['Product ID']= prod_id
    d['Pizza Name']= p_name
    d['Stock']= stock
    print(tabulate(d, headers= 'keys',tablefmt= 'psql'))
    
def stock_data():
    global pizza_instock
    print('CURRENT STOCK LIST')
    d= {}
    p_name= []
    prod_id= []
    stock= []
    for i in pizza_instock:
            p_name.append(i)
            prod_id.append(pizza_instock[i]['Product ID'])
            stock.append(pizza_instock[i]['Stock'])
          
    d['Product ID']= prod_id
    d['Pizza Name']= p_name
    d['Stock']= stock
    print(tabulate(d, headers= 'keys',tablefmt= 'psql'))
    
def customer_report():
    global cus_det
    order_id= []
    name= []
    amount= []
    address=[]
    city=[]
    state= []
    pin= []
    ph_no= []
    
    pur= []
    for i in cus_det:
        for j in cus_det[i]:
            if j=='Amount':
                pur.append(cus_det[i][j])
    sorted_pur= sorted(pur,reverse= True)
    sorted_cus_det={}
    for i in sorted_pur:
        for j in cus_det:
            if i == cus_det[j]['Amount']:
              sorted_cus_det[j]=cus_det[j]
    for i in sorted_cus_det:
      order_id.append(i)
      name.append(sorted_cus_det[i]['Name'])
      address.append(sorted_cus_det[i]['Address'])
      pin.append(sorted_cus_det[i]['Pincode'])
      city.append(sorted_cus_det[i]['City'])
      state.append(sorted_cus_det[i]['State'])
      ph_no.append(sorted_cus_det[i]['Phone number'])
      amount.append(sorted_cus_det[i]['Amount'])
    det= {}
    det['Order ID']=order_id
    det['Name']=name
    det['Amount']=amount
    det['Address']=address
    det['Pincode']=pin
    det['City']=city
    det['State']=state
    det['Phone no.']=ph_no
    print('DATE :',date.today())
    print()
    print(tabulate(det,headers= 'keys', tablefmt= 'psql'))

def customer_feedback():
  global cus_det
  order_id= []
  name= []
  amount= []
  fb= []
  rate= []
  for i in cus_det:
    order_id.append(i)
    name.append(cus_det[i]['Name'])
    amount.append(cus_det[i]['Amount'])
    fb.append(cus_det[i]['Feedback'])
    rate.append(cus_det[i]['Ratings'])
  det= {}
  det['Order ID']=order_id
  det['Name']=name
  det['Amount']=amount
  det['Feedback']= fb
  det['Ratings']=rate
  print('DATE :',date.today())
  print()
  print(tabulate(det,headers= 'keys', tablefmt= 'psql'))

def today_offer():
        global l,price,pizza_instock
        p_off= []
        while True:
                op= input('Do you want to provide an offer (yes/no) ? ')
                if op[1]=='e':
                        l=[]
                        offer=[]
                        n= input('Enter the name of the offer : ')
                        off= []
                        lin= int(input('Enter no. of lines you need for description :'))
                        print('Enter your description : ')
                        for i in range(lin):
                                des= input()
                                l.append(des)
                        price= int(input('Enter the price : '))
                        num= int(input('Enter no. of pizzas you gave as an offer : '))
                        for i in range(num):
                          p= input('Enter the pizza name : ')
                          qty= int(input('Enter the quantity : '))
                          p_off.append([p,qty])
                        break
                elif op[1]=='o':
                        print('NO offer today')
                        break
                else:
                        print('INVALID INPUT')
        return l,n, price,p_off

def change_coupon():
  while True:
                op= input('Do you want to change the coupon code (yes/no) ? ')
                if op[1]=='e':
                        coup_code= input('Enter the coupon code : ')
                        dis= int(input('Enter the discount (in %) : '))
                        break
                elif op[1]=='o':
                        coup_code= None
                        break
                else:
                        print('INVALID INPUT')
                        
  return coup_code, dis

def alter_data():
    global pizza_instock
    while True:
                op= input('Do you want to change the menu (yes/no) ? ')
                if op[1]=='e':
                        while True:
                            ch= input('Do you want to add an extra item or replace an item (extra/remove) ? ')
                            if ch[1]=='x':
                                prod_id= input('Enter the product ID : ')
                                pizza_name= input('Enter the pizza name : ')
                                stock= int(input('Enter the stock : '))
                                c_small= int(input('Enter the cost of small size : '))
                                c_medium= int(input('Enter the cost of medium size : '))
                                c_large= int(input('Enter the cost of large size : '))
                                e={'Product ID':prod_id,'Stock': stock,'Small':c_small,'Medium':c_medium,'Large':c_large}
                                pizza_instock[pizza_name]= e
                            elif ch[1]=='e':
                                pizza_name= input('Enter the pizza name to be removed : ')
                                del pizza_instock[pizza_name]
                                
                            else:
                                print('INVALID INPUT')
                                
                            print('CURRENT MENU')
                            d= {}
                            p_name= []
                            prod_id= []
                            small= []
                            medium= []
                            large= []
                            for i in pizza_instock:
                              p_name.append(i)
                              prod_id.append(pizza_instock[i]['Product ID'])
                              small.append(pizza_instock[i]['Small'])
                              medium.append(pizza_instock[i]['Medium'])
                              large.append(pizza_instock[i]['Large'])
                            d['Product ID']= prod_id
                            d['Pizza Name']= p_name
                            d['Small (in ₹)']= small
                            d['Medium (in ₹)']= medium
                            d['Large (in ₹)']= large
                            print(tabulate(d, headers= 'keys',tablefmt= 'psql'))
                            break
                elif op[1]=='o':
                        break
                else:
                        print('INVALID INPUT')
                        
    return pizza_instock


offer ='Sorry, Today we have no offers for you :('
coup= None
order_id= 0
cus_det= {}
pizza_instock =   {'Silician Pizza': {'Product ID': 'PDSP 1234','Stock': 50,'Small': 200,'Medium': 300,'Large': 400},
                   'Margherita Pizza': {'Product ID': 'PDMP 2345','Stock': 50,'Small': 99,'Medium': 199,'Large': 299},
                   'Hawaiian Pizza': {'Product ID': 'PDHP 3456','Stock': 50,'Small': 300,'Medium': 400,'Large': 500 },
                   'BBQ Chicken Pizza': {'Product ID': 'PDBP 4567','Stock': 50,'Small': 150,'Medium': 250,'Large': 350},
                   "Pequod's Pizza": {'Product ID': 'PDPP 5678','Stock': 50,'Small': 350, 'Medium': 450,'Large': 550}}

topping= {'Pepperoni':65,
          'Spicy Sausage':63,
          'Tomato':60,
          'Chicken':70,
          'Mozzarella cheese':62}

sauce= [['Mayonnaise'], ['Barbecue sauce'], ['Tomato ketchup'], ['Sriracha'], ['Garlic sauce']]

while True:
  print('1.USER',
        '2.ADMIN',
        '3.EXIT',sep='\n')
  ch= int(input('Enter your choice : '))
  if ch==1:
    for word in 'Welcome to Pizza Dine'.split():
        print(f'{word.capitalize():=^65}')
    time.sleep(0.5)
    print()
    print('Thank you for choosing Pizza Dine  :)')
    print('It\'s our pleasure to have you here')
    user(offer,coup)
  elif ch==2:
    admin()
  elif ch==3:
    break
    
