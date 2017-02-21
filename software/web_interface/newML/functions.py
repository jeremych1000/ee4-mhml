import numpy as np
import math


def json2Feature(json):
    if 'data' not in json.keys():
        assert 'JSON is missing the data array'
    else:
        hr = [];
        rr = [];
        gsr = [];
        temp = [];
        accX = [];
        accY = [];
        accZ = [];
        feature = {};
        for data in json.get('data'):
            hr.append(data["HR"])
            rr.append(data["RR"])
            gsr.append(data["GSR"])
            temp.append(data["SkinT"])
            accX.append(data["AccX"])
            accY.append(data["AccY"])
            accZ.append(data["AccZ"])
        feature["mean_hr"] = np.mean(hr)
        feature["std_hr"] = np.std(hr)
        feature["mean_rr"] = np.mean(rr)
        feature["std_rr"] = np.std(rr)
        feature["mean_gsr"] = np.mean(gsr)
        feature["std_gsr"] = np.std(gsr)
        feature["mean_temp"] = np.mean(temp)
        feature["std_temp"] = np.std(temp)
        feature["mean_acc"] = np.mean([math.sqrt(x ** 2 + y ** 2 + z ** 2) for x, y, z in zip(accX, accY, accZ)])
        return feature
