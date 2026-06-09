import sys

from wav_format import *

EXTENSIONS = ['.wav', '.mp3']


def get_extension(file_path):
    len_file = len(file_path.split('.'))

    return '.' + file_path.split('.')[len_file - 1]


def check_extension(file_path):
    if not (get_extension(file_path) in EXTENSIONS):
        print("Error: invalid file format")
        return False

    return True


def reading_wav_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(44)
            data = file.read()
    except FileNotFoundError:
        print("Error: no such file or directory")

    return header, data


def crop_audio(file_path, start_time, end_time, extension):
    if extension == '.wav':
        header, data = reading_wav_file(file_path)
        wav_audio = WavAudio(header, data)
        wav_audio.crop_wav_audio(file_path, start_time, end_time)


def split_audio(file_path, split_time, extension):
    if extension == '.wav':
        header, data = reading_wav_file(file_path)
        wav_audio = WavAudio(header, data)
        wav_audio.split_wav_audio(file_path, split_time)


def speed_audio(file_path, speed, extension):
    if extension == '.wav':
        header, data = reading_wav_file(file_path)
        wav_audio = WavAudio(header, data)
        wav_audio.speed_wav_audio(file_path, speed)


def merge_audio(first_file_path, second_file_path, extension):
    if extension == '.wav':
        first_header, first_data = reading_wav_file(first_file_path)
        first_wav_audio = WavAudio(first_header, first_data)
        second_header, second_data = reading_wav_file(second_file_path)
        second_wav_audio = WavAudio(second_header, second_data)
        first_wav_audio.merge_wav_audio(first_file_path, second_wav_audio)


def crop_parameters(index):
    if len(sys.argv) < index + 2:
        start_time = int(input("Enter start time: "))
        end_time = int(input("Enter end time: "))
    else:
        start_time = int(sys.argv[index])
        end_time = int(sys.argv[index + 1])

    return start_time, end_time


def split_parameters(index):
    if len(sys.argv) < index + 1:
        split_time = int(input("Enter split time: "))
    else:
        split_time = int(sys.argv[index])

    return split_time


def speed_parameters(index):
    if len(sys.argv) < index + 1:
        speed = input("Enter playback speed: ")
    else:
        speed = int(sys.argv[index])

    return speed


def merge_parameters(index):
    if len(sys.argv) < index + 1:
        second_file_path = input("Enter path to second file: ")
    else:
        second_file_path = sys.argv[index]

    return second_file_path


def reading_file_path(index):
    if len(sys.argv) < index + 1:
        file_path = input("Enter path to file: ")
    else:
        file_path = sys.argv[index]

    return file_path


def result_func(index):
    is_stop = False

    while not is_stop:
        user_input = input()

        if user_input == 'stop':
            print("The program was stopped by the user")
            is_stop = True

        elif user_input == 'crop':
            start_time, end_time = crop_parameters(index)
            extension = get_extension(path_to_file)
            crop_audio(path_to_file, start_time, end_time, extension)
            index += 2

        elif user_input == 'split':
            split_time = split_parameters(index)
            extension = get_extension(path_to_file)
            split_audio(path_to_file, split_time, extension)
            index += 1

        elif user_input == 'speed':
            speed = speed_parameters(index)
            extension = get_extension(path_to_file)
            speed_audio(path_to_file, speed, extension)
            index += 1

        elif user_input == 'merge':
            first_file_path = path_to_file
            second_file_path = merge_parameters(index)

            if check_extension(second_file_path):
                extension = get_extension(first_file_path)
                merge_audio(first_file_path, second_file_path, extension)
                index += 1
        else:
            print("Error: non-existent editing type")


if __name__ == "__main__":
    try:
        attempt = 1
        path_to_file = reading_file_path(attempt)

        while not check_extension(path_to_file):
            path_to_file = reading_file_path(attempt)
            attempt += 1

        result_func(attempt)

    except KeyboardInterrupt:
        sys.exit()
