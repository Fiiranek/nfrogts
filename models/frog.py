import operator
from json import load

from models.gadget import Gadget


class Frog:
    def __init__(self, number):
        self.number = number
        self.data = self.read_info()
        self.name = self.data['name']
        self.body = self.data['body']
        self.gadgets = self.data['gadgets']

    def read_info(self):
        with open('metadata_correct.json', 'r') as metadata_file:
            data = load(metadata_file)[str(self.number)]
            metadata_file.close()
            return data


class FrogMetadata:
    def __init__(self, number):
        self.number = number
        self.name = f"NFROGT #{number}"
        self.gadgets = []
        self.image = ""
        self.body = ""

    def add_gadget(self, gadget: Gadget):
        self.gadgets.append(gadget)

    def can_add_gadget(self, gadget: Gadget, rarity_data: dict):
        for owned_gadget in self.gadgets:
            if gadget.place == owned_gadget.place:
                return False
        # if rarity_data['maxTotalGadgets'][gadget.name] <= 0:
        #     return False
        return True

    def set_body(self, body):
        self.body = body

    def __str__(self):
        gadgets_str = ""
        for gadget in self.gadgets:
            gadgets_str += str(gadget) + " "
        return f"#{self.number} - {self.body} - {gadgets_str} - {self.image}"

    def to_json(self):
        gadgets = []
        for gadget in self.gadgets:
            gadgets.append(gadget.name)
        return {
            str(self.number): {
                'name': self.name,
                'body': self.body,
                'gadgets': gadgets,
                'image': self.image,
            }
        }

    def to_dict(self):
        gadgets = []
        for gadget in self.gadgets:
            gadgets.append(gadget.name)
        return {
            'name': self.name,
            'body': self.body,
            'gadgets': gadgets,
            'image': self.image,
        }

    def sort_gadgets(self):
        self.gadgets.sort(key=operator.attrgetter('name'))

    def gadgets_str(self):
        gadgets_str = ""
        for gadget in self.gadgets:
            gadgets_str += str(gadget) + "-"
        return gadgets_str
