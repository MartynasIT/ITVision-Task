import time
import random


class Helpers:
    def __init__(self, start, end, length, answer):
        self.start = start
        self.ended = end
        self.chat_len = length
        self.answer_state = answer

    # simple call simulation system
    # pic random action for the call
    def pick_action(self):
        action = random.randint(1, 3)
        # user hang up
        if action == 1:
            do = 'Call failed'
        # user was moved to group with extension 300 but no one answered
        elif action == 2:
            do = 'Move to group with 300'
            self.answer_state = "not_answered"
        # someone answered with extension of 200
        else:
            wait_time = random.randint(3, 7)
            time.sleep(wait_time)
            do = 'Group picked up with 200'
            # simulate time they talked
            self.chat_len = random.randint(1, 90)
            self.answer_state = "answered"
        return do

    # functions for setting call times and calculations
    def start_call_time(self):
        self.start = int(time.time())
        return self.start

    def total_call_time(self):
       return self.ended - self.start + self.chat_len

    def end_call_time(self):
        self.ended = int(time.time())

    def get_call_end(self):
        return self.ended

    def chat_start(self):
        self.start = time.time()

    def get_chat_duration(self):
        return self.chat_len

    def get_answer_state(self):
        return self.answer_state

