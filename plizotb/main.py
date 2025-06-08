import tkinter as tk
from tkinter import ttk
import pygame.mixer
import time
import threading
import wave
import pyaudio
import numpy as np
from pydub import AudioSegment
from tkinter import filedialog

pygame.mixer.init()

# hangkuki
sounds = {
    "Kick": pygame.mixer.Sound("sounds/kick.wav"),
    "Snare": pygame.mixer.Sound("sounds/snare.wav"),
    "Hi-Hat": pygame.mixer.Sound("sounds/hihat.wav"),
    "C4": pygame.mixer.Sound("sounds/C4.wav"),
    "D4": pygame.mixer.Sound("sounds/D4.wav"),
    "E4": pygame.mixer.Sound("sounds/E4.wav")
}

# jatszocucc
TRACKS = ["Kick", "Snare", "Hi-Hat", "Piano"]
STEPS = 16
BPM = 180
STEP_DELAY = 60.0 / BPM

# valtozoka
timeline = {
    "Kick" : [False]*STEPS,
    "Snare" : [False]*STEPS,
    "Hi-Hat": [False]*STEPS,
    "Piano": [None]*STEPS  
}
current_step = 0
playing = False
bpm_value = BPM
recorded_notes = []

root = tk.Tk()
root.title("On The Beat")
root.configure(bg="black")

frame_drum = tk.Frame(root)
frame_drum.pack(pady=10)

# bpm
bpm_frame = tk.Frame(root, bg="black")
bpm_frame.pack(pady=10)

# sliderbpm
bpm_slider = tk.Scale(bpm_frame, from_=60, to=240, orient="horizontal", length=300, label="BPM")
bpm_slider.set(BPM)
bpm_slider.pack(side="left", padx=10)

# inputbmp
bpm_entry = tk.Entry(bpm_frame, width=5)
bpm_entry.insert(0, str(BPM))
bpm_entry.pack(side="left", padx=5)

bpm_label = tk.Label(bpm_frame, text="BPM", fg="white", bg="black")
bpm_label.pack(side="left")

def update_entry_from_slider(value):
    bpm_entry.delete(0, tk.END)
    bpm_entry.insert(0, value)

def update_slider_from_entry(event=None):
    try:
        value = int(bpm_entry.get())
        if 60 <= value <= 240:
            bpm_slider.set(value)
    except:
        pass

bpm_slider.config(command=update_entry_from_slider)
bpm_entry.bind("<FocusOut>", update_slider_from_entry)
bpm_entry.bind("<Return>", update_slider_from_entry)

def play_sound(name):
    sounds[name].play()

for name in ["Kick", "Snare", "Hi-Hat"]:
    btn = tk.Button(frame_drum, text=name, width=10, command=lambda n=name: play_sound(n))
    btn.pack(side=tk.LEFT, padx=5)

# zong
btn_piano = tk.Button(frame_drum, text="Piano", width=10, command=lambda: play_sound("C4"))
btn_piano.pack(side=tk.LEFT, padx=5)

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

def toggle_step(track, step, button=None):
    index = TRACKS.index(track)
    if track == "Piano":
        if button == "right":
            # torol
            timeline[track][step] = None
            timeline_buttons[index][step].config(bg="lightgray", text="")
        else:
            # zongivalasztas
            choose_piano_note(step)
    else:
        if button == "right":
            # ez mar nemtom mi
            timeline[track][step] = False
            timeline_buttons[index][step].config(bg="lightgray")
        else:
            # eztse
            timeline[track][step] = not timeline[track][step]
            color = "green" if timeline[track][step] else "lightgray"
            timeline_buttons[index][step].config(bg=color)

# play
play_button = tk.Button(root, text="▶️ Indítás", width=15)

# honnan jatszos lejatszos
slider_frame = tk.Frame(root, bg="black")
slider_frame.pack(pady=10)

