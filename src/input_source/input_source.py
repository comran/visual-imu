import cv2 as cv

class InputSource:
    def __init__(self, path=None):
        self.metadata_keys = list()
        self.metadata_keys_to_values = dict()

        if path is None:
            self.input = cv.VideoCapture(0)
        else:
            video_path = path + ".mp4"
            csv_path = path + ".csv"
            self.input = cv.VideoCapture(video_path)
            self.metadata_file = open(csv_path, "r")
            first_line = self.metadata_file.readline()

            header_names = first_line.split(",")
            print(len(header_names))
            for header_name in header_names:
                header_name = header_name.strip()
                self.metadata_keys.append(header_name)
                self.metadata_keys_to_values[header_name] = None

    def fetch(self):
        ret, frame = self.input.read()

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

        return frame, metadata
