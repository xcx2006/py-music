import tkinter as tk
from tkinter import filedialog, ttk
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("音乐播放器")
        self.root.geometry("400x500")

        pygame.mixer.init()

        self.song_list = []
        self.current_song_index = 0
        self.song_length = 0

        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self.root, text="加载歌曲", command=self.load_songs)
        self.load_button.pack()

        self.song_listbox = tk.Listbox(self.root)
        self.song_listbox.pack(fill=tk.BOTH, expand=True)
        self.song_listbox.bind('<<ListboxSelect>>', self.on_song_select)

        self.play_button = tk.Button(self.root, text="播放", command=self.play_song)
        self.play_button.pack()

        self.pause_button = tk.Button(self.root, text="暂停", command=self.pause_song)
        self.pause_button.pack()

        self.next_button = tk.Button(self.root, text="下一首", command=self.next_song)
        self.next_button.pack()

        self.prev_button = tk.Button(self.root, text="上一首", command=self.prev_song)
        self.prev_button.pack()

        self.progress = ttk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.seek_song)
        self.progress.pack(fill=tk.X)

        self.update_progress()

    def load_songs(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("音频文件", "*.mp3;*.wav")])
        new_songs = list(file_paths)
        self.song_list.extend(new_songs)
        for song in new_songs:
            self.song_listbox.insert(tk.END, song)

    def on_song_select(self, event):
        if self.song_listbox.curselection():
            self.current_song_index = self.song_listbox.curselection()[0]
            self.play_song()

    def play_song(self):
        if self.song_list:
            pygame.mixer.music.load(self.song_list[self.current_song_index])
            pygame.mixer.music.play()
            self.song_length = pygame.mixer.Sound(self.song_list[self.current_song_index]).get_length()
            self.update_progress()

    def pause_song(self):
        pygame.mixer.music.pause()

    def next_song(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
            self.play_song()

    def prev_song(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
            self.play_song()

    def seek_song(self, value):
        if self.song_list:
            pygame.mixer.music.pause()
            pygame.mixer.music.set_pos(float(value) * self.song_length / 100)
            pygame.mixer.music.unpause()

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() / 1000
            self.progress.set((current_pos / self.song_length) * 100)
        self.root.after(1000, self.update_progress)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    player.run()