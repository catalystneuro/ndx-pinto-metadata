import os
from pynwb import load_namespaces, register_class
from pynwb.file import DynamicTable
from hdmf.utils import docval, get_docval

spec_path = os.path.abspath(os.path.dirname(__file__))
ns_path = os.path.join(spec_path, "spec", "ndx-pinto-metadata.namespace.yaml")

load_namespaces(ns_path)


@register_class("StimulusParametersExtension", "ndx-pinto-metadata")
class StimulusParametersExtension(DynamicTable):
    """
    Table for storing stimulus protocol information
    """

    stimulus_protocol_attributes = [
        "numTrials",
        "numTrialsPerMin",
        "criteriaNTrials",
        "warmupNTrials",
        "warmupMaxNTrials",
        "numSessions",
        "performance",
        "maxBias",
        "warmupMaze",
        "warmupPerform",
        "warmupBias",
        "warmupMotor",
        "easyBlock",
        "easyBlockNTrials",
        "numBlockTrials",
        "blockPerform",
        "nTrialRange",
        "nTrialRangeEasy",
        "geoDistP",
        "geoDistPEasy",
        "numTrials",
        "numTrialsPerMin",
        "criteriaNTrials",
        "warmupNTrials",
        "warmupMaxNTrials",
        "numSessions",
        "performance",
        "maxBias",
        "warmupMaze",
        "warmupPerform",
        "warmupBias",
        "warmupMotor",
        "easyBlock",
        "easyBlockNTrials",
        "numBlockTrials",
        "blockPerform",
        "nTrialRange",
        "nTrialRangeEasy",
        "geoDistP",
        "geoDistPEasy",
        "numTrials",
        "numTrialsPerMin",
        "criteriaNTrials",
        "warmupNTrials",
        "warmupMaxNTrials",
        "numSessions",
        "performance",
        "maxBias",
        "warmupMaze",
        "warmupPerform",
        "warmupBias",
        "warmupMotor",
        "easyBlock",
        "easyBlockNTrials",
        "numBlockTrials",
        "blockPerform",
        "nTrialRange",
        "nTrialRangeEasy",
        "geoDistP",
        "geoDistPEasy",
    ]

    __columns__ = tuple(
        {
            "name": attr,
            "description": "stimulus protocol information",
            "required": False,
            "index": False,
            "table": False,
        }
        for attr in stimulus_protocol_attributes
    )

    @docval(
        dict(
            name="name", type=str, doc="name of this StimulusParametersExtension"
        ),  # required
        dict(name="description", type=str, doc="Description of this DynamicTable"),
        *get_docval(DynamicTable.__init__, "id", "columns", "colnames")
    )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
