from copy import deepcopy


class SummableDict(dict):
    """
    All values from other dict are summed to self if key is present, else key is created with other's value
    """

    def __add__(self, other):
        me = deepcopy(self)
        for key, other_value in other.items():
            self_value = me.get(key, None)
            if self_value is None:
                me[key] = deepcopy(other_value)
            else:
                me[key] += other_value

        return me
