import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import librosa
import numpy as np
from PIL import Image, ImageTk  # PIL library for handling images
import threading

# Function to get tempo from audio file
def get_tempo(audio_path):
    try:
        print(f"Loading audio file: {audio_path}")
        y, sr = librosa.load(audio_path)
        print("Audio file loaded successfully")

        # Updating progress bar during audio loading
        for i in range(5):
            progress_bar["value"] += 20
            root.update_idletasks()
            root.after(500)  # Simulate loading delay

        print("Extracting tempo")
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Updating progress bar during tempo extraction
        for i in range(5):
            progress_bar["value"] += 20
            root.update_idletasks()
            root.after(500)  # Simulate tempo extraction delay

        print(f"Extracted tempo: {tempo} BPM")

        # Convert tempo to scalar if it's a numpy array
        if isinstance(tempo, np.ndarray):
            tempo = tempo.item()

        return tempo
    except Exception as e:
        print(f"Error in get_tempo: {e}")
        raise

# Function to browse for audio file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac")])
    if file_path:
        try:
            progress_bar["value"] = 0  # Reset progress bar
            progress_bar["maximum"] = 100  # Set maximum value for progress bar
            progress_bar.start(10)  # Start indeterminate progress

            print(f"Selected file: {file_path}")
            song_name_label.config(text=f"Selected Song: {file_path}")

            # Use threading to prevent blocking the GUI
            threading.Thread(target=process_audio, args=(file_path,)).start()
        except Exception as e:
            print(f"Error in browse_file: {e}")
            messagebox.showerror("Error", f"Failed to process the audio file:\n{e}")
            progress_bar.stop()  # Stop progress bar
            progress_bar["value"] = 0  # Reset progress bar

# Function to process audio in a separate thread
def process_audio(file_path):
    try:
        tempo = get_tempo(file_path)
        result_label.config(text=f"Tempo: {tempo:.2f} BPM")

        progress_bar.stop()  # Stop progress bar
        progress_bar["value"] = 0  # Reset progress bar
    except Exception as e:
        print(f"Error in process_audio: {e}")
        messagebox.showerror("Error", f"Failed to process the audio file:\n{e}")
        progress_bar.stop()  # Stop progress bar
        progress_bar["value"] = 0  # Reset progress bar

# Function to reset the application state
def reset():
    song_name_label.config(text="Selected Song: None")
    result_label.config(text="Tempo: N/A")
    progress_bar.stop()
    progress_bar["value"] = 0

# Setting up the main application window
root = tk.Tk()
root.title("Tempo Extractor")
root.geometry("600x400")  # Initial window size
root.resizable(True, True)  # Allow resizing in both directions

# Load background image
bg_image_path = r"C:\Users\ashan\Desktop\Tempo Extracter\img1.jpg"  # Replace with your background image path
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((600, 400), Image.LANCZOS)  # Resize image to fit window with high-quality downsampling
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Heading title
title_label = ttk.Label(root, text="Tempo Extractor", font=('Helvetica', 24, 'bold'), background='#4CAF50', foreground='black')
title_label.pack(pady=20)

# Customizing style for buttons and progress bar
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12, 'bold'), background='#4CAF50', foreground='black')
style.configure("TProgressbar", thickness=5, background='#4CAF50')

# Adding a button to browse files
browse_button = ttk.Button(root, text="Browse Audio File", style='TButton', command=browse_file)
browse_button.pack(pady=10)

# Label to display the selected song name
song_name_label = ttk.Label(root, text="Selected Song: None", font=('Helvetica', 12), background='#4CAF50', foreground='white')
song_name_label.pack(pady=10)

# Progress bar (hidden initially)
progress_bar = ttk.Progressbar(root, style="TProgressbar", orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=20)
progress_bar.stop()

# Label to display the result
result_label = ttk.Label(root, text="Tempo: N/A", font=('Helvetica', 16, 'bold'), background='#4CAF50', foreground='white')
result_label.pack(pady=20)

# Reset button
reset_button = ttk.Button(root, text="Reset", style='TButton', command=reset)
reset_button.pack(pady=10)

# Running the application
root.mainloop()
