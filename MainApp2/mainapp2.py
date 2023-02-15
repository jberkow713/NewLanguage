
import kivy 
kivy.require('1.9.0')
from kivy.app import App
import json
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
# from kivy.metrics import dp
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
# from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.core.window import Window
import random
from kivy.properties import Clock
import sys
import string
from kivy.uix.image import Image, AsyncImage

class Scramboozled(Widget):
    
    x_buffer = .2
    y_buffer = .2
    let_buff = .1
    let_ratio = .85
    font_percent = .03
    grab_buffer = 1.005
    letters = string.ascii_lowercase
    x_letter_size = None
    y_letter_size = None
    Next_available = 1
    F = FloatLayout()
        
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.correct = SoundLoader.load('button.wav')
        self.wrong = SoundLoader.load('incorrect.wav')
        self.cheer = SoundLoader.load('Cheer.wav')
        self.SCREEN = SoundLoader.load('Screen.wav')
        self.LETTER = SoundLoader.load('Letter.wav')
        self.CLEAR = SoundLoader.load('Delete.wav')
        self.single_delete = SoundLoader.load('Delete1.wav')
        self.Background = SoundLoader.load('Background.mp3')
        self.LEVEL = SoundLoader.load('Level2.mp3')
        self.Lines = 8
        self.Score = 0
        self.Time = 100
        self.Music_timer = 0
        self.points = 0
        self.Level = 1
        self.Speed = 1
        self.word = ''
        self.FIRST = 'X'
        self.Rules = False
        self.Rules_Buttons = {}
        self.POS = Window.bind(mouse_pos = self.on_mouse_pos)
        self.Rules_Colors =  [(1,0,0),(1,1,1), (1,1,1), (1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1)]
        self.highlight_color = (0,1,0,.8)
        self.stored_color = None
        self.stored_slot = None
        self.current_letter = None
        self.reset()

    def reset(self):
        self.Score = 0
        self.points = 0            
        self.deleted_letters = []
        self.buttons = []
        self.press_buttons = []
        self.can_not_add = False        
        self.word_slots = {}
        self.word_coords= {}
        self.grid_coords = {}
        self.Letters = {}
        self.Letter_Dict = {}
        self.positions = {}
        self.other_buttons = {}
        self.init_buttons = {}
        self.Highlight_Dict = {}
        self.color_index = 1
        self.Button_Colors =  [(1,0,0), (0,0,1), (1,0,1),(0,1,0)]
        self.Timer_Color = (1,0,0)
        self.Score_Color = (1,0,0)
        self.Level_Color = (1,0,0)
        self.color_dict = {(1,0,0):2, (1,1,1):1, (0,0,1):3,(1,0,1):10}
        self.initialized = False
        self.reset_index = False
        self.level_up = False
        return              
    def Rules_Display(self):
        # Screen for displaying the rules, etc.
        Positions = [(self.width*.1, .83*self.height),(self.width*.1, self.height*.7),(self.width*.1, self.height*.6),\
            (self.width*.1, self.height*.5),(self.width*.1, self.height*.4),(self.width*.1, self.height*.3),\
                (self.width*.1, self.height*.2),(self.width*.1, self.height*.1),(self.width*.1,0)] 
        Text = ["BACK TO MAIN MENU","1)Click on letters to add them to the empty slots on the board",\
            '2) Click on the WORD button to verify if the word is real','3) If the word is real, points will be added to the Timer',
            '4) Red tiles are worth 2 points, Blue are worth 3, Purple are worth 10',\
                '5)To receive a new first letter, click LETTER, lose 5 seconds from the Timer',\
                    '6)To get a totally new board, click BOARD, lose 10 seconds from the Timer',\
                        '7)To clear the entire word, hit CLEAR. To delete letters in order, hit DELETE',\
                            '8)New level with every 30,40,or 50 points. Timer moves faster, points increase!']
        Names = ["BACK TO MAIN MENU", 1, 2, 3, 4, 5, 6, 7, 8]
                                                      
        
        Size = [(self.width*.8, self.height*.15),(self.width*.8, self.height*.1),(self.width*.8, self.height*.1),\
            (self.width*.8, self.height*.1), (self.width*.8, self.height*.1),(self.width*.8, self.height*.1),\
                (self.width*.8, self.height*.1),(self.width*.8, self.height*.1),(self.width*.8, self.height*.1)]
        Font_Size = [self.font_percent*self.width*.85,self.font_percent*self.width*.85,self.font_percent*self.width*.85,\
            self.font_percent*self.width*.85,self.font_percent*self.width*.85,self.font_percent*self.width*.75,\
                self.font_percent*self.width*.75, self.font_percent*self.width*.75,self.font_percent*self.width*.75]    
        count = 0                    
        for _ in range(0, len(Positions)):
            with self.canvas:
                # Check word Button
                x_pos, y_pos = Positions[count]
                btn = Button(text=Text[count],
                                size_hint =(None,None),
                                size=Size[count],
                                pos =(x_pos,y_pos))
                btn.background_color = self.Rules_Colors[count]
                btn.font_size = Font_Size[count]
                btn.halign= 'center'
                btn.valign= 'center'
                self.Rules_Buttons[Names[count]] = Positions[count], Size[count], self.Rules_Colors[count]
                self.F.add_widget(btn)
                count +=1               
        return      

    def start_game(self):
        # Initializes game 
        self.create_first_letter()
        self.create_letters()
        self.draw_grid()
        self.play_music()
        self.clock = Clock.schedule_interval(self.update,1/self.Speed)
    
    def restart(self):
        # Does this when restarting game
        
        self.Time = 100
        self.Level = 1
        self.Speed = 1 
        self.color_index = 1
        self.Music_timer = 0
        self.Timer_Color = (1,0,0)
        self.Score_Color = (1,0,0)
        self.Level_Color = (1,0,0)               
        self.restart_clear_word()        
        

    def restart_clear_word(self):
        for _ in range(self.Next_available):
            self.delete_slot()           
        self.word = ''
        self.Next_available = 1
        self.reset()
        return     

    def play_music(self):
        self.Background.play()
        
    def stop_music(self):
        self.Background.stop()    
    
    def change_clock(self):        
        self.clock.cancel()
        self.clock = Clock.schedule_interval(self.update,1/self.Speed)
    def change_color(self):        
        # Alters color of level slightly
        pos = self.color_index%len(self.Button_Colors)
        color = self.Button_Colors[pos]
        Color = tuple([0 if x == 0 else 1-random.uniform(0, .5) for x in color])        
        self.color_index+=1
        self.Timer_Color=self.Level_Color=self.Score_Color = Color        
        return

    def init_screen_display(self):
        # TODO these are the initial buttons for the entry screen       
      
        Positions = [(self.width*.333, .8*self.height),(self.width*.1, self.height*.4), (self.width*.4, self.height*.4),\
            (self.width*.7, self.height*.4), (self.width*.4, self.height*.1)] 
        Names = ["SCRAMBOOZLED", 'EASY', 'MEDIUM', 'HARD', 'RULES']
        Colors = [(1,0,0), (0,0,1), (1,0,1),(0,1,0), (1,0,0)]
        Size = [(self.width*.333, self.height*.2), (self.width*.2, self.height*.2),(self.width*.2, self.height*.2),\
            (self.width*.2, self.height*.2),(self.width*.2, self.height*.2)]
        count = 0                    
        for _ in range(0, len(Positions)):
            with self.canvas:
                # Check word Button
                x_pos, y_pos = Positions[count]
                btn = Button(text=Names[count],
                                size_hint =(None,None),
                                size=Size[count],
                                pos =(x_pos,y_pos))
                btn.background_color = Colors[count]
                btn.font_size = self.font_percent*self.width*.85
                btn.halign= 'center'
                btn.valign= 'center'
                self.press_buttons.append(btn)
                self.init_buttons[Names[count]] = Positions[count], Size[count]
                self.F.add_widget(btn)
                count +=1               
        return            
    
    def bg_color(self):
        Colors = [(1,0,0), (0,0,1), (1,1,1), (1,0,1)]
        val = random.randint(0,10)
        if val>=9:
            rand2 = random.randint(0,50)
            if rand2 >=48:
                return Colors[3]
            val2 = random.randint(0,1)
            if val2 == 0:
                return Colors[0]
            else:
                return Colors[1]
        return Colors[2]

    def create_letters(self):        
        for i in range(self.Lines**2):
            self.Letters[i] = self.letters[random.randint(0, len(self.letters)-1)], self.bg_color()
        return     
    
    def create_first_letter(self):
        New = string.ascii_uppercase.replace('X', "").replace(self.FIRST,"")        
        First = New[random.randint(0,len(New)-1)]
        self.word+=First
        self.FIRST = First               
        return                

    def draw_grid(self):
        # Color will dictate color of grid lines, and text lines
        with self.canvas:
            Color(0,0,1)
            
            x_gap = ((1-2*self.x_buffer) * self.width) / self.Lines
            letter_size = x_gap*self.let_ratio
            y_gap = ((1-2*self.y_buffer) * self.height)/ self.Lines 
            start_x = self.x_buffer*self.width
            start_y = self.y_buffer*self.height
            letter_y = self.let_buff*self.height
            end_x = (1-self.x_buffer)*self.width
            end_y = (1-self.y_buffer)*self.height
            self.x_letter_size = x_gap
            self.y_letter_size = y_gap 
            x_positions = []
            y_positions = []

            for i in range(self.Lines+1):
                Line(points=[start_x+i*x_gap,start_y,start_x+i*x_gap,end_y],width=3)
                x_positions.append(start_x+i*x_gap)

            for i in range(self.Lines+1):
                Line(points=[start_x,start_y+i*y_gap,end_x,start_y+i*y_gap],width=3)
                y_positions.append(start_y+i*y_gap)

            for i in range(self.Lines):
                x_1 = (x_gap -letter_size)/2+start_x+i*x_gap
                Line(points=(x_1, letter_y, start_x+(i+1)*x_gap - (x_gap -letter_size)/2, letter_y),width=3)
                self.word_coords[i]= (x_1,letter_y),None

            count = 0
            x_index = 0
            for i in range(self.Lines):
                x_pos = x_positions[x_index]
                y_index =0
                for i in range(self.Lines):
                    y_pos = y_positions[y_index]
                    POS = x_pos, y_pos
                    for k,v in self.Letters.items():
                        if k == count:
                            self.Letter_Dict[count] = POS,v[0]
                    y_index+=1
                    count +=1
                x_index+=1
        return

    def place_letter(self, val, letter,color=None):
        # places letter at given tile slot based on letter and optional color        
        with self.canvas:            
            V = self.word_coords[val][0]                                  
            x_pos = V[0]
            y_pos = V[1]
            x_size = self.x_letter_size*self.let_ratio 
            y_size = self.y_letter_size*self.let_ratio           
            btn = Button(text=letter,
                        size_hint =(None,None),
                        size=(x_size,y_size),
                        pos =(x_pos,y_pos))
            if color!=None:
                btn.background_color=color            
            btn.font_size = self.font_percent*self.width
            btn.halign= 'center'
            btn.valign= 'center'
            self.F.add_widget(btn)
        return         
    
    def delete_letter(self, val):
        # Delete letter from grid   
        curr = self.Letter_Dict[val][0]        
        self.Letter_Dict[val]= curr, None
        Color = self.Letters[val][1]
        self.Letters[val] = None, Color                        
        with self.canvas:            
            Coords = self.positions[val]                   
            x_pos = Coords[0][0]
            y_pos = Coords[1][0]
            x_size = self.x_letter_size
            y_size = self.y_letter_size            
            btn = Button(
                        size_hint =(None,None),
                        size=(x_size,y_size),
                        pos =(x_pos,y_pos))
            self.F.add_widget(btn)
        return    
    def on_mouse_pos(self, *args):
        Temp_Button_Colors = [(1,0,0),(1,1,1), (1,1,1), (1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1)]
                    
        POS = self.POS = args[1]
        if self.initialized == False:
            if self.Rules == True:
                for button,coords in self.Rules_Buttons.items():
                    if POS[0]>coords[0][0] and POS[0]<=coords[0][0]+coords[1][0]:
                        if POS[1]>=coords[0][1] and POS[1]<=coords[0][1]+coords[1][1]:
                            if button != 'BACK TO MAIN MENU':
                                
                                self.Rules_Colors = Temp_Button_Colors
                                self.Rules_Colors[button]=self.highlight_color
                                self.on_size()
                                return                                
        
        #Checks to see if game has started outside of loading screen 
        elif self.initialized == True:            
            if self.stored_color!=None:
                # Referring to lettering being out of slot after clicked
                if self.Letter_Dict[self.stored_slot][1]!=None:
                # self.Current_button.background_color = self.stored_color
                #TODO remove the changed button, place this button back in, by drawing it 
                    if self.stored_slot!=None:
                        for slot, position in self.positions.items():
                            if POS[0]>position[0][0]*self.grab_buffer and POS[0] <position[0][1]/self.grab_buffer:
                                if POS[1]>position[1][0]*self.grab_buffer and POS[1]<position[1][1]/self.grab_buffer:
                                    if slot != self.stored_slot:
                    
                                        x_pos, y_pos = self.Letter_Dict[self.stored_slot][0]                        
                                        x_size = self.x_letter_size
                                        y_size = self.y_letter_size                     
                                        
                                        self.input_letter(self.stored_slot,self.current_letter, x_pos,y_pos,self.x_letter_size,self.y_letter_size,self.stored_color)
                                        if self.stored_slot in self.Highlight_Dict.keys():
                                            del self.Highlight_Dict[self.stored_slot]

            for slot, position in self.positions.items():
                if POS[0]>position[0][0]*self.grab_buffer and POS[0] <position[0][1]/self.grab_buffer:
                    if POS[1]>position[1][0]*self.grab_buffer and POS[1]<position[1][1]/self.grab_buffer:
                        button = self.buttons[slot]
                                                
                        self.Current_button = button                                               
                        self.stored_color = self.Letters[slot][1]
                        # slot of button
                        self.stored_slot = slot
                        # Letter of button
                        self.current_letter = curr_letter = self.Letters[slot][0]
                        x_pos, y_pos = self.Letter_Dict[slot][0]                        
                        x_size = self.x_letter_size
                        y_size = self.y_letter_size
                        color = self.highlight_color
                        if slot not in self.Highlight_Dict.keys():
                            BTN = self.input_letter(slot,curr_letter, x_pos,y_pos,x_size,y_size,color)
                            self.Highlight_Dict[slot]=BTN

                        return                            
        
    def on_touch_down(self, touch):
        # move letters to spots in order in grid in which they are clicked
        
        POS = touch.pos
        # TODO entry screen
        if self.initialized==False:
            if self.Rules == False:

                for button,coords in self.init_buttons.items():
                    if POS[0]>coords[0][0] and POS[0]<=coords[0][0]+coords[1][0]:
                        if POS[1]>=coords[0][1] and POS[1]<=coords[0][1]+coords[1][1]:
                            if button =="EASY":
                                self.Lines = 6
                                self.Level_Points = 50
                            elif button =='MEDIUM':
                                self.Lines = 8
                                self.Level_Points = 40
                            elif button == 'HARD':
                                self.Lines = 10
                                self.Level_Points = 30
                            elif button =='RULES':
                                self.Rules = True
                                self.on_size() 
                                self.Rules_Display()
                                return     
                            # TODO
                            # Add the Rules button here, and the rabbit hole from this position once button is touched
                            else:
                                return
                            self.initialized=True
                            self.start_game()
                            self.on_size()
                            return
            if self.Rules == True:
                for button, coords in self.Rules_Buttons.items():
                    if POS[0]>coords[0][0] and POS[0]<=coords[0][0]+coords[1][0]:
                        if POS[1]>=coords[0][1] and POS[1]<=coords[0][1]+coords[1][1]:
                            if button == 'BACK TO MAIN MENU':
                                self.Rules = False
                                self.on_size()
                                     
            # TODO add prompts for entry screen here
        if self.initialized == True:

            for button, coords in self.other_buttons.items():
                if POS[0]>=coords[0][0] and POS[0]<=coords[0][0]+coords[1][0]:
                    if POS[1]>=coords[0][1] and POS[1]<=coords[0][1]+coords[1][1]:
                        # This will then trigger another class function, dependent on button clicked
                        # TODO
                        if button == 'CLEAR':
                            self.clear_full_word()
                        elif button == 'DELETE':
                            self.full_delete()                                                
                        elif button =='WORD':
                            self.validate_word()
                        elif button == "LETTER":
                            self.change_first_letter()
                        elif button == "BOARD":
                            self.clear_grid()
                        elif button == "RESTART":
                            self.initialized=False
                            self.restart()
                            self.clock.cancel()
                            self.on_size()
                        elif button =='QUIT':
                            # TODO send to score, and end screen
                            sys.exit()    
                        return 
            if self.Next_available ==self.Lines:
                return
            if self.can_not_add == False:                        
            # First loop represents adding letters to word            
                for slot, position in self.positions.items():
                    if POS[0]>position[0][0]*self.grab_buffer and POS[0] <position[0][1]/self.grab_buffer:
                        if POS[1]>position[1][0]*self.grab_buffer and POS[1]<position[1][1]/self.grab_buffer:

                            Letter = self.Letters[slot]                        
                            letter = Letter[0]
                            if letter == None:
                                return
                            elif Letter[1] in self.color_dict.keys():
                                Color = Letter[1]
                            else:
                                Color = None
                            #Going to create an empty space where the letter was    
                            self.delete_letter(slot)                        
                            self.deleted_letters.append(letter)    
                            self.word_slots[self.Next_available]=slot
                            self.word +=letter
                            self.word = self.word.lower()                       
                            self.place_letter(self.Next_available, letter, Color)
                            if self.Next_available<self.Lines:
                                self.Next_available +=1
                            else:
                                self.can_not_add = True                                                                                    
        return

    def bonus_timer(self):
        # TODO create bonus timer that when it turns on, allows people to get bonus points in that window
        pass

    def special_letters(self):
        # TODO low frequency and random, add special color letters, and a bonus timer
        # if you use flashing letter in word before bonus timer runs out, big bonus points
        pass 
        
    def narrow(self,word):       
    # Narrows down word into small subset, to be parsed
        val = str(len(word))
        with open('Words.json') as json_file:
            data = json.load(json_file)
        with open('Word_Enums.json', 'r') as json_file:
            Enums = json.load(json_file)    
                
        first = word[0]
        indexes = Enums[val]
        start = indexes[first]        
        next = [x for x in indexes.values() if x > start][0]                
        if isinstance(next,int):
            return data[val][start:]
        return data[val][start:next]         

    def validate_word(self):
        # returns True or False if specific word is in English Language        
        if len(self.word)<3:
            self.wrong.play()
            return        
        if self.word in self.narrow(self.word):            
            Score = self.calc_points()
            if len(self.word)==self.Lines:
                self.cheer.play()
            else:
                if self.level_up ==False:
                    self.correct.play()
            self.Score +=Score            
            self.Time +=Score
            self.display_score()
            self.display_timer()
            self.deleted_letters.clear()
            self.refill_board()
            self.level_up =False
            return
        else:
            self.wrong.play()
        return

    def refill_board(self):
        # Refills board after word has been approved        
        for k,v in self.Letter_Dict.items():
            if v[1]==None:                
                new_letter = self.letters[random.randint(0,len(self.letters)-1)]
                new_color = self.bg_color()
                coords = self.Letter_Dict[k][0]
                self.Letter_Dict[k]= coords, new_letter
                self.Letters[k] = new_letter, new_color
                                
                with self.canvas:                                                                         
                    x_pos = coords[0]
                    y_pos = coords[1]
                    x_size = self.x_letter_size
                    y_size = self.y_letter_size
                    btn = Button(text=new_letter,
                                size_hint =(None,None),
                                size=(x_size,y_size),
                                pos =(x_pos,y_pos))
                    btn.background_color = (new_color)   
                    btn.font_size = self.font_percent*self.width
                    btn.halign= 'center'
                    btn.valign= 'center'
                    self.F.add_widget(btn)
                    self.buttons[k]=btn
        self.word = self.word[0]
        self.Next_available = 1
        self.word_slots = {}
        self.on_size()
        return 

    def calc_points(self):        
        if self.Level >=2:
            multiplier = self.Level//2
        else:
            multiplier = 0

        doubles = ['z','q','Z','Q']
        values = [self.Letters[x][1] for x in self.word_slots.values()]
        Score = 1        
        for v in values:
            for c,p in self.color_dict.items():
                if v ==c:
                    Score+=p
        
        if len(self.word)==self.Lines:
            Score *=4+multiplier
        elif len(self.word)>=5 and len(self.word)<self.Lines:
            Score*=2+multiplier
        
        if self.FIRST in doubles:
            self.points += Score*2
            Multiplier = 2
        else:
            self.points +=Score
            Multiplier = 1

        if self.points >=self.Level_Points:
            count = self.points // self.Level_Points
            self.points = self.points - count*self.Level_Points                
            
            for _ in range(count):
                self.Speed +=.5
                self.Level +=1
                self.change_color()
                self.change_clock()
                self.LEVEL.play()
            self.level_up = True                                      
        return Score * Multiplier

    def full_delete(self):
        if len(self.word)>1:
            self.single_delete.play()
        self.delete_slot()
        self.on_size()
        return

    def delete_slot(self):        
        self.can_not_add = False
        if self.Next_available ==1:
            return
        to_add_back = self.word_slots[self.Next_available-1]

        curr = self.Letter_Dict[to_add_back][0]
        self.Letter_Dict[to_add_back]= curr, self.deleted_letters[-1]
        Color = self.Letters[to_add_back][1]
        self.Letters[to_add_back] = self.deleted_letters[-1], Color

        self.deleted_letters = self.deleted_letters[:-1]        
        self.word = self.word[:-1]       
        del self.word_slots[self.Next_available-1]
        self.Next_available -=1
        return
        
    def clear_word(self):
        if len(self.word)>1:
            self.CLEAR.play()
        for _ in range(self.Next_available):
            self.delete_slot()
        self.word = self.word[:1]
        self.Next_available = 1
        self.word_slots = {}
        return 

    def clear_full_word(self):
        # Clears full word quickly
        self.clear_word()
        self.on_size()
        return 
        
    def update_word_slots(self):
        # Places letters back on grid in reverse order they were removed
        count = 0
        for spot, item in self.word_coords.items():
            if spot in self.word_slots.keys():
                LETT = self.word_slots[spot]
                self.word_coords[spot]=item[0], LETT
                Letter = self.Letters[LETT]
                L = self.deleted_letters[count]
                C = Letter[1]
                # Should be if ! (1,1,1)
                if C == (1,0,0) or C == (0,0,1) or C == (1,0,1):
                    Color = C
                else:
                    Color = None
                self.place_letter(spot,L,Color)
                count +=1
        return
    
    def clear_grid(self):
        self.SCREEN.play()

        self.clear_word()
        self.create_letters()
        self.Time -=10
        self.on_size()
        return

    def change_first_letter(self):
        self.LETTER.play()
        self.clear_word()
        self.word = ''
        self.create_first_letter()
        self.start_letter = self.FIRST
        self.Time -=5
        self.on_size()       
        return    
    
    def visual_effects(self):
        #TODO Throw in fireworks or something when player gets a word as long as the board
        #Other visual effects
        pass
    
    def on_size(self, *args):
        
        self.F.children.clear()
        # self.max_children = len(self.F.children)+self.Lines

        if self.initialized ==False:
            if self.Rules == False:

                self.canvas.clear()
                self.init_screen_display()
                self.stop_music()
            elif self.Rules == True:
                self.canvas.clear()
                self.Rules_Display()

        if self.initialized==True:
            # Resizes text and grid
                                
            self.canvas.clear()
            self.create_buttons()
            self.draw_grid()
            self.display_level()
            self.display_timer()
            self.display_score()
            self.input_letters()
            self.place_letter(0, self.FIRST)
            self.update_word_slots()
            return 
            
    def display_timer(self):        
        # displays timer as it counts down
        if self.Time <=0:
            TIME = 0
        else:
            TIME = self.Time    
        with self.canvas:            
            x_pos = .01*self.width
            y_pos = .835*self.height
            x_size = .15*self.width
            y_size = .15*self.height            
            btn = Button(text =f"Time:{str(TIME)}",
                        size_hint =(None,None),
                        size=(x_size,y_size),
                        pos =(x_pos,y_pos))                       
            # btn.text_size = (x_size,y_size)
            btn.background_color = self.Timer_Color
            btn.font_size = self.font_percent*self.width
            btn.halign= 'center'
            btn.valign= 'center'
            self.F.add_widget(btn)
        return

    def display_level(self):
        with self.canvas:            
            x_pos = .425*self.width
            y_pos = .835*self.height
            x_size = .15*self.width
            y_size = .15*self.height            
            btn = Button(text =f"Level:{str(self.Level)}",
                        size_hint =(None,None),
                        size=(x_size,y_size),
                        pos =(x_pos,y_pos))                       
            # btn.text_size = (x_size,y_size)
            btn.background_color = self.Level_Color
            btn.font_size = self.font_percent*self.width
            btn.halign= 'center'
            btn.valign= 'center'
            self.F.add_widget(btn)
        return    

    def display_score(self):
        #Displays score as it updates 
        with self.canvas:            
            x_pos = .84*self.width
            y_pos = .835*self.height
            x_size = .15*self.width
            y_size = .15*self.height            
            btn = Button(text =f"Score:{str(self.Score)}",
                        size_hint =(None,None),
                        size=(x_size,y_size),
                        pos =(x_pos,y_pos))                       
            # btn.text_size = (x_size,y_size)
            btn.background_color = self.Score_Color
            btn.font_size = self.font_percent*self.width
            btn.halign= 'center'
            btn.valign= 'center'
            self.F.add_widget(btn)
        return            
    def input_letter(self,slot,letter, x_pos,y_pos,x_size,y_size,color):

        self.F.children = self.F.children[0:120]
        
        if letter==None:
            return
        # OLD_BUTTON = self.buttons[slot]
        # self.F.remove_widget(OLD_BUTTON)        
        with self.canvas:
            btn = Button(text=letter,
            size_hint =(None,None),
            size=(x_size*.995,y_size*.995),
            pos =(x_pos,y_pos))
            btn.background_color = color
            btn.font_size = self.font_percent*self.width
            btn.halign= 'center'
            btn.valign= 'center'
            self.buttons[slot]=btn
            self.F.add_widget(btn)
            self.draw_grid()
            # self.draw_grid()  
            return

    def input_letters(self):
        # Inputs all letters onto the board based on their values in the self.Letter_Dict
        self.buttons.clear()
        with self.canvas:
            for i in range(self.Lines**2):
                V = self.Letter_Dict[i]                
                Coords = V[0]
                Letter = V[1]                
                x_pos = Coords[0]
                y_pos = Coords[1]
                x_size = self.x_letter_size
                y_size = self.y_letter_size
                if Letter!=None:

                    btn = Button(text=Letter,
                                size_hint =(None,None),
                                size=(x_size,y_size),
                                pos =(x_pos,y_pos))
                    btn.background_color = (self.Letters[i][1])            
                else:
                    btn = Button(size_hint =(None,None),
                                size=(x_size,y_size),
                                pos =(x_pos,y_pos))                                    
                # btn.background_color = (self.Letters[i][1])
                btn.font_size = self.font_percent*self.width
                btn.halign= 'center'
                btn.valign= 'center'
                # Adding to buttons for use, always correlates to index in dictionary of letter
                self.buttons.append(btn)
                self.positions[i] = (x_pos,x_pos+x_size), (y_pos, y_pos+y_size)
                # Adding to the Floating Layout for display
                self.F.add_widget(btn)
        return

    def create_buttons(self):
        # Creates the buttons: Clear, Word, and Delete
        # Adds positions to the other_buttons dictionary, with positions and sizes, to be used for on press and commands
        Positions = [(self.width*.45, .005*self.height) ,(self.width*.2, .005*self.height) , (self.width*.7, .005*self.height),\
            (self.width*.05, self.height*.45), (self.width*.85, self.height*.45), (self.width*.05, self.height*.05),\
                (self.width*.85,self.height*.05)] 
        Names = ["WORD","CLEAR","DELETE", "LETTER","BOARD", "RESTART", "QUIT"]
        Colors = [(1,0,0), (0,1,0), (0,1,0), (0,1,0), (0,0,1), (0,0,1), (0,0,1)]
        count = 0
        for _ in range(0, len(Positions)):
            with self.canvas:
                # Check word Button
                x_pos, y_pos = Positions[count]
                btn = Button(text=Names[count],
                                size_hint =(None,None),
                                size=(self.width*.1,self.height*.07),
                                pos =(x_pos,y_pos))
                btn.background_color = Colors[count]
                btn.font_size = self.font_percent*self.width*.85
                btn.halign= 'center'
                btn.valign= 'center'
                self.press_buttons.append(btn)
                self.other_buttons[Names[count]] = (x_pos,y_pos), (self.width*.1,self.height*.07)
                self.F.add_widget(btn)
                count +=1            
        return

    def update(self, dt):
        
        if self.initialized==True:

            if self.Time<=0:                
                print('Game Over')
                sys.exit()
            self.display_timer()
            self.Time-=1
            self.Music_timer+=1
            if self.Music_timer ==39:
                self.play_music()
                self.Music_timer = 0
            self.display_score()            
            return
                
#This calls mainapp2.kv, which calls MainWidget 
class MainApp2(App):
    pass

MainApp2().run()
       
       
       