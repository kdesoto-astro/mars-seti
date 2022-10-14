import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def read_in_logs(csv_file):
    """
    Reads in log file and returns pandas
    dataframe.
    """
    df = pd.read_csv(csv_file)
    df.columns =['MJD', 'Frequency', 'Power', 'Spacecraft']
    return df

def plot_signal_durations(df, spacecraft):
    print(df['Spacecraft'])
    filtered_df = df[df['Spacecraft'] == spacecraft]
    unique_mjd = np.unique(df['MJD']) # includes MJD where signal was not sent by specific spacecraft
    
    freq_arr = np.zeros(len(unique_mjd))
    power_arr = np.zeros(len(unique_mjd))
    
    matching_mjds = np.isin(unique_mjd, filtered_df['MJD'])
    freq_arr[matching_mjds] = filtered_df['Frequency']
    power_arr[matching_mjds] = filtered_df['Power']
    
    plt.plot(unique_mjd / 1000., freq_arr)
    plt.xlabel("MJD")
    plt.ylabel("Frequency (Hz)")
    plt.savefig("test_freq.png")
    plt.close()
    
def main():
    CSV_TEST = "Canberra_1665769138000_1665770259000_down.csv"
    df = read_in_logs(CSV_TEST)
    plot_signal_durations(df, "MVN")

main()
    
    
    