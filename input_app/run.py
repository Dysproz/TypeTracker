from pynput import keyboard
from pynput import mouse
from datetime import datetime
import csv
import threading

class TypeListener:
    def __init__(self, save_time=60):
        self.data = {}
        self.save_time = save_time

    def append_data(self, key):
        try:
            self.data[key] += 1
        except KeyError:
            self.data[key] = 1

    def on_release_keyboard(self, key):
        print(key)
        self.append_data(key)
        if key == keyboard.Key.esc:
            return False

    def on_click_mouse(self, x ,y ,button, pressed):
        print(button)
        if pressed:
            self.append_data(button)

    def on_scroll_mouse(self, x, y, dx, dy):
        print('scroll')
        self.append_data('scroll')

    def save_data(self, date_time):
        date = str(date_time.date())
        time = date_time.strftime('%d-%m-%Y %H:%M:%S')
        with open('data/typer_{date}'.format(date=date), 'a') as log_file:
            csv_writer = csv.writer(log_file, delimiter=',')
            for key, value in self.data.iteritems():
                csv_writer.writerow([time, key, value])
        print('Data saved to typer_{date} for {time}'.format(date=date, time=time))
        self.data = {}

    def listen(self):
        # thread1 = threading.Thread(target=self.listener)
        # thread1.start()
        self.listener()
        timer = datetime.now()
        while True:
            if (datetime.now()-timer).seconds >= self.save_time:
                        self.save_data(timer)
                        timer = datetime.now()

    def listener(self):
        with keyboard.Listener(on_release=self.on_release_keyboard) as keyboard_listener:
            if not keyboard_listener.is_alive():
                keyboard_listener.start()

if __name__ == '__main__':
    SAVE_TIME = 30
    listener = TypeListener(SAVE_TIME)
    listener.listen()
