import random
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class App(tk.Tk):
    text_font = ('Courier', 11)
    default_font = ('TkDefaultFont', 11)

    def __init__(self, title: str) -> None:
        super().__init__()

        self.title(title)
        self.resizable(width=False, height=False)

        f_left = ttk.Frame(self)
        f_left.grid(row=1, column=0)

        ttk.Label(f_left, text='Your Message', font=self.default_font).pack(padx=5, pady=5)

        t_message = ScrolledText(
            f_left, width=20, height=5, font=self.text_font, spacing2=3, spacing3=3, wrap='word')
        t_message.pack(padx=10, pady=5)

        t_message.bind('<KeyRelease>', self.input_key_pressed)

        self.message = t_message

        f_right = ttk.Frame(self)
        f_right.grid(row=1, column=1)

        ttk.Label(f_right, text='sPoNgECaSe', font=self.default_font).pack(padx=5, pady=5)

        t_spongecase = ScrolledText(
            f_right, width=20, height=5, font=self.text_font, spacing2=3, spacing3=3, wrap='word')
        t_spongecase['state'] = 'disabled'
        t_spongecase.pack(padx=10, pady=5)

        self.spongecase = t_spongecase

        f_buttons = ttk.Frame(self)
        f_buttons.grid(row=2, column=0, columnspan=2)

        b_quit = ttk.Button(f_buttons, text='Quit', command=self.destroy)
        b_quit.pack(side=tk.LEFT, padx=5, pady=10, ipady=3)

        b_clip = ttk.Button(f_buttons, text='sPoNgeCAsE to Clipboard', command=self.spongecase_to_clipboard)
        b_clip.pack(padx=5, pady=10, ipadx=10, ipady=3)

        f_bottom = ttk.Frame(self, height=5)
        f_bottom.grid(row=3, column=0, columnspan=2)

        style = ttk.Style(self)
        style.configure('TButton', font=self.default_font)

        t_message.focus()

    def input_key_pressed(self, event: tk.Event) -> None:
        if not event.keysym.isprintable():
            return
        to_upper = False
        message = self.message.get(1.0, tk.END)
        bucket = []
        for ch in message:
            bucket.append(ch.upper() if to_upper else ch.lower())
            if random.random() > 0.1:
                to_upper = not to_upper
        spongecase = ''.join(bucket)
        widget_state = self.spongecase['state']
        self.spongecase['state'] = 'normal'
        self.spongecase.delete(1.0, tk.END)
        self.spongecase.insert(tk.END, spongecase.strip('\n'))
        self.spongecase['state'] = widget_state

    def spongecase_to_clipboard(self) -> None:
        spongecase = self.spongecase.get(1.0, tk.END)
        self.spongecase.clipboard_clear()
        self.spongecase.clipboard_append(spongecase)


if __name__ == '__main__':
    App('sPoNGgEcAsE').mainloop()
