#Current Tasks:
#1. Add 11-0 victory animation
#2. Bug/issues: N/a
#3. Test high score functionality
import tkinter as tk
from tkinter import messagebox
import time
import pyodbc
import pygame  # Add pygame import

pygame.mixer.init()  # Initialize the mixer module

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
        self.control = False  
        self.gif_label = None  # Initialize gif_label to None
        self.gif_frames = []  # Initialize gif_frames to an empty list

        # Create the GUI elements with borders
        self.red_frame = tk.Frame(master, bg='red', bd=20, relief='ridge', highlightbackground="#32CD32", highlightcolor="#32CD32", highlightthickness=25)
        self.red_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.red_frame.bind('<Button-1>', self.red_frame_clicked)

        self.blue_frame = tk.Frame(master, bg='blue', bd=20, relief='groove', highlightbackground="blue", highlightcolor="blue", highlightthickness=25)
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
        # Function to unfocus (exit out of) Entry widget (text box) when Return or Escape keys are pressed
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
            self.red_frame.config(bd=20, relief='ridge', highlightbackground="#32CD32", highlightcolor="#32CD32", highlightthickness=25)
            self.blue_frame.config(bd=20, relief='groove', highlightbackground="blue", highlightcolor="blue", highlightthickness=25)
            self.serves = 0  # Reset serves
        else:
            self.increase_red_score(event)

    def blue_frame_clicked(self, event):
        if self.master.focus_get() == self.blue_name_entry:
            return  # Ignore clicks if the text box is focused
        if not self.game_started:
            self.current_server = "blue"
            self.game_started = True
            self.blue_frame.config(bd=20, relief='ridge', highlightbackground="#32CD32", highlightcolor="#32CD32", highlightthickness=25)
            self.red_frame.config(bd=20, relief='groove', highlightbackground="red", highlightcolor="red", highlightthickness=25)
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
        if self.deuce_mode:
            # In deuce mode, switch the server after every point
            self.toggle_server()
        else:
            # Change server after every 2 serves (normal mode)
            # Change server after every 2 serves, and allow for both increase and decrease
            if self.serves == 2:  # Forward serves, time to toggle
                self.toggle_server()
            elif self.serves == -1:  # Reverse serves, time to toggle back
                self.toggle_server()

    def toggle_server(self):
        if self.current_server == "red":
            self.current_server = "blue"
            self.red_frame.config(bd=20, relief='groove', highlightbackground="red", highlightcolor="red", highlightthickness=25)
            self.blue_frame.config(bd=20, relief='ridge', highlightbackground="#32CD32", highlightcolor="#32CD32", highlightthickness=25)
        else:
            self.current_server = "red"
            self.blue_frame.config(bd=20, relief='groove', highlightbackground="blue", highlightcolor="blue", highlightthickness=25)
            self.red_frame.config(bd=20, relief='ridge', highlightbackground="#32CD32", highlightcolor="#32CD32", highlightthickness=25)
        
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
        if self.red_score < self.winning_score and self.blue_score < self.winning_score:
            self.deuce_mode = False

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

        # Clear high scores display
        if hasattr(self, 'high_scores_label'):
            self.high_scores_label.pack_forget()  # Remove the high scores label
            del self.high_scores_label  # Delete reference

        # Remove GIF if it exists but do not delete it
        if hasattr(self, 'gif_label') and self.gif_label is not None:
            # Stop the GIF animation
            self.current_frame = 0  # Reset the frame index to the start
            self.gif_label.pack_forget()  # Hide the GIF label
            del self.gif_label  # Delete reference
            # You can also reset the GIF or modify it here if needed

        # If you want to reset the frames list
        if hasattr(self, 'gif_frames'):
            self.gif_frames.clear()  # Clear the frames list to reuse later

        pygame.mixer.music.stop()  # Stop the sound when the game is reset
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
                self.red_frame.config(bd=20, relief='ridge', highlightbackground="#32CD32", highlightcolor="#32CD32", highlightthickness=25)
                self.blue_frame.config(bd=20, relief='groove', highlightbackground="blue", highlightcolor="blue", highlightthickness=25)
                self.serves = 0  # Reset serves
            elif event.keysym in ['Right', 'y', 'h', 'n', 'u', 'j', 'm', 'i', 'k', 'o', 'l', 'p', '6', '7', '8', '9', '0']:
                self.current_server = "blue"
                self.game_started = True
                self.blue_frame.config(bd=20, relief='ridge', highlightbackground="#32CD32", highlightcolor="#32CD32", highlightthickness=25)
                self.red_frame.config(bd=20, relief='groove', highlightbackground="red", highlightcolor="red", highlightthickness=25)
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

    def connect_to_database(self):
            """Connect to the Access database"""
            # Update the path to your Access database file 
            db_path = r'C:\Users\exuxjas\Documentss\DatabasePGUI.accdb'  # Change this to your Access DB path
            conn_str = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                f'DBQ={db_path};'
            )
            try:
                conn = pyodbc.connect(conn_str)
                return conn
            except pyodbc.Error as e:
                messagebox.showerror("Database Error", f"Error connecting to database: {e}")
                return None

    def save_final_score(self, red_score, blue_score, winner_name, loser_name):
            """Save the final score to the database after confirmation"""
            # Show confirmation popup
            confirm = messagebox.askyesno("Confirm", f"Do you want to save the result?\n"
                                                    f"Winner: {winner_name}\n"
                                                    f"Score: {red_score} - {blue_score}")
            if confirm:
                # Proceed with saving to the database
                conn = self.connect_to_database()
                if conn:
                    cursor = conn.cursor()
                    try:
                        # Insert the game result into the table
                        cursor.execute(
                            "INSERT INTO game_results (red_score, blue_score, winner, loser) VALUES (?, ?, ?, ?)",
                            (red_score, blue_score, winner_name, loser_name)
                        )
                        conn.commit()
                        print("Success! Game result saved to the database!")
                    except pyodbc.Error as e:
                        messagebox.showerror("Database Error", f"Error saving game result: {e}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    messagebox.showerror("Error", "Could not connect to the database.")
            else:
                # User chose not to save
                print("Cancelled. Game result not saved.")
            return confirm
    
    @staticmethod
    def update_high_scores(winner_name, control):
        #strip name to avoid whitespace
        winner_name = winner_name.strip()

        if control:
            # Connect to your Access database
            conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\exuxjas\Documents\DatabasePGUI.accdb;')
            cursor = conn.cursor()

            # Check if the player already exists in the High_Scores table
            cursor.execute("SELECT wins FROM High_Score WHERE player_name=?", (winner_name,))
            row = cursor.fetchone()

            if row:
                # If the player exists, update the number of wins and last win date
                cursor.execute(
                    "UPDATE High_Score SET wins = wins + 1 WHERE Player_Name = ?",
                    (winner_name)
                )
            else:
                # If the player doesn't exist, insert a new record
                cursor.execute(
                    "INSERT INTO High_Score (player_name, wins) VALUES (?, 1)",
                    (winner_name)
                )

            # Commit changes and close connection
            conn.commit()
            conn.close()

            # Show confirmation message
            print("Success! High Scores updated!")
        else:
            # User chose not to save
            print("Cancelled. High Scores not updated.")
            
    @staticmethod
    def fetch_high_scores():
        # Connect to your Access database
        conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\exuxjas\Documents\DatabasePGUI.accdb;')
        cursor = conn.cursor()

        # Retrieve the top 5 players based on the number of wins
        cursor.execute("SELECT player_name, wins FROM high_score ORDER BY wins DESC")
        high_scores = cursor.fetchmany(5)  # Fetch the top 5 results

        conn.close()
        return high_scores

    def show_winner(self, winner):
        # Determine the winner's name
        winner_name = self.red_name_entry.get() if winner == "red" else self.blue_name_entry.get()
        loser_name = self.red_name_entry.get() if winner == "blue" else self.blue_name_entry.get()

        # Save final score to the database after confirmation
        self.control = self.save_final_score(self.red_score, self.blue_score, winner_name, loser_name)

        # Update high scores in the database
        PongScoreKeeper.update_high_scores(winner_name, self.control)

        # Determine the winner's color and name
        winner_color = "red" if winner == "red" else "blue"

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

        # Display the GIF reward
        if self.red_score == 0 or self.blue_score == 0:
            self.show_gif_reward(winner_color, winner_name)

        # Fetch and display high scores
        high_scores = PongScoreKeeper.fetch_high_scores()
        high_scores_text = "Top 5 High Scores:\n"
        for idx, (player_name, wins) in enumerate(high_scores, start=1):
            if player_name not in ["LEFT PLAYER", "RIGHT PLAYER"]:
                high_scores_text += f"{idx}. {player_name}: {wins} wins\n"

        # Display high scores below the winner
        self.high_scores_label = tk.Label(self.master, text=high_scores_text, font=('Helvetica', 24), bg=winner_color, fg='white')
        self.high_scores_label.pack(pady=20)

        # Set a flag indicating a win has occurred
        self.game_over = True

    def show_gif_reward(self, winner_color, winner_name):
        # Load the GIF
        self.gif_frames = [tk.PhotoImage(file=r"C:\Users\exuxjas\Documents\PingPongGUI\media\giphy.gif", format=f"gif -index {i}") for i in range(50)]
        
        # Create a label to display the GIF
        self.gif_label = tk.Label(self.master, bg=winner_color)
        self.gif_label.pack(pady=20)

        # Start the GIF animationclear
        self.current_frame = 0
        self.animate_gif()

        # Play sound and set it to loop
        pygame.mixer.music.load(r"C:\Users\exuxjas\Documents\PingPongGUI\media\victory-sound.mp3")  # Path to your sound file
        pygame.mixer.music.play(-1)  # -1 will make the sound loop indefinitely

    def animate_gif(self):
        # Ensure gif_label exists before updating the GIF frame
        if hasattr(self, 'gif_label'):
            self.gif_label.config(image=self.gif_frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)  # Loop back to the start

            # Schedule the next frame update after a short delay
            self.master.after(55, self.animate_gif)  # Change 100 to a suitable delay for your GIF


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x300")  # Set a fixed size for better centering
    pong_score_keeper = PongScoreKeeper(root)
    root.mainloop()
