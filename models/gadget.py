class Gadget:
    def __init__(self, name, place):
        self.name = name
        self.place = place

    def __str__(self):
        return f"{self.name} - {self.place}"
