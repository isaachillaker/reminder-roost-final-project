"""
AUTHOR: Isaac Hillaker
ASSIGNMENT: Final Project: Task Manager
DATE: 04/28/2023
INFO:

    This driver runs the Task Manager app, utilizing the rr_classes.py file, found in this same directory.

I completed this assignment without any unauthorized assistance.
"""

from rr_classes import User, GUI
from tkinter import Tk


def main():
    # create root window
    root = Tk()

    # create GUI object and pass in root window
    gui = GUI(root)

    # start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()
