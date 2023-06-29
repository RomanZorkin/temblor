import numpy as np

from scipy import signal


def snv(input_data: np.ndarray) -> np.ndarray:
    # Define a new array and populate it with the corrected data
    output_data = np.zeros_like(input_data)
    for i in range(input_data.shape[0]):

        # Apply correction
        output_data[i, :] = (input_data[i, :] - np.mean(input_data[i, :])) / np.std(input_data[i, :])

    return output_data


def msc(X) -> np.ndarray:
# https://www.programmersought.com/article/738510087629/
# +++++ input: x = m × P matrix, M sample, P feature. X should be NDARRAY data type)
# +++++ output: x_msc = m × P
    me = np.mean(X, axis=0)
    m, p = np.shape(X)
    X_msc = np.zeros((m, p))

    for i in range(m):
        poly = np.polyfit(me, X[i], 1)  # Each sample is made once a unit linear regression
        j = 0
        for j in range(p):
            X_msc[i, j] = (X[i, j] - poly[1]) / poly[0]

    return X_msc


def savgol(msc_arr: np.ndarray) -> np.ndarray:
    savgol_arr_train = msc_arr.copy()
    for num in range(msc_arr.shape[0]):
        savgol_arr_train[num] = signal.savgol_filter(
            savgol_arr_train[num], window_length=22, polyorder=10, mode="nearest"
        )  # 23*16
    return savgol_arr_train
