import tkinter as tk
from tkinter import ttk, messagebox
import time
from threading import Thread

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TESDA Pomodoro Timer")
        self.root.geometry("550x650")
        self.root.configure(bg="#003366")  # TESDA blue

        self.header_label = tk.Label(root, text="BARMM Pomodoro Timer", font=("Arial", 20, "bold"), fg="white", bg="#003366")
        self.header_label.pack(pady=10)

        self.timer_label = tk.Label(root, text="25:00", font=("Courier", 48, "bold"), fg="white", bg="#003366")
        self.timer_label.pack(pady=10)

        self.status_label = tk.Label(root, text="Ready", font=("Helvetica", 14), fg="white", bg="#003366")
        self.status_label.pack(pady=5)

        # Timer Buttons
        self.start_button = tk.Button(root, text="Start Work", width=20, bg="#0059b3", fg="white", command=self.start_work)
        self.start_button.pack(pady=5)

        self.break_button = tk.Button(root, text="Start Break", width=20, bg="#006699", fg="white", command=self.start_break)
        self.break_button.pack(pady=5)

        self.long_break_button = tk.Button(root, text="Start Long Break", width=20, bg="#004080", fg="white", command=self.start_long_break)
        self.long_break_button.pack(pady=5)

        # Custom Timer Entry
        self.custom_time_label = tk.Label(root, text="Custom Timer (minutes):", fg="white", bg="#003366", font=("Helvetica", 12))
        self.custom_time_label.pack(pady=(20, 0))

        self.custom_time_entry = tk.Entry(root, width=10, justify="center")
        self.custom_time_entry.pack(pady=5)

        self.custom_timer_button = tk.Button(root, text="Start Custom Timer", command=self.start_custom_timer, bg="#ff9933", fg="white")
        self.custom_timer_button.pack(pady=5)

        # Task Entry
        self.task_entry_label = tk.Label(root, text="Task to Complete:", fg="white", bg="#003366", font=("Helvetica", 12))
        self.task_entry_label.pack(pady=(20, 0))

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=5)

        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#0073e6", fg="white")
        self.add_task_button.pack(pady=5)

        # Task Table
        self.tree = ttk.Treeview(root, columns=("Task", "Status"), show="headings", height=6)
        self.tree.heading("Task", text="Task")
        self.tree.heading("Status", text="Status")
        self.tree.column("Task", anchor="w", width=300)
        self.tree.column("Status", anchor="center", width=100)
        self.tree.pack(pady=10)

        # Task Buttons
        self.complete_task_button = tk.Button(root, text="Mark Task as Complete", command=self.complete_task, bg="#28a745", fg="white")
        self.complete_task_button.pack(pady=5)

        self.save_tasks_button = tk.Button(root, text="Save Tasks to File", command=self.save_tasks, bg="#17a2b8", fg="white")
        self.save_tasks_button.pack(pady=5)

        self.running = False

    def start_timer(self, minutes, label):
        if self.running:
            return
        self.running = True
        self.status_label.config(text=label)
        total_seconds = minutes * 60

        def run():
            nonlocal total_seconds
            while total_seconds >= 0 and self.running:
                mins, secs = divmod(total_seconds, 60)
                time_str = f"{mins:02d}:{secs:02d}"
                self.timer_label.config(text=time_str)
                time.sleep(1)
                total_seconds -= 1
            self.running = False
            self.status_label.config(text="Done")

        Thread(target=run).start()

    def start_work(self):
        self.start_timer(25, "Work Session")

    def start_break(self):
        self.start_timer(5, "Short Break")

    def start_long_break(self):
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
            # Specify the exact path
            log_file_path = r"C:\Users\ADMIN\Downloads\task_log.txt"

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
