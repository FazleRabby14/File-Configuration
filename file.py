import tkinter as tk
from tkinter import filedialog
import csv
import io

def convert_to_text(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def compare_text_files(text1, text2, file1, file2, source1, source2):
    lines1 = text1.split('\n')
    lines2 = text2.split('\n')

    mismatch_info = []

    # Compare lines
    for i, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
        if line1 != line2:
            mismatch_info.append({
                'Line Number': i,
                'Mismatch in': f"{source1} {file1} and {source2} {file2}",
                'Text 1': line1,
                'Text 2': line2
            })

    return mismatch_info

def browse_file(entry_widget, source):
    file_path = filedialog.askopenfilename()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def run_comparison():
    file1 = entry_file1.get()
    file2 = entry_file2.get()

    text1 = convert_to_text(file1)
    text2 = convert_to_text(file2)

    global mismatch_info
    mismatch_info = compare_text_files(text1, text2, file1, file2, "NCR", "ATM")

    # Display mismatch information in a new window
    result_window = tk.Toplevel(root)
    result_text = tk.Text(result_window)
    result_text.pack(expand=True, fill=tk.BOTH)

    for info in mismatch_info:
        line_number = info['Line Number']
        text_1 = info['Text 1']
        text_2 = info['Text 2']

        # Find the position where the mismatch occurs
        mismatch_start = next((i for i, (c1, c2) in enumerate(zip(text_1, text_2)) if c1 != c2), None)
        mismatch_end = mismatch_start + len(text_1[mismatch_start:])

        # Insert the non-mismatched parts normally
        result_text.insert(tk.END, f"Mismatch at line {line_number} in {info['Mismatch in']}:\n")
        result_text.insert(tk.END, f"    {text_1[:mismatch_start]}")

        # Tag and format the entire mismatched value with color
        result_text.insert(tk.END, text_1[mismatch_start:mismatch_end], "mismatch_tag")
        
        # Insert the rest of the non-mismatched part normally
        result_text.insert(tk.END, f"{text_1[mismatch_end:]}\n")

        # Add the second text for comparison
        result_text.insert(tk.END, f"!=  {text_2}\n\n")

    # Configure the "mismatch_tag" for color formatting
    result_text.tag_configure("mismatch_tag", foreground="red", font=("TkDefaultFont", 10, "bold"))

    result_text.config(state=tk.DISABLED)

def save_mismatch():
    if not mismatch_info:
        tk.messagebox.showinfo("No Mismatches", "There are no mismatches to save.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    
    if save_path:
        extension = save_path.split('.')[-1].lower()

        if extension == 'csv':
            with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Line Number', 'Mismatch in', 'Text 1', 'Text 2']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(mismatch_info)
        else:
            with open(save_path, 'w', encoding='utf-8') as txtfile:
                for info in mismatch_info:
                    txtfile.write(f"Mismatch at line {info['Line Number']} in {info['Mismatch in']}:\n"
                                  f"    {info['Text 1']}\n"
                                  f"!=  {info['Text 2']}\n")

# Create the main Tkinter window
root = tk.Tk()
root.title("Text File Comparison")

# Entry widgets for file paths
entry_file1 = tk.Entry(root, width=40)
entry_file2 = tk.Entry(root, width=40)

# Browse buttons to select files
button_browse1 = tk.Button(root, text="NCR", command=lambda: browse_file(entry_file1, "NCR"))
button_browse2 = tk.Button(root, text="ATM", command=lambda: browse_file(entry_file2, "ATM"))

# Run button to initiate comparison
button_run = tk.Button(root, text="Run Comparison", command=run_comparison)

# Save button to save mismatch data
button_save = tk.Button(root, text="Save Mismatch", command=save_mismatch)

# Arrange widgets using grid layout
entry_file1.grid(row=0, column=0, padx=10, pady=10)
button_browse1.grid(row=0, column=1, padx=5)
entry_file2.grid(row=1, column=0, padx=10, pady=10)
button_browse2.grid(row=1, column=1, padx=5)
button_run.grid(row=2, column=0, columnspan=2, pady=10)
button_save.grid(row=3, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
