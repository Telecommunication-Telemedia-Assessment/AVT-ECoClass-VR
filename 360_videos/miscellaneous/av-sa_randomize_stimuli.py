"""
A script to randomize the stimuli for the AV-SA test(s) in the ECoClass-VR DFG proposal
AFTER creating them with the corresponding script.

@author: sfremerey
"""
import json
import random
import itertools
import os


# Function to load JSON file
def load_json(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)


# Function to save JSON to file
def save_json(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


# Shuffle the chairs_speaker_story_mapping array
def shuffle_chairs_data(data):
    for item in data:
        random.shuffle(item)


# Function to merge files
def merge_json_files():
    for subject_number in range(1, 31):
        training_videos_list = ["{}_1_training", "{}_2_training", "{}_5_training", "{}_10_training"]
        formatted_training_videos_list = [video.format(subject_number) for video in training_videos_list]
        test_videos_list = ["{}_2", "{}_3", "{}_4", "{}_5", "{}_6", "{}_7", "{}_8", "{}_9", "{}_10"]
        formatted_test_videos_list = [video.format(subject_number) for video in test_videos_list]

        training_file = "cmds_used/ecoclass-vr_chairs_speaker_story_mapping_{}_training.json".format(subject_number)
        training_data = load_json(training_file)['chairs_speaker_story_mapping']

        non_training_file = "cmds_used/ecoclass-vr_chairs_speaker_story_mapping_{}.json".format(subject_number)
        non_training_data = load_json(non_training_file)['chairs_speaker_story_mapping'][:]

        combined_videos_list = list(zip(formatted_test_videos_list, non_training_data[:]))
        random.shuffle(combined_videos_list)
        formatted_test_videos_list_shuffled, non_training_data_shuffled = zip(*combined_videos_list)
        formatted_test_videos_list_shuffled, non_training_data_shuffled = list(formatted_test_videos_list_shuffled), list(non_training_data_shuffled)
        merged_data = training_data + non_training_data_shuffled
        save_json("ecoclass-vr_chairs_speaker_story_mapping_{}.json".format(subject_number),
                  {"chairs_speaker_story_mapping": merged_data})
        # Create playlist file with shuffled non-training file order
        playlist = {
            "label": "{}".format(subject_number),
            "videos": []
        }
        scene_id = 1
        for video in formatted_training_videos_list:
            playlist["videos"].append({"scene_id": scene_id, "filename": video})
            scene_id += 1
        for video in formatted_test_videos_list_shuffled:
            playlist["videos"].append({"scene_id": scene_id, "filename": video})
            scene_id += 1
        save_json("{}.json".format(subject_number), playlist)

merge_json_files()
