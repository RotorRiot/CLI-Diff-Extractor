import difflib
import tkinter as tk
from tkinter import filedialog, messagebox


def select_file(entry_field):
    """Open a file dialog to select a file and update the entry field."""
    file_path = filedialog.askopenfilename(title="Select a File")
    if file_path:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, file_path)
    check_fields()


def check_fields():
    """Enable the 'Generate Diff' button if the base and altered files are selected."""
    if file1_entry.get() and file2_entry.get():
        generate_button.config(state=tk.NORMAL)
    else:
        generate_button.config(state=tk.DISABLED)


def compare_files(file1, file2):
    """Compare two files and return the differences."""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    # Use difflib to find differences
    diff = difflib.unified_diff(file1_lines, file2_lines, lineterm='')
    differences = [line[1:] for line in diff if line.startswith('+') and not line.startswith('+++')]
    return differences


def create_diff_file():
    """Create the diff file based on user input."""
    file1 = file1_entry.get()
    file2 = file2_entry.get()

    # Ask the user for a save location
    save_path = filedialog.asksaveasfilename(
        title="Select Save Location",
        defaultextension=".txt",
        initialfile="New Diff.txt"
    )

    if not save_path:
        messagebox.showerror("Error", "No save location selected!")
        return

    try:
        differences = compare_files(file1, file2)
        with open(save_path, 'w') as output_file:
            output_file.writelines(differences)
            # Add the two lines at the end of the file
            output_file.write("\n")  # Empty line
            output_file.write("save\n")  # Line with "save"

        messagebox.showinfo("Success", f"Differences saved to: {save_path}")
        # Clear the file selection fields after success
        file1_entry.delete(0, tk.END)
        file2_entry.delete(0, tk.END)
        check_fields()  # Update the button state
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def main():
    # Create the main application window
    root = tk.Tk()
    root.title("File Comparison Tool")
    root.geometry("600x250")  # Adjusted size to prevent cutoff
    root.resizable(False, False)

    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 600
    window_height = 250
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Configure grid layout for centering
    root.grid_rowconfigure(0, weight=1)  # Top padding
    root.grid_rowconfigure(4, weight=1)  # Bottom padding
    root.grid_columnconfigure(0, weight=1)  # Left padding
    root.grid_columnconfigure(2, weight=1)  # Right padding

    # Create labels and entry fields
    frame = tk.Frame(root)
    frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

    tk.Label(frame, text="Select Base File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    global file1_entry
    file1_entry = tk.Entry(frame, width=60)
    file1_entry.grid(row=0, column=1, padx=10, pady=10)
    file1_button = tk.Button(frame, text="Browse", command=lambda: select_file(file1_entry))
    file1_button.grid(row=0, column=2, padx=10, pady=10)

    tk.Label(frame, text="Select Altered File:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    global file2_entry
    file2_entry = tk.Entry(frame, width=60)
    file2_entry.grid(row=1, column=1, padx=10, pady=10)
    file2_button = tk.Button(frame, text="Browse", command=lambda: select_file(file2_entry))
    file2_button.grid(row=1, column=2, padx=10, pady=10)

    # Create the 'Generate Diff' button
    global generate_button
    generate_button = tk.Button(frame, text="Generate Diff", command=create_diff_file, state=tk.DISABLED)
    generate_button.grid(row=2, column=1, pady=20)

    # Run the application
    root.mainloop()


if __name__ == "__main__":
    main()