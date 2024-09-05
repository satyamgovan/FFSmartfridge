import logging
import subprocess


class WindowManager:
    def __init__(self, window):
        self.window = window
        self.file_paths = {
            'gui2': '../home/gui.py',
            'gui3': '../inventory/gui.py',
            'gui4': '../login/gui.py',
            'gui5': '../manual/gui.py',
            'gui6': '../profile/gui.py',
            'gui7': '../remove/gui.py',
            'gui8': '../report/gui.py',
            'gui9': '../users/gui.py',
            'gui10': '../add_user/gui.py',
            'gui11': '../delivery_display/gui.py'
        }

    def run_new_file(self, file_key, user_id=None):
        self.window.destroy()
        command = ['python', self.file_paths[file_key]]
        if user_id is not None:
            command.append(str(user_id))
        subprocess.run(command)

    def clear_text_widget(self, text_widget):
        if text_widget:
            text_widget.delete("1.0", "end")
        else:
            logging.warning("Attempting to clear a non-existent text widget.")

