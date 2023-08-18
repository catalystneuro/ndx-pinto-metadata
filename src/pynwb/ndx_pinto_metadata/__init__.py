from pynwb import get_class
from .maze_extension import MazeExtension
from .stimulus_parameters_extension import StimulusParametersExtension

LabMetaDataExtension = get_class("LabMetaDataExtension", "ndx-pinto-metadata")
StimulusProtocolExtension = get_class("StimulusProtocolExtension", "ndx-pinto-metadata")
