import math 
import random
import time
import pygame 
pygame.init()

#class variables
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer Game")
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (0, 25, 40) 
LIVES = 20
BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("times new roman", 24) #creates font object

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y 
        self.size = 0
        self.grow = True

    def update(self): #function to update the size of the target whether its shrinking or growing
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        if self.grow:
            self.size += self.GROWTH_RATE
        else: 
            self.size -= self.GROWTH_RATE

    def draw(self, win): #function to draw the target
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y): #checking if the user's mouse is colliding with a target by finding the distance between the mouse and ccenter of target
       distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
       return distance <= self.size
  

def draw(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100) 
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60) 
    return f"{minutes:02d}:{seconds:02d}:{milli: 02d}" #uses f string to formate the time stamp. 02d rounds to the second decimal point and if there is onl 1 number it will start with 0 

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "white", (0,0, WIDTH, BAR_HEIGHT))

    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black") #render font obj
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(speed_label, (270,5))
    win.blit(hits_label, (470,5))
    win.blit(time_label, (20,5)) #blit displayes different surfaces on game window 
    win.blit(lives_label, (670,5))  

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white") #render font obj
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    if targets_pressed == 0:
        accuracy_label = LABEL_FONT.render(f"Accuracy: 0%", 1, "white")
    else:
        accuracy = round(targets_pressed / clicks * 100, 1)
        accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(speed_label, (get_middle(speed_label),100))
    win.blit(hits_label, (get_middle(hits_label),200))
    win.blit(time_label, (get_middle(time_label),300))
    win.blit(accuracy_label, (get_middle(accuracy_label),400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2

def main():
    run = True
    targets = []
    clock = pygame.time.Clock() #clock object from time module

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT) #trigger target_event every target_increment seconds

    while run:
        clock.tick(50) #regulates framerate and speed of of the while loop at 60 frames per second 
        click = False
        mouse_position = pygame.mouse.get_pos() #returns a tuple of x and y coordinate of mouse position
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING , WIDTH - TARGET_PADDING) #prevent targets from developing off screen
                y = random.randint(TARGET_PADDING + BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)
            if event.type == pygame.MOUSEBUTTONDOWN:  
                click = True
                clicks += 1
            

        for target in targets:
            target.update()

            if target.size <= 0: #removes target once it has shrunk back down to zero
                targets.remove(target)
                misses += 1
            
            if click and target.collide(*mouse_position): #using the * breaks up the tuple into its individual arguments in this case it is x & y
                targets.remove(target)
                targets_pressed += 1
        
        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks) 

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main() 