"""老陳專注計時器：使用 Python 內建 tkinter 的 25 分鐘專注倒數計時器。"""

import math
import time
import tkinter as tk
from tkinter import messagebox


FOCUS_SECONDS = 25 * 60


class FocusTimer:
    def __init__(self, root):
        self.root = root
        self.remaining_seconds = float(FOCUS_SECONDS)
        self.deadline = None
        self.after_id = None

        root.title("老陳專注計時器")
        root.geometry("420x320")
        root.minsize(360, 290)
        root.configure(bg="#142235")
        root.protocol("WM_DELETE_WINDOW", self.close)

        self.clock_text = tk.StringVar(value="25:00")
        self.status_text = tk.StringVar(value="準備開始")

        tk.Label(
            root,
            text="老陳專注計時器",
            font=("Microsoft JhengHei UI", 22, "bold"),
            fg="#F9FAFB",
            bg="#142235",
        ).pack(pady=(28, 4))

        tk.Label(
            root,
            text="一次專注，從 25 分鐘開始",
            font=("Microsoft JhengHei UI", 11),
            fg="#C5D0DE",
            bg="#142235",
        ).pack()

        tk.Label(
            root,
            textvariable=self.clock_text,
            font=("Consolas", 55, "bold"),
            fg="#F7C96B",
            bg="#142235",
        ).pack(pady=(12, 1))

        tk.Label(
            root,
            textvariable=self.status_text,
            font=("Microsoft JhengHei UI", 11),
            fg="#C5D0DE",
            bg="#142235",
        ).pack()

        buttons = tk.Frame(root, bg="#142235")
        buttons.pack(pady=(22, 8))

        self.start_button = self.make_button(buttons, "開始", self.start, "#287C6F")
        self.pause_button = self.make_button(buttons, "暫停", self.pause, "#596B86")
        self.reset_button = self.make_button(buttons, "重設", self.reset, "#8B5E43")

        self.start_button.grid(row=0, column=0, padx=6)
        self.pause_button.grid(row=0, column=1, padx=6)
        self.reset_button.grid(row=0, column=2, padx=6)
        self.pause_button.configure(state="disabled")

    @staticmethod
    def make_button(parent, label, command, background):
        return tk.Button(
            parent,
            text=label,
            command=command,
            width=8,
            font=("Microsoft JhengHei UI", 11, "bold"),
            fg="white",
            bg=background,
            activeforeground="white",
            activebackground=background,
            relief="flat",
            cursor="hand2",
            padx=4,
            pady=8,
        )

    def refresh_clock(self):
        seconds = math.ceil(max(0.0, self.remaining_seconds))
        minutes, seconds = divmod(seconds, 60)
        self.clock_text.set(f"{minutes:02d}:{seconds:02d}")

    def cancel_tick(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def start(self):
        if self.deadline is not None:
            return
        if self.remaining_seconds <= 0:
            self.remaining_seconds = float(FOCUS_SECONDS)

        # 用單調時鐘計時，避免視窗卡頓令倒數越走越慢。
        self.deadline = time.monotonic() + self.remaining_seconds
        self.status_text.set("專注進行中")
        self.start_button.configure(state="disabled")
        self.pause_button.configure(state="normal")
        self.tick()

    def pause(self):
        if self.deadline is None:
            return
        self.remaining_seconds = max(0.0, self.deadline - time.monotonic())
        self.deadline = None
        self.cancel_tick()
        self.refresh_clock()
        if self.remaining_seconds <= 0:
            self.finish()
            return
        self.status_text.set("已暫停")
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled")

    def reset(self):
        self.deadline = None
        self.cancel_tick()
        self.remaining_seconds = float(FOCUS_SECONDS)
        self.refresh_clock()
        self.status_text.set("準備開始")
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled")

    def tick(self):
        self.after_id = None
        if self.deadline is None:
            return

        self.remaining_seconds = max(0.0, self.deadline - time.monotonic())
        self.refresh_clock()
        if self.remaining_seconds <= 0:
            self.finish()
        else:
            self.after_id = self.root.after(100, self.tick)

    def finish(self):
        self.deadline = None
        self.cancel_tick()
        self.remaining_seconds = 0.0
        self.refresh_clock()
        self.status_text.set("時間到")
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled")
        self.root.bell()
        messagebox.showinfo(
            "時間到",
            "25 分鐘的專注時間已結束，辛苦了！",
            parent=self.root,
        )

    def close(self):
        self.deadline = None
        self.cancel_tick()
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    FocusTimer(window)
    window.mainloop()
