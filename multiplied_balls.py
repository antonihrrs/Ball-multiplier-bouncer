
import random
import tkinter as tk
import customtkinter as ctk
import pygame.midi

class MultiplySquares:
    def __init__(self, master):
        self.master = master
        self.master.title("Balls Multiplier")
        self.root_geometry()

        self.master.configure(bg="#000000")

        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="#000000",
                                highlightbackground="#7B8591", highlightthickness=2)
        self.canvas.pack(expand=True)

        self.square_size = 45 #average sized ones = 45 #Also they're not squares, they're balls
        self.squares = []

        self.counter_label = ctk.CTkLabel(self.master, text="")
        self.counter_label.place(relx=0.5, rely=0.88, anchor="center")

        pygame.mixer.init()
        self.boing_sound=pygame.mixer.Sound("Pop Bubble Sound Effect.mp3")

        #self.colors_list = ["#006666", "#009999", "#00CCCC", "#00FFFF", "#33FFFF", "#66FFFF", "#99FFFF", "#CCFFFF"] #blues
        #self.colors_list = ["#E0E0E0", "#C0C0C0", "#A0A0A0", "#808080", "#606060", "#404040", "#202020"] #Grey scale

        #self.colors_list = ["#E5CCFF", "#CC99FF", "#B266FF", "#9933FF", "#7F00FF", "#6600CC", "#4C0099"] #Purple scale
        #self.colors_list=["#FF69B4", "#FF1493", "#DB7093", "#C71585", "#DA70D6", "#FF00FF", "#EE82EE", "#DDA0DD", "#D8BFD8"] #pink scale

        #self.colors_list = ["#DAF7A6", "#FFC300", "#FF5733", "#C70039", "#900C3F", "#581845"] #Warm cozy kind of colors

        #self.colors_list=["#ff5733", "#ff8a33", "#ffbd33", "#fff033", "#dbff33", "#a8ff33"] #stabilo TM

        self.colors_list = ["#FFB5EC", "#9AE3F2", "#B4F589", "#CB7FEC", "#F9D74D", "#FF8844", "#F57D7D"] #OG colors

        #pink, blue, green, purple, 
        # yellow, orange, salmon

        self.master.after(100, self.create_ball)

    def update_counter(self):
        self.counter_label.configure(text=f"Number of balls : {len(self.squares)}",
                                     font=("Helvetica", 22, "bold"), text_color="#9EB2CD")
       

    def create_ball(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        print(f"Canvas dimensions: {canvas_width}x{canvas_height}")

        if canvas_width <= 0 or canvas_height <= 0 or (canvas_width < self.square_size) or (canvas_height < self.square_size):
            print("Canvas dimensions don't work")
            return

        color = random.choice(self.colors_list)

        x = random.randint(0, canvas_width - self.square_size)
        y = random.randint(0, canvas_height - self.square_size)

        square = self.canvas.create_oval(x, y, x + self.square_size, y + self.square_size, fill=color, outline="white")

        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        self.squares.append({'id': square, 'dx': dx, 'dy': dy})

        self.update_counter()
        self.move_squares()

    def move_squares(self):
        new_squares = []

        for square in self.squares:
            current_coords = self.canvas.coords(square['id'])
            if not current_coords:
                print(f"Square {square['id']} coordinates not found.")
                continue

            current_x = current_coords[0]
            current_y = current_coords[1]

            new_x = current_x + square['dx']
            new_y = current_y + square['dy']

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            
            if new_x <= 0 or new_x + self.square_size >= canvas_width:
                square['dx'] = -square['dx']
                
                new_squares.append({'x': random.randint(0, canvas_width - self.square_size),
                                    'y': random.randint(0, canvas_height - self.square_size)})
                self.boing_sound.play()
            
            if new_y <= 0 or new_y + self.square_size >= canvas_height:
                square['dy'] = -square['dy']
                new_squares.append({'x': random.randint(0, canvas_width - self.square_size),
                                    'y': random.randint(0, canvas_height - self.square_size)})
                self.boing_sound.play()

            self.canvas.move(square['id'], square['dx'], square['dy'])

        for pos in new_squares:
            self.create_square_at_position(pos['x'], pos['y'])

        self.master.after(10, self.move_squares)

    def create_square_at_position(self, x, y):

        if len(self.squares) >= 500:
            return
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0 or (canvas_width < self.square_size) or (canvas_height < self.square_size):
            print("Canvas dimensions are invalid or too small.")
            return

        color = random.choice(self.colors_list)
        square = self.canvas.create_oval(x, y, x + self.square_size, y + self.square_size, fill=color, outline="white")
        dx = random.choice([-2, 1])
        dy = random.choice([-2, 1])
        self.squares.append({'id': square, 'dx': dx, 'dy': dy})

        self.update_counter()

    def root_geometry(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}")

if __name__ == "__main__":
    root = tk.Tk()
    game = MultiplySquares(root)
    root.mainloop()
