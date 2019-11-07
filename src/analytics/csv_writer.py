class CsvWriter:
    def __init__(self, logfile_name):
        self.file = open(logfile_name, "w+")
        self.first_print = True

    def write(self, keys, keys_to_values):
        print(keys)
        print(keys_to_values)
        lines = ""

        # Log the header on first write.
        if self.first_print:
            for key_i in range(len(keys)):
                last = (key_i == len(keys) - 1)
                lines += keys[key_i]

                if not last:
                    lines += ","
                else:
                    lines += "\n"

        for key_i in range(len(keys)):
            last = (key_i == len(keys) - 1)
            key = keys[key_i]

            lines += str(keys_to_values[key])

            if not last:
                lines += ","
            else:
                pass

        self.file.write(lines)
        self.file.flush()

        self.first_print = False
