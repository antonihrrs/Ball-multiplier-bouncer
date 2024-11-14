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
        self.canvas.pack(expand=True, pady=(0, 2))

        self.ball_size = 40
        self.squares = []

        pygame.mixer.init()
        self.boing_sound = pygame.mixer.Sound("Pop Bubble Sound Effect.mp3")
        self.winning_sound = pygame.mixer.Sound("Success Sound Effect.mp3")

        self.color_names={
            "Pink" : "#FFB5EC",
            "Blue" : "#9AE3F2",
            "Green" : "#B4F589"
        }

        self.colors = ["#FFB5EC", "#9AE3F2", "#B4F589"]

        self.color_counters = {color: 0 for color in self.colors}
        self.total_counter = 0

        self.label_frame = tk.Frame(self.master, bg="#000000")
        self.label_frame.pack(pady=(0, 5)) 

        self.labels = {}
        for i, (name, color) in enumerate(self.color_names.items()):
            label = ctk.CTkLabel(self.label_frame, text=f"{name}: 0", text_color="black", font=("Helvetica", 20),
                                 fg_color=color, width=100, height=30, corner_radius=10)
            label.grid(row=0, column=i, padx=5)
            self.labels[color] = label

        self.total_label = ctk.CTkLabel(self.master, text="", fg_color="#9CABBF", font=("Helvetica", 20),
                                        width=100, height=30, corner_radius=10)
        self.total_label.pack(pady=(5, 5))

        self.first_ball = True
        self.master.after(100, self.create_ball)

    def update_counter(self):
        for color, label in self.labels.items():
            color_name = next(name for name, hex in self.color_names.items() if hex == color)
            label.configure(text=f"{color_name}: {self.color_counters[color]}")
        self.total_label.configure(text=f"Total: {self.total_counter}")

        for color, count in self.color_counters.items():
            if color == "#FFB5EC" and count >= 150:  #Pink
                self.squares = []
                self.boing_sound.stop()
                self.winning_sound.play()
                self.winning_message = ctk.CTkLabel(self.master, text=f"Pink won !\nIt has reached {count} balls firt!",
                                                    text_color="#F2E4E4", font=("Euphemia", 25), fg_color="black", width=200, height=130,
                                                    corner_radius=10)
                self.winning_message.place(relx=0.5, rely=0.5, anchor="center")

            elif color == "#9AE3F2" and count >= 150:  #Blue
                self.squares = []
                self.boing_sound.stop()
                self.winning_sound.play()
                self.winning_message = ctk.CTkLabel(self.master, text=f"Blue won !\nIt has reached {count} balls firt!",
                                                    text_color="#F2E4E4", font=("Euphemia", 25), fg_color="black", width=200, height=130,
                                                    corner_radius=10)
                self.winning_message.place(relx=0.5, rely=0.5, anchor="center")

            elif color == "#B4F589" and count >= 150:  #Green
                self.squares = []
                self.boing_sound.stop()
                self.winning_sound.play()
                self.winning_message = ctk.CTkLabel(self.master, text=f"Green won !\nIt has reached {count} balls firt!",
                                                    text_color="#F2E4E4", font=("Euphemia", 25), fg_color="black", width=200, height=130,
                                                    corner_radius=10)
                self.winning_message.place(relx=0.5, rely=0.5, anchor="center")


    def create_ball(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0 or (canvas_width < self.ball_size) or (canvas_height < self.ball_size):
            return

        x = random.randint(0, canvas_width - self.ball_size)
        y = random.randint(0, canvas_height - self.ball_size)

        if self.first_ball:
            color = "white"
            self.first_ball = False
        else:
            color = random.choice(self.colors)

        ball = self.canvas.create_oval(x, y, x + self.ball_size, y + self.ball_size, fill=color, outline="white")

        if color != "white":
            self.color_counters[color] += 1

        self.total_counter += 1

        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        self.squares.append({'id': ball, 'dx': dx, 'dy': dy, 'color': color})

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
                new_squares.append({"x": random.randint(0, canvas_width - self.ball_size),
                                    "y": random.randint(0, canvas_height - self.ball_size)})
                self.boing_sound.play()

            if new_y <= 0 or new_y + self.ball_size >= canvas_height:
                square["dy"] = -square["dy"]
                new_squares.append({"x": random.randint(0, canvas_width - self.ball_size),
                                    "y": random.randint(0, canvas_height - self.ball_size)})
                self.boing_sound.play()

            self.canvas.move(square["id"], square["dx"], square["dy"])

        for pos in new_squares:
            self.create_square_at_position(pos["x"], pos["y"])

        self.master.after(10, self.move_balls)

    def create_square_at_position(self, x, y):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 0 or canvas_height <= 0 or (canvas_width < self.ball_size) or (canvas_height < self.ball_size):
            return

        color = random.choice(self.colors)
        self.color_counters[color] += 1
        self.total_counter += 1

        square = self.canvas.create_oval(x, y, x + self.ball_size, y + self.ball_size, fill=color, outline="white")
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
