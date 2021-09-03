import random
class Randomize():
    def __init__(self, players, num_dice, goal_val):
        self.players = players
        self.num_dice = num_dice
        self.goal_val = goal_val
        
       
    def __repr__(self):
        
        return (f'The game has {self.players} players, rolling {self.num_dice} dice, the goal is to roll {self.goal_val}')
    
    def roll(self):
        for i in range(self.players):
            print(f'Now rolling, player {i}')
            count = 0
            for j in range(self.num_dice):
                die = random.randint(0,6)
                count += die
            print(f'player{i} rolled {count}')
            if count >= self.goal_val:
                print(f'player {i} has won')
                return      
        print('Nobody reached the goal, better luck next time')    
a = Randomize(3,4,15)
print(a)
a.roll()
