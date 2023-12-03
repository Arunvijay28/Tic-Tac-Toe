import pygame as pg
import os,sys
import numpy as np
from random import randint

WIN_SIZE=600
CELL_SIZE=WIN_SIZE//3
vec2=pg.math.Vector2
CELL_CENTER=vec2(CELL_SIZE/2)

#the class tictac toe contains all the main logic of the game which has a seperate main  run method
class Tictactoe:
    def __init__(self,game) -> None:
        self.game=game
        img_pathG = os.path.join("simple_num_project_3122215002016", "resources", "Grid.png")
        img_pathO1 = os.path.join("simple_num_project_3122215002016", "resources", "O1.png")
        img_pathX1 = os.path.join("simple_num_project_3122215002016", "resources", "X1.png")

        # img = pg.image.load(img_path)
        self.grid_image=self.get_scaled_image(path=img_pathG,res=[WIN_SIZE]*2)
        self.O_image=self.get_scaled_image(path=img_pathO1,res=[CELL_SIZE]*2)
        self.X_image=self.get_scaled_image(path=img_pathX1,res=[CELL_SIZE]*2)

        #using numpy array
        self.game_array=np.full((3,3),np.inf)

        #to choose which player goes first
        self.player=randint(0,1)
        #array of indices for checking the winner of the game/status of the game i.e, draw win or lose
        self.line_indices=[[[0,0],[0,1],[0,2]],
                           [[1,0],[1,1],[1,2]],
                           [[2,0],[2,1],[2,2]],
                           [[0,0],[1,0],[2,0]],
                           [[0,1],[1,1],[2,1]],
                           [[0,2],[1,2],[2,2]],
                           [[0,0],[1,1],[2,2]],
                           [[0,2],[1,1],[2,0]]]
        self.winner=None
        self.steps_taken=0
        self.font=pg.font.SysFont('Verdana',CELL_SIZE//4,True)
    def check_winner(self):
        for line in self.line_indices:
            sum_line=sum([self.game_array[i][j] for i,j in line])
            if sum_line in {0,3}:
                self.winner='XO'[sum_line==0]
                self.winner_line=[vec2(line[0][::-1])*CELL_SIZE+CELL_CENTER,
                                  vec2(line[2][::-1])*CELL_SIZE+CELL_CENTER]
    #method for launching the main game process
    def run_game_process(self):
        cur_cell=vec2(pg.mouse.get_pos())//CELL_SIZE
        col,row=map(int,cur_cell)
        left_click=pg.mouse.get_pressed()[0]
        #if mouse left is clicked
        if left_click and self.game_array[row][col]==float("inf") and not self.check_winner():
            self.game_array[row][col]=self.player
            #changing the player by logical negation
            self.player=not self.player
            self.steps_taken+=1
            self.check_winner()
    #METHOD TO DISPLAY the gameplay
    def draw_objects(self):
        for y,row in enumerate(self.game_array):
            for x,obj in enumerate(row):
                if obj!=float('inf'):
                    self.game.screen.blit(self.X_image if obj else self.O_image,vec2(x,y)*CELL_SIZE)
    
    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.game.screen,'red',*self.winner_line,CELL_SIZE//8)
            label1=self.font.render(f'Player "{self.winner}" Wins!',True,'black','white')
            self.game.screen.blit(label1,(WIN_SIZE//2-label1.get_width()//2,WIN_SIZE//4))
        elif self.steps_taken==9:
            label2=self.font.render(f'It is a DRAW!',True,'black','white')
            self.game.screen.blit(label2,(WIN_SIZE//2-label2.get_width()//2,WIN_SIZE//4))



    #static method to load and scale
    def draw(self):
        self.game.screen.blit(self.grid_image,(0,0))
        self.draw_objects()
        self.draw_winner()
    @staticmethod
    def get_scaled_image(path,res):
        img=pg.image.load(path)
        return pg.transform.smoothscale(img,res)
    
    def print_caption(self):
        pg.display.set_caption(f'Player "{"XO"[self.player]}" turn!')
        if self.winner:
            pg.display.set_caption(f'player"{self.winner}" wins! Press Space for Newgame.')
        elif self.steps_taken==9:
            pg.display.set_caption(f"It is a DRAW,GAME OVER Press Space for Newgame")
    
    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()

#create the main game class where event check and launch method are checked

class Game:
    def __init__(self) -> None:
        #initailize pygame here..
        pg.init()
        self.screen=pg.display.set_mode([WIN_SIZE]*2)  #screen is set
        self.clock=pg.time.Clock()  #for setting the frame rate 
        self.tictactoe=Tictactoe(self)

    def new_game(self):
        self.tictactoe=Tictactoe(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    self.new_game()
    def run(self):
        while True:
            self.tictactoe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)  #number of frames as 60





#main program
if __name__=="__main__":
    g=Game()
    g.run()
