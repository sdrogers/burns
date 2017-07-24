import sys
import csv
from pyopenms import *


def load_di(file_name,out_file = None,min_length = 10,min_intense = 0.0):
    file = MzMLFile()
    exp = MSExperiment()
    file.load(file_name, exp)
    mtd = MassTraceDetection()
    traces = []
    mtd.run(exp,traces)
    traces = filter(lambda x: x.getTraceLength() > min_length,traces)
    traces = filter(lambda x: x.getMaxIntensity(False) > min_intense,traces)
    spectrum = []

    for trace in traces:
        mz = trace.getCentroidMZ()
        intensity = trace.getMaxIntensity(False)
        spectrum.append((mz,intensity))

    if out_file:
        with open(out_file,'w') as f:
            writer = csv.writer(f)
            for mz,intensity in spectrum:
                writer.writerow([mz,intensity])
                
    return spectrum


if __name__ == '__main__':
    file_name = sys.argv[1]
    out_file = sys.argv[2]
    min_length = float(sys.argv[3])
    min_intense = float(sys.argv[4])
    load_di(file_name,out_file,min_length = min_length,min_intense = min_intense)

