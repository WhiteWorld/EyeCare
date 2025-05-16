import threading
import time
from datetime import datetime, time as dt_time

class EyeTimers:
    def __init__(self, eye_rest_interval, eye_drop_interval, eye_rest_reminder_cb, eye_drop_reminder_cb):
        self.rest_time_range = (None, None)
        self.drop_time_range = (None, None)
        self.eye_rest_start_time = None
        self.eye_drop_start_time = None
        self.eye_rest_interval = eye_rest_interval
        self.eye_drop_interval = eye_drop_interval
        self.eye_rest_timer = None
        self.eye_drop_timer = None
        self.periodic_rest = False
        self.periodic_drop = False
        self.eye_rest_reminder_cb = eye_rest_reminder_cb
        self.eye_drop_reminder_cb = eye_drop_reminder_cb

    def set_rest_interval(self, interval):
        self.eye_rest_interval = interval

    def set_drop_interval(self, interval):
        self.eye_drop_interval = interval

    def start_rest_timer(self, periodic=False):
        self.periodic_rest = periodic
        if self.eye_rest_timer:
            self.eye_rest_timer.cancel()
        
        def wrapped_rest_reminder():
            self.eye_rest_reminder_cb()
            if self.periodic_rest and self.is_within_time_range('rest'):
                self.start_rest_timer(self.periodic_rest) # Restart only rest timer
                
        self.eye_rest_timer = threading.Timer(self.eye_rest_interval, wrapped_rest_reminder)
        self.eye_rest_timer.start()
        self.eye_rest_start_time = time.time()

    def start_drop_timer(self, periodic=False):
        self.periodic_drop = periodic
        if self.eye_drop_timer:
            self.eye_drop_timer.cancel()
            
        def wrapped_drop_reminder():
            self.eye_drop_reminder_cb()
            if self.periodic_drop and self.is_within_time_range('drop'):
                self.start_drop_timer(self.periodic_drop) # Restart only drop timer
                
        self.eye_drop_timer = threading.Timer(self.eye_drop_interval, wrapped_drop_reminder)
        self.eye_drop_timer.start()
        self.eye_drop_start_time = time.time()

    def start_timers(self, periodic_rest=False, periodic_drop=False):
        self.start_rest_timer(periodic_rest)
        self.start_drop_timer(periodic_drop)

    def cancel_rest_timer(self):
        if self.eye_rest_timer:
            self.eye_rest_timer.cancel()
            self.eye_rest_start_time = None # Reset start time

    def cancel_drop_timer(self):
        if self.eye_drop_timer:
            self.eye_drop_timer.cancel()
            self.eye_drop_start_time = None # Reset start time

    def cancel_timers(self):
        self.cancel_rest_timer()
        self.cancel_drop_timer()

    def set_time_range(self, timer_type, start_time_str, end_time_str):
        try:
            start_time = dt_time(*map(int, start_time_str.split(':')))
            end_time = dt_time(*map(int, end_time_str.split(':')))
            if timer_type == 'rest':
                self.rest_time_range = (start_time, end_time)
            elif timer_type == 'drop':
                self.drop_time_range = (start_time, end_time)
        except ValueError:
            pass

    def is_within_time_range(self, timer_type):
        now = datetime.now().time()
        if timer_type == 'rest':
            start, end = self.rest_time_range
        elif timer_type == 'drop':
            start, end = self.drop_time_range
        else:
            return False
        if start and end:
            if start <= end:
                return start <= now <= end
            else:
                return start <= now or now <= end
        return True

    def get_remaining_time(self, timer_type):
        if timer_type == 'rest':
            if self.eye_rest_start_time is None:
                return '0分0秒'
            elapsed = time.time() - self.eye_rest_start_time
            remaining = max(0, self.eye_rest_interval - elapsed)
            return f'{int(remaining//60)}分{int(remaining%60)}秒'
        elif timer_type == 'drop':
            if self.eye_drop_start_time is None:
                return '0分0秒'
            elapsed = time.time() - self.eye_drop_start_time
            remaining = max(0, self.eye_drop_interval - elapsed)
            return f'{int(remaining//60)}分{int(remaining%60)}秒'
        return '未知类型'