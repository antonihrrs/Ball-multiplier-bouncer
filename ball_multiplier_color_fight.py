import random
import tkinter as tk
import customtkinter as ctk
import pygame.midi

class MultiplySquares:
    def __init__(self, master):
        self.master = master
        self.master.title("Balls Multiplier")
        self.root_geometry()

        self.master.config(bg="#000000")

        self.canvas = tk.Canvas(self.master, width=600, height=600, bg="#000000",
                                highlightbackground="#7B8591", highlightthickness=2)
        self.canvas.pack(expand=True)

        self.ball_size = 25
        self.squares = []

        pygame.mixer.init()
        self.boing_sound = pygame.mixer.Sound("Pop Bubble Sound Effect.mp3")
        self.winning_sound = pygame.mixer.Sound("Success Sound Effect.mp3")

        self.color_names = {
            "Pink": "#FFB5EC",
            "Blue": "#9AE3F2",
            "Green": "#B4F589"
        }

        self.colors = ["#FFB5EC", "#9AE3F2", "#B4F589"]

        self.color_counters = {color: 0 for color in self.colors}
        self.total_counter = 0

        self.labels = {}
        for i, (name, color) in enumerate(self.color_names.items()):
            label = ctk.CTkLabel(self.master, text=f"{name}: 0", text_color="black",
                                 fg_color=color, width=100, height=30, corner_radius=10)
            label.place(relx=0.75, rely=0.37 - i * 0.05, anchor="center")
            self.labels[color] = label

        self.total_label = ctk.CTkLabel(self.master, text="", fg_color="#9CABBF", width=100, height=30, corner_radius=10)
        self.total_label.place(relx=0.75, rely=0.55, anchor="center")

        self.master.after(100, self.create_ball)

    def update_counter(self):
        for color, label in self.labels.items():
            color_name = next(name for name, hex in self.color_names.items() if hex == color)
            label.configure(text=f"{color_name}: {self.color_counters[color]}")
        self.total_label.configure(text=f"Total: {self.total_counter}")

        for color, count in self.color_counters.items():
            if color == "#FFB5EC" and count >= 100:  #Pink
                self.squares = []
                self.boing_sound.stop()
                self.winning_sound.play()
                self.winning_message = ctk.CTkLabel(self.master, text=f"Pink won !\nIt's outnumbered the others\nAnd has reached {count} balls !",
                                                    text_color="#F2E4E4", font=("Euphemia", 25), fg_color="black", width=200, height=130,
                                                    corner_radius=10)
                self.winning_message.place(relx=0.5, rely=0.5, anchor="center")

            elif color == "#9AE3F2" and count >= 100:  #Blue
                self.squares = []
                self.boing_sound.stop()
                self.winning_sound.play()
                self.winning_message = ctk.CTkLabel(self.master, text=f"Blue won !\nIt's outnumbered the others\nAnd has reached {count} balls !",
                                                    text_color="#F2E4E4", font=("Euphemia", 25), fg_color="black", width=200, height=130,
                                                    corner_radius=10)
                self.winning_message.place(relx=0.5, rely=0.5, anchor="center")

            elif color == "#B4F589" and count >= 100:  #Green
                self.squares = []
                self.boing_sound.stop()
                self.winning_sound.play()
                self.winning_message = ctk.CTkLabel(self.master, text=f"Green won !\nIt's outnumbered the others\nAnd has reached {count} balls !",
                                                    text_color="#F2E4E4", font=("Euphemia", 25), fg_color="black", width=200, height=130,
                                                    corner_radius=10)
                self.winning_message.place(relx=0.5, rely=0.5, anchor="center")


    def create_ball(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0 or (canvas_width < self.ball_size) or (canvas_height < self.ball_size):
            return

        #Create OG pink ball
        x = random.randint(0, canvas_width - self.ball_size)
        y = random.randint(0, canvas_height - self.ball_size)
        pink_color = "#FFB5EC"
        pink_ball = self.canvas.create_oval(x, y, x + self.ball_size, y + self.ball_size, fill=pink_color, outline="white")
        self.color_counters[pink_color] += 1
        self.squares.append({'id': pink_ball, 'dx': random.choice([-1.5, 1.5]), 'dy': random.choice([-1.5, 1.5]), 'color': pink_color})

        #Create OG blue ball
        x = random.randint(0, canvas_width - self.ball_size)
        y = random.randint(0, canvas_height - self.ball_size)
        blue_color = "#9AE3F2"
        blue_ball = self.canvas.create_oval(x, y, x + self.ball_size, y + self.ball_size, fill=blue_color, outline="white")
        self.color_counters[blue_color] += 1
        self.squares.append({'id': blue_ball, 'dx': random.choice([-1.5, 1.5]), 'dy': random.choice([-1.5, 1.5]), 'color': blue_color})

        #Create OG green ball
        x = random.randint(0, canvas_width - self.ball_size)
        y = random.randint(0, canvas_height - self.ball_size)
        green_color = "#B4F589"
        green_ball = self.canvas.create_oval(x, y, x + self.ball_size, y + self.ball_size, fill=green_color, outline="white")
        self.color_counters[green_color] += 1
        self.squares.append({'id': green_ball, 'dx': random.choice([-1.5, 1.5]), 'dy': random.choice([-1.5, 1.5]), 'color': green_color})

        self.total_counter += 3

        self.update_counter()
        self.move_balls()

    def move_balls(self):
        new_squares = []

        for square in self.squares:
            current_coords = self.canvas.coords(square['id'])
            if not current_coords:
                continue

            current_x = current_coords[0]
            current_y = current_coords[1]

            new_x = current_x + square["dx"]
            new_y = current_y + square["dy"]

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if new_x <= 0 or new_x + self.ball_size >= canvas_width:
                square["dx"] = -square["dx"]
                new_squares.append({
                    "x": random.randint(0, canvas_width - self.ball_size),
                    "y": random.randint(0, canvas_height - self.ball_size),
                    "color": square["color"]
                })
                self.boing_sound.play()

            if new_y <= 0 or new_y + self.ball_size >= canvas_height:
                square["dy"] = -square["dy"]
                new_squares.append({
                    "x": random.randint(0, canvas_width - self.ball_size),
                    "y": random.randint(0, canvas_height - self.ball_size),
                    "color": square["color"]
                })
                self.boing_sound.play()

            self.canvas.move(square["id"], square["dx"], square["dy"])

            self.check_collisions(square)

        for pos in new_squares:
            self.create_balls_at_position(pos["x"], pos["y"], pos["color"])  #Pass the color

        self.master.after(10, self.move_balls)


    def check_collisions(self, square):
        current_coords = self.canvas.coords(square['id'])

        for other_square in self.squares:
            if other_square == square:
                continue

            other_coords = self.canvas.coords(other_square['id'])

            #Check for collisions
            if (abs(current_coords[0] - other_coords[0]) < self.ball_size and
                abs(current_coords[1] - other_coords[1]) < self.ball_size):

                #If pink touches blue, turn the blue into pink
                if square['color'] == "#FFB5EC" and other_square['color'] == "#9AE3F2":
                    self.canvas.itemconfig(other_square['id'], fill="#FFB5EC")
                    other_square['color'] = "#FFB5EC"
                    self.color_counters["#FFB5EC"] += 1
                    self.color_counters["#9AE3F2"] -= 1
                    self.update_counter()

                #If blue touches green, turn green into blue
                elif square['color'] == "#9AE3F2" and other_square['color'] == "#B4F589":
                    self.canvas.itemconfig(other_square['id'], fill="#9AE3F2")
                    other_square['color'] = "#9AE3F2"
                    self.color_counters["#9AE3F2"] += 1
                    self.color_counters["#B4F589"] -= 1
                    self.update_counter()

                #If green touches pink, turn pink into green
                elif square['color'] == "#B4F589" and other_square['color'] == "#FFB5EC":
                    self.canvas.itemconfig(other_square['id'], fill="#B4F589")
                    other_square['color'] = "#B4F589"
                    self.color_counters["#B4F589"] += 1
                    self.color_counters["#FFB5EC"] -= 1
                    self.update_counter()

                
    def create_balls_at_position(self, x, y, color):
        if self.total_counter >= 1000:
            return
    
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0 or (canvas_width < self.ball_size) or (canvas_height < self.ball_size):
            return

        # Use the color passed as a parameter instead of picking a random color
        self.color_counters[color] += 1
        self.total_counter += 1

        square = self.canvas.create_oval(x, y, x + self.ball_size, y + self.ball_size, fill=color, outline="white")
        dx = random.choice([-1.5, 1.5])
        dy = random.choice([-1.5, 1.5])
        self.squares.append({'id': square, 'dx': dx, 'dy': dy, 'color': color})

        self.update_counter()


    def root_geometry(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width}x{screen_height}")

if __name__ == "__main__":
    root = tk.Tk()
    game = MultiplySquares(root)
    root.mainloop()
