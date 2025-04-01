from dataclasses import dataclass


@dataclass
class Configuration:
    resources_folder: str = None
    pixel_per_universe: int = 128  # FIXME ensure READ ONLY
