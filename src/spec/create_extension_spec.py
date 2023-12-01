# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec


def main():
    ns_builder = NWBNamespaceBuilder(
        doc="type for storing metadata for Pinto lab",
        name="ndx-pinto-metadata",
        version="0.1.2",
        author=["Szonja Weigl", "Ben Dichter"],
        contact=["ben.dichter@catalystneuro.com"],
    )

    ns_builder.include_type("LabMetaData", namespace="core")
    ns_builder.include_type("DynamicTable", namespace="core")
    ns_builder.include_type("Subject", namespace="core")

    lab_meta_data_extension = NWBGroupSpec(
        doc="type for storing metadata for Pinto lab",
        neurodata_type_def="LabMetaDataExtension",
        neurodata_type_inc="LabMetaData",
    )

    lab_meta_data_extension.add_attribute(
        name="experiment_name",
        doc="The name of experiment run in ViRMEN.",
        dtype="text",
    )

    lab_meta_data_extension.add_attribute(
        name="experiment_code",
        doc="The name of the code of experiment run in ViRMEN.",
        dtype="text",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="session_index",
        doc="The index of session.",
        dtype="int",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="total_reward",
        doc="The total reward in milliliters.",
        dtype="float",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="rig",
        doc="The name of the rig",
        dtype="text",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="num_trials",
        doc="The number of total trials for this session.",
        dtype="int",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="num_iterations",
        doc="The number of ViRMEN iterations for this session.",
        dtype="int",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="session_duration",
        doc="The duration of session in seconds.",
        dtype="float",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="advance",
        doc="Defines whether the overall performance of the animal in the current session has met learning criteria to advance to the next maze.",
        dtype="int",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="surface_quality",
        doc="Defines the surface quality of the treadmill. Metric for the quality of the displacement readings.",
        dtype="float",
        required=False,
    )

    maze_extension = NWBGroupSpec(
        doc="type for storing maze information",
        neurodata_type_def="MazeExtension",
        neurodata_type_inc="DynamicTable",
    )

    lab_meta_data_extension.add_group(
        name="mazes",
        neurodata_type_inc="MazeExtension",
        doc="type for storing maze information",
    )

    lab_meta_data_extension.add_group(
        name="stimulus_protocol",
        neurodata_type_inc="DynamicTable",
        doc="type for storing stimulus protocol information that varies from task to task",
        quantity="?",
    )

    subject_extension = NWBGroupSpec(
        doc="type for subject metadata for Pinto lab",
        neurodata_type_def="SubjectExtension",
        neurodata_type_inc="Subject",
    )
    subject_extension.add_attribute(
        name="zygosity",
        doc="The zygosity of the subject.",
        dtype="text",
        required=False,
    )
    subject_extension.add_attribute(
        name="ear_tag_id",
        doc="The text identification of the ear tag.",
        dtype="text",
        required=False,
    )

    new_data_types = [
        lab_meta_data_extension,
        maze_extension,
        subject_extension,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "spec")
    )
    export_spec(ns_builder, new_data_types, output_dir)
    print(
        "Spec files generated. Please make sure to rerun `pip install .` to load the changes."
    )


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
