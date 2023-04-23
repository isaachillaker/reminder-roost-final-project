from rr_classes import User, GUI
from tkinter import Tk





# user = User("Isaac", "Hillaker")
# user.add_task("A", 1)
# user.add_task("B", 2)
# user.add_task("C", 3)
# print(user.to_do_tasks._queue)
# print(user.to_do_tasks.print_queue())
#
# print("")
#
# user.delete_task("C")
# print(user.to_do_tasks._queue)
# print(user.to_do_tasks.print_queue())
#
# print("")
#
# user.undo()
#
# print(user.to_do_tasks._queue)
# print(user.to_do_tasks.print_queue())

def main():
    # create root window
    root = Tk()

    # create GUI object and pass in root window
    gui = GUI(root)

    # start the event loop
    root.mainloop()


if __name__ == '__main__':
    main()
