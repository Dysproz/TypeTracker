from pynput import keyboard
from pynput import mouse
from datetime import datetime
import csv
import threading


class Recorder():
    def __init__(self):
        self.data = {}

    def append_data(self, key):
        try:
            self.data[key] += 1
        except KeyError:
            self.data[key] = 1

    def get_data(self):
        return self.data

    def clear_data(self):
        self.data = {}


class KeyListener:
    def __init__(self, recorder):
        self.recorder = recorder

    def on_release_keyboard(self, key):
        print(key)
        self.recorder.append_data(key)
        if key == keyboard.Key.esc:
            return False

    def listen(self):
        with keyboard.Listener(on_release=self.on_release_keyboard) as keyboard_listener:
            keyboard_listener.join()


class MouseListener:
    def __init__(self, recorder):
        self.recorder = recorder

    def on_click_mouse(self, x ,y ,button, pressed):
        print(button)
        if not pressed:
            self.recorder.append_data(button)

    def on_scroll_mouse(self, x, y, dx, dy):
        print('scroll')
        self.recorder.append_data('scroll')

    def listen(self):
        with mouse.Listener(on_click=self.on_click_mouse,
                            on_scroll=self.on_scroll_mouse) as mouse_listener:
            mouse_listener.join()


class DataSaver:
    def __init__(self, recoder, save_time=60):
        self.recorder = recorder
        self.save_time = save_time

    def save_data(self, date_time):
        date = str(date_time.date())
        time = date_time.strftime('%d-%m-%Y %H:%M:%S')
        with open('data/typer_{date}.csv'.format(date=date), 'a') as log_file:
            csv_writer = csv.writer(log_file, delimiter=',')
            data = self.recorder.get_data().copy()
            for key, value in data.iteritems():
                csv_writer.writerow([time, key, value])
        print('Data saved to typer_{date} for {time}'.format(date=date, time=time))
        self.recorder.clear_data()

    def check_for_saving(self):
        timer = datetime.now()
        while True:
            if (datetime.now()-timer).seconds >= self.save_time:
                self.save_data(timer)
                timer = datetime.now()

if __name__ == '__main__':
    SAVE_TIME = 5
    recorder = Recorder()
    saver = DataSaver(recorder, SAVE_TIME)
    key_listener = KeyListener(recorder)
    mouse_listener = MouseListener(recorder)
    thread_keylistener = threading.Thread(target=key_listener.listen)
    thread_mouse_listener = threading.Thread(target=mouse_listener.listen)
    thread_saver = threading.Thread(target=saver.check_for_saving)
    thread_keylistener.setDaemon(True)
    thread_mouse_listener.setDaemon(True)
    thread_saver.setDaemon(True)
    thread_keylistener.start()
    thread_mouse_listener.start()
    thread_saver.start()
    while True:
        if not thread_saver.is_alive():
            thread_saver.start()
        if not thread_keylistener.is_alive():
            thread_keylistener.start()
        if not thread_mouse_listener.is_alive():
            thread_mouse_listener.start()
        pass