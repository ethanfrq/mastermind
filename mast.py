import tkinter as tk
from tkinter import messagebox
import random
import sqlite3
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class MastermindGame:
    def __init__(self, master):
        self.master = master
        master.title("Mastermind Game")
        master.geometry("700x300")
        master.configure(bg='black')

        self.username = None  # Placeholder for username
        self.user_ip = None  # Placeholder for IP address

        # Initialize colors and color map before generating the secret code
        self.colors = ['R', 'G', 'B', 'Y', 'O', 'P']
        self.color_map = {
            'R': 'red',
            'G': 'green',
            'B': 'blue',
            'Y': 'yellow',
            'O': 'orange',
            'P': 'purple'
        }

        self.secret_code = self.generate_secret_code()  # Secret code now has access to colors
        logging.info(f"Secret code generated: {self.secret_code}")
        self.attempts = 0

        self.setup_ui()
        self.setup_database()

    def setup_ui(self):
        # Create label and entry for pseudo (username)
        self.username_label = tk.Label(self.master, text="Enter your username:", bg='black', fg='white')
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=5)

        self.submit_pseudo_button = tk.Button(self.master, text="Submit", command=self.submit_pseudo, bg='gray', fg='white')
        self.submit_pseudo_button.pack(pady=10)

    def submit_pseudo(self):
        # Retrieve username from the entry field
        self.username = self.username_entry.get()

        if not self.username:
            messagebox.showerror("Error", "Please enter a valid username.")
        else:
            logging.info(f"Username entered: {self.username}")
            self.user_ip = self.get_user_ip()
            self.init_game()

    def init_game(self):
        # Once username is entered, initialize the game UI and hide pseudo entry
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.submit_pseudo_button.pack_forget()

        self.circles_frame = tk.Frame(self.master, bg='black')
        self.circles_frame.pack(pady=20)

        self.color_vars = []
        self.color_menus = []
        self.circle_canvases = []

        for i in range(4):
            circle = tk.Canvas(self.circles_frame, width=100, height=100, bg='black', highlightthickness=0)
            self.circle_canvases.append(circle)
            circle.create_oval(10, 10, 90, 90, fill="white", outline="white")
            circle.grid(row=0, column=i, padx=20)

            color_var = tk.StringVar(self.master)
            color_var.set(self.colors[0])
            self.color_vars.append(color_var)

            color_menu = tk.OptionMenu(self.circles_frame, color_var, *self.colors, command=lambda color, i=i: self.update_circle_color(i, color))
            color_menu.grid(row=1, column=i, padx=20)
            self.color_menus.append(color_menu)

        self.submit_button = tk.Button(self.master, text="Validate", command=self.check_guess, bg='gray', fg='white')
        self.submit_button.pack(pady=20)

        self.result_label = tk.Label(self.master, text="", bg='black', fg='white')
        self.result_label.pack()

    def setup_database(self):
        self.conn = sqlite3.connect('mastermind.db')
        self.cursor = self.conn.cursor()

    def get_user_ip(self):
        try:
            response = requests.get('https://api64.ipify.org?format=json')
            ip = response.json()['ip']
            logging.info(f"User IP: {ip}")
            return ip
        except requests.RequestException as e:
            logging.error(f"Error fetching IP address: {e}")
            return 'Unknown'

    def generate_secret_code(self):
        return random.sample(self.colors, k=4)  # Unique colors

    def update_circle_color(self, circle_index, selected_color):
        color_hex = self.color_map[selected_color]
        logging.info(f"Color selected for circle {circle_index}: {selected_color} ({color_hex})")
        self.circle_canvases[circle_index].delete("all")
        self.circle_canvases[circle_index].create_oval(10, 10, 90, 90, fill=color_hex, outline=color_hex)

    def reset_circles(self):
        logging.info("Resetting all circles to white")
        for circle in self.circle_canvases:
            circle.delete("all")
            circle.create_oval(10, 10, 90, 90, fill="white", outline="white")

    def check_guess(self):
        guess = [var.get() for var in self.color_vars]
        logging.info(f"User guess: {guess}")
        self.attempts += 1
        exact_matches, color_matches = self.compare_guess(self.secret_code, guess)
        logging.info(f"Attempt #{self.attempts}: Exact matches = {exact_matches}, Color matches = {color_matches}")

        if exact_matches == 4:
            logging.info(f"User won the game in {self.attempts} attempts!")
            messagebox.showinfo("Congratulations", f"You guessed the secret code in {self.attempts} attempts!")
            self.save_score()
            self.master.quit()
        else:
            self.result_label.config(text=f"Exact matches: {exact_matches}, Color matches: {color_matches}")
            self.reset_circles()

    def compare_guess(self, secret_code, guess):
        exact_matches = 0
        color_matches = 0
        temp_secret_code = secret_code.copy()

        for i in range(4):
            if guess[i] == secret_code[i]:
                exact_matches += 1
                temp_secret_code[i] = None

        for color in guess:
            if color in temp_secret_code and color is not None:
                color_matches += 1
                temp_secret_code[temp_secret_code.index(color)] = None

        return exact_matches, color_matches

    def save_score(self):
        self.cursor.execute('''
            INSERT INTO users (username, ip_address, attempts)
            VALUES (?, ?, ?)
        ''', (self.username, self.user_ip, self.attempts))
        self.conn.commit()
        logging.info(f"Score saved: {self.username}, IP: {self.user_ip}, Attempts: {self.attempts}")
        self.conn.close()

root = tk.Tk()
game = MastermindGame(root)
root.mainloop()
