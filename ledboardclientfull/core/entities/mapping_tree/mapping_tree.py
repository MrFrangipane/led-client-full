from dataclasses import dataclass, field

from ledboardclientfull.core.entities.mapping_tree.structures import MappingTreeStructure
from ledboardclientfull.core.entities.mapping_tree.leaves import Leaves


@dataclass
class MappingTree:
    structure: MappingTreeStructure = field(default_factory=MappingTreeStructure)
    leaves: Leaves = field(default_factory=Leaves)

    def __add__(self, other):
        return MappingTree(
            structure=self.structure + other.structure,
            leaves=self.leaves + other.leaves
        )
