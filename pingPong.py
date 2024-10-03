import tkinter as tk
from tkinter import messagebox
import time

class PongScoreKeeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Pong Score Keeper")

        # Initialize scores and state
        self.winning_score = 7
        self.red_score = 0
        self.blue_score = 0
        self.last_press_time = 0
        self.delay = 0  # Delay in seconds for key presses
        self.deuce_mode = False  # Flag for deuce state
        self.current_server = None  # No initial server
        self.serves = 0  # Count serves to manage serving logic
        self.game_started = False  # Flag to check if the game has started

        # Create the GUI elements with borders
        self.red_frame = tk.Frame(master, bg='red', bd=10, relief='sunken', highlightbackground="yellow", highlightcolor="yellow", highlightthickness=15)
        self.red_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.red_frame.bind('<Button-1>', self.red_frame_clicked)

        self.blue_frame = tk.Frame(master, bg='blue', bd=10, relief='sunken', highlightbackground="blue", highlightcolor="blue", highlightthickness=15)
        self.blue_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.blue_frame.bind('<Button-1>', self.blue_frame_clicked)

        # Create textboxes for player names (transparent background)
        self.red_name_entry = tk.Entry(self.red_frame, bg='red', fg='white', font=('Helvetica', 24), relief='flat', insertbackground='white')
        self.red_name_entry.insert(0, "LEFT PLAYER")
        self.red_name_entry.pack()

        self.blue_name_entry = tk.Entry(self.blue_frame, bg='blue', fg='white', font=('Helvetica', 24), relief='flat', insertbackground='white')
        self.blue_name_entry.insert(0, "RIGHT PLAYER")
        self.blue_name_entry.pack()

        # Create score labels
        self.red_label = tk.Label(self.red_frame, text="0", bg='red', fg='white', font=('Helvetica', 48))
        self.red_label.pack(expand=True)

        self.blue_label = tk.Label(self.blue_frame, text="0", bg='blue', fg='white', font=('Helvetica', 48))
        self.blue_label.pack(expand=True)

        # Bind key events
        self.master.bind('<Key>', self.key_pressed)
        self.master.bind('<Configure>', self.resize_labels)

        # Call focus-unbinding function here
        self.bind_focus_unbind_keys()

        # Initial label font size
        self.resize_labels()

    def bind_focus_unbind_keys(self):
        # Function to unfocus from Entry widget
        def unfocus(event):
            event.widget.master.focus()  # Shift focus to parent (frame or root window)

        # Bind Return (Enter) and Escape keys to remove focus from Entry widgets
        self.red_name_entry.bind('<Return>', unfocus)
        self.blue_name_entry.bind('<Return>', unfocus)
        self.red_name_entry.bind('<Escape>', unfocus)
        self.blue_name_entry.bind('<Escape>', unfocus)

    def red_frame_clicked(self, event):
        if self.master.focus_get() == self.red_name_entry:
            return  # Ignore clicks if the text box is focused
        if not self.game_started:
            self.current_server = "red"
            self.game_started = True
            self.red_frame.config(bd=10, relief='sunken', highlightbackground="yellow", highlightcolor="yellow", highlightthickness=15)
            self.blue_frame.config(bd=10, relief='sunken', highlightbackground="blue", highlightcolor="blue", highlightthickness=15)
            self.serves = 0  # Reset serves
        else:
            self.increase_red_score(event)

    def blue_frame_clicked(self, event):
        if self.master.focus_get() == self.blue_name_entry:
            return  # Ignore clicks if the text box is focused
        if not self.game_started:
            self.current_server = "blue"
            self.game_started = True
            self.blue_frame.config(bd=10, relief='sunken', highlightbackground="yellow", highlightcolor="yellow", highlightthickness=15)
            self.red_frame.config(bd=10, relief='sunken', highlightbackground="red", highlightcolor="red", highlightthickness=15)
            self.serves = 0  # Reset serves
        else:
            self.increase_blue_score(event)

    def increase_red_score(self, event):
        self.red_score += 1
        self.serves += 1
        self.red_label.config(text=str(self.red_score))
        self.check_winner()
        self.update_server()

    def increase_blue_score(self, event):
        self.blue_score += 1
        self.serves += 1
        self.blue_label.config(text=str(self.blue_score))
        self.check_winner()
        self.update_server()

    def update_server(self):
        # Change server after every 2 serves, and allow for both increase and decrease
        if self.serves == 2:  # Forward serves, time to toggle
            self.toggle_server()
        elif self.serves == -1:  # Reverse serves, time to toggle back
            self.toggle_server()

    def toggle_server(self):
        if self.current_server == "red":
            self.current_server = "blue"
            self.red_frame.config(bd=10, relief='sunken', highlightbackground="red", highlightcolor="red", highlightthickness=15)
            self.blue_frame.config(bd=10, relief='sunken', highlightbackground="yellow", highlightcolor="yellow", highlightthickness=15)
        else:
            self.current_server = "red"
            self.blue_frame.config(bd=10, relief='sunken', highlightbackground="blue", highlightcolor="blue", highlightthickness=15)
            self.red_frame.config(bd=10, relief='sunken', highlightbackground="yellow", highlightcolor="yellow", highlightthickness=15)
        
        # Reset serves after toggling, with direction
        if self.serves > 0:
            self.serves = 0  # Reset forward serves
        elif self.serves == -1:  # Reset reverse serves:
            self.serves = 1  # Reset reverse serves
        else:
            self.serves = 0  # Reset reverse serves to 0

    def resize_labels(self, event=None):
        width = self.master.winfo_width()
        title_font_size = max(16, int(width / 40))
        score_font_size = max(36, int(width / 10))
        self.red_name_entry.config(font=('Helvetica', title_font_size))
        self.blue_name_entry.config(font=('Helvetica', title_font_size))
        self.red_label.config(font=('Helvetica', score_font_size))
        self.blue_label.config(font=('Helvetica', score_font_size))

    def check_winner(self):
        if self.red_score >= self.winning_score or self.blue_score >= self.winning_score:
            if abs(self.red_score - self.blue_score) > 1:
                winner = "red" if self.red_score > self.blue_score else "blue"
                if not getattr(self, 'winner_displayed', False):
                    self.show_winner(winner)
                    self.winner_displayed = True  # Set flag to prevent repeat display
            else:
                self.deuce_mode = True
                self.winner_displayed = False  # Reset flag for deuce state

        if self.deuce_mode and abs(self.red_score - self.blue_score) >= 2:
            winner = "red" if self.red_score > self.blue_score else "blue"
            if not getattr(self, 'winner_displayed', False):
                self.show_winner(winner)
                self.winner_displayed = True  # Set flag to prevent repeat display

    def reset_scores(self):
        # Reset scores and flags
        self.red_score = 0
        self.blue_score = 0
        self.red_label.config(text="0")
        self.blue_label.config(text="0")
        self.deuce_mode = False
        self.winner_displayed = False  # Reset the winner display flag
        self.serves = 0
        self.current_server = None
        self.game_started = False

        # Restore the game frames
        self.red_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.blue_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Remove winner display if it exists
        if hasattr(self, 'winner_label'):
            self.winner_label.pack_forget()  # Remove the winner label
            del self.winner_label  # Delete reference
        if hasattr(self, 'score_label'):
            self.score_label.pack_forget()  # Remove the score label
            del self.score_label  # Delete reference

    def key_pressed(self, event):
        if self.master.focus_get() in [self.red_name_entry, self.blue_name_entry]:
            return  # Ignore key presses if a text box is focused

        # Reset the game if a key is pressed after a win
        if hasattr(self, 'winner_label'):
            self.reset_scores()
            return  # Exit the method to prevent any other actions

        current_time = time.time()
        if current_time - self.last_press_time < self.delay:
            return  # Ignore key press if within delay

        ctrl_pressed = event.state & 0x0004

        if not self.game_started:
            # Set server based on key press
            if event.keysym in ['Left', 'q', 'a', 'z', 'w', 's', 'x', 'e', 'd', 'c', 'r', 'f', 'v', 't', 'g', 'b', '1', '2', '3', '4', '5']:
                self.current_server = "red"
                self.game_started = True
                self.red_frame.config(bd=10, relief='sunken', highlightbackground="yellow", highlightcolor="yellow", highlightthickness=15)
                self.blue_frame.config(bd=10, relief='sunken', highlightbackground="blue", highlightcolor="blue", highlightthickness=15)
                self.serves = 0  # Reset serves
            elif event.keysym in ['Right', 'y', 'h', 'n', 'u', 'j', 'm', 'i', 'k', 'o', 'l', 'p', '6', '7', '8', '9', '0']:
                self.current_server = "blue"
                self.game_started = True
                self.blue_frame.config(bd=10, relief='sunken', highlightbackground="yellow", highlightcolor="yellow", highlightthickness=15)
                self.red_frame.config(bd=10, relief='sunken', highlightbackground="red", highlightcolor="red", highlightthickness=15)
                self.serves = 0  # Reset serves
        else:
            # Check for score increment keys
            if event.keysym in ['Left', 'q', 'a', 'z', 'w', 's', 'x', 'e', 'd', 'c', 'r', 'f', 'v', 't', 'g', 'b', '1', '2', '3', '4', '5']:
                if ctrl_pressed:
                    self.decrease_red_score()
                else:
                    self.increase_red_score(event)
            elif event.keysym in ['Right', 'y', 'h', 'n', 'u', 'j', 'm', 'i', 'k', 'o', 'l', 'p', '6', '7', '8', '9', '0', 'bracketleft', 'bracketright', 'backslash', 'semicolon', 'apostrophe', 'comma', 'period', 'slash', 'minus', 'equal']:
                if ctrl_pressed:
                    self.decrease_blue_score()
                else:
                    self.increase_blue_score(event)
            elif event.keysym == 'space':
                self.reset_scores()

        self.last_press_time = current_time

    def decrease_red_score(self):
        if self.red_score > 0:
            self.red_score -= 1
            self.serves -= 1  # Decrement serves count
            self.red_label.config(text=str(self.red_score))
            self.update_server()  # Check if server should be switched
            self.check_winner()  # Check for a winner after decreasing the score

    def decrease_blue_score(self):
        if self.blue_score > 0:
            self.blue_score -= 1
            self.serves -= 1  # Decrement serves count
            self.blue_label.config(text=str(self.blue_score))
            self.update_server()  # Check if server should be switched
            self.check_winner()  # Check for a winner after decreasing the score

    def show_winner(self, winner):
        # Determine the winner's color and name
        winner_color = "red" if winner == "red" else "blue"
        winner_name = self.red_name_entry.get() if winner == "red" else self.blue_name_entry.get()

        # Set the window's background color to match the winner's side
        self.master.config(bg=winner_color)

        # Display the winner's name
        self.winner_label = tk.Label(self.master, text=f"{winner_name} wins!", font=('Helvetica', 48), bg=winner_color, fg='white')
        self.winner_label.pack(pady=20)

        # Display the final score
        self.score_label = tk.Label(self.master, text=f"Score: {self.red_score} - {self.blue_score}", font=('Helvetica', 36), bg=winner_color, fg='white')
        self.score_label.pack(pady=20)

        # Hide the game frames
        self.red_frame.pack_forget()
        self.blue_frame.pack_forget()

        # Set a flag indicating a win has occurred
        self.game_over = True

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x300")  # Set a fixed size for better centering
    pong_score_keeper = PongScoreKeeper(root)
    root.mainloop()
