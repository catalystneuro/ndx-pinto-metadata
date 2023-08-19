# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec


def main():
    ns_builder = NWBNamespaceBuilder(
        doc="type for storing metadata for Pinto lab",
        name="ndx-pinto-metadata",
        version="0.1.0",
        author=["Szonja Weigl", "Ben Dichter"],
        contact=["ben.dichter@catalystneuro.com"],
    )

    ns_builder.include_type("LabMetaData", namespace="core")
    ns_builder.include_type("DynamicTable", namespace="core")

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
        dtype="int",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="advance",
        doc="ViRMEN configuration parameter.",
        dtype="int",
        required=False,
    )

    lab_meta_data_extension.add_attribute(
        name="squal",
        doc="ViRMEN configuration parameter.",
        dtype="float",
        required=False,
    )

    stimulus_protocol_extension = NWBGroupSpec(
        doc="type for storing stimulus protocol metadata",
        neurodata_type_def="StimulusProtocolExtension",
        neurodata_type_inc="LabMetaData",
    )

    stimulus_protocol_extension.add_attribute(
        name="num_mazes_in_protocol",
        doc="The number of mazes for this stimulus protocol.",
        dtype="int",
        required=False,
    )

    stimulus_protocol_extension.add_attribute(
        name="trial_draw",
        doc="The name of trial draw.",  # TODO confirm what "trialDraw" means
        dtype="text",
        required=False,
    )

    stimulus_protocol_extension.add_attribute(
        name="stimulus_draw",
        doc="The name of stimulus draw.",  # TODO confirm what "stimDraw" means
        dtype="text",
        required=False,
    )

    stimulus_protocol_extension.add_attribute(
        name="cue_shown",
        doc="Indicates whether cue was shown for this stimulus protocol.",  # TODO confirm "0" is no cue, "1" is cue
        dtype="int",
        required=False,
    )

    stimulus_protocol_extension.add_attribute(
        name="cue_min_separation",
        doc="The minimum time in ms between the cues.",  # TODO confirm in ms (e.g. 12)
        dtype="int",
        required=False,
    )

    stimulus_protocol_extension.add_attribute(
        name="trial_repeat_probability",
        doc="The probability of repeated trials.",  # TODO confirm
        dtype="float",
        required=False,
    )

    stimulus_protocol_extension.add_attribute(
        name="num_repeat_trials",
        doc="The number of repeated trials.",  # TODO confirm
        dtype="int",
        required=False,
    )

    stimulus_protocol_extension.add_dataset(
        name="visual_color",
        doc="no description",  # TODO confirm
        dtype="int",
        shape=(None,),
        quantity="?",
    )

    stimulus_protocol_extension.add_dataset(
        name="memory_color",
        doc="no description",  # TODO confirm
        dtype="float",
        shape=(None,),
        quantity="?",
    )

    stimulus_protocol_extension.add_dataset(
        name="mask_color",
        doc="no description",  # TODO confirm
        dtype="float",
        shape=(None,),
        quantity="?",
    )

    stimulus_protocol_extension.add_dataset(
        name="color1",
        doc="no description",  # TODO confirm
        dtype="uint8",
        shape=(None,),
        quantity="?",
    )

    stimulus_protocol_extension.add_dataset(
        name="color2",
        doc="no description",  # TODO confirm
        dtype="uint8",
        shape=(None,),
        quantity="?",
    )

    stimulus_protocol_extension.add_attribute(
        name="is_princeton_implementation",
        doc="Indicates whether uses Princeton implementation.",  # TODO confirm
        dtype="int",
        required=False,
    )

    stimulus_protocol_extension.add_attribute(
        name="hTrim",
        doc="no description",  # TODO confirm
        dtype="float",
        required=False,
    )

    for attr in [
        "hWidth",
        "wHeight",
        "mHeight",
        "towerHeight",
        "R",
        "armLength",
        "rzLength",
        "trialEndPauseDuration",
        "interTrialCorrectDuration",
        "interTrialWrongDuration",
        "targetNumTrials",
        "panSessionTrials",
        "rewardFraction",
        "antiFraction",
    ]:
        stimulus_protocol_extension.add_attribute(
            name=attr,
            doc="Stimulus protocol parameter.",  # TODO confirm
            dtype="int",
            required=False,
        )

    lab_meta_data_extension.add_group(
        name="stimulus_protocol",
        neurodata_type_inc="StimulusProtocolExtension",
        doc="type for storing stimulus protocol",
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

    new_data_types = [
        lab_meta_data_extension,
        maze_extension,
        stimulus_protocol_extension,
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
