import json


class Bears:

    def __init__(self):
        self._bear_Boris = {"bear_type": "BROWN",
                            "bear_name": "Boris", "bear_age": 16}
        self._bear_Semen = {"bear_type": "BLACK",
                            "bear_name": "Semen", "bear_age": 17.5}

    def get_Boris(self):
        return self._bear_Boris.copy()

    def get_Semen(self):
        return self._bear_Semen.copy()


def bears_eq(b1, b2):
    if 'bear_id' in b1 and 'bear_id' in b2:
        if b1['bear_id'] != b2['bear_id']:
            return False
    return b1['bear_type'] == b2['bear_type'] and b1['bear_name'].upper() == b2['bear_name'].upper() and b1['bear_age'] == b2['bear_age']


def bears_to_dict(bears):
    bears_dict = dict()
    for bear in bears:
        bears_dict[bear['bear_id']] = bear.copy()
    return bears_dict
