#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
import pygame
import time
from threading import Thread

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

class AudioPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stay Hydrated - Audio Player with Timeout")

        # Set default timeout duration (in minutes)
        self.timeout_duration_minutes = 20
        self.remaining_time = self.timeout_duration_minutes * 60  # Convert to seconds

        # GUI Elements
        self.create_widgets()

        # Start the countdown thread
        self.countdown_thread = None
        self.stop_thread = False

    def create_widgets(self):
        # Timeout Input Label and Entry
        self.timeout_label = tk.Label(self.root, text="Set Timeout (minutes):")
        self.timeout_label.pack(pady=10)

        self.timeout_input = tk.Entry(self.root)
        self.timeout_input.insert(tk.END, str(self.timeout_duration_minutes))
        self.timeout_input.pack(pady=5)

        # File Selection Button
        self.file_button = tk.Button(self.root, text="Select Audio File", command=self.select_file)
        self.file_button.pack(pady=10)

        # Audio Player Control Button
        self.play_button = tk.Button(self.root, text="Play Audio", state=tk.DISABLED, command=self.play_audio)
        self.play_button.pack(pady=5)

        # Countdown Display
        self.countdown_display = tk.Label(self.root, text="Timeout: 20:00", font=("Helvetica", 16))
        self.countdown_display.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.ogg")])
        if file_path:
            self.audio_file = file_path
            self.play_button.config(state=tk.NORMAL)  # Enable the play button once a file is selected

    def play_audio(self):
        # Start the audio
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play(loops=0, start=0.0)
        self.start_countdown()

    def start_countdown(self):
        # Start the countdown in a separate thread to avoid blocking the GUI
        self.stop_thread = False
        self.countdown_thread = Thread(target=self.run_countdown)
        self.countdown_thread.start()

    def run_countdown(self):
        while self.remaining_time > 0 and not self.stop_thread:
            time.sleep(1)
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.update_countdown_display(minutes, seconds)

        # If the time reaches zero, replay the audio and reset the timer
        if self.remaining_time <= 0 and not self.stop_thread:
            pygame.mixer.music.play(loops=0, start=0.0)  # Restart the audio
            self.remaining_time = int(self.timeout_input.get()) * 60  # Reset timer to input value
            self.run_countdown()

    def update_countdown_display(self, minutes, seconds):
        # Update the countdown label
        self.countdown_display.config(text=f"Timeout: {minutes:02d}:{seconds:02d}")
        self.countdown_display.update_idletasks()

    def stop_countdown(self):
        self.stop_thread = True
        if self.countdown_thread:
            self.countdown_thread.join()

    def reset_timer(self):
        self.remaining_time = int(self.timeout_input.get()) * 60  # Reset to user input
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.update_countdown_display(minutes, seconds)
        self.stop_countdown()

# Create the Tkinter window
root = tk.Tk()
app = AudioPlayerApp(root)

# Run the application
root.mainloop()
