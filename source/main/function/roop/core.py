1  #!/usr/bin/env python3

import os, random
import sys
import gc
from time import sleep
from flask import jsonify
import mysql.connector

db = mysql.connector.connect(
    host="localhost", user="sonpro", password="Ratiendi89", database="FutureLove4"
)

# single thread doubles cuda performance - needs to be set before torch import
if any(arg.startswith("--execution-provider") for arg in sys.argv):
    os.environ["OMP_NUM_THREADS"] = "1"
# reduce tensorflow log level
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import warnings
from typing import List
import platform
import signal
import shutil
import torch
import argparse
import onnxruntime
import tensorflow
from source.main.function import roop
from source.main.function.roop.predictor import predict_image, predict_video
from source.main.function.roop.frame.core import get_frame_processors_modules
from source.main.function.roop.utilities import (
    has_image_extension,
    is_image,
    is_video,
    detect_fps,
    create_video,
    extract_frames,
    get_temp_frame_paths,
    restore_audio,
    create_temp,
    move_temp,
    clean_temp,
    normalize_output_path,
)

warnings.filterwarnings("ignore", category=FutureWarning, module="insightface")
warnings.filterwarnings("ignore", category=UserWarning, module="torchvision")



def parse_args() -> None:
    program = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=100)
    )
    # signal.signal(signal.SIGINT, lambda signal_number, frame: destroy())
    program.add_argument(
        "-s",
        "--source",
        default="./roop/src.jpg",
        help="select an source image",
        dest="source_path",
    )
    program.add_argument(
        "-t",
        "--target",
        default="./roop/tar.jpg",
        help="select an target image or video",
        dest="target_path",
    )
    program.add_argument(
        "-o",
        "--output",
        default="./output/output.jpg",
        help="select output file or directory",
        dest="output_path",
    )
    program.add_argument(
        "--frame-processor",
        help="frame processors (choices: face_swapper, face_enhancer, ...)",
        dest="frame_processor",
        default=["face_swapper"],
        nargs="+",
    )
    program.add_argument(
        "--keep-fps", help="keep target fps", dest="keep_fps", action="store_true"
    )
    program.add_argument(
        "--keep-frames",
        help="keep temporary frames",
        dest="keep_frames",
        action="store_true",
    )
    program.add_argument(
        "--skip-audio", help="skip target audio", dest="skip_audio", action="store_true"
    )
    program.add_argument(
        "--many-faces",
        help="process every face",
        dest="many_faces",
        action="store_true",
    )
    program.add_argument(
        "--reference-face-position",
        help="position of the reference face",
        dest="reference_face_position",
        type=int,
        default=0,
    )
    program.add_argument(
        "--reference-frame-number",
        help="number of the reference frame",
        dest="reference_frame_number",
        type=int,
        default=0,
    )
    program.add_argument(
        "--similar-face-distance",
        help="face distance used for recognition",
        dest="similar_face_distance",
        type=float,
        default=0.85,
    )
    program.add_argument(
        "--temp-frame-format",
        help="image format used for frame extraction",
        dest="temp_frame_format",
        default="png",
        choices=["jpg", "png"],
    )
    program.add_argument(
        "--temp-frame-quality",
        help="image quality used for frame extraction",
        dest="temp_frame_quality",
        type=int,
        default=0,
        choices=range(101),
        metavar="[0-100]",
    )
    program.add_argument(
        "--output-video-encoder",
        help="encoder used for the output video",
        dest="output_video_encoder",
        default="libx264",
        choices=["libx264", "libx265", "libvpx-vp9", "h264_nvenc", "hevc_nvenc"],
    )
    program.add_argument(
        "--output-video-quality",
        help="quality used for the output video",
        dest="output_video_quality",
        type=int,
        default=35,
        choices=range(101),
        metavar="[0-100]",
    )
    program.add_argument(
        "--max-memory", help="maximum amount of RAM in GB", dest="max_memory", type=int
    )
    program.add_argument(
        "--execution-provider",
        help="available execution provider (choices: cpu, cuda, ...)",
        dest="execution_provider",
        default=["cuda"],
        choices=suggest_execution_providers(),
        nargs="+",
    )
    program.add_argument(
        "--execution-threads",
        help="number of execution threads",
        dest="execution_threads",
        type=int,
        default=suggest_execution_threads(),
    )
    program.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{roop.metadata.name} {roop.metadata.version}",
    )

    args = program.parse_args()

    roop.globals.source_path = args.source_path
    roop.globals.target_path = args.target_path
    roop.globals.output_path = normalize_output_path(
        roop.globals.source_path, roop.globals.target_path, args.output_path
    )
    roop.globals.headless = (
        roop.globals.source_path is not None
        and roop.globals.target_path is not None
        and roop.globals.output_path is not None
    )
    roop.globals.frame_processors = args.frame_processor
    roop.globals.keep_fps = args.keep_fps
    roop.globals.keep_frames = args.keep_frames
    roop.globals.skip_audio = args.skip_audio
    roop.globals.many_faces = args.many_faces
    roop.globals.reference_face_position = args.reference_face_position
    roop.globals.reference_frame_number = args.reference_frame_number
    roop.globals.similar_face_distance = args.similar_face_distance
    roop.globals.temp_frame_format = args.temp_frame_format
    roop.globals.temp_frame_quality = args.temp_frame_quality
    roop.globals.output_video_encoder = args.output_video_encoder
    roop.globals.output_video_quality = args.output_video_quality
    roop.globals.max_memory = args.max_memory
    roop.globals.execution_providers = decode_execution_providers(
        args.execution_provider
    )
    roop.globals.execution_threads = args.execution_threads

    print("_____args.max_memory________" + str(args.max_memory))


def encode_execution_providers(execution_providers: List[str]) -> List[str]:
    return [
        execution_provider.replace("ExecutionProvider", "").lower()
        for execution_provider in execution_providers
    ]


def decode_execution_providers(execution_providers: List[str]) -> List[str]:
    return [
        provider
        for provider, encoded_execution_provider in zip(
            onnxruntime.get_available_providers(),
            encode_execution_providers(onnxruntime.get_available_providers()),
        )
        if any(
            execution_provider in encoded_execution_provider
            for execution_provider in execution_providers
        )
    ]


def suggest_execution_providers() -> List[str]:
    return encode_execution_providers(onnxruntime.get_available_providers())


def suggest_execution_threads() -> int:
    if "CUDAExecutionProvider" in onnxruntime.get_available_providers():
        return 4
    return 1


def limit_resources() -> None:
    gpus = tensorflow.config.experimental.list_physical_devices("GPU")
    for gpu in gpus:
        print("_____GPU FOR:____" + str(gpu))
        tensorflow.config.experimental.set_virtual_device_configuration(
            gpu,
            [
                tensorflow.config.experimental.VirtualDeviceConfiguration(
                    memory_limit=1024
                )
            ],
        )
    # limit memory usage
    if roop.globals.max_memory:
        print("roop.globals.max_memory____" + str(roop.globals.max_memory))
        memory = roop.globals.max_memory * 1024**3
        if platform.system().lower() == "darwin":
            memory = roop.globals.max_memory * 1024**6
            print("____roop.globals.max_memory * 1024**6____" + str(memory))
        if platform.system().lower() == "windows":
            import ctypes

            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            kernel32.SetProcessWorkingSetSize(
                -1, ctypes.c_size_t(memory), ctypes.c_size_t(memory)
            )
            print("____ctypes.windll.kernel32____" + str(kernel32))
        else:
            import resource

            resource.setrlimit(resource.RLIMIT_DATA, (memory, memory))


def update_status(message: str, scope: str = "ROOP.CORE") -> None:
    print(f"[{scope}] {message}")


def release_resources() -> None:
    if "CUDAExecutionProvider" in roop.globals.execution_providers:
        torch.cuda.empty_cache()


def start(src_path, target_path, output):
    try:
        print(src_path, target_path, output)
        gc.collect()

        torch.cuda.empty_cache()
        # for frame_processor in get_frame_processors_modules(roop.globals.frame_processors):
        #     if not frame_processor.pre_start():
        #         return
        # process image to image
        # roop.globals.decode_execution_providers(["cuda"])
        # process frame
        print("_______________________sang phan chon decoder____ " + target_path)
        for frame_processor in get_frame_processors_modules(
            roop.globals.frame_processors
        ):
            update_status("Progressing...", frame_processor.NAME)
            frame_processor.process_image(src_path, target_path, output)
            print("Error here")
            frame_processor.post_process()
            # validate image
            update_status("Processing to image succeed!")
            if is_image(output):  # Sửa lỗi logic ở đây
                update_status("Processing to image succeed!")
            else:
                update_status("Processing to image failed!")
        torch.cuda.empty_cache()
        gc.collect()
    except Exception as e:
        print(e)
        return jsonify({"message": f"Error {e}", "status": 500})


def swapvid(src_path, vid_path, output):
    gc.collect()

    torch.cuda.empty_cache()
    # process image to videos
    # roop.globals.execution_providers = decode_execution_providers(["cuda"])

    # torch.cuda.empty_cache()
    print("_______________________________vid_path___CUA_____swapvid__" + str(vid_path))
    temp_path = extract_frames(vid_path)

    temp_frame_paths = get_temp_frame_paths(temp_path[0])
    # print("____temp_frame_paths____" + str(temp_frame_paths))
    for frame_processor in get_frame_processors_modules(roop.globals.frame_processors):
        frame_processor.process_video(src_path, temp_frame_paths)
        frame_processor.post_process()
        # release_resources()
        torch.cuda.empty_cache()
        gc.collect()

    # handles fps
    if roop.globals.keep_fps:
        update_status("Detecting fps...")
        fps = detect_fps(temp_path[0])
        update_status(f"Creating video with {fps} fps...")
        create_video(temp_path[0], fps)
    else:
        update_status("Creating video with 30.0 fps...")
        create_video(temp_path[0])
    print(roop.globals.skip_audio)
    # handle audio
    # if roop.globals.skip_audio:
    #     move_temp(temp_path[0], output)
    #     update_status("Skipping audio...")
    # else:
    #     if roop.globals.keep_fps:
    #         update_status("Restoring audio...")
    #     else:
    #         update_status("Restoring audio might cause issues as fps are not kept...")

    restore_audio(vid_path, temp_path[0], output)
    # print(temp_path[0])
    clean_temp(temp_path[0])

    torch.cuda.empty_cache()
    gc.collect()

    if is_video(output):
        update_status("Processing to video succeed!")
    else:
        update_status("Processing to video failed!")


def is_folder_empty(folder_path):
    if not os.path.exists(folder_path):
        return True
    return len(os.listdir(folder_path)) == 0


def run(src_path, target_path, output):
    try:
        print("____CHAY_PHAN_SWAP_ANH___")
        # code viet update
        print(f"______Source Path______: {src_path}")
        print(f"______Target Path_____: {target_path}")
        print(f"______Output______: {output}")
        parse_args()
        limit_resources()
        start(src_path, target_path, output)
    except Exception as e:
        print(f"Error at run function: {e}")


def runvid(src_path, vid_path, output):
    try:
        parse_args()
        limit_resources()
        if db.is_connected():
            cur = db.cursor()
            cur.execute("SELECT * FROM status WHERE id = 1")
            turn = cur.fetchall()
            while True:
                if turn[0][1] == 1:
                    mycur = db.cursor()
                    mycur.execute("UPDATE status SET turn = 0 WHERE status.id = 1")
                    db.commit()
                    swapvid(src_path, vid_path, output)
                    mycur.execute("UPDATE status SET turn = 1 WHERE status.id = 1")
                    db.commit()
                    mycur.close()
                    cur.close()
                    break
                else:
                    sleep(5)
        else:
            swapvid(src_path, vid_path, output)
    except Exception as e:
        print(e)
    finally:
        newcur = db.cursor()
        newcur.execute("UPDATE status SET turn = 1 WHERE status.id = 1")
        db.commit()
        newcur.close()
