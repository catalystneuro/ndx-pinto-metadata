from datetime import datetime

import numpy as np
from hdmf.testing import TestCase, remove_test_file
from pynwb import NWBHDF5IO
from pynwb.testing.mock.file import mock_NWBFile

from ndx_pinto_metadata import (
    MazeExtension,
    LabMetaDataExtension,
    StimulusParametersExtension,
    StimulusProtocolExtension,
)

class TestLabMetaDataExtensionConstructor(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nwbfile = mock_NWBFile()

        cls.maze = dict(
            antiFraction=0,
            cueDensityPerM=3,
            cueDuration=np.nan,
            cueProbability=np.inf,
            cueVisibleAt=10,
            hideHintUntil=-15,
            lContext=10,
            lCue=45,
            lMemory=10,
            lStart=5,
            maxTrialDuration=180,
            turnHint=1,
        )

        cls.stimulus_parameters = dict(
            numTrials=80,
            numTrialsPerMin=2,
            criteriaNTrials=100,
            warmupNTrials=3,
            warmupMaxNTrials=3,
            numSessions=1,
            performance=np.inf,
            maxBias=0.2,
            warmupMaze=3,
            warmupPerform=0.85,
            warmupBias=0.1,
            warmupMotor=0.75,
            easyBlock=np.nan,
            easyBlockNTrials=10,
            numBlockTrials=40,
            blockPerform=0.55,
            nTrialRange=np.nan,
            nTrialRangeEasy=np.nan,
            geoDistP=np.nan,
            geoDistPEasy=np.nan,
        )

        cls.global_settings = dict(
            num_mazes_in_protocol=11,
            trial_draw="EradeCapped",
            stimulus_draw="LeftOneOnly",
            visual_color=[0, 0, 1],
            memory_color=[0.5, 0.5, 0.0],
            is_princeton_implementation=1,
            cue_min_separation=12,
            num_repeat_trials=2,
            trial_repeat_probability=0.05,
        )

        cls.nwbfile_path = "test.nwb"

    @classmethod
    def tearDownClass(cls):
        remove_test_file(cls.nwbfile_path)

    def test_add_to_nwbfile(self):
        # Add stimulus parameters (one row for each maze)
        stimulus_parameters_extension = StimulusParametersExtension(
            name="stimulus_parameters",
            description="stimulus protocol parameters",
        )
        stimulus_parameters_extension.add_row(**self.stimulus_parameters)

        # Create stimulus protocol with global settings and add table with protocol parameters
        stimulus_protocol_extension = StimulusProtocolExtension(
            name="stimulus_protocol",
            stimulus_parameters=stimulus_parameters_extension,
            **self.global_settings,
        )

        # Add MazeExtension
        maze_extension = MazeExtension(name="mazes", description="maze information")
        maze_extension.add_row(**self.maze)

        # Create LabMetaData container
        lab_metadata_dict = dict(
            name="LabMetaData",
            experiment_name="test",
            mazes=maze_extension,
            stimulus_protocol=stimulus_protocol_extension,
        )

        # Populate metadata extension
        lab_metadata = LabMetaDataExtension(**lab_metadata_dict)

        # Add to file
        self.nwbfile.add_lab_meta_data(lab_metadata)

        nwbfile_lab_metadata = self.nwbfile.lab_meta_data["LabMetaData"]
        self.assertContainerEqual(nwbfile_lab_metadata.mazes, maze_extension)
        self.assertContainerEqual(
            nwbfile_lab_metadata.stimulus_protocol, stimulus_protocol_extension
        )

    def test_roundtrip(self):
        with NWBHDF5IO(self.nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_nwbfile_lab_metadata = read_nwbfile.lab_meta_data["LabMetaData"]
            self.assertContainerEqual(
                read_nwbfile_lab_metadata.mazes,
                self.nwbfile.lab_meta_data["LabMetaData"].mazes,
            )
            self.assertContainerEqual(
                read_nwbfile_lab_metadata.stimulus_protocol,
                self.nwbfile.lab_meta_data["LabMetaData"].stimulus_protocol,
            )
