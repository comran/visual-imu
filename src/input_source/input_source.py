import cv2 as cv
import queue

STOP_AFTER_FIRST_RUN = True

class InputSource:
    def __init__(self, path=None):
        self.metadata_keys = list()
        self.metadata_keys_to_values = dict()

        self.reverse = False
        self.reverse_stack = queue.LifoQueue()

        if path is None:
            self.input = cv.VideoCapture(0)
        else:
            video_path = path + ".mp4"
            csv_path = path + ".csv"
            self.input = cv.VideoCapture(video_path)
            self.metadata_file = open(csv_path, "r")
            first_line = self.metadata_file.readline()

            header_names = first_line.split(",")
            for header_name in header_names:
                header_name = header_name.strip()
                self.metadata_keys.append(header_name)
                self.metadata_keys_to_values[header_name] = None

    def fetch(self):
        ret, frame = self.input.read()

        if not ret and not self.reverse:
            if STOP_AFTER_FIRST_RUN:
                return (None, None)
            self.reverse = True

        if self.reverse:
            if self.reverse_stack.empty():
                self.input.set(cv.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.input.read()
                if self.metadata_file is not None:
                    self.metadata_file.seek(0, 0)
                    self.metadata_file.readline()

                self.reverse = False
            else:
                frame_metadata = self.reverse_stack.get_nowait()
                return frame_metadata

        metadata = None
        if self.metadata_file is not None:
            for key in self.metadata_keys:
                self.metadata_keys_to_values[key] = None

            line = self.metadata_file.readline()
            values = line.split(",")

            i = 0
            for value in values:
                key = self.metadata_keys[i]
                self.metadata_keys_to_values[key] = value
                i += 1

            metadata = (self.metadata_keys, self.metadata_keys_to_values)

        self.reverse_stack.put((frame, metadata))

        return frame, metadata
