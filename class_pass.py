import random 
class Nested():
    def __init__(self, nums):
        self.nums = nums
        self.lst = self.make_list()
    def make_list(self):
        lst = []
        for i in range(self.nums):
            x = random.randint(0,self.nums)
            lst.append(x)
           
        return lst     

class Nested_More():
    def __init__(self, nums):
        self.nested = []
        self.letters = 'abcdefghijklmnopqrstuvwxyz'
        for i in range(26):
                        
            new = False
            while new == False:
                b = random.randint(1,nums)
                a = Nested(b).lst

                if a not in self.nested:
                    self.nested.append(a)
                    new = True 
    def create_keys(self):
        index = 0
        length = len(self.letters)
        
        letters = []
        avg = []

        while length >0:
            a = self.letters[index]
            b = self.nested[index]
            c = int(round(sum(b)/len(b),1)*10)
            letters.append(a)
            avg.append(c)

            index +=1
            length -=1

        crypt_dict = dict(zip(letters, avg))
        return crypt_dict

a = Nested_More(25)
print(len(a.nested))
print(a.create_keys())

