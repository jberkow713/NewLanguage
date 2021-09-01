def divide_tips(cash_tips, card_tips):

    Total_Tips = cash_tips + card_tips
    
    names = []
    hours = []
    Staff_To_add = True
    
    while Staff_To_add ==True:
        name = input("Enter Name: ")
        hour = input("Enter Hours: ")
        names.append(name)
        hours.append(int(hour))
        
        anyone_left = input('anyone else left to add? Enter 1 for yes, and 0 for no: ')
        if anyone_left == str(0):
            Staff_To_add = False

    Employee_Dict = dict(zip(names, hours))
    total = sum(hours)

    Final_Cut = []
    for v in Employee_Dict.values():
        Final_Cut.append(round((v/total)*Total_Tips,2))
    
    length = len(names)
    tuples = []
    index = 0

    while length >0:
        
        a = hours[index]
        b = Final_Cut[index]
        tupl = (a,b)
        
        tuples.append(tupl)
            
        index +=1
        length -=1

    Final_Dict = dict(zip(names, tuples))
    for k,v, in Final_Dict.items():
        print("{} earned ${} in tips by working {} hours".format(k,v[1], v[0])) 
    
    return Final_Dict



divide_tips(10,20)    