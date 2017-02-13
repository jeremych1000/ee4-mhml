from MLBlock.models import RawData
import csv
import numpy as np


def genfeatureFromCSV(fileURL, winSize):
    fHandle = open(fileURL)
    csvReader = csv.reader(fHandle)
    csvReader.__next__()
    rowCount = winSize
    winSlice = []
    mean_hr = []
    std_hr = []
    mean_rr = []
    std_rr = []
    mean_gsr = []
    std_gsr = []
    mean_temp = []
    std_temp = []
    mean_acc = []
    for row in csvReader:
        if rowCount != 0:
            winSlice.append(row)
            rowCount -= 1
        else:
            winSlice = np.array(winSlice)
            mean_hr.append(np.mean([float(ele) for ele in winSlice[:,1]]))
            std_hr.append(np.std([float(ele) for ele in winSlice[:,1]]))
            mean_rr.append(np.mean([float(ele) for ele in winSlice[:,2]]))
            std_rr.append(np.std([float(ele) for ele in winSlice[:,2]]))
            mean_gsr.append(np.mean([float(ele) for ele in winSlice[:,4]]))
            std_gsr.append(np.std([float(ele) for ele in winSlice[:,4]]))
            mean_temp.append(np.mean([float(ele) for ele in winSlice[:,5]]))
            std_temp.append(np.std([float(ele) for ele in winSlice[:,5]]))
            mean_acc.append(
                abs(np.mean([float(ele) for ele in winSlice[:,6]])) ** 2 + abs(
                    np.mean([float(ele) for ele in winSlice[:,7]])) ** 2 + abs(
                    np.mean([float(ele) for ele in winSlice[:,8]]) ** 2))
            rowCount = winSize
            winSlice = []
    if len(winSlice) != 0:
        winSlice = np.array(winSlice)
        mean_hr.append(np.mean([float(ele) for ele in winSlice[:, 1]]))
        std_hr.append(np.std([float(ele) for ele in winSlice[:, 1]]))
        mean_rr.append(np.mean([float(ele) for ele in winSlice[:, 2]]))
        std_rr.append(np.std([float(ele) for ele in winSlice[:, 2]]))
        mean_gsr.append(np.mean([float(ele) for ele in winSlice[:, 4]]))
        std_gsr.append(np.std([float(ele) for ele in winSlice[:, 4]]))
        mean_temp.append(np.mean([float(ele) for ele in winSlice[:, 5]]))
        std_temp.append(np.std([float(ele) for ele in winSlice[:, 5]]))
        mean_acc.append(
            abs(np.mean([float(ele) for ele in winSlice[:, 6]])) ** 2 + abs(
                np.mean([float(ele) for ele in winSlice[:, 7]])) ** 2 + abs(
                np.mean([float(ele) for ele in winSlice[:, 8]]) ** 2))
    return [mean_hr, std_hr, mean_rr, std_rr, mean_gsr, std_gsr, mean_temp, std_temp, mean_acc]