position_slider = tk.Scale(slider_frame, from_=0, to=STEPS - 1, orient="horizontal", length=STEPS * 42)
position_slider.set(0)
position_slider.pack()

slider_label = tk.Label(slider_frame, text="Indulási pozíció", fg="white", bg="black")
slider_label.pack()

def toggle_play():
    global playing, current_step, bpm_value
    playing = not playing
    play_button.config(text="⏹️ Stop" if playing else "▶️ Indítás")
    if playing:
        current_step = position_slider.get()

        try:
            bpm_value = int(bpm_slider.get())
        except:
            bpm_value = 120

        thread = threading.Thread(target=play_loop)
        thread.start()
    else:
        current_step = 0

play_button.config(command=toggle_play)
play_button.pack(pady=10)


# lup
def play_loop():
    global current_step, playing, bpm_value, recorded_notes
    start_time = time.time()

    while playing:
        elapsed = time.time() - start_time
        for track_index, track in enumerate(TRACKS[:3]):
            if timeline[track][current_step]:
                sounds[track].play()
                recorded_notes.append((elapsed, track))

        piano_note = timeline["Piano"][current_step]
        if piano_note and piano_note in sounds:
            sounds[piano_note].play()
            recorded_notes.append((elapsed, piano_note))

        current_step = (current_step + 1) % STEPS
        time.sleep(max(0, 60.0 / bpm_value - 0.001))  

# billentyuzetes vergodes
def key_press(event):
    if event.char in key_map:
        sound_name = key_map[event.char]
        if sound_name in sounds:
            play_sound(sound_name)
    elif event.char in ['f', 'g', 'h']:
        note_name = {'f': 'C4', 'g': 'D4', 'h': 'E4'}[event.char]
        play_sound(note_name)
        add_piano_note(note_name, current_step)

# afsasfasf
def add_piano_note(note, step):
    timeline["Piano"][step] = True
    timeline_buttons[3][step].config(bg="orange")

def get_sound_array(sound):
    from io import BytesIO
    with BytesIO() as b:
        with wave.open(b, 'wb') as wf:
            wf.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
            data = sound.get_raw()
            wf.writeframes(data)
        b.seek(0)
        return np.frombuffer(b.read(), dtype=np.int16)
    
def array_to_audiosegment(arr):
    from pydub import AudioSegment
    raw = arr.tobytes()
    return AudioSegment(raw, frame_rate=44100, sample_width=2, channels=1)

def save_playback_to_wav():
    total_duration = int(STEPS * (60.0 / bpm_value) * 1000)
    silence = AudioSegment.silent(duration=total_duration)

    for note_time, sound_name in recorded_notes:
        if sound_name in sounds:
            sound = sounds[sound_name]
            sample_array = get_sound_array(sound)
            audio_segment = array_to_audiosegment(sample_array)
            silence = silence.overlay(audio_segment, position=int(note_time * 1000))

    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Wave File", "*.wav")])
    if file_path:
        silence.export(file_path, format="wav")
        print(f"Mentve: {file_path}")

def apply_delay(sound_array, delay_ms=100, decay=0.5):
    delay_samples = int(delay_ms * 44100 / 1000)
    
    sound_float = sound_array.astype(np.float32)
    output = np.zeros(len(sound_float) + delay_samples, dtype=np.float32)
    
    output[:len(sound_float)] += sound_float
    output[delay_samples:] += decay * sound_float
    
    
    return np.clip(output, -32768, 32767).astype(np.int16)

sound_array = get_sound_array(sounds["C4"])
delayed_array = apply_delay(sound_array, delay_ms=200)
delayed_sound = array_to_audiosegment(delayed_array)
delayed_sound.export("C4_delay.wav", format="wav")

# xport
export_button = tk.Button(root, text="💾 Exportálás (.wav)", width=25,
                          command=save_playback_to_wav,
                          bg="#444", fg="white")
export_button.pack(pady=10)

root.bind("<Key>", key_press)

root.mainloop()