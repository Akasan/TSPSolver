import csv


class DataWriter:
    def __init__(self, output_filename="result.csv"):
        """
        Keyword Arguments:
        ------------------
            output_filename {str} -- output file name (default: "result.csv")
        """
        self.fp = open(output_filename, "w", encoding="utf-8")
        self.writer = csv.writer(self.fp, lineterminator="\n")

    def write(self, distance):
        """ write iteartion's result

        Arguments:
        ----------
            distance {list[float]} -- iteartion's result of distance
        """
        self.writer.writerow(distance)

    def save(self):
        """ save """
        self.fp.close()