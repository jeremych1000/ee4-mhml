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
    outcome = False
    for row in csvReader:
        if len(row) == 10:
            outcome = (row[9] == "true" or row[9] == "True" or row[9] == "TRUE")
        if rowCount != 0:
            winSlice.append(row)
            rowCount -= 1
        else:
            winSlice = np.array(winSlice)
            hr_slice = [float(ele[1]) for ele in winSlice]
            rr_slice = [float(ele[2]) for ele in winSlice]
            gsr_slice = [float(ele[4]) for ele in winSlice]
            temp_slice = [float(ele[5]) for ele in winSlice]
            acc_x_slice = [float(ele[6]) for ele in winSlice]
            acc_y_slice = [float(ele[7]) for ele in winSlice]
            acc_z_slice = [float(ele[8]) for ele in winSlice]
            mean_hr.append(np.mean(hr_slice))
            std_hr.append(np.std(hr_slice))
            mean_rr.append(np.mean(rr_slice))
            std_rr.append(np.std(rr_slice))
            mean_gsr.append(np.mean(gsr_slice))
            std_gsr.append(np.std(gsr_slice))
            mean_temp.append(np.mean(temp_slice))
            std_temp.append(np.std(temp_slice))
            mean_acc.append(
                abs(np.mean(acc_x_slice)) ** 2 + abs(
                    np.mean(acc_y_slice)) ** 2 + abs(
                    np.mean(acc_z_slice) ** 2))
            rowCount = winSize
            winSlice = []

    if len(winSlice) != 0:
        winSlice = np.array(winSlice)
        hr_slice = [float(ele[1]) for ele in winSlice]
        rr_slice = [float(ele[2]) for ele in winSlice]
        gsr_slice = [float(ele[4]) for ele in winSlice]
        temp_slice = [float(ele[5]) for ele in winSlice]
        acc_x_slice = [float(ele[6]) for ele in winSlice]
        acc_y_slice = [float(ele[7]) for ele in winSlice]
        acc_z_slice = [float(ele[8]) for ele in winSlice]
        mean_hr.append(np.mean(hr_slice))
        std_hr.append(np.std(hr_slice))
        mean_rr.append(np.mean(rr_slice))
        std_rr.append(np.std(rr_slice))
        mean_gsr.append(np.mean(gsr_slice))
        std_gsr.append(np.std(gsr_slice))
        mean_temp.append(np.mean(temp_slice))
        std_temp.append(np.std(temp_slice))
        mean_acc.append(
            abs(np.mean(acc_x_slice)) ** 2 + abs(
                np.mean(acc_y_slice)) ** 2 + abs(
                np.mean(acc_z_slice) ** 2))
    return [mean_hr, std_hr, mean_rr, std_rr, mean_gsr, std_gsr, mean_temp, std_temp, mean_acc, outcome]
