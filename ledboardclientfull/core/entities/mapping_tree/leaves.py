from dataclasses import dataclass, field

from ledboardclientfull.core.entities.mapping_tree.leaf import MappingTreeLeaf
from ledboardclientfull.python_extensions.summable_dict import SummableDict


@dataclass
class LeavesUniverse:
    index: int = -1
    leaves: SummableDict[int, list[MappingTreeLeaf]] = field(default_factory=SummableDict)

    def __add__(self, other):
        return LeavesUniverse(
            leaves=self.leaves + other.leaves
        )


@dataclass
class Leaves:
    universes: SummableDict[int, LeavesUniverse] = field(default_factory=SummableDict)

    def all(self):
        all_leaves = list()

        for universe in self.universes.values():
            for leaves in universe.leaves.values():
                all_leaves += leaves

        return all_leaves

    def __add__(self, other):
        return Leaves(
            universes=self.universes + other.universes
        )
