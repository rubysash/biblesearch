"""
Bible Verse Viewer with Navigation

This module provides a graphical user interface (GUI) for navigating and viewing
verses from various books and chapters of the Bible. The application uses the
`tkinter` library for its interface and supports features such as:
- Navigating to previous and next chapters.
- Highlighting specific verses.
- Displaying a popup window to view verses from a selected chapter.

The verse data for each book and chapter is defined in the `books` dictionary.

Dependencies:
- tkinter
- re (for potential regex operations)

Usage:
Run this script directly to launch the Bible Verse Viewer application.

Author: James Fraze (guiding AI)
Version: 1.0
Date: 2023-08-27
"""
import tkinter as tk
from tkinter import ttk, messagebox
import re

books = {
    "All": [0, 0, "All Books"],
    "Ge": [1, 50, "Genesis"],
    "Ex": [2, 40, "Exodus"],
    "Le": [3, 27, "Leviticus"],
    "Nu": [4, 36, "Numbers"],
    "De": [5, 34, "Deuteronomy"],
    "Jos": [6, 24, "Joshua"],
    "Jg": [7, 21, "Judges"],
    "Ru": [8, 4, "Ruth"],
    "1Sa": [9, 31, "1 Samuel"],
    "2Sa": [10, 24, "2 Samuel"],
    "1Ki": [11, 22, "1 Kings"],
    "2Ki": [12, 25, "2 Kings"],
    "1Ch": [13, 29, "1 Chronicles"],
    "2Ch": [14, 36, "2 Chronicles"],
    "Ezr": [15, 10, "Ezra"],
    "Ne": [16, 13, "Nehemiah"],
    "Es": [17, 10, "Esther"],
    "Job": [18, 42, "Job"],
    "Ps": [19, 150, "Psalms"],
    "Pr": [20, 31, "Proverbs"],
    "Ec": [21, 12, "Ecclesiastes"],
    "Song": [22, 8, "Song of Solomon"],
    "Isa": [23, 66, "Isaiah"],
    "Jer": [24, 52, "Jeremiah"],
    "La": [25, 5, "Lamentations"],
    "Eze": [26, 48, "Ezekiel"],
    "Da": [27, 12, "Daniel"],
    "Ho": [28, 14, "Hosea"],
    "Joe": [29, 3, "Joel"],
    "Am": [30, 9, "Amos"],
    "Ob": [31, 1, "Obadiah"],
    "Jon": [32, 4, "Jonah"],
    "Mic": [33, 7, "Micah"],
    "Na": [34, 3, "Nahum"],
    "Hab": [35, 3, "Habakkuk"],
    "Zep": [36, 3, "Zephaniah"],
    "Hag": [37, 2, "Haggai"],
    "Zec": [38, 14, "Zechariah"],
    "Mal": [39, 4, "Malachi"],
    "Mt": [40, 28, "Matthew"],
    "Mr": [41, 16, "Mark"],
    "Lu": [42, 24, "Luke"],
    "Joh": [43, 21, "John"],
    "Ac": [44, 28, "Acts"],
    "Ro": [45, 16, "Romans"],
    "1Co": [46, 16, "1 Corinthians"],
    "2Co": [47, 13, "2 Corinthians"],
    "Ga": [48, 6, "Galatians"],
    "Eph": [49, 6, "Ephesians"],
    "Php": [50, 4, "Philippians"],
    "Col": [51, 4, "Colossians"],
    "1Th": [52, 5, "1 Thessalonians"],
    "2Th": [53, 3, "2 Thessalonians"],
    "1Ti": [54, 6, "1 Timothy"],
    "2Ti": [55, 4, "2 Timothy"],
    "Tit": [56, 3, "Titus"],
    "Phm": [57, 1, "Philemon"],
    "Heb": [58, 13, "Hebrews"],
    "Jas": [59, 5, "James"],
    "1Pe": [60, 5, "1 Peter"],
    "2Pe": [61, 3, "2 Peter"],
    "1Jo": [62, 5, "1 John"],
    "2Jo": [63, 1, "2 John"],
    "3Jo": [64, 1, "3 John"],
    "Jude": [65, 1, "Jude"],
    "Re": [66, 22, "Revelation"],
}

# python -m vulture tk.biblesearch.1.0.py
# python -m site --user-base
# C:\Users\User\AppData\Roaming\Python\Python310\Scripts\pylint tk.biblesearch.1.0.py
# C:\Users\User\AppData\Roaming\Python\Python310\Scripts\deadcode tk.biblesearch.1.0.py


