# week 4, task 2
# IMPORTANT: don't change Account class for testing on the site "coursera.org"

class Value:
    def __set__(self, instance, value):
        self.value = value - value * instance.commission

    def __get__(self, instance, owner):
        return self.value


# class Account:
#     amount = Value()
#
#     def __init__(self, commission):
#         self.commission = commission