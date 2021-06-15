import random
import string


class password_generator:
    total_set = string.ascii_uppercase + string.ascii_lowercase + string.digits

    def __init__(self, password_length=8, **kwargs):
        self.password_length = password_length
        if len(kwargs) != 0:
            self.total_set = ""
            for arg in kwargs.values():
                self.total_set += arg

    def generate(self):
        temp = random.sample(self.total_set, self.password_length)
        password = "".join(temp)
        return password
