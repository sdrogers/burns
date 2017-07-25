import sys
import csv
from pyopenms import *


def load_di(file_name,out_file = None,blank_file = None,min_length = 10,min_intense = 0.0,mz_tol = 5,normalise = 100.0):
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


    spectrum = sorted(spectrum,key = lambda x: x[0])


    if blank_file:
        import bisect
        file = MzMLFile()
        exp = MSExperiment()
        file.load(blank_file,exp)
        mtd = MassTraceDetection()
        traces = []
        mtd.run(exp,traces)
        traces = filter(lambda x: x.getTraceLength() > min_length,traces)
        traces = filter(lambda x: x.getMaxIntensity(False) > min_intense,traces)
        blank_spectrum = []
        for trace in traces:
            mz = trace.getCentroidMZ()
            intensity = trace.getMaxIntensity(False)
            blank_spectrum.append((mz,intensity))
        # For each peak in blank_spectrum, find the closest in spectrum
        true_mz,ti = zip(*spectrum)
        for mz,intensity in blank_spectrum:
            pos = bisect.bisect_right(true_mz,mz)
            left_er = 1e6
            right_er = 1e6
            if pos > 0:
                left_er = 1e6*abs(mz - true_mz[pos-1])/mz
            if pos < len(true_mz):
                right_er = 1e6*abs(mz - true_mz[pos])/mz

            er = min(left_er,right_er)
            if er < 5:
                if er == left_er:
                    pos -= 1
            
                old_peak = spectrum[pos]
                new_peak = (old_peak[0],old_peak[1] - intensity)
                spectrum[pos] = new_peak
        new_spectrum = []
        for peak in spectrum:
            if peak[1] > 0:
                new_spectrum.append(peak)
        spectrum = new_spectrum

                


    if normalise:
        mz,inte = zip(*spectrum)
        max_inte = max(inte)
        for i,peak in enumerate(spectrum):
            new_peak = (peak[0],normalise*peak[1]/max_inte)
            spectrum[i] = new_peak


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

