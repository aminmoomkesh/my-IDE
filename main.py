import tkinter as tk
from tkinter import filedialog,scrolledtext
import re
KEYWORDS = ["if", "else", "while", "for", "def", "return", "import", "class"]
STRING_PATTERN = r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''
COMMENT_PATTERN = r'#.*$'
class vision:
    def __init__(self,win):
        self.win = win
        win.title("vision")
        self.create_menu()
        self.create_button()
        self.create_editor()
    def create_menu(self):
        menubar = tk.Menu(self.win)
        file_menu = tk.Menu(menubar,tearoff=0)
        file_menu.add_command(label='save',command=self.save_file)
        file_menu.add_command(label='open',command=self.open_file)
        edit_menu = tk.Menu(menubar,tearoff=0)
        edit_menu.add_command(label='undo',command=self.undo())
        edit_menu.add_command(label='redo',command=self.redo())
        menubar.add_cascade(label='File',menu=file_menu)
        menubar.add_cascade(label='Edit',menu=edit_menu)
        self.win.config(menu=menubar)
    def create_button(self):
        button_frame = tk.Frame(self.win, bg="lightblue", width=200, height=100)
        button_frame.pack(side="top",anchor="ne")  # Add padding on the y-axis
        run_button = tk.Button(button_frame,text="Run",command=self.run_file)
        run_button.grid(column=1,row=0)
        debug_button = tk.Button(button_frame,text="debug",bg="gray",command=self.debug_file)
        debug_button.grid(column=0,row=0)
    def create_editor(self):
        self.editor = scrolledtext.ScrolledText(self.win,wrap=tk.NONE)
        self.editor.pack(side=tk.BOTTOM,anchor=tk.S,fill=tk.BOTH, expand=1)
        self.editor.bind('<KeyRelease>', self.highlight_syntax)
        self.configure_tags()
    def configure_tags(self):
        self.keywords = ['def', 'class', 'if', 'else', 'for', 'while', 'import']
        self.editor.tag_configure('keyword', foreground='blue')
        self.editor.tag_configure('string', foreground='#00aa00')
    def highlight_syntax(self,event=None):
        # Remove previous tags
        self.editor.tag_remove("keyword", "1.0", tk.END)
        self.editor.tag_remove("string", "1.0", tk.END)
        self.editor.tag_remove("comment", "1.0", tk.END)

        # Get the entire text from the widget
        code = self.editor.get("1.0", tk.END)

        # Highlight strings first
        string_matches = list(re.finditer(STRING_PATTERN, code))
        for match in string_matches:
            start = f"1.0 + {match.start()}c"
            end = f"1.0 + {match.end()}c"
            self.editor.tag_add("string", start, end)

        # Highlight comments (ensure they are not inside strings)
        for match in re.finditer(COMMENT_PATTERN, code, re.MULTILINE):
            start_index = match.start()
            end_index = match.end()

            comment_start = f"1.0 + {start_index}c"
            comment_end = f"1.0 + {end_index}c"

            # Check if the comment starts inside a string and adjust the start position
            inside_string = False
            for string_match in string_matches:
                if string_match.start() <= start_index < string_match.end():
                    comment_start = f"1.0 + {string_match.end()}c"  # Start comment after the string
                    break

            self.editor.tag_add("comment", comment_start, comment_end)

        # Highlight keywords (ignoring strings and comments)
        for keyword in KEYWORDS:
            start = "1.0"
            while True:
                start = self.editor.search(r'\m' + keyword + r'\M', start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(keyword)}c"

                # Ensure it's not inside a string or comment
                inside_string_or_comment = False
                for tag in self.editor.tag_names(start):
                    if tag in ("string", "comment"):
                        inside_string_or_comment = True
                        break

                if not inside_string_or_comment:
                    self.editor.tag_add("keyword", start, end)
                start = end

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save File",
            defaultextension=".py",
            filetypes=(("python Files", "*.py"), ("All Files", "*.*"))
        )
        if file_path:
            try:
                # Write some data to the file
                with open(file_path, "w") as file:
                    file.writelines(self.file_text)
                print(f"File saved successfully:{file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")
            
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("python Files", "*.py"), ("All Files", "*.*"))
        )
        if file_path:
            print(f"Selected file: {file_path}")
            try:
                with open(file_path,"r") as file:
                    file = file.readlines()
            except Exception as e:
                print(f"Error opening file: {e}")

                
    def debug_file(self):
        pass
    def undo(self):
        pass
    def redo(self):
        pass
    def run_file(self):
        pass
    def get_file_name(self):
        question_window = tk.Toplevel(self.win)
        question_window.title("Enter the name of your project")


if __name__ == "__main__":
    win = tk.Tk()
    vision(win)
    win.mainloop()


