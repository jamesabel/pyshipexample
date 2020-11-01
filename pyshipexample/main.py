import sys
from threading import Thread, Event

from mttkinter.mtTkinter import Tk, BOTH, Button, Frame, Label, StringVar

from pyshipupdate import UpdaterAwsS3, restart_return_code, ok_return_code

from pyshipexample import __application_name__, __author__
from pyshipexample import __version__ as current_version

exit_event = Event()

return_code = ok_return_code


class UpdateApplication(Thread):
    def __init__(self, window):
        self.window = window
        super().__init__()

    def run(self):
        global return_code
        updater = UpdaterAwsS3(__application_name__, __author__)
        updater.update(current_version)
        return_code = restart_return_code
        self.window.master.quit()  # exit the application


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        # changing the title of our master widget
        self.master.title(__application_name__)

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        self.current_version_label = Label(self, text=f"current_version={current_version}")
        self.current_version_label.pack()

        self.available_versions_value = StringVar()
        self.available_versions_value_label = Label(self, textvariable=self.available_versions_value)
        self.available_versions_value_label.pack()

        self.greatest_version_value = StringVar()
        self.greatest_version_value_label = Label(self, textvariable=self.greatest_version_value)
        self.greatest_version_value_label.pack()

        Label(self).pack()  # space

        self.update_button = Button(self, text="Update Application", command=self.update_application)
        self.update_button.pack()

        Label(self).pack()  # space

        self.status_value = StringVar()
        self.status_value_label = Label(self, textvariable=self.status_value)
        self.status_value_label.pack()

        self.master.focus_force()

        self.get_versions()

        self.update_application = None

    def get_versions(self):
        updater = UpdaterAwsS3(__application_name__, __author__)
        available_versions = updater.get_available_versions()
        greatest_version = updater.get_greatest_version()
        self.available_versions_value.set(f"available_versions={','.join([str(v) for v in available_versions])}")
        self.greatest_version_value.set(f"greatest_version={str(greatest_version)}")

    def update_application(self):
        if self.update_application is None or not self.update_application.is_alive():
            self.status_value.set("Updating ...")
            self.update_application = UpdateApplication(self)
            self.update_application.start()


def main():
    root = Tk()

    # size and position of window
    w = 600
    h = 300
    x = (root.winfo_screenwidth() / 2) - (w / 2)  # middle of desktop
    y = (root.winfo_screenheight() / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    Window(root)
    root.mainloop()

    sys.exit(return_code)  # tell the launcher we want to be restarted
