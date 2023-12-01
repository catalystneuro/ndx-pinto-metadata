from datetime import datetime
from uuid import uuid4

from dateutil.tz import tzlocal
from hdmf.testing import TestCase, remove_test_file
from pynwb import NWBHDF5IO, NWBFile

from ndx_pinto_metadata import SubjectExtension


class TestLabMetaDataExtensionConstructor(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nwbfile = NWBFile(
            session_description="session_description",
            identifier=str(uuid4()),
            session_start_time=datetime(1970, 1, 1, tzinfo=tzlocal()),
        )

        cls.subject_metadata = dict(
            ear_tag_id="13005",
            zygosity="Homozygous",
            age="P7D",
            genotype="ChAT-Ai96",
            sex="M",
            species="Mus musculus",
            subject_id="DrChicken",
        )

        cls.nwbfile_path = "test.nwb"

    @classmethod
    def tearDownClass(cls):
        remove_test_file(cls.nwbfile_path)

    def test_constructor(self):
        self.nwbfile.subject = SubjectExtension(**self.subject_metadata)

        self.assertEqual(
            self.nwbfile.subject.ear_tag_id, self.subject_metadata["ear_tag_id"]
        )
        self.assertEqual(
            self.nwbfile.subject.zygosity, self.subject_metadata["zygosity"]
        )

    def test_roundtrip(self):
        with NWBHDF5IO(self.nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertIsInstance(read_nwbfile.subject, SubjectExtension)
            self.assertContainerEqual(
                read_nwbfile.subject,
                self.nwbfile.subject,
            )
