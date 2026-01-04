try:
    import tkinter as tk
    from tkinter import ttk, messagebox, font
except Exception:  # Tkinter may be missing in headless/test environments
    tk = None
    ttk = None
    messagebox = None
    font = None
import time
from threading import Thread
import random
from pathlib import Path


class PixelPomodoroGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 PIXEL POMODORO ARCADE 🎮")
        self.root.geometry("800x900")
        self.root.resizable(False, False)

        # Retro pixel fonts
        self.title_font = font.Font(family="Courier", size=28, weight="bold")
        self.timer_font = font.Font(family="Courier", size=64, weight="bold")
        self.button_font = font.Font(family="Courier", size=12, weight="bold")
        self.small_font = font.Font(family="Courier", size=10, weight="bold")

        # Arcade colors
        self.colors = {
            'bg': '#0F0F1F',
            'accent1': '#FF006E',
            'accent2': '#FFBE0B',
            'accent3': '#00F5FF',
            'accent4': '#8338EC',
            'green': '#06FFA5',
            'text': '#FFFFFF',
            'shadow': '#000000'
        }

        # Main canvas
        self.canvas = tk.Canvas(
            root,
            width=800,
            height=900,
            bg=self.colors['bg'],
            highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Draw retro background
        self.draw_pixel_background()

        # Animated stars
        self.stars = []
        self.create_stars()
        self.animate_stars()

        # Main arcade cabinet frame
        cabinet_frame = tk.Frame(self.canvas, bg='#1A1A2E', bd=0)
        cabinet_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=700,
            height=800)

        # Draw pixel border
        self.draw_pixel_border(cabinet_frame)

        # TITLE SCREEN with pixel art style
        title_container = tk.Frame(cabinet_frame, bg='#16213E')
        title_container.pack(fill="x", pady=20)

        # Blinking INSERT COIN text
        self.coin_label = tk.Label(
            title_container,
            text="◆ INSERT COIN ◆",
            font=self.button_font,
            fg=self.colors['accent2'],
            bg='#16213E')
        self.coin_label.pack(pady=5)
        self.blink_coin_text()

        # Title with pixel effect
        title_frame = tk.Frame(title_container, bg='#FF006E', bd=0)
        title_frame.pack(pady=10)

        # Shadow text effect
        shadow_label = tk.Label(
            title_frame,
            text="POMODORO",
            font=self.title_font,
            fg='#000000',
            bg='#FF006E')
        shadow_label.place(x=3, y=3)

        main_label = tk.Label(
            title_frame,
            text="POMODORO",
            font=self.title_font,
            fg=self.colors['accent2'],
            bg='#FF006E')
        main_label.pack(padx=20, pady=10)

        # Score/Timer Display (Arcade Screen)
        screen_frame = tk.Frame(
            cabinet_frame,
            bg='#000000',
            bd=8,
            relief="sunken")
        screen_frame.pack(pady=20, padx=40)

        # Scanline effect container
        scanline_container = tk.Frame(screen_frame, bg='#001F1F')
        scanline_container.pack(padx=10, pady=10)

        # Timer display with CRT effect
        self.timer_display = tk.Frame(
            scanline_container,
            bg='#001F1F',
            width=400,
            height=160)
        self.timer_display.pack()

        self.timer_label = tk.Label(
            self.timer_display,
            text="25:00",
            font=self.timer_font,
            fg=self.colors['green'],
            bg='#001F1F')
        self.timer_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add scanlines
        self.add_scanlines(self.timer_display)

        # Status bar (like game HP/MP bar)
        status_bar = tk.Frame(cabinet_frame, bg='#1A1A2E')
        status_bar.pack(fill="x", padx=40, pady=10)

        self.status_label = tk.Label(
            status_bar,
            text="▶ READY TO START",
            font=self.button_font,
            fg=self.colors['text'],
            bg='#1A1A2E')
        self.status_label.pack()

        # Progress bar (pixel style)
        self.progress_canvas = tk.Canvas(
            status_bar,
            width=500,
            height=30,
            bg='#0F0F1F',
            highlightthickness=0)
        self.progress_canvas.pack(pady=5)
        self.draw_pixel_progress_bar(0)

        # ARCADE BUTTONS SECTION
        buttons_container = tk.Frame(cabinet_frame, bg='#1A1A2E')
        buttons_container.pack(pady=20)

        # Row 1 - Main action buttons
        btn_row1 = tk.Frame(buttons_container, bg='#1A1A2E')
        btn_row1.pack(pady=8)

        self.create_arcade_button(
            btn_row1,
            "▶ WORK",
            self.colors['accent1'],
            self.start_work,
            "A").pack(
            side="left",
            padx=8)

        self.create_arcade_button(
            btn_row1,
            "☕ BREAK",
            self.colors['accent3'],
            self.start_break,
            "B").pack(
            side="left",
            padx=8)

        # Row 2 - Secondary buttons
        btn_row2 = tk.Frame(buttons_container, bg='#1A1A2E')
        btn_row2.pack(pady=8)

        self.create_arcade_button(
            btn_row2,
            "🌙 LONG",
            self.colors['accent4'],
            self.start_long_break,
            "X").pack(
            side="left",
            padx=8)

        self.finish_btn = self.create_arcade_button(
            btn_row2, "✓ FINISH", self.colors['green'], self.finish_session, "Y")
        self.finish_btn.pack(side="left", padx=8)
        self.finish_btn.config(state="disabled")

        # Custom timer (Arcade style input)
        custom_container = self.create_pixel_panel(cabinet_frame, "#0F1626")
        custom_container.pack(pady=12, padx=40, fill="x")

        custom_label = tk.Label(
            custom_container,
            text="⚡ CUSTOM TIME:",
            font=self.small_font,
            fg=self.colors['accent2'],
            bg="#0F1626")
        custom_label.pack(side="left", padx=10)

        self.custom_entry = tk.Entry(
            custom_container,
            width=8,
            font=self.button_font,
            justify="center",
            bg='#001F1F',
            fg=self.colors['green'],
            insertbackground=self.colors['green'],
            bd=3)
        self.custom_entry.pack(side="left", padx=5)

        self.create_small_button(
            custom_container,
            "GO!",
            self.colors['accent2'],
            self.start_custom_timer).pack(
            side="left",
            padx=5)

        # Quest log (Task list)
        quest_container = self.create_pixel_panel(cabinet_frame, "#1A0F26")
        quest_container.pack(pady=12, padx=40, fill="x")

        quest_label = tk.Label(
            quest_container,
            text="📝 NEW QUEST:",
            font=self.small_font,
            fg=self.colors['accent1'],
            bg="#1A0F26")
        quest_label.pack(side="left", padx=10)

        self.task_entry = tk.Entry(
            quest_container,
            width=25,
            font=self.button_font,
            bg='#001F1F',
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            bd=3)
        self.task_entry.pack(side="left", padx=5)

        self.create_small_button(
            quest_container,
            "ADD",
            self.colors['accent1'],
            self.add_task).pack(
            side="left",
            padx=5)

        # Quest Board (Task List) - Arcade scoreboard style
        board_title = tk.Label(
            cabinet_frame,
            text="═══ QUEST BOARD ═══",
            font=self.button_font,
            fg=self.colors['accent2'],
            bg='#1A1A2E')
        board_title.pack(pady=10)

        # High score style list
        list_container = self.create_pixel_panel(cabinet_frame, "#000000")
        list_container.pack(pady=10, padx=40, fill="both", expand=True)

        # Custom style for arcade look
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Arcade.Treeview",
                        background="#001F1F",
                        foreground=self.colors['green'],
                        fieldbackground="#001F1F",
                        font=self.small_font,
                        rowheight=35,
                        borderwidth=0)
        style.configure("Arcade.Treeview.Heading",
                        background="#0F0F1F",
                        foreground=self.colors['accent2'],
                        font=self.button_font,
                        borderwidth=2,
                        relief="raised")
        style.map("Arcade.Treeview",
                  background=[("selected", "#FF006E")],
                  foreground=[("selected", "#FFFFFF")])

        self.tree = ttk.Treeview(
            list_container,
            columns=(
                "Task",
                "Status"),
            show="headings",
            height=5,
            style="Arcade.Treeview")
        self.tree.heading("Task", text="⚔ QUEST NAME")
        self.tree.heading("Status", text="⭐ STATUS")
        self.tree.column("Task", anchor="w", width=400)
        self.tree.column("Status", anchor="center", width=150)
        self.tree.pack(padx=5, pady=5, fill="both", expand=True)

        # Action buttons (Arcade style)
        action_frame = tk.Frame(cabinet_frame, bg='#1A1A2E')
        action_frame.pack(pady=15)

        self.create_arcade_button(
            action_frame,
            "✓ COMPLETE",
            self.colors['green'],
            self.complete_task,
            "").pack(
            side="left",
            padx=5)

        self.create_arcade_button(
            action_frame,
            "💾 SAVE",
            self.colors['accent3'],
            self.save_tasks,
            "").pack(
            side="left",
            padx=5)

        # Footer with pixel hearts
        footer = tk.Label(
            cabinet_frame,
            text="♥♥♥ LIVES: 3 ♥♥♥  |  LEVEL: 1  |  SCORE: 0000",
            font=self.small_font,
            fg=self.colors['accent2'],
            bg='#1A1A2E')
        footer.pack(pady=10)

        self.running = False
        self.current_selected_task = None
        self.progress = 0

    def draw_pixel_background(self):
        """Draw retro arcade background"""
        # Grid pattern
        for i in range(0, 800, 40):
            self.canvas.create_line(i, 0, i, 900, fill='#1A1A2E', width=1)
        for i in range(0, 900, 40):
            self.canvas.create_line(0, i, 800, i, fill='#1A1A2E', width=1)

        # Corner decorations (pixel style)
        self.draw_pixel_decoration(20, 20)
        self.draw_pixel_decoration(760, 20)
        self.draw_pixel_decoration(20, 860)
        self.draw_pixel_decoration(760, 860)

    def draw_pixel_decoration(self, x, y):
        """Draw pixel art corner decoration"""
        colors = [
            self.colors['accent1'],
            self.colors['accent2'],
            self.colors['accent3']]
        size = 8
        for i in range(3):
            self.canvas.create_rectangle(x + i * size, y, x + (i + 1) * size, y + size,
                                         fill=colors[i], outline="")
            self.canvas.create_rectangle(x,
                                         y + i * size,
                                         x + size,
                                         y + (i + 1) * size,
                                         fill=colors[i],
                                         outline="")

    def create_stars(self):
        """Create animated stars for background"""
        for _ in range(50):
            x = random.randint(0, 800)
            y = random.randint(0, 900)
            size = random.randint(1, 3)
            star = self.canvas.create_rectangle(x, y, x + size, y + size,
                                                fill='#FFFFFF', outline="")
            self.stars.append({'id': star, 'speed': random.uniform(0.5, 2)})

    def animate_stars(self):
        """Animate starfield"""
        for star in self.stars:
            coords = self.canvas.coords(star['id'])
            if coords:
                new_y = coords[1] + star['speed']
                if new_y > 900:
                    new_y = 0
                    coords[0] = random.randint(0, 800)
                self.canvas.coords(star['id'], coords[0], new_y,
                                   coords[2], new_y + (coords[3] - coords[1]))

        self.root.after(50, self.animate_stars)

    def blink_coin_text(self):
        """Blink the INSERT COIN text"""
        current_color = self.coin_label.cget("fg")
        new_color = self.colors['accent2'] if current_color == '#16213E' else '#16213E'
        self.coin_label.config(fg=new_color)
        self.root.after(500, self.blink_coin_text)

    def add_scanlines(self, widget):
        """Add CRT scanline effect"""
        for i in range(0, 160, 4):
            line = tk.Frame(widget, bg='#000000', height=2)
            line.place(x=0, y=i, width=400)

    def draw_pixel_progress_bar(self, percent):
        """Draw retro style progress bar"""
        self.progress_canvas.delete("all")

        # Border
        self.progress_canvas.create_rectangle(
            0, 0, 500, 30, outline=self.colors['text'], width=3)

        # Fill (pixel blocks)
        filled_width = int((percent / 100) * 480)
        block_width = 20

        for i in range(0, filled_width, block_width):
            color = self.colors['green'] if percent < 100 else self.colors['accent2']
            self.progress_canvas.create_rectangle(
                10 + i,
                5,
                10 + i + block_width - 2,
                25,
                fill=color,
                outline=self.colors['text'])

    def draw_pixel_border(self, widget):
        """Draw pixel art border around widget"""
        canvas = tk.Canvas(
            widget,
            width=700,
            height=800,
            bg='#1A1A2E',
            highlightthickness=0)
        canvas.place(x=0, y=0)
        canvas.lower()

        # Draw border blocks
        block_size = 10
        colors = [
            self.colors['accent1'],
            self.colors['accent3'],
            self.colors['accent4']]

        for i in range(0, 700, block_size * 3):
            for j, color in enumerate(colors):
                # Top border
                canvas.create_rectangle(i + j * block_size,
                                        0,
                                        i + (j + 1) * block_size,
                                        block_size,
                                        fill=color,
                                        outline="")
                # Bottom border
                canvas.create_rectangle(i + j * block_size, 790,
                                        i + (j + 1) * block_size, 800, fill=color, outline="")

        for i in range(0, 800, block_size * 3):
            for j, color in enumerate(colors):
                # Left border
                canvas.create_rectangle(0,
                                        i + j * block_size,
                                        block_size,
                                        i + (j + 1) * block_size,
                                        fill=color,
                                        outline="")
                # Right border
                canvas.create_rectangle(690,
                                        i + j * block_size,
                                        700,
                                        i + (j + 1) * block_size,
                                        fill=color,
                                        outline="")

    def create_arcade_button(self, parent, text, color, command, key):
        """Create retro arcade button with shadow"""
        container = tk.Frame(parent, bg='#1A1A2E')

        # Shadow
        shadow = tk.Label(container, text=text, font=self.button_font,
                          bg='#000000', fg='#000000', padx=25, pady=12)
        shadow.place(x=4, y=4)

        # Main button
        btn = tk.Button(container, text=text, font=self.button_font,
                        bg=color, fg='#FFFFFF', bd=4, relief="raised",
                        command=command, cursor="hand2", padx=25, pady=12,
                        activebackground=color)
        btn.pack()

        # Button label
        if key:
            key_label = tk.Label(container,
                                 text=f"[{key}]",
                                 font=self.small_font,
                                 fg=self.colors['accent2'],
                                 bg='#1A1A2E')
            key_label.place(relx=0.5, rely=1, anchor="n")

        def on_enter(e):
            btn.config(relief="sunken")

        def on_leave(e):
            btn.config(relief="raised")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def create_small_button(self, parent, text, color, command):
        """Create smaller arcade button"""
        btn = tk.Button(parent, text=text, font=self.small_font,
                       bg=color, fg='#FFFFFF', bd=3, relief="raised",
                       command=command, cursor="hand2", padx=12, pady=6)
        return btn

    def create_pixel_panel(self, parent, bg_color):
        """Create pixel-style panel"""
        frame = tk.Frame(parent, bg=bg_color, bd=4, relief="sunken")
        return frame

    def start_timer(self, minutes, label):
        if self.running:
            return

        selected_item = self.tree.selection()
        self.current_selected_task = selected_item[0] if selected_item else None

        self.running = True
        self.status_label.config(text=label)
        total_seconds = minutes * 60
        initial_seconds = total_seconds

        self.finish_btn.config(state="disabled")

        def run():
            nonlocal total_seconds
            while total_seconds >= 0 and self.running:
                mins, secs = divmod(total_seconds, 60)
                time_str = f"{mins:02d}:{secs:02d}"
                self.timer_label.config(text=time_str)

                # Update progress bar
                progress = (
                    (initial_seconds - total_seconds) / initial_seconds) * 100
                self.draw_pixel_progress_bar(progress)

                time.sleep(1)
                total_seconds -= 1

            self.running = False
            self.status_label.config(text="⭐ LEVEL COMPLETE! PRESS FINISH!")
            self.draw_pixel_progress_bar(100)
            self.finish_btn.config(state="normal")

        Thread(target=run).start()

    def finish_session(self):
        if self.current_selected_task:
            try:
                current_values = self.tree.item(
                    self.current_selected_task)["values"]
                self.tree.item(
                    self.current_selected_task, values=(
                        current_values[0], "⭐ COMPLETE"))
                messagebox.showinfo(
                    "🎮 VICTORY!", "Quest Complete! +100 EXP! 🏆")
            except Exception:
                messagebox.showwarning("ERROR", "Could not update quest!")
        else:
            messagebox.showwarning("NO QUEST", "Select a quest first! ⚠️")

        self.finish_btn.config(state="disabled")
        self.status_label.config(text="▶ READY TO START")
        self.draw_pixel_progress_bar(0)
        self.current_selected_task = None

    def start_work(self):
        self.start_timer(25, "⚔ BATTLE IN PROGRESS...")

    def start_break(self):
        self.start_timer(5, "☕ RECOVERY MODE...")

    def start_long_break(self):
        self.start_timer(15, "🌙 RESTING AT INN...")

    def add_task(self):
        task_name = self.task_entry.get().strip()
        if task_name:
            self.tree.insert("", "end", values=(task_name, "⏳ PENDING"))
            self.task_entry.delete(0, tk.END)

    def complete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected = selected_item[0]
            current_values = self.tree.item(selected)["values"]
            self.tree.item(
                selected,
                values=(
                    current_values[0],
                    "⭐ COMPLETE"))
        else:
            messagebox.showwarning("NO QUEST", "Select a quest! 📜")

    def format_quest_log(self, tasks):
        """Return formatted quest log string given iterable of (task, status) tuples."""
        lines = []
        lines.append("═══════════════════════════════")
        lines.append("    🎮 ARCADE QUEST LOG 🎮    ")
        lines.append("═══════════════════════════════")
        lines.append("")
        for task, status in tasks:
            lines.append(f"[{status}] {task}")
        lines.append("")
        lines.append("═══════════════════════════════")
        lines.append("      GAME SAVED! 💾")
        lines.append("═══════════════════════════════")
        return "\n".join(lines)

    def save_tasks(self, path: Path | None = None):
        try:
            log_file_path = Path.home() / "quest_log.txt" if path is None else Path(path)
            content = self.format_quest_log(
                [(self.tree.item(child)["values"][0], self.tree.item(child)["values"][1])
                 for child in self.tree.get_children()]
            )
            with log_file_path.open("w", encoding="utf-8") as file:
                file.write(content + "\n")
            messagebox.showinfo("💾 SAVED!", f"Game saved!\n{str(log_file_path)}")
        except Exception as e:
            messagebox.showerror("ERROR", f"Save failed:\n{str(e)}")

    def start_custom_timer(self):
        try:
            minutes = int(self.custom_entry.get())
            if minutes <= 0:
                raise ValueError
            self.start_timer(minutes, "⚡ CUSTOM QUEST...")
        except ValueError:
            messagebox.showerror("INVALID", "Enter valid number! ⚠️")


if __name__ == "__main__":
    root = tk.Tk()
    app = PixelPomodoroGame(root)
    root.mainloop()
