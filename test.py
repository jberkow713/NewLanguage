import random 

def rand(num,Range, num_lists):
    final = []
    for i in range(num_lists):

        final.append( [random.randint(0,num) for x in range(Range)])
    return final 
    
def find_highest(num, Range,lists):    
    c = rand(num,Range,lists)
    counts = {}
    for x in range(len(c)):
        l = c[x]
        count = 0
        for y in l:
            count +=y
        counts[x]=count 

    Counts = counts.values()
    c = max(Counts)
    for k,v in counts.items():
        if v == c:
            print(f' list with highest sum was {k} with a sum of {v} and an average of {v/Range}' )

find_highest(100,100,50)

