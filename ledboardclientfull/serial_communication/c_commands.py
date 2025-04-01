from dataclasses import dataclass

from pythonarduinoserial.types import *


@dataclass
class BeginSamplePointsReceptionCommand:
    count: IntegerType() = 0


@dataclass
class EndSamplePointsReceptionCommand:
    unused: IntegerType() = 0


@dataclass
class RebootInBootloaderModeCommand:
    unused: IntegerType() = 0


@dataclass
class SaveControlParametersCommand:
    unused: IntegerType() = 0  # FIXME


@dataclass
class SaveSamplingPointsCommand:
    unused: IntegerType() = 0  # FIXME


__all__ = [
    BeginSamplePointsReceptionCommand,
    EndSamplePointsReceptionCommand,
    RebootInBootloaderModeCommand,
    SaveControlParametersCommand,
    SaveSamplingPointsCommand,
]
