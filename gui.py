import pygame
import numpy as np
from time import sleep
import sudoku_bt as bt
import sudoku_ch
from sudoku_bt import empty_cells, validator
pygame.font.init()

import inspect, re

def varname(p):
  for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
    m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
      return m.group(1)

class App:
    # grid = [
    #     [0,7,0,0,2,0,0,4,6],
    #     [0,6,0,0,0,0,8,9,0],
    #     [2,0,0,8,0,0,7,1,5],
    #     [0,8,4,0,9,7,0,0,0],
    #     [7,1,0,0,0,0,0,5,9],
    #     [0,0,0,1,3,0,4,8,0],
    #     [6,9,7,0,0,2,0,0,8],
    #     [0,5,8,0,0,0,0,6,0],
    #     [4,3,0,0,8,0,0,7,0]
    # ]
    # grid = [
    #     [7,8,0,4,0,0,1,2,0],
    #     [6,0,0,0,7,5,0,0,9],
    #     [0,0,0,6,0,1,0,7,8],
    #     [0,0,7,0,4,0,2,6,0],
    #     [0,0,1,0,5,0,9,3,0],
    #     [9,0,4,0,6,0,0,0,5],
    #     [0,7,0,3,0,0,0,1,2],
    #     [1,2,0,0,0,7,4,0,0],
    #     [0,4,9,2,0,6,0,0,7]
    # ]
    # grid = np.array(grid)
    
    grid = sudoku_ch.createagrid(1) # 0 -> 1, where 0 is easy and 1 is hard

    ogrid = grid.copy()
    
    rows = cols = 9

    clr = {'lines': '#ff96ad',  'bg': '#fff5fd', 
           'temp' : (120,)*3, 'val': (250,)*3,
           'slc'  : (25, )*3}
    
    pinkyblue = {'lines': (255, 150, 173),  'bg': (255, 245, 253), 
                 'frst' : (0, 90, 141), 'tval': (2, 46, 87),
                 'slc'  : (25, )*3,  'fval': (207, 0, 0),
                 'notes': (150,)*3,  'slvr': (28, 197, 220)}
    
    scottish = {'lines': (22, 22, 22),  'bg': (52, 103, 81), 
                 'frst' : (200, 75, 49), 'tval': (236, 219, 186),
                 'slc'  : (25, )*3,  'fval': (207, 0, 0),
                 'notes': (150,)*3,  'slvr': (28, 197, 220)}
    
    raven = {'lines': (72, 0, 50),  'bg': (0, 87, 146), 
                 'frst' : (252, 146, 227), 'tval': (242, 244, 195),
                 'slc'  : (25, )*3,  'fval': (207, 0, 0),
                 'notes': (150,)*3,  'slvr': (28, 197, 220)}

    watermelon = {'lines': (245, 92, 71),  'bg': (159, 230, 160), 
                 'frst' : (74, 169, 108), 'tval': (86, 74, 74),
                 'slc'  : (25, )*3,  'fval': (207, 0, 0),
                 'notes': (150,)*3,  'slvr': (28, 197, 220)}
    
    calm = {'lines': (94, 139, 126) ,  'bg': (47, 93, 98),
           'frst' : (167, 196, 188), 'tval': (223, 238, 234),
           'slc'  : (25, )*3,        'fval': (207, 0, 0),
           'notes': (150,)*3,        'slvr': (28, 197, 220)}
    clrs = [pinkyblue, scottish, raven, watermelon, calm]
    clr = pinkyblue
           
    wshifts = {1:0,4:0,7:0,2:1,5:1,8:1,3:2,6:2,9:2}


    def __init__(self, screen):
        self.set_dims()
        self.set_statuses()
        self.selected = None
        self.solve()
        self.notes = 0
        self.init_images()
        # print(self.clr['bg'])
        screen.fill(self.clr['bg'])

    def set_statuses(self):
        self.statuses = []
        for r in range(self.rows):
            c_row = []
            for c in range(self.cols):
                if self.grid[r, c] != 0:
                    stat = 'frst'
                    notes = 0
                else:
                    stat = 'n'
                    notes = 0
                c_row.append((stat,notes))
            self.statuses.append(c_row)
                

    def set_dims(self):
        self.offw = round(wind_w * w_clearance)
        self.offh = round(wind_h * h_clearance)
        
        self.side = round(wind_w * (1 - (2 * w_clearance)))
        self.step = self.side / self.rows

        self.fonts = []
        self.fonts.append(pygame.font.SysFont("comicsans", round(self.side/25)))
        self.fonts.append(pygame.font.SysFont("comicsans", round(self.side/13)))
    

    def init_images(self):
        self.icon1_s=60
        self.icon1_coords=((self.offw+self.side-self.icon1_s ,self.offh+self.side+2))
        anotes = pygame.image.load('icons/notes.png')
        self.anotes = pygame.transform.scale(anotes, (self.icon1_s,)*2).convert_alpha()

        self.icon3_s=40
        self.icon3_coords=((self.offw+self.side-self.icon3_s-self.icon1_s ,self.offh+self.side+10))
        atheme = pygame.image.load('icons/theme.png')
        self.atheme = pygame.transform.scale(atheme, (self.icon3_s,)*2).convert_alpha()
        
        self.icon2_s=50
        self.icon2_coords=((self.offw+self.side-self.icon2_s-self.icon1_s-self.icon3_s-10 ,self.offh+self.side+2))
        asolve = pygame.image.load('icons/solve.png')
        self.asolve = pygame.transform.scale(asolve, (self.icon2_s,)*2).convert_alpha()

        

        

    
    def solver(self):
        self.notes = 0
        for r in range(self.rows):
            for c in range(self.cols):
                stat = self.statuses[r][c]
                if stat[0] != 'tval' and stat[0] != 'frst':
                    self.grid[r, c] = 0
                    self.statuses[r][c] = ('slvr', 0)
                    
        # return
        self.draw(window)
        pygame.display.update()

        coords = empty_cells(self.grid)
        
        def adder(coords):
            self.draw(window)
            pygame.display.update()
            # sleep(0.05)
            if not len(coords):
                return True

            coord = coords.pop(0)
            for val in range(1, 10):
                if validator(self.grid, coord, val):
                    self.grid[tuple(coord)] = val
                    self.draw(window)

                    if adder(coords.copy()):
                        return True
                    
                    self.grid[tuple(coord)] = 0
                    self.draw(window)
                    self.draw(window)
                    pygame.display.update()
                    sleep(0.1)

            return False

        adder(coords)



    def solve(self):
        self.bt_grid = self.grid.copy()
        bt.solver(self.bt_grid)
        # bt.printer(self.bt_grid)

    def draw(self, window):
        self.gap = self.side / self.rows

        window.fill(self.clr['bg'])

        window.blit(self.anotes, self.icon1_coords)
        window.blit(self.asolve, self.icon2_coords)
        window.blit(self.atheme, self.icon3_coords)
        

        #bg
        # pygame.draw.rect(window, self.clr['bg'], 
        #                     (self.offw, self.offh, 
        #                     self.offw+self.side-10 ,self.offh+self.side-55))
                            
        for i in range(1, self.rows):
            th = 1 if (i % 3) else 3
            
            # rows
            pygame.draw.line(window, self.clr['lines'], 
                             (self.offw           , self.offh+(i*self.gap)), # (<>, ♢)
                             (self.offw+self.side , self.offh+(i*self.gap)),
                             th)
            # cols
            pygame.draw.line(window, self.clr['lines'], 
                             (self.offw+(i*self.gap) , self.offh          ), 
                             (self.offw+(i*self.gap) , self.offh+self.side),
                             th)
        

        for r in range(self.rows):
            for c in range(self.cols):
                val = self.grid[r, c]
                if val != 0:
                    stat, notes = self.statuses[r][c]
                    
                    self.write(r, c, val, self.clr[stat], notes)


    def write(self, r, c, val, tclr, notes):
        wplace = self.offw + self.step * c
        hplace = self.offh + self.step * r

        
        if notes:
            offw=(self.wshifts[val]/3) * self.step + 5
            offh=(((val-1)//3 * self.step) / 3) + 2
            text = self.fonts[0].render(str(val), True, self.clr['notes'])
            window.blit(text, (wplace + offw,
                               hplace + offh))
        else:
            text = self.fonts[1].render(str(val), True, tclr)
            window.blit(text, (wplace + ((self.step - text.get_width())/2),
                               hplace + ((self.step - text.get_height())/2)))



    def clicked(self):
        pos = list(pygame.mouse.get_pos())
        self.check_flip(pos)
        self.check_solve(pos)
        self.check_theme(pos)
        pos[0] -= self.offw
        pos[1] -= self.offh

        if (pos[0] < 0) or (pos[0] > self.side):
            return False
        if (pos[1] < 0) or (pos[1] > self.side):
            return False
        
        self.selected = (int(pos[1] // self.gap), int(pos[0] // self.gap))
        
        return True

    def check_flip(self, pos):
        if (pos[0] > self.icon1_coords[0]) and (pos[0] < (self.icon1_coords[0]+self.icon1_s)):
            if (pos[1] > self.icon1_coords[1]) and (pos[1] < (self.icon1_coords[1]+self.icon1_s)):
                self.notes_flip()
    
    def check_solve(self, pos):
        if (pos[0] > self.icon2_coords[0]) and (pos[0] < (self.icon2_coords[0]+self.icon2_s)):
            if (pos[1] > self.icon2_coords[1]) and (pos[1] < (self.icon2_coords[1]+self.icon2_s)):
                self.solver()
        
    def check_theme(self, pos):
        if (pos[0] > self.icon3_coords[0]) and (pos[0] < (self.icon3_coords[0]+self.icon2_s)):
            if (pos[1] > self.icon3_coords[1]) and (pos[1] < (self.icon3_coords[1]+self.icon2_s)):
                self.next_clr()

    def notes_flip(self):
        self.notes = 1 - self.notes
    
    def next_clr(self):
        idx = self.clrs.index(self.clr)
        print(idx)
        if ((idx+1) == len(self.clrs)):
            print('made it')
            idx=0
        # print(varname(self.clrs[idx]))
        self.clr = self.clrs[idx+1]


    def update(self, key):
        if self.selected:
            r, c = self.selected
            self.grid[r, c] = key
            self.statuses[0]
            if self.bt_grid[r, c] == key:
                self.statuses[r][c]=('tval', self.notes)
            else:
                self.statuses[r][c]=('fval', self.notes)



    def clear(self):
        r, c = self.selected
        self.grid[r, c] = 0

    def is_full(self):
        if np.all(self.grid):
            return True
        return False
            


if __name__ == "__main__":

    # Set window dimensions and clearance
    wind_w, wind_h = 600, 750
    w_clearance, h_clearance = 0.01, 0.07
    window = pygame.display.set_mode((wind_w, wind_h))
    pygame.display.set_caption("Sudoku")

    # Instantiate an object
    mygrid = App(window)
    
    # List where the index maps to the pyagme key number
    pynumbers = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                 pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]


    status = True
    key = 0
    mygrid.draw(window)

    # Continuous loop will the user closes the app
    while status:
        
        # Iterate over events happenning
        for event in pygame.event.get():
            # Checks if the event was to quit
            if event.type == pygame.QUIT:
                status = False

            # Checks if the event was a key press
            if event.type == pygame.KEYDOWN:
                # 'n' for notes
                if pygame.key.name(event.key) == 'n':
                    mygrid.notes_flip()
                
                # 's' for backtracking solver
                if pygame.key.name(event.key) == 's':
                    mygrid.solver()
                
                # Try
                try:
                    key = 1 + pynumbers.index(event.key)
                    mygrid.update(key)
                except ValueError:
                    if event.key == pygame.K_DELETE:
                        mygrid.clear()
                        key = None
                    
                
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                key=0
                mygrid.clicked()


        mygrid.draw(window)
        pygame.display.update()
        