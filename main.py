import tkinter as tk # This module is used to create GUI
from tkinter import messagebox # This module is used to create checkbox
from PIL import Image, ImageTk # This module is used for image loading
import matplotlib.pyplot as plt # This module is used for creating diagram
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main window
newWindow = tk.Tk()
newWindow.title("To-Do List by Kaustubh")

# Set the window size
newWindow.geometry("590x800+270+200")  # Increased height to accommodate pie chart

# Set the background color
newWindow.configure(bg="#0d1525")

# Function to resize images
def resize_image(image_path, size, background_color=(13, 21, 37)):
    with Image.open(image_path) as img:
        # Create a new image with a background color
        bg = Image.new('RGBA', img.size, background_color + (255,))
        bg.paste(img, (0, 0), img)  # Paste the original image on top of the background
        img = bg.resize(size, Image.LANCZOS)  # Resize the image with the background color
        return ImageTk.PhotoImage(img)

# Resize the icons with NECESSARY background
done_icon = resize_image("done_icon.png", (20, 20), background_color=(13, 21, 37))
delete_icon = resize_image("delete_icon.png", (20, 20), background_color=(13, 21, 37))

# Function to mark a task as done
def mark_as_done(task_label, done_button):
    task_label.config(fg="gray", font=("Helvetica", 18, "overstrike"))
    done_button.config(image=done_icon, state=tk.DISABLED, disabledforeground="green")
    update_task_count()

# Function to delete a specific task and update serial numbers
def delete_task(task_frame):
    task_frame.destroy()
    update_serial_numbers()
    update_task_count()

# Function to add a task
def add_task(task=None):
    if not task:
        task = task_entry.get()
    if task:
        task_frame = tk.Frame(task_container, bg="white", pady=5)
        task_number = len(task_container.winfo_children()) + 1
        task_label = tk.Label(task_frame, text=f"{task_number}. {task}", bg="white", fg="#ffffff", font=("Helvetica", 18))
        task_label.pack(side=tk.LEFT, padx=10)

        done_button = tk.Button(task_frame, image=done_icon, command=lambda: mark_as_done(task_label, done_button), bg="#add8e6", fg="#1cbd52", font=("Helvetica", 12))
        done_button.pack(side=tk.RIGHT, padx=5)

        delete_button = tk.Button(task_frame, image=delete_icon, command=lambda: delete_task(task_frame), bg="#ff6347", fg="#e0194b", font=("Helvetica", 12))
        delete_button.pack(side=tk.RIGHT, padx=5)

        task_frame.pack(fill=tk.X, pady=5)
        task_entry.delete(0, tk.END)
        update_serial_numbers()
        update_task_count()
        canvas.update_idletasks()  # Update the canvas to reflect the new task
        canvas.configure(scrollregion=canvas.bbox("all"))  # Update the scroll region

# Function to update the serial numbers of the tasks
def update_serial_numbers():
    for index, task_frame in enumerate(task_container.winfo_children()):
        task_label = task_frame.winfo_children()[0]
        task_text = task_label.cget("text")
        if ". " in task_text:
            task_text = task_text.split(". ", 1)[1]
        task_label.config(text=f"{index + 1}. {task_text}")

# Function to delete all tasks
def delete_all_tasks():
    for widget in task_container.winfo_children():
        widget.destroy()
    update_task_count()

# Function to update task count labels
def update_task_count():
    total_tasks = len(task_container.winfo_children())
    done_tasks = sum(1 for task_frame in task_container.winfo_children() if "overstrike" in task_frame.winfo_children()[0].cget("font"))
    remaining_tasks = total_tasks - done_tasks

    total_tasks_label.config(text=f"Total Tasks: {total_tasks}")
    remaining_tasks_label.config(text=f"Remaining Tasks: {remaining_tasks}")
    done_tasks_label.config(text=f"Completed Tasks: {done_tasks}")
    update_pie_chart(total_tasks, remaining_tasks, done_tasks)

# Function to update the pie chart
def update_pie_chart(total_tasks, remaining_tasks, done_tasks):
    # Clear the previous pie chart
    for widget in pie_chart_frame.winfo_children():
        widget.destroy()

    if total_tasks == 0:
        return  # No tasks to display

    # Create a new pie chart
    labels = 'Completed Tasks', 'Remaining Tasks'
    sizes = [done_tasks, remaining_tasks]
    colors = ['#4caf50', '#ffeb3b']
    explode = (0.1, 0)  # explode the 1st slice (Completed Tasks)

    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)  # Adjust the size and DPI as needed
    fig.patch.set_facecolor('#0d1525')  # Match the Tkinter background color

    ax.pie(sizes, explode=explode, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Add a legend
    ax.legend(labels, loc="best")

    # Embed the pie chart into Tkinter
    canvas_chart = FigureCanvasTkAgg(fig, master=pie_chart_frame)
    canvas_chart.draw()
    canvas_chart.get_tk_widget().pack()

    plt.close(fig)  # Close the figure to release memory

# Function to save tasks to a file
def save_tasks():
    with open("tasks.csv", "w") as file:
        for task_frame in task_container.winfo_children():
            task_label = task_frame.winfo_children()[0]
            task_text = task_label.cget("text").split(". ", 1)[1]
            task_done = "1" if "overstrike" in task_label.cget("font") else "0"
            file.write(f"{task_text}|{task_done}\n")
    messagebox.showinfo("Save Tasks", "Tasks have been saved successfully.")


# Function to load tasks from a file
def load_tasks():
    try:
        with open("tasks.csv", "r") as file:
            for line in file:
                task_text, task_done = line.strip().split("|")
                add_task(task_text)
                if task_done == "1":
                    task_frame = task_container.winfo_children()[-1]
                    task_label = task_frame.winfo_children()[0]
                    done_button = task_frame.winfo_children()[1]
                    mark_as_done(task_label, done_button)
        update_task_count()
    except FileNotFoundError:
        pass  # No file to load from

# Create a canvas to allow scrolling
canvas = tk.Canvas(newWindow, bg="#0d1525")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = tk.Scrollbar(newWindow, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.LEFT, fill="y")

# Configure the canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame inside the canvas
task_container = tk.Frame(canvas, bg="#0d1525")
canvas.create_window((0, 0), window=task_container, anchor="nw")

# Create a navigation bar heading
nav_frame = tk.Frame(newWindow, bg="#1d2332")
nav_frame.pack(fill=tk.X)

nav_label = tk.Label(nav_frame, text="To-Do List", bg="#1d2332", fg="red", font=("Helvetica", 24, "bold"))
nav_label.pack(pady=10)

# Create an entry widget for adding tasks
task_entry = tk.Entry(newWindow, width=35, bg="#1d2332", fg="#ffffff", font=("Helvetica", 22))
task_entry.pack(pady=10)

# Create a button to add tasks
add_task_button = tk.Button(newWindow, text="Add Task", command=add_task, bg="#add8e6", fg="#000000", font=("Helvetica", 12))
add_task_button.pack(pady=5)

# Create a button to delete all tasks
delete_all_button = tk.Button(newWindow, text="Delete All Tasks", command=delete_all_tasks, bg="#ff6347", fg="#000000", font=("Helvetica", 12))
delete_all_button.pack(pady=5)

# Create buttons to save and load tasks
save_button = tk.Button(newWindow, text="Save Tasks", command=save_tasks, bg="#4caf50", fg="#000000", font=("Helvetica", 12))
save_button.pack(pady=5)

# create buttons to load tasks
load_button = tk.Button(newWindow, text="Load Tasks", command=load_tasks, bg="#ffc107", fg="#000000", font=("Helvetica", 12))
load_button.pack(pady=5)

# Add vertical gap
tk.Label(newWindow, text="", bg="#0d1525").pack(pady=10)

# Labels to display task counts
total_tasks_label = tk.Label(newWindow, text="Total Tasks: 0", bg="#0d1525", fg="#ffffff", font=("Helvetica", 18))
total_tasks_label.pack(pady=2)

remaining_tasks_label = tk.Label(newWindow, text="Remaining Tasks: 0", bg="#0d1525", fg="yellow", font=("Helvetica", 18))
remaining_tasks_label.pack(pady=2)

done_tasks_label = tk.Label(newWindow, text="Completed Tasks: 0", bg="#0d1525", fg="lime", font=("Helvetica", 18))
done_tasks_label.pack(pady=2)

# Frame for the pie chart
pie_chart_frame = tk.Frame(newWindow, bg="#0d1525")
pie_chart_frame.pack(pady=20)

# Run the main loop
newWindow.mainloop()