"""
A small script to generate the stimuli for the AV-SA test(s) in the ECoClass-VR DFG proposal.

@author: sfremerey
"""
import io
import json
import os
import random

def avsa_generate_ffmpeg_cmd(ffmpeg_call, background_image, video_list, time, vcodec, crf, pix_fmt, output_filename):
    ffmpeg_base_cmd_complex_fitlers = [
        """'[1:v]v360=equirect:equirect:yaw=0[out1];""",
        """[2:v]v360=equirect:equirect:yaw=18[out2];""",
        """[3:v]v360=equirect:equirect:yaw=36[out3];""",
        """[4:v]v360=equirect:equirect:yaw=54[out4];""",
        """[5:v]v360=equirect:equirect:yaw=72[out5];""",
        """[6:v]v360=equirect:equirect:yaw=90[out6];""",
        """[7:v]v360=equirect:equirect:yaw=108[out7];""",
        """[8:v]v360=equirect:equirect:yaw=126[out8];""",
        """[9:v]v360=equirect:equirect:yaw=144[out9];""",
        """[10:v]v360=equirect:equirect:yaw=162[out10];""",
        """[11:v]v360=equirect:equirect:yaw=180[out11];""",
        """[12:v]v360=equirect:equirect:yaw=-162[out12];""",
        """[13:v]v360=equirect:equirect:yaw=-144[out13];""",
        """[14:v]v360=equirect:equirect:yaw=-126[out14];""",
        """[15:v]v360=equirect:equirect:yaw=-108[out15];""",
        """[16:v]v360=equirect:equirect:yaw=-90[out16];""",
        """[17:v]v360=equirect:equirect:yaw=-72[out17];""",
        """[18:v]v360=equirect:equirect:yaw=-54[out18];""",
        """[19:v]v360=equirect:equirect:yaw=-36[out19];""",
        """[20:v]v360=equirect:equirect:yaw=-18[out20];""",
        """[0:v][out1]overlay[tmp1];""",
        """[tmp1][out2]overlay[tmp2];""",
        """[tmp2][out3]overlay[tmp3];""",
        """[tmp3][out4]overlay[tmp4];""",
        """[tmp4][out5]overlay[tmp5];""",
        """[tmp5][out6]overlay[tmp6];""",
        """[tmp6][out7]overlay[tmp7];""",
        """[tmp7][out8]overlay[tmp8];""",
        """[tmp8][out9]overlay[tmp9];""",
        """[tmp9][out10]overlay[tmp10];""",
        """[tmp10][out11]overlay[tmp11];""",
        """[tmp11][out12]overlay[tmp12];""",
        """[tmp12][out13]overlay[tmp13];""",
        """[tmp13][out14]overlay[tmp14];""",
        """[tmp14][out15]overlay[tmp15];""",
        """[tmp15][out16]overlay[tmp16];""",
        """[tmp16][out17]overlay[tmp17];""",
        """[tmp17][out18]overlay[tmp18];""",
        """[tmp18][out19]overlay[tmp19];""",
        """[tmp19][out20]overlay[out]'"""
    ]
    ffmpeg_base_cmd = ["{ffmpeg_call}",
                       "-framerate 29.97 -loop 1 -i {background_image}",
                       "-stream_loop 2 -i {video_1}",
                       "-stream_loop 2 -i {video_2}",
                       "-stream_loop 2 -i {video_3}",
                       "-stream_loop 2 -i {video_4}",
                       "-stream_loop 2 -i {video_5}",
                       "-stream_loop 2 -i {video_6}",
                       "-stream_loop 2 -i {video_7}",
                       "-stream_loop 2 -i {video_8}",
                       "-stream_loop 2 -i {video_9}",
                       "-stream_loop 2 -i {video_10}",
                       "-stream_loop 2 -i {video_11}",
                       "-stream_loop 2 -i {video_12}",
                       "-stream_loop 2 -i {video_13}",
                       "-stream_loop 2 -i {video_14}",
                       "-stream_loop 2 -i {video_15}",
                       "-stream_loop 2 -i {video_16}",
                       "-stream_loop 2 -i {video_17}",
                       "-stream_loop 2 -i {video_18}",
                       "-stream_loop 2 -i {video_19}",
                       "-stream_loop 2 -i {video_20}",
                       "-t {time} -filter_complex",
                       "".join(ffmpeg_base_cmd_complex_fitlers),
                       "-map '[out]:v'",
                       "-c:v {vcodec}",
                       "-crf {crf}",
                       "-pix_fmt {pix_fmt}",
                       "-an",
                       "-n",
                       "'{output_filename}'"
                       ]

    ffmpeg_cmd = " ".join(ffmpeg_base_cmd).format(ffmpeg_call=ffmpeg_call,
                                        background_image=background_image,
                                        video_1=video_list[0],
                                        video_2=video_list[1],
                                        video_3=video_list[2],
                                        video_4=video_list[3],
                                        video_5=video_list[4],
                                        video_6=video_list[5],
                                        video_7=video_list[6],
                                        video_8=video_list[7],
                                        video_9=video_list[8],
                                        video_10=video_list[9],
                                        video_11=video_list[10],
                                        video_12=video_list[11],
                                        video_13=video_list[12],
                                        video_14=video_list[13],
                                        video_15=video_list[14],
                                        video_16=video_list[15],
                                        video_17=video_list[16],
                                        video_18=video_list[17],
                                        video_19=video_list[18],
                                        video_20=video_list[19],
                                        time=time,
                                        vcodec=vcodec,
                                        crf=crf,
                                        pix_fmt=pix_fmt,
                                        output_filename=output_filename)
    return ffmpeg_cmd

def generate_and_write_hpc_tuil_lsf_file(subject, ffmpeg_cmds):
    f = io.open("ecoclass-vr_exp1_stimuligen_cmds_{}.lsf".format(subject), "w", newline='\n')
    f.write("""#!/bin/tcsh
#BSUB -q highmem
#BSUB -R "rusage[mem=270000] span[hosts=1]"
#BSUB -oo ecoclass-vr_exp1_stimuligen_cmds_{}.log
#BSUB -eo ecoclass-vr_exp1_stimuligen_cmds_{}.err
#BSUB -J ecoclassvr_{}
#BSUB -L /bin/tcsh
#BSUB -n 20

module purge
module load intel/python3
date
pwd
module purge

cd /usr/scratch4/stfr4066/projects/ECoClass-VR
""".format(subject, subject, subject))
    for ffmpeg_cmd in ffmpeg_cmds:
        f.write("{}\n".format(ffmpeg_cmd))

randomization = "random_generbalanced"  # random or random_generbalanced (gender balancing of active speakers) is supported
background_image = "input/classroom.jpg"
subjects = 30
max_parallel_speakers = 10
ffmpeg_call = "./ffmpeg"
vcodec = "libx265"
crf = "1"
pix_fmt = "yuv420p"
time = 120
training = True
possible_story_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
random.shuffle(possible_story_list)

if os.path.isfile("ecoclass-vr_exp1_stimuligen_cmds.sh"):
    os.remove("ecoclass-vr_exp1_stimuligen_cmds.sh")

if randomization == "random":
    for subject in range(1, subjects+1):
        if os.path.isfile("ecoclass-vr_chairs_speaker_story_mapping_{}.json".format(subject)):
            os.remove("ecoclass-vr_chairs_speaker_story_mapping_{}.json".format(subject))
        chairs_speaker_story_mapping = json.dumps({"chairs_speaker_story_mapping": []})
        ffmpeg_cmds = []
        for parallel_speakers in range(2, max_parallel_speakers+1):
            speaker_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
            possible_story_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            video_list = []
            random.shuffle(speaker_list)
            random.shuffle(possible_story_list)
            story_list = []
            for j in range(1, parallel_speakers+1):
                story_list.append(possible_story_list[0])
                del possible_story_list[0]
            while len(story_list) != 20:  # Add "silence" story until 20 "stories" are included in the array
                story_list.append(11)
            random.shuffle(speaker_list)
            random.shuffle(story_list)
            chairs_speaker_story_mapping_json_to_append = "{"
            for speaker_id in range(0, 20):
                video_list.append("input/{}_{}.mov".format(speaker_list[speaker_id], story_list[speaker_id]))
                if speaker_id < 19:
                    chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_'+str(speaker_id+1)+'":{"speaker": '+str(speaker_list[speaker_id])+', "story": '+str(story_list[speaker_id])+', "assigned_story": 11},'
                if speaker_id == 19:
                    chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_' + str(
                        speaker_id + 1) + '":{"speaker": ' + str(speaker_list[speaker_id]) + ', "story": ' + str(
                        story_list[speaker_id]) + ', "assigned_story": 11}}'
                    chairs_speaker_story_mapping_json = json.loads(chairs_speaker_story_mapping)
                    chairs_speaker_story_mapping_json["chairs_speaker_story_mapping"].append(json.loads(chairs_speaker_story_mapping_json_to_append))
                    chairs_speaker_story_mapping = json.dumps(chairs_speaker_story_mapping_json, indent=4)
            output_filename = "output/{}_{}.mp4".format(subject, parallel_speakers)
            ffmpeg_cmd = avsa_generate_ffmpeg_cmd(ffmpeg_call, background_image, video_list, time, vcodec, crf, pix_fmt, output_filename)
            ffmpeg_cmds.append(ffmpeg_cmd)
        jsonf = io.open("ecoclass-vr_chairs_speaker_story_mapping_{}.json".format(subject), "a")
        jsonf.write(chairs_speaker_story_mapping)

        if training:
            if os.path.isfile("ecoclass-vr_chairs_speaker_story_mapping_{}_training.json".format(subject)):
                os.remove("ecoclass-vr_chairs_speaker_story_mapping_{}_training.json".format(subject))
            chairs_speaker_story_mapping = json.dumps({"chairs_speaker_story_mapping": []})
            for parallel_speakers in [1, 2, 5, 10]:
                speaker_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
                possible_story_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                video_list = []
                random.shuffle(speaker_list)
                random.shuffle(possible_story_list)
                story_list = []
                for j in range(1, parallel_speakers + 1):
                    story_list.append(possible_story_list[0])
                    del possible_story_list[0]
                while len(story_list) != 20:  # Add "silence" story until 20 "stories" are included in the array
                    story_list.append(11)
                random.shuffle(speaker_list)
                random.shuffle(story_list)
                chairs_speaker_story_mapping_json_to_append = "{"
                for speaker_id in range(0, 20):
                    video_list.append("input/{}_{}.mov".format(speaker_list[speaker_id], story_list[speaker_id]))
                    if speaker_id < 19:
                        chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_' + str(
                            speaker_id + 1) + '":{"speaker": ' + str(speaker_list[speaker_id]) + ', "story": ' + str(
                            story_list[speaker_id]) + ', "assigned_story": 11},'
                        chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_' + str(
                            speaker_id + 1) + '":{"speaker": ' + str(speaker_list[speaker_id]) + ', "story": ' + str(
                            story_list[speaker_id]) + ', "assigned_story": 11},'
                    if speaker_id == 19:
                        chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_' + str(
                            speaker_id + 1) + '":{"speaker": ' + str(speaker_list[speaker_id]) + ', "story": ' + str(
                            story_list[speaker_id]) + ', "assigned_story": 11}}'
                        chairs_speaker_story_mapping_json = json.loads(chairs_speaker_story_mapping)
                        chairs_speaker_story_mapping_json["chairs_speaker_story_mapping"].append(
                            json.loads(chairs_speaker_story_mapping_json_to_append))
                        chairs_speaker_story_mapping = json.dumps(chairs_speaker_story_mapping_json, indent=4)
                output_filename = "output/{}_{}_training.mp4".format(subject, parallel_speakers)
                ffmpeg_cmd = avsa_generate_ffmpeg_cmd(ffmpeg_call, background_image, video_list, time, vcodec, crf, pix_fmt,
                                                      output_filename)
                ffmpeg_cmds.append(ffmpeg_cmd)
            jsonf = io.open("ecoclass-vr_chairs_speaker_story_mapping_{}_training.json".format(subject), "a")
            jsonf.write(chairs_speaker_story_mapping)
        generate_and_write_hpc_tuil_lsf_file(subject, ffmpeg_cmds)
        sshfile = io.open("ecoclass-vr_exp1_stimuligen_cmds.sh", "a")
        for ffmpeg_cmd in ffmpeg_cmds:
            sshfile.write("{}\n".format(ffmpeg_cmd))

elif randomization == "random_generbalanced":
    for subject in range(1, subjects+1):
        if os.path.isfile("ecoclass-vr_chairs_speaker_story_mapping_{}.json".format(subject)):
            os.remove("ecoclass-vr_chairs_speaker_story_mapping_{}.json".format(subject))
        chairs_speaker_story_mapping = json.dumps({"chairs_speaker_story_mapping": []})
        ffmpeg_cmds = []
        for parallel_speakers in range(2, max_parallel_speakers+1):
            speaker_list = []
            male_speakers = [1, 4, 7, 8, 9, 12, 16, 18, 19, 20]
            female_speakers = [2, 3, 5, 6, 10, 11, 13, 14, 15, 17]
            random.shuffle(male_speakers)
            random.shuffle(female_speakers)
            male_counter = 0
            female_counter = 0
            possible_story_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            random.shuffle(possible_story_list)
            for speaker_no in range(1, parallel_speakers+1):
                male_female_random = random.choice([1, 2])
                diff_male_female = male_counter - female_counter
                if diff_male_female == 0:  # case for both genders equally covered
                    if male_female_random == 1:  # Random male
                        random.shuffle(male_speakers)
                        speaker_list.append(male_speakers[0])
                        del male_speakers[0]
                        male_counter += 1
                    elif male_female_random == 2:  # Random female
                        random.shuffle(female_speakers)
                        speaker_list.append(female_speakers[0])
                        del female_speakers[0]
                        female_counter += 1
                elif diff_male_female > 0:  # case for more male than female
                    random.shuffle(female_speakers)
                    speaker_list.append(female_speakers[0])
                    del female_speakers[0]
                    female_counter += 1
                elif diff_male_female < 0:  # case for more female than male
                    random.shuffle(male_speakers)
                    speaker_list.append(male_speakers[0])
                    del male_speakers[0]
                    male_counter += 1
            video_list = []
            story_list = []
            for j in range(1, parallel_speakers+1):
                story_list.append(possible_story_list[0])
                del possible_story_list[0]
            while len(story_list) != 20:  # Add "silence" story until 20 "stories" are included in the array
                story_list.append(11)
                try:
                    speaker_list.append(male_speakers[0])
                    del male_speakers[0]
                except IndexError:
                    speaker_list.append(female_speakers[0])
                    del female_speakers[0]

            # Shuffle both lists again, but in the same order (important!)
            temp = list(zip(speaker_list, story_list))
            random.shuffle(temp)
            speaker_list_final, story_list_final = zip(*temp)
            # res1 and res2 come out as tuples, and so must be converted to lists.
            speaker_list_final, story_list_final = list(speaker_list_final), list(story_list_final)

            chairs_speaker_story_mapping_json_to_append = "{"
            for speaker_id in range(0, 20):
                video_list.append("input/{}_{}.mov".format(speaker_list_final[speaker_id], story_list_final[speaker_id]))
                if speaker_id < 19:
                    chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_'+str(speaker_id+1)+'":{"speaker": '+str(speaker_list_final[speaker_id])+', "story": '+str(story_list_final[speaker_id])+', "assigned_story": 11},'
                if speaker_id == 19:
                    chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_' + str(
                        speaker_id + 1) + '":{"speaker": ' + str(speaker_list_final[speaker_id]) + ', "story": ' + str(
                        story_list_final[speaker_id]) + ', "assigned_story": 11}}'
                    chairs_speaker_story_mapping_json = json.loads(chairs_speaker_story_mapping)
                    chairs_speaker_story_mapping_json["chairs_speaker_story_mapping"].append(json.loads(chairs_speaker_story_mapping_json_to_append))
                    chairs_speaker_story_mapping = json.dumps(chairs_speaker_story_mapping_json, indent=4)
            output_filename = "output/{}_{}.mp4".format(subject, parallel_speakers)
            ffmpeg_cmd = avsa_generate_ffmpeg_cmd(ffmpeg_call, background_image, video_list, time, vcodec, crf, pix_fmt, output_filename)
            ffmpeg_cmds.append(ffmpeg_cmd)
        jsonf = io.open("ecoclass-vr_chairs_speaker_story_mapping_{}.json".format(subject), "a")
        jsonf.write(chairs_speaker_story_mapping)

        if training:
            if os.path.isfile("ecoclass-vr_chairs_speaker_story_mapping_{}_training.json".format(subject)):
                os.remove("ecoclass-vr_chairs_speaker_story_mapping_{}_training.json".format(subject))
            chairs_speaker_story_mapping = json.dumps({"chairs_speaker_story_mapping": []})
            for parallel_speakers in [1, 2, 5, 10]:
                speaker_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
                possible_story_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                video_list = []
                random.shuffle(speaker_list)
                random.shuffle(possible_story_list)
                story_list = []
                for j in range(1, parallel_speakers + 1):
                    story_list.append(possible_story_list[0])
                    del possible_story_list[0]
                while len(story_list) != 20:  # Add "silence" story until 20 "stories" are included in the array
                    story_list.append(11)
                random.shuffle(speaker_list)
                random.shuffle(story_list)
                chairs_speaker_story_mapping_json_to_append = "{"
                for speaker_id in range(0, 20):
                    video_list.append("input/{}_{}.mov".format(speaker_list[speaker_id], story_list[speaker_id]))
                    if speaker_id < 19:
                        chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_' + str(
                            speaker_id + 1) + '":{"speaker": ' + str(speaker_list[speaker_id]) + ', "story": ' + str(
                            story_list[speaker_id]) + ', "assigned_story": 11},'
                        chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_' + str(
                            speaker_id + 1) + '":{"speaker": ' + str(speaker_list[speaker_id]) + ', "story": ' + str(
                            story_list[speaker_id]) + ', "assigned_story": 11},'
                    if speaker_id == 19:
                        chairs_speaker_story_mapping_json_to_append = chairs_speaker_story_mapping_json_to_append + '"chair_' + str(
                            speaker_id + 1) + '":{"speaker": ' + str(speaker_list[speaker_id]) + ', "story": ' + str(
                            story_list[speaker_id]) + ', "assigned_story": 11}}'
                        chairs_speaker_story_mapping_json = json.loads(chairs_speaker_story_mapping)
                        chairs_speaker_story_mapping_json["chairs_speaker_story_mapping"].append(
                            json.loads(chairs_speaker_story_mapping_json_to_append))
                        chairs_speaker_story_mapping = json.dumps(chairs_speaker_story_mapping_json, indent=4)
                output_filename = "output/{}_{}_training.mp4".format(subject, parallel_speakers)
                ffmpeg_cmd = avsa_generate_ffmpeg_cmd(ffmpeg_call, background_image, video_list, time, vcodec, crf, pix_fmt,
                                                      output_filename)
                ffmpeg_cmds.append(ffmpeg_cmd)
            jsonf = io.open("ecoclass-vr_chairs_speaker_story_mapping_{}_training.json".format(subject), "a")
            jsonf.write(chairs_speaker_story_mapping)
        generate_and_write_hpc_tuil_lsf_file(subject, ffmpeg_cmds)
        sshfile = io.open("ecoclass-vr_exp1_stimuligen_cmds.sh", "a")
        for ffmpeg_cmd in ffmpeg_cmds:
            sshfile.write("{}\n".format(ffmpeg_cmd))
