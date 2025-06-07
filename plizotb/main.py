import tkinter as tk
from tkinter import ttk
import pygame.mixer
import time
import threading

# Pygame inicializálása
pygame.mixer.init()

# Hangok betöltése
sounds = {
    "Kick": pygame.mixer.Sound("sounds/kick.wav"),
    "Snare": pygame.mixer.Sound("sounds/snare.wav"),
    "Hi-Hat": pygame.mixer.Sound("sounds/hihat.wav"),
    "C4": pygame.mixer.Sound("sounds/C4.wav"),
    "D4": pygame.mixer.Sound("sounds/D4.wav"),
    "E4": pygame.mixer.Sound("sounds/E4.wav")
}

# Idővonal beállítások
TRACKS = ["Kick", "Snare", "Hi-Hat", "Piano"]
STEPS = 16
BPM = 180
STEP_DELAY = 60.0 / BPM

# Globális változók
# Globális változók
timeline = {
    "Kick": [False]*STEPS,
    "Snare": [False]*STEPS,
    "Hi-Hat": [False]*STEPS,
    "Piano": [None]*STEPS  # Most None vagy hangnevek vannak itt
}
current_step = 0
playing = False

# Tkinter ablak
root = tk.Tk()
root.title("🎹 Drum + Piano Zenekészítő")
root.configure(bg="black")

# Dobszám gombok
frame_drum = tk.Frame(root)
frame_drum.pack(pady=10)

def play_sound(name):
    sounds[name].play()

for name in ["Kick", "Snare", "Hi-Hat"]:
    btn = tk.Button(frame_drum, text=name, width=10, command=lambda n=name: play_sound(n))
    btn.pack(side=tk.LEFT, padx=5)

# Piano gomb
btn_piano = tk.Button(frame_drum, text="Piano", width=10, command=lambda: play_sound("C4"))
btn_piano.pack(side=tk.LEFT, padx=5)

# Idővonal
frame_timeline = tk.Frame(root)
frame_timeline.pack(pady=20)

timeline_buttons = []

key_map = {
    'a': 'Kick',
    's': 'Snare',
    'd': 'Hi-Hat',
    'f': 'C4',
    'g': 'D4',
    'h': 'E4'
}

note_to_track = {
    'C4': 'Piano',
    'D4': 'Piano',
    'E4': 'Piano'
}

for row, track in enumerate(TRACKS):
    lbl = tk.Label(frame_timeline, text=track)
    lbl.grid(row=row*2, column=0, sticky="w", padx=5)

    row_buttons = []
    for col in range(STEPS):
        btn = tk.Button(frame_timeline, text="", width=4, height=2, bg="lightgray")
        btn.grid(row=row*2+1, column=col, padx=2, pady=2)
        btn.bind("<Button-1>", lambda e, t=track, c=col: toggle_step(t, c))
        btn.bind("<Button-3>", lambda e, t=track, c=col: toggle_step(t, c, "right"))
        row_buttons.append(btn)
    timeline_buttons.append(row_buttons)

def choose_piano_note(step):
    note_window = tk.Toplevel(root)
    note_window.title("Hang választás")

    for note in ["C4", "D4", "E4", "F4", "G4"]:
        btn = tk.Button(note_window, text=note, width=10,
                        command=lambda n=note, w=note_window, s=step: set_piano_note(n, s, w))
        btn.pack(pady=5)

def set_piano_note(note, step, window):
    timeline["Piano"][step] = note
    index = TRACKS.index("Piano")
    timeline_buttons[index][step].config(bg="orange", text=note)
    window.destroy()
# Aktivált cellák frissítése
def toggle_step(track, step, button=None):
    index = TRACKS.index(track)
    if track == "Piano":
        if button == "right":
            # Törlés
            timeline[track][step] = None
            timeline_buttons[index][step].config(bg="lightgray", text="")
        else:
            # Hang választás
            choose_piano_note(step)
    else:
        if button == "right":
            # Inaktiválás
            timeline[track][step] = False
            timeline_buttons[index][step].config(bg="lightgray")
        else:
            # Aktiválás
            timeline[track][step] = not timeline[track][step]
            color = "green" if timeline[track][step] else "lightgray"
            timeline_buttons[index][step].config(bg=color)

# Lejátszás gomb
play_button = tk.Button(root, text="▶️ Indítás", width=15)

# Csúszka az indulási pozíció beállításához
position_slider = tk.Scale(root, from_=0, to=STEPS - 1, orient="horizontal", label="Indulási pozíció")
position_slider.set(0)  # Alapértelmezett érték
position_slider.pack(pady=10)

def toggle_play():
    global playing, current_step
    playing = not playing
    play_button.config(text="⏹️ Stop" if playing else "▶️ Indítás")
    if playing:
        current_step = position_slider.get()  # ← itt olvassuk ki a slider értékét
        thread = threading.Thread(target=play_loop)
        thread.start()
    else:
        current_step = 0  # Visszaugrás az elejére

play_button.config(command=toggle_play)
play_button.pack(pady=10)
position_slider.pack(pady=10)  # ← ez jön ide

# Loop függvény
def play_loop():
    global current_step, playing
    while playing:
        for track_index, track in enumerate(TRACKS[:3]):
            if timeline[track][current_step]:
                sounds[track].play()

        piano_note = timeline["Piano"][current_step]
        if piano_note and piano_note in sounds:
            sounds[piano_note].play()

        current_step = (current_step + 1) % STEPS
        time.sleep(STEP_DELAY)

# Billentyűzet támogatás
def key_press(event):
    if event.char in key_map:
        sound_name = key_map[event.char]
        if sound_name in sounds:
            play_sound(sound_name)
    elif event.char in ['f', 'g', 'h']:
        note_name = {'f': 'C4', 'g': 'D4', 'h': 'E4'}[event.char]
        play_sound(note_name)
        add_piano_note(note_name, current_step)

# Piano hang hozzáadása az aktuális pozícióhoz (opcionális)
def add_piano_note(note, step):
    timeline["Piano"][step] = True
    timeline_buttons[3][step].config(bg="orange")

root.bind("<Key>", key_press)

# Program indítása
root.mainloop()