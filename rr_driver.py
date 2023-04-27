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
