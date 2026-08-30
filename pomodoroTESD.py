import tkinter as tk
from tkinter import ttk, messagebox
import time
from pathlib import Path

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TESDA Pomodoro Timer")
        self.root.geometry("550x700")
        self.root.configure(bg="#003366")  # TESDA blue

        # Color scheme (TESDA blue family, with an accent palette)
        self.BG       = "#003366"
        self.PANEL_BG = "#004a8a"
        self.FG       = "white"

        # ---- section helper: a framed panel with a title ----
        def section(parent, title):
            panel = tk.Frame(parent, bg=self.PANEL_BG, padx=16, pady=10)
            panel.pack(fill="x", padx=16, pady=(8, 4))
            tk.Label(panel, text=title, font=("Arial", 12, "bold"),
                     fg="#ffd166", bg=self.PANEL_BG).pack(anchor="w")
            return panel

        # ===================== Header =====================
        self.header_label = tk.Label(root, text="BARMM Pomodoro Timer", font=("Arial", 20, "bold"), fg="#ffd166", bg=self.BG)
        self.header_label.pack(pady=(14, 4))

        # ===================== Timer panel =====================
        timer_panel = section(root, "Focus Session")

        self.timer_label = tk.Label(timer_panel, text="25:00", font=("Courier", 56, "bold"), fg="white", bg=self.PANEL_BG)
        self.timer_label.pack(pady=(2, 2))

        self.status_label = tk.Label(timer_panel, text="Ready", font=("Helvetica", 14), fg="#cfe4ff", bg=self.PANEL_BG)
        self.status_label.pack()

        self.counter_label = tk.Label(timer_panel, text="Completed: 0 of 4 today", font=("Helvetica", 11), fg="#ffd166", bg=self.PANEL_BG)
        self.counter_label.pack(pady=(2, 4))

        # ---- mode selector: Work / Short Break / Long Break ----
        self.mode_var = tk.StringVar(value="Work")
        modes = [("Work", "Work Session"), ("Short Break", "Short Break"), ("Long Break", "Long Break")]
        mode_row = tk.Frame(timer_panel, bg=self.PANEL_BG)
        mode_row.pack(pady=(2, 6))
        for label, session in modes:
            tk.Radiobutton(mode_row, text=label, variable=self.mode_var, value=session,
                           command=self.start_selected_mode, fg="white", bg=self.PANEL_BG,
                           selectcolor=self.BG, activebackground=self.PANEL_BG,
                           activeforeground="white", font=("Helvetica", 10, "bold")).pack(side="left", padx=6)

        # ---- timer control buttons ----
        self.start_button = tk.Button(timer_panel, text="Start", width=12, bg="#28a745", fg="white",
                                      font=("Helvetica", 12, "bold"), command=self.start_selected_mode)
        self.start_button.pack(side="left", expand=True, padx=(0, 4), pady=6)

        self.stop_button = tk.Button(timer_panel, text="Stop", width=12, bg="#dc3545", fg="white",
                                     font=("Helvetica", 12, "bold"), command=self.stop_timer, state="disabled")
        self.stop_button.pack(side="left", expand=True, padx=(4, 0), pady=6)

        self.finish_button = tk.Button(root, text="Finish Session & Complete Task", bg="#17a2b8", fg="white",
                                       command=self.finish_session, state="disabled")
        self.finish_button.pack(pady=(4, 10), ipadx=20, ipady=4)

        # ===================== Custom timer =====================
        custom_panel = section(root, "Custom Timer")

        self.custom_time_label = tk.Label(custom_panel, text="Minutes:", fg="white", bg=self.PANEL_BG, font=("Helvetica", 11))
        self.custom_time_label.pack(side="left", pady=4)

        self.custom_time_entry = tk.Entry(custom_panel, width=6, justify="center")
        self.custom_time_entry.pack(side="left", padx=8, pady=4)
        self.custom_time_entry.insert(0, "25")

        self.custom_timer_button = tk.Button(custom_panel, text="Start", bg="#ff9933", fg="white",
                                             command=self.start_custom_timer, font=("Helvetica", 10, "bold"))
        self.custom_timer_button.pack(side="left", padx=4, pady=4)

        # ===================== Task list =====================
        task_panel = section(root, "Tasks")

        task_entry_row = tk.Frame(task_panel, bg=self.PANEL_BG)
        task_entry_row.pack(fill="x", pady=4)
        self.task_entry_label = tk.Label(task_entry_row, text="Task:", fg="white", bg=self.PANEL_BG)
        self.task_entry_label.pack(side="left")
        self.task_entry = tk.Entry(task_entry_row, width=32)
        self.task_entry.pack(side="left", padx=8)

        self.add_task_button = tk.Button(task_entry_row, text="Add Task", command=self.add_task,
                                         bg="#0073e6", fg="white")
        self.add_task_button.pack(side="left")

        self.tree = ttk.Treeview(root, columns=("Task", "Status"), show="headings", height=6)
        self.tree.heading("Task", text="Task")
        self.tree.heading("Status", text="Status")
        self.tree.column("Task", anchor="w", width=300)
        self.tree.column("Status", anchor="center", width=100)
        self.tree.pack(pady=(4, 8), padx=16, fill="x")

        task_buttons = tk.Frame(root, bg=self.BG)
        task_buttons.pack(pady=(0, 6))
        self.complete_task_button = tk.Button(task_buttons, text="Mark Complete", command=self.complete_task,
                                              bg="#28a745", fg="white")
        self.complete_task_button.pack(side="left", padx=4)
        self.save_tasks_button = tk.Button(task_buttons, text="Save to File", command=self.save_tasks,
                                           bg="#17a2b8", fg="white")
        self.save_tasks_button.pack(side="left", padx=4)

        # ---- Enter-key shortcuts ----
        self.custom_time_entry.bind("<Return>", lambda e: self.start_custom_timer())
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        self.running = False
        self.completed_work_sessions = 0
        self.can_complete = False
        self.current_selected_task = None

    def start_timer(self, minutes, label):
        if self.running:
            messagebox.showinfo("Timer Running", "A timer is already running. Click Stop to cancel it first.") 
            return
        
        # Store the currently selected task when timer starts
        selected_item = self.tree.selection()
        self.current_selected_task = selected_item[0] if selected_item else None

        self.running = True
        self.can_complete = label == "Work Session"
        self.status_label.config(text=label)
        self.finish_button.config(state="disabled")
        self.stop_button.config(state="normal")

        # Record when the timer should finish, using a monotonic clock so
        # it never drifts and is immune to system clock changes.
        self.end_time = time.monotonic() + (minutes * 60)
        self._tick()

    def _tick(self):
        if not self.running:
            return
        remaining = self.end_time - time.monotonic()
        if remaining <= 0:
            # Timer finished - update once more, then stop
            self.timer_label.config(text="00:00")
            self.running = False
            self.status_label.config(text="Done! Click 'Finish Session' to complete task")
            self.stop_button.config(state="disabled")
            if self.can_complete:
                self.completed_work_sessions += 1
                self.counter_label.config(text=f"Completed: {self.completed_work_sessions} of 4 today")
                self.finish_button.config(state="normal")
            return
        mins, secs = divmod(int(remaining), 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        # Schedule the next tick on the GUI thread - no Thread needed.
        self._timer = self.root.after(1000, self._tick)
    
    def stop_timer(self):
        if not self.running:
            return
        # Cancel the pending tick so it never fires again
        if hasattr(self, "_timer"):
            self.root.after_cancel(self._timer)
        self.running = False
        self.timer_label.config(text="00:00")
        self.status_label.config(text="Stopped")
        self.finish_button.config(state="disabled")
        self.stop_button.config(state="disabled")
        self.current_selected_task = None

    def finish_session(self):
        """Mark the selected task as complete when session finishes"""
        if self.current_selected_task:
            try:
                current_values = self.tree.item(self.current_selected_task)["values"]
                self.tree.item(self.current_selected_task, values=(current_values[0], "Completed"))
                messagebox.showinfo("Session Complete", "Great work! Task marked as completed.")
            except Exception as e:
                messagebox.showwarning("Error", f"Could not update task status: {e}")
        else:
            messagebox.showwarning("No Task Selected", "Please select a task before starting the timer.")
        
        # Disable finish button after use
        self.finish_button.config(state="disabled")
        self.status_label.config(text="Ready")
        self.current_selected_task = None

    def start_selected_mode(self):
        """Start whichever mode the radio selector currently shows."""
        mode = self.mode_var.get()
        if mode == "Work Session":
            self.start_timer(25, "Work Session")
        elif mode == "Short Break":
            self.start_timer(5, "Short Break")
        elif mode == "Long Break":
            self.start_timer(15, "Long Break")

    def add_task(self):
        task_name = self.task_entry.get().strip()
        if task_name:
            self.tree.insert("", "end", values=(task_name, "Pending"))
            self.task_entry.delete(0, tk.END)

    def complete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.item(selected_item, values=(self.tree.item(selected_item)["values"][0], "Completed"))
        else:
            messagebox.showwarning("No selection", "Please select a task to mark as complete.")

    def save_tasks(self):
        try:
            # Save to the user's home folder so it works on any computer
            log_file_path = Path.home() / "task_log.txt"

            # Save the task log
            with open(log_file_path, "w") as file:
                for child in self.tree.get_children():
                    task, status = self.tree.item(child)["values"]
                    file.write(f"{task} - {status}\n")

            messagebox.showinfo("Saved", f"Tasks have been saved to:\n{log_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def start_custom_timer(self):
        try:
            minutes = int(self.custom_time_entry.get())
            if minutes <= 0:
                raise ValueError
            self.start_timer(minutes, "Custom Task Timer")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer for minutes.")


# Run the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
