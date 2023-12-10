import tkinter as tk
import random
import time


win = "none"


class WumpusWorld:
    global win
    def __init__(self, size=4):
        self.size = size
        self.agent_position = (0, 0)
        self.wumpus_position = self.generate_random_position(exclude=[self.agent_position])
        self.gold_position = self.generate_random_position(exclude=[self.agent_position, self.wumpus_position])
        self.pit_positions = [self.generate_random_position(exclude=[self.agent_position, self.wumpus_position, self.gold_position]) for _ in range(size)]
        self.arrows = 1
        self.game_over = False
        self.breeze_positions = self.get_adjacent_positions(self.pit_positions)
        self.stench_positions = self.get_adjacent_positions([self.wumpus_position])

    def generate_random_position(self, exclude=[]):
        available_positions = [(x, y) for x in range(self.size) for y in range(self.size) if (x, y) not in exclude]
        return random.choice(available_positions)
    
    def get_adjacent_positions(self, positions):
        adjacent_positions = set()
        for x, y in positions:
            adjacent_positions.add((x - 1, y))
            adjacent_positions.add((x + 1, y))
            adjacent_positions.add((x, y - 1))
            adjacent_positions.add((x, y + 1))
        return list(adjacent_positions)

    def move_agent(self, action):
        global win
        if not self.game_over:
            if(action == "NO SOLUTION"):
                win = "no solution"
                self.game_over = True
                return "Stuck!"
            new_position = self.get_new_position(action)
            # print("action:",action)
            # print("new:",str(new_position))
            if self.is_valid_position(new_position):
                self.agent_position = new_position
                if self.agent_position == self.wumpus_position:
                    self.game_over = True
                    win = "wumpus"
                    return "You encountered the Wumpus! Game over."
                elif self.agent_position in self.pit_positions:
                    win = "pit"
                    self.game_over = True
                    return "You fell into a pit! Game over."
                elif self.agent_position == self.gold_position:
                    win = "gold"
                    self.game_over = True
                    return "Congratulations! You found the gold."
                else:
                    return "You moved {}.".format(action)
            else:
                return "Invalid move."
        else:
            return "Game over. Press Restart to play again."

    def get_new_position(self, action):
        x, y = self.agent_position
        if action == "UP":
            return x, y+1
        elif action == "DOWN":
            return x, y-1
        elif action == "LEFT":
            return x-1, y
        elif action == "RIGHT":
            return x+1, y

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def run_ai(self):
        if not self.game_over:
            # Rule-based AI considering breeze and stench
            if self.agent_position == self.gold_position:
                return "Congratulations! You found the gold."

            valid_actions = []
            x, y = self.agent_position
            valid_actions.append("RIGHT")
            valid_actions.append("LEFT")
            valid_actions.append("DOWN")
            valid_actions.append("UP")
            
            
            action = self.choose_best_action(valid_actions)
            return self.move_agent(action)
        else:
            return "Game over. Press Restart to play again."
    def choose_best_action(self, actions):
        valid_actions = []
        # print("--------------------")
        # print(self.agent_position)
        goldpos = "none"
        for action in actions:
            new_position = self.get_new_position(action)
            
            if self.is_valid_position(new_position) and new_position not in self.wumpus_position and new_position not in self.pit_positions:
                if(new_position in self.gold_position):
                    print("gold is at:"+str(new_position))
                    goldpos = action
                # print("wumpus:"+str(self.wumpus_position))
                # print("new:",str(new_position))
                # print(action)
                valid_actions.append(action)
            if new_position == self.wumpus_position:
                
                print("wumpus is at:"+str(new_position))
                
                

                try:
                    valid_actions.remove(action)

                except:
                    pass
                    
            

               
                

            if(new_position == self.gold_position):
                goldpos = action

            if(new_position in self.pit_positions):

                
                print("pit at:"+str(new_position))
                try:
                    valid_actions.remove(action)
                
                except:
                    pass
                
            if(new_position in self.breeze_positions):
                print("breeze at:"+str(new_position))
            if(new_position in self.stench_positions):
                print("stench at:"+str(new_position))
        

        if(goldpos != "none"):
            #print("gold found")
            return goldpos
        return random.choice(valid_actions) if valid_actions else "NO SOLUTION"

