import struct


class WavAudio:
    def __init__(self, header, data):
        self.header = header
        self.data = data
        self.chunk_size = struct.unpack('I', self.header[4:8])[0]
        self.num_channels = struct.unpack('H', self.header[22:24])[0]
        self.sample_rate = struct.unpack('I', self.header[24:28])[0]
        self.bits_per_sample = struct.unpack('H', self.header[34:36])[0] / 8
        self.sub_chunk_size = struct.unpack('I', self.header[40:44])[0]

    def crop_wav_audio(self, file_path, start_time, end_time):
        start_position = int(start_time * self.num_channels * self.sample_rate
                             * self.bits_per_sample + 44)
        end_position = int(end_time * self.num_channels * self.sample_rate
                           * self.bits_per_sample + 44)

        self.data = self.data[start_position:end_position]
        self.chunk_size = struct.pack('I', len(self.data) + 36)
        self.sub_chunk_size = struct.pack('I', len(self.data))
        self.header = (self.header[:4] + self.chunk_size + self.header[8:40]
                       + self.sub_chunk_size)
        writing_wav_file(file_path, self.header, self.data)

        print(f'File was successfully cropped and saved.')

    def split_wav_audio(self, file_path, split_time):
        split_position = int(split_time * self.num_channels * self.sample_rate
                             * self.bits_per_sample + 44)

        first_data = self.data[:split_position]
        first_chunk_size = struct.pack('I', len(first_data) + 36)
        first_sub_chunk_size = struct.pack('I', len(first_data))
        first_header = (self.header[:4] + first_chunk_size + self.header[8:40]
                        + first_sub_chunk_size)
        writing_wav_file(f'{file_path[:-4]}_1pt.wav', first_header,
                         first_data)

        second_data = self.data[split_position:]
        second_chunk_size = struct.pack('I', len(second_data) + 36)
        second_sub_chunk_size = struct.pack('I', len(second_data))
        second_header = (self.header[:4] + second_chunk_size +
                         self.header[8:40] + second_sub_chunk_size)
        writing_wav_file(f'{file_path[:-4]}_2pt.wav', second_header,
                         second_data)

        print(f'File was successfully split and saved.')

    def speed_wav_audio(self, file_path, speed):
        speed = 1 / float(speed)
        self.sample_rate = struct.pack('I', int((self.sample_rate
                                                 // float(speed))))
        self.header = self.header[:24] + self.sample_rate + self.header[28:]

        writing_wav_file(file_path, self.header, self.data)
        print(f'File was successfully speeded and saved.')

    def merge_wav_audio(self, file_path, second_wav_audio):
        self.data = self.data + second_wav_audio.data

        writing_wav_file(file_path, self.header, self.data)

        print(f'Files were successfully merged and saved.')


def writing_wav_file(file_path, new_header, new_audio_data):
    with open(file_path, 'wb') as file:
        file.write(new_header)
        file.write(new_audio_data)
