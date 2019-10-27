import analytics.csv_writer as csv_writer
import analytics.chart as chart

class Analytics:
    def __init__(self, title="Visual IMU", show_chart=False, logfile_name=None):
        self.file = None
        self.key_order = list()
        self.values = dict()
        self.first_pass = True

        self.csv_logger = None
        if logfile_name is not None:
            self.csv_logger = csv_writer.CsvWriter(logfile_name)

        self.chart = None
        if show_chart:
            self.chart = chart.Chart(title=title)

    def feed(self, key, value):
        if key in self.values and self.values[key] is not None:
            print("Key was already set!")
            return

        if not self.first_pass and key not in self.values.keys():
            print("Key must be defined at the first iteration.")
            return

        if self.first_pass:
            self.key_order.append(key)

        self.values[key] = value

    def complete(self):
        self.first_pass = False

        if self.csv_logger is not None:
            self.csv_logger.write(self.key_order, self.values)

        if self.chart is not None:
            self.chart.write(self.key_order, self.values)

        # Clear values dictionary.
        for key in self.values.keys():
            self.values[key] = None
