from pynput import keyboard
from pynput import mouse
from datetime import datetime, timedelta
import csv
import threading


class Recorder():
    def __init__(self):
        self.data_keyboard = {}
        self.data_mouse = {}

    def append_data(self, key, input_type):
        if input_type == "mouse":
            try:
                self.data_mouse[key] += 1
            except KeyError:
                self.data_mouse[key] = 1
        else:
            try:
                self.data_keyboard[key] += 1
            except KeyError:
                self.data_keyboard[key] = 1

    def get_data_keyboard(self):
        return self.data_keyboard

    def get_data_mouse(self):
        return self.data_mouse

    def clear_data(self):
        self.data_keyboard = {}
        self.data_mouse = {}


class KeyListener:
    def __init__(self, recorder):
        self.recorder = recorder

    def on_release_keyboard(self, key):
        if str(key) in self.special_keys:
            key_formated = self.special_keys[str(key)]
        else:
            key_formated = str(key)
            if key_formated[:2] == "u'":
                key_formated = key_formated[2:-1]
        self.recorder.append_data(key_formated, 'keyboard')

    def listen(self):
        with keyboard.Listener(on_release=self.on_release_keyboard) as keyboard_listener:
            keyboard_listener.join()

    @property
    def special_keys(self):
        return {'<65437>': 5,
                '<65027>': 'Key.alt_r',
                '<269025026>': 'Key.brightnes_up',
                '<269025027>': 'Key.brightnes_down',
                '<269025167>': 'Key.no_camera',
                '<0>': 'Key.airplane',
                '<269025202>': 'Key.close_window',
                '<269025043>': 'Key.volume_up',
                '<269025041>': 'Key.volume_down',
                '<269025042>': 'Key.mute',
                '<269025047>': 'Key.next_track',
                '<269025046>': 'Key.previous_track',
                '<269025044>': 'Key.play_pause'
                }


class MouseListener:
    def __init__(self, recorder):
        self.recorder = recorder

    def on_click_mouse(self, x, y, button, pressed):
        if not pressed:
            self.recorder.append_data(button, 'mouse')

    def on_scroll_mouse(self, x, y, dx, dy):
        self.recorder.append_data('scroll', 'mouse')

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
            data_keyboard = self.recorder.get_data_keyboard().copy()
            data_mouse = self.recorder.get_data_mouse().copy()
            for key, value in data_keyboard.items():
                csv_writer.writerow([time, key, value, 'k'])
            for key, value in data_mouse.items():
                csv_writer.writerow([time, key, value, 'm'])
            if len(data_keyboard) == 0 and len(data_mouse) == 0:
                csv_writer.writerow([time, 'Key.enter', 0])
            else:
                minute_ahead = str((date_time+timedelta(seconds=60)).strftime('%d-%m-%Y %H:%M:%S'))
                csv_writer.writerow([minute_ahead, 'Key.enter', 0, 'k'])
        print('Data saved to typer_{date} for {time}'.format(date=date, time=time))
        self.recorder.clear_data()

    def check_for_saving(self):
        timer = datetime.now()
        while True:
            if (datetime.now()-timer).seconds >= self.save_time:
                self.save_data(timer)
                timer = datetime.now()


if __name__ == '__main__':
    SAVE_TIME = 60
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