class BibleSearchApp(tk.Tk):
    """
    A tkinter application to search through Bible verses.

    This app provides an interface for the user to search through Bible verses
    based on keywords, book, and chapter. It allows the user to filter verses,
    search for specific terms, and navigate to specific books and chapters.

    Attributes:
    - data (list[str]): Loaded Bible verses.
    - selected_book_var (tk.StringVar): Holds the currently selected book's name.
    - selected_chapter_var (tk.StringVar): Holds the currently selected chapter.
    - search_var (tk.StringVar): Holds the text the user wishes to search for.
    - ... (additional GUI elements)
    """

    def __init__(self):
        """
        Initialize the main application window and its components.
        """
        super().__init__()

        # Setting up the window
        title_font = ("Arial", 18)
        self.title("Bible Search")
        self.option_add("*Font", title_font)

        self.geometry("1024x600")
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Set global font for all ttk widgets
        font_tuple = ("Arial", 14)

        self.style.configure("TButton", font=font_tuple)
        self.style.configure("TLabel", font=font_tuple)
        self.style.configure("TEntry", font=font_tuple)
        self.style.configure("TCombobox", font=font_tuple)
        self.style.configure("Treeview", font=font_tuple)
        self.style.configure("Treeview.Heading", font=font_tuple)

        # Variables
        self.selected_book_var = tk.StringVar(self)
        self.selected_chapter_var = tk.StringVar(self)
        self.search_var = tk.StringVar(self)
        self.chapter_popup = None

        # Load data
        self.data = self.load_data("biblesearch.txt")

        # Search
        self.search_entry = ttk.Entry(self, textvariable=self.search_var, width=50)
        self.search_entry.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

        # Dropdowns
        book_names = [book_data[2] for book_data in books.values()]
        self.book_dropdown = ttk.Combobox(
            self, textvariable=self.selected_book_var, values=book_names
        )
        self.book_dropdown.bind("<<ComboboxSelected>>", self.update_chapters)
        self.book_dropdown.grid(column=1, row=0, padx=10, pady=10, sticky="ew")

        self.chapter_dropdown = ttk.Combobox(
            self, textvariable=self.selected_chapter_var, width=5
        )
        self.chapter_dropdown.grid(column=2, row=0, padx=10, pady=10, sticky="ew")

        # Buttons
        self.search_button = ttk.Button(
            self, text="Search", command=self.perform_search
        )
        self.search_button.grid(column=3, row=0, padx=10, pady=10)
        self.go_button = ttk.Button(self, text="Go", command=self.go_to_chapter)
        self.go_button.grid(column=4, row=0, padx=10, pady=10)

        # Results tree
        self.tree = ttk.Treeview(
            self, columns=("Book", "Chapter", "VerseNum", "Verse"), show="headings"
        )

        max_book_length = max(len(book_data[2]) for book_data in books.values())
        id_width = 0
        book_width = min(150, max_book_length * 12)
        chapter_width = 50
        verse_num_width = 50
        initial_frame_width = 1024
        remaining_width = (
            initial_frame_width
            - id_width
            - book_width
            - chapter_width
            - verse_num_width
            - 20
        )

        self.tree.column("Book", width=book_width)
        self.tree.column("Chapter", width=chapter_width)
        self.tree.column("VerseNum", width=verse_num_width)
        self.tree.column("Verse", width=remaining_width)

        self.tree.heading("Book", text="Book")
        self.tree.heading("Chapter", text="Chp")
        self.tree.heading("VerseNum", text="V#")
        self.tree.heading("Verse", text="Verse")

        self.tree.grid(column=0, row=1, columnspan=5, padx=10, pady=10, sticky="nsew")

        # Create an invisible image to adjust row height in treeview
        self.transparent_image = tk.PhotoImage(width=1, height=25)

        self.grid_columnconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # Default book and chapter to "ALL"
        self.selected_book_var.set("All Books")
        self.update_chapters(None)
        self.selected_chapter_var.set("ALL")

        # Set focus to search entry
        self.search_entry.focus_set()

        # Bind Enter key to search
        self.bind("<Return>", lambda event: self.perform_search())
        self.tree.bind("<Double-1>", self.on_tree_item_double_click)

    def on_tree_item_double_click(self, event):
        """
        Handle double click event on a tree item to show the ChapterPopup.

        Event Params:
        - event: The event that triggered the method.
        """

        # Get the selected item
        item = self.tree.selection()[0]

        # Retrieve book, chapter, and verse values
        book = self.tree.item(item, "values")[0]
        chapter = self.tree.item(item, "values")[1]
        verse_text = self.tree.item(item, "values")[2]

        # Extract the verse number from the verse_text
        verse_num = None
        match = re.match(r"^(\d+)", verse_text)
        if match:
            verse_num = int(match.group(1))

        if book and chapter:
            verses = self.get_verses_for_chapter(book, chapter)
            self.chapter_popup = ChapterPopup(
                self, book, chapter, verses, highlight_verse=verse_num
            )

    def load_data(self, filename):
        """
        Load Bible data from a file.

        Parameters:
        - filename (str): Path to the file containing Bible data.

        Returns:
        - list[str]: List of lines (verses) loaded from the file.
        """
        #with open(filename, "r", encoding="utf-8") as f:
        #    return f.readlines()
        with open(filename, "r", encoding="windows-1252") as f:
            return f.readlines()

    def update_chapters(self, event):
        """
        Update the chapters dropdown based on the selected book.

        Event Params:
        - event: The event that triggered the method.
        """
        book_full_name = self.selected_book_var.get()
        if book_full_name == "All Books":
            self.chapter_dropdown["values"] = ["ALL"]
            return
        abbrev = next(
            abbrev
            for abbrev, book_data in books.items()
            if book_data[2] == book_full_name
        )
        max_chapter = books[abbrev][1]
        self.chapter_dropdown["values"] = ["ALL"] + list(range(1, max_chapter + 1))

    def perform_search(self):
        """
        Search the Bible data based on user's input and display the results.
        """

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_str = self.search_var.get().lower()
        selected_book_full = self.selected_book_var.get()
        selected_chapter = self.selected_chapter_var.get()

        # Filter data based on selected book and chapter
        if selected_book_full != "All Books":
            abbrev = next(
                abbrev
                for abbrev, book_data in books.items()
                if book_data[2] == selected_book_full
            )
            filtered_data = [line for line in self.data if line.startswith(abbrev)]
            if selected_chapter != "ALL":
                filtered_data = [
                    line
                    for line in filtered_data
                    if line.split()[1].startswith(selected_chapter + ":")
                ]
        else:
            filtered_data = self.data

        # Using regex to search for whole word matches
        pattern = r"(?:\W|^)" + re.escape(search_str) + r"(?:\W|$)"
        for line in filtered_data:
            if re.search(pattern, line, re.IGNORECASE):  # Using re.IGNORECASE to make it case insensitive
                parts = re.match(r"(\w+) (\d+):(\d+) (.+)", line)
                if parts:
                    book_abbrev, chapter, verse_num, verse_text = parts.groups()
                    book_full = books[book_abbrev][2]
                    self.tree.insert(
                        "",
                        "end",
                        values=(book_full, chapter, verse_num, verse_text),
                        image=self.transparent_image,
                    )

    def perform_search2(self):
        """
        Search the Bible data based on user's input and display the results.
        """

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_str = self.search_var.get().lower()
        selected_book_full = self.selected_book_var.get()
        selected_chapter = self.selected_chapter_var.get()

        # Filter data based on selected book and chapter
        if selected_book_full != "All Books":
            abbrev = next(
                abbrev
                for abbrev, book_data in books.items()
                if book_data[2] == selected_book_full
            )
            filtered_data = [line for line in self.data if line.startswith(abbrev)]
            if selected_chapter != "ALL":
                filtered_data = [
                    line
                    for line in filtered_data
                    if line.split()[1].startswith(selected_chapter + ":")
                ]
        else:
            filtered_data = self.data

        for line in filtered_data:
            if search_str in line.lower():
                parts = re.match(r"(\w+) (\d+):(\d+) (.+)", line)
                if parts:
                    book_abbrev, chapter, verse_num, verse_text = parts.groups()
                    book_full = books[book_abbrev][2]
                    self.tree.insert(
                        "",
                        "end",
                        values=(book_full, chapter, verse_num, verse_text),
                        image=self.transparent_image,
                    )

    def get_verses_for_chapter(self, book_full_name, chapter):
        """
        Retrieve verses for a specified book and chapter.

        Parameters:
        - book_full_name (str): Full name of the book.
        - chapter (str): Chapter number.

        Returns:
        - list[str]: List of verses for the given book and chapter.
        """
        abbrev = next(
            abbrev
            for abbrev, book_data in books.items()
            if book_data[2] == book_full_name
        )
        chapter_prefix = f"{abbrev} {chapter}:"
        return [
            " ".join(line.split()[2:])
            for line in self.data
            if line.startswith(chapter_prefix)
        ]

    def go_to_chapter(self):
        """
        Navigate to the specified book and chapter using the ChapterPopup.
        """
        if (
            self.selected_book_var.get() == "All Books"
            or self.selected_chapter_var.get() == "ALL"
        ):
            messagebox.showinfo("Info", "Please select a specific Book and Chapter.")
            return

        verses = self.get_verses_for_chapter(
            self.selected_book_var.get(), self.selected_chapter_var.get()
        )
        self.chapter_popup = ChapterPopup(
            self, self.selected_book_var.get(), self.selected_chapter_var.get(), verses
        )


class ChapterPopup(tk.Toplevel):
    """
    Initialize a popup window to display the verses of a given book and chapter.

    Parameters:
    - parent (tk.Widget): The parent widget that this popup belongs to.
    - book (str): The name of the book.
    - chapter (str): The chapter number of the book.
    - verses (list[str]): List of verses for the given book and chapter.
    - highlight_verse (int, optional): The verse number to highlight. Defaults to None.

    Attributes:
    - parent (tk.Widget): The parent widget that this popup belongs to.
    - book (str): The name of the book.
    - chapter (str): The chapter number of the book.
    - highlight_verse (int): The verse number to highlight. 
      If not provided, no verse is highlighted.
    """

    def __init__(self, parent, book, chapter, verses, highlight_verse=None):
        super().__init__(parent)

        self.parent = parent
        self.book = book
        self.chapter = chapter
        self.highlight_verse = highlight_verse

        self.title(f"{self.book} {self.chapter}")
        self.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.prev_button = ttk.Button(
            self, text="Previous", command=self.previous_chapter
        )
        self.prev_button.grid(row=0, column=0, padx=5, pady=5)

        self.next_button = ttk.Button(self, text="Next", command=self.next_chapter)
        self.next_button.grid(row=0, column=2, padx=5, pady=5)

        self.header_label = tk.Label(
            self, text=f"{self.book} {self.chapter}", font=("Arial", 24)
        )
        self.header_label.grid(row=0, column=1, padx=5, pady=5)

        self.text_widget = tk.Text(
            self,
            wrap=tk.WORD,
            font=("Arial", 14),
            borderwidth=0,
            highlightthickness=0,
            bg=self.cget("bg"),
        )
        self.text_widget.grid(
            row=1, column=0, columnspan=3, padx=20, pady=5, sticky="nsew"
        )

        # Adding a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, command=self.text_widget.yview)
        self.scrollbar.grid(row=1, column=4, sticky="ns")
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)

        # Configure the tags for bold, italic and highlight, etc
        self.text_widget.tag_configure("bold", font=("Arial", 14, "bold"))
        self.text_widget.tag_configure("highlight", background="yellow")

        # Populate the text widget with the verses from the list passed
        self.populate_verses(verses)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def populate_verses(self, verses):
        """
        Clear and repopulate the text widget with the provided verses.

        Parameters:
        - verses (list[str]): A list of strings where each string represents a verse.

        This method will clear the text widget and then insert each verse from
        the provided list. The inserted verses are formatted with their
        corresponding verse number in bold. If a verse number matches the
        `highlight_verse` attribute, that verse is highlighted with a yellow background.
        """
        self.text_widget.delete(1.0, tk.END)
        for idx, verse in enumerate(verses, start=1):
            reference = f"{idx}.  "

            # Highlight the specific verse if specified
            if self.highlight_verse and idx == self.highlight_verse:
                self.text_widget.insert(tk.END, reference, ("bold", "highlight"))
                self.text_widget.insert(tk.END, f" {verse}\n\n", "highlight")
            else:
                self.text_widget.insert(tk.END, reference, "bold")
                self.text_widget.insert(tk.END, f" {verse}\n\n")

    def next_chapter(self):
        """
        Navigate to the next chapter.

        If there's a subsequent chapter, it retrieves the verses for that chapter
        using the `get_verses_for_chapter` method of the parent widget and updates
        the displayed chapter accordingly. If there's no subsequent chapter (i.e.,
        it's the last chapter of the book), the "Next" button is disabled.
        """
        self.highlight_verse = None

        # Convert the chapter to an integer, increment it, then convert back to a string
        self.chapter = str(int(self.chapter) + 1)
        new_verses = self.parent.get_verses_for_chapter(
            self.book, self.chapter
        )
        if new_verses:
            self.header_label.config(text=f"{self.book} {self.chapter}")
            self.populate_verses(new_verses)
        else:
            # (disable the "Next" button)
            self.next_button.config(state=tk.DISABLED)

    def previous_chapter(self):
        """
        Navigate to the previous chapter.

        If there's a preceding chapter, it retrieves the verses for that chapter
        using the `get_verses_for_chapter` method of the parent widget and updates
        the displayed chapter accordingly. If there's no preceding chapter (i.e.,
        it's the first chapter of the book), the "Previous" button is disabled.
        """
        self.highlight_verse = None

        # Convert the chapter to an integer, decrement (if required, convert back
        if int(self.chapter) > 1:
            self.chapter = str(int(self.chapter) - 1)
            new_verses = self.parent.get_verses_for_chapter(self.book, self.chapter)
            self.header_label.config(text=f"{self.book} {self.chapter}")
            self.populate_verses(new_verses)
        else:
            # (disable the "Previous" button)
            self.prev_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = BibleSearchApp()
    app.mainloop()
