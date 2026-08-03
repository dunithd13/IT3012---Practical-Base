import random


class SimpleReflexAgent:

    def sense_and_act(self, percept):

        if percept["food_here"]:
            return "Stay"

        if percept["wall_ahead"]:
            return "Left"

        return "Up"


class ModelBasedAgent:

    def __init__(self):
        self.last_action = None
        self.stuck_counter = 0

    def sense_and_act(self, percept):

        if percept["food_here"]:
            return "Stay"

        if percept["wall_ahead"]:

            if self.last_action == "Left":
                action = "Right"
            else:
                action = "Left"

            self.last_action = action
            return action

        self.last_action = "Up"
        return "Up"