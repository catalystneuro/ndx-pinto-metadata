import numpy as np
from hdmf.common.table import DynamicTable
from hdmf.testing import TestCase, remove_test_file
from pynwb import NWBHDF5IO
from pynwb.testing.mock.file import mock_NWBFile

from ndx_pinto_metadata import (
    MazeExtension,
    LabMetaDataExtension,
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
            numTrials=80,
            numTrialsPerMin=2,
            criteriaNTrials=100,
            numSessions=1,
            performance=np.inf,
            maxBias=0.2,
            easyBlock=np.nan,
            easyBlockNTrials=10,
            numBlockTrials=40,
            blockPerform=0.55,
            geoDistP=np.nan,
            geoDistPEasy=np.nan,
        )

        cls.global_settings = dict(
            cueMinSeparation=12,
            totalRepeatProbability=0.05,
            numRepeatTrials=2,
            visualcolor=np.array([0, 0, 1]),
            memorycolor=np.array([0, 0, 1]),
            princetonImplementation=1,
            numMazesInProtocol=11,
            trialDraw="EradeCapped",
            stimDraw="LeftOneOnly",
        )

        cls.nwbfile_path = "test.nwb"

    @classmethod
    def tearDownClass(cls):
        remove_test_file(cls.nwbfile_path)

    def test_add_to_nwbfile(self):
        # Add MazeExtension
        maze_extension = MazeExtension(name="mazes", description="maze information")
        maze_extension.add_row(**self.maze)

        # Create stimulus protocol with global settings
        stimulus_protocol = DynamicTable(
            name="stimulus_protocol",
            description="Holds information about the stimulus protocol.",
        )

        for name in list(self.global_settings.keys()):
            stimulus_protocol.add_column(
                name=name,
                description="stimulus protocol parameter.",
            )

        stimulus_protocol.add_row(**self.global_settings)

        # Create LabMetaData container
        lab_metadata_dict = dict(
            name="LabMetaData",
            experiment_name="test",
            mazes=maze_extension,
            stimulus_protocol=stimulus_protocol,
        )

        # Populate metadata extension
        lab_metadata = LabMetaDataExtension(**lab_metadata_dict)

        # Add to file
        self.nwbfile.add_lab_meta_data(lab_metadata)

        nwbfile_lab_metadata = self.nwbfile.lab_meta_data["LabMetaData"]
        self.assertContainerEqual(nwbfile_lab_metadata.mazes, maze_extension)
        self.assertContainerEqual(
            nwbfile_lab_metadata.stimulus_protocol, stimulus_protocol
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
