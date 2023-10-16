import tkinter as tk
from tkinter import messagebox

import keyboard
import pyperclip


def setup_window():
    win = tk.Tk()
    win.title("BreakoutCopyMate")
    win.geometry("600x400")
    win.configure(bg='#f0f0f0')
    return win


def read_lines_from_file(filename="input.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines()]
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return []
    return lines


def get_next_line(lines, line_num):
    return lines[line_num] if line_num < len(lines) else None


def main():
    root = setup_window()
    lines = read_lines_from_file()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(3, weight=1)

    line_num = 0
    paste_mode = False

    def toggle_paste_mode():
        nonlocal paste_mode
        paste_mode = not paste_mode
        mode_button.config(text=f"Paste Mode: {'ON' if paste_mode else 'OFF'}")

    def paste_next_line_handler(event=None):
        nonlocal line_num
        if paste_mode:
            next_line_text = get_next_line(lines, line_num)
            if next_line_text:
                pyperclip.copy(next_line_text)
                current_line.set(next_line_text)
                line_num += 1
                next_line_to_copy = get_next_line(lines, line_num)
                next_line.set(next_line_to_copy)
                keyboard.press_and_release('enter')
                if not next_line_to_copy:
                    show_end_message()
            else:
                next_line.set("")
                show_end_message()

    def show_end_message():
        messagebox.showinfo("End", "All lines have been copied.")
        root.destroy()

    current_line = tk.StringVar()
    next_line = tk.StringVar()

    button_frame = tk.Frame(root, bg='#f0f0f0')
    button_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    mode_button = tk.Button(button_frame, text="Paste Mode: OFF", command=toggle_paste_mode, bg='#4CAF50', fg='#ffffff',
                            font=('Helvetica', 12), padx=10, pady=5, borderwidth=0)
    mode_button.pack(side=tk.LEFT)

    file_content_label = tk.Label(root, text="Input File Content:", font=('Helvetica', 16, 'bold'), fg='#333')
    file_content_label.grid(row=1, column=0, sticky="w", padx=10, pady=(20, 0))

    file_content = tk.Text(root, wrap=tk.WORD, bg='#ffffff', relief=tk.SUNKEN, state=tk.DISABLED,
                           font=('Helvetica', 14), height=10)
    file_content.grid(row=2, column=0, sticky="nsew", padx=10)

    file_content.configure(state=tk.NORMAL)
    for line_idx, line in enumerate(lines):
        line = line.strip()
        file_content.insert(tk.END, line + "\n")
        tag_start = file_content.index(tk.END + "-1c linestart")
        tag_end = file_content.index(tk.END + "-1c lineend")
        file_content.tag_add(f"line{line_idx}", tag_start, tag_end)
        file_content.tag_configure(f"line{line_idx}", underline=True)
        file_content.tag_bind(f"line{line_idx}", "<Button-1>", paste_next_line_handler)

    file_content.configure(state=tk.DISABLED)

    current_line_info = tk.Label(root, textvariable=current_line, font=('Helvetica', 14), fg="#2196F3")
    current_line_info.grid(row=3, column=1, sticky="w", padx=10, pady=(20, 0))

    next_line_label = tk.Label(root, text="Next Copy Line:", font=('Helvetica', 16, 'bold'), fg='#333')
    next_line_label.grid(row=4, column=0, sticky="ew", padx=10, pady=(20, 0))

    next_line_info = tk.Label(root, textvariable=next_line, font=('Helvetica', 14), fg="#FF0000")
    next_line_info.grid(row=4, column=1, sticky="w", padx=10, pady=(20, 0))

    keyboard.add_hotkey('ctrl+v', paste_next_line_handler)
    first_line = get_next_line(lines, line_num)
    next_line.set(first_line if first_line else "All lines have been copied")
    root.protocol("WM_DELETE_WINDOW", lambda: paste_next_line_handler(None))
    root.mainloop()


if __name__ == '__main__':
    main()