class WumpusWorldGUI:
    global win
    def __init__(self, master, size=4):
        self.master = master
        self.master.title("Wumpus World")
        
        self.world = WumpusWorld(size)

        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.result_label = tk.Label(self.master, text="Welcome to Wumpus World!", font=("Helvetica", 12))
        self.result_label.pack()

        self.update_display()

        # Direction buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack()
        tk.Button(button_frame, text="Up", command=lambda: self.handle_action("LEFT")).grid(row=0, column=1) # right
        tk.Button(button_frame, text="Left", command=lambda: self.handle_action("DOWN")).grid(row=1, column=0) #left
        tk.Button(button_frame, text="Right", command=lambda: self.handle_action("UP")).grid(row=1, column=2) #down
        tk.Button(button_frame, text="Down", command=lambda: self.handle_action("RIGHT")).grid(row=2, column=1)#up


        # tk.Button(button_frame, text="Up", command=lambda: self.handle_action("LEFT")).grid(row=2, column=1) # left 
        # tk.Button(button_frame, text="Left", command=lambda: self.handle_action("UP")).grid(row=1, column=0) #up
        # tk.Button(button_frame, text="Right", command=lambda: self.handle_action("RIGHT")).grid(row=1, column=2) #right
        # tk.Button(button_frame, text="Down", command=lambda: self.handle_action("DOWN")).grid(row=0, column=1)#down


        # Shoot button

        # Run AI button
        tk.Button(self.master, text="Run AI Once", command=self.handle_run_ai).pack()
        tk.Button(self.master, text="Run AI Until win", command=self.autoAi).pack()

        # Restart button
        tk.Button(self.master, text="Restart", command=self.handle_restart).pack()
       # tk.Button(self.master, text="", command=self.handle_restart).pack() higher speed?


    def autoAi(self):
        while not self.world.game_over:
            time.sleep(0.25)
            result = self.world.run_ai()
            self.result_label.config(text=result)
            self.update_display()
            self.master.update()
        


    def handle_action(self, action):
        result = self.world.move_agent(action)
        self.result_label.config(text=result)
        self.update_display()

    def handle_shoot(self):
        result = self.world.shoot_arrow()
        self.result_label.config(text(result))
        self.update_display()

    def handle_run_ai(self):
        result = self.world.run_ai()
        self.result_label.config(text=result)
        self.update_display()

    def handle_restart(self):
        self.world = WumpusWorld()
        self.result_label.config(text="Welcome to Wumpus World!")
        self.update_display()

    def update_display(self):
        self.canvas.delete("all")
        cell_size = 400 // self.world.size

        for i in range(self.world.size):
            for j in range(self.world.size):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                
                if (i, j) == self.world.agent_position:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue violet", outline="black")
                    self.canvas.create_text(x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, text="Agent", fill="white", font=("Helvetica", 12))
                elif (i, j) == self.world.wumpus_position:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")
                    self.canvas.create_text(x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, text="Wumpus", fill="black", font=("Helvetica", 12))
                elif (i, j) in self.world.pit_positions:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
                    self.canvas.create_text(x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, text="Pit", fill="white", font=("Helvetica", 12))
                elif (i, j) == self.world.gold_position:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gold", outline="black")
                    self.canvas.create_text(x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, text="Gold", fill="black", font=("Helvetica", 12))
                elif (i, j) in self.world.breeze_positions:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                    self.canvas.create_text(x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, text="Breeze", fill="blue", font=("Helvetica", 12))
                elif (i, j) in self.world.stench_positions:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                    self.canvas.create_text(x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, text="Stench", fill="red", font=("Helvetica", 12))
        global win
        #print(win)
        if self.world.game_over:
            if(win == "gold"):
                self.canvas.create_text(200, 200, text="Congrats you got the gold!", font=("Helvetica", 24), fill="green")
            else:
                self.canvas.create_text(200, 200, text="Game Over!!", font=("Helvetica", 24), fill="red")

            

root = tk.Tk()
game = WumpusWorldGUI(root)
root.mainloop()