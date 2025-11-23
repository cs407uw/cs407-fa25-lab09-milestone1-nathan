import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks

def moving_average(data, window_size):
    # Simple moving average filter
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')

def lowpass_filter(data, cutoff_freq, sampling_rate, order=4):
    # Butterworth low-pass filter
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def detect_steps(filename):
    # Read data
    df = pd.read_csv(filename)

    timestamps = df['timestamp'].values
    accel_x = df['accel_x'].values
    accel_y = df['accel_y'].values
    accel_z = df['accel_z'].values

    # Calculate acceleration magnitude
    accel_mag = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)

    # Calculate sampling rate
    dt = np.mean(np.diff(timestamps)) / 1e9  # Convert nanoseconds to seconds
    sampling_rate = 1.0 / dt

    # Apply smoothing - using moving average
    window_size = 10
    smoothed_accel = moving_average(accel_mag, window_size)

    # Also try low-pass filter
    cutoff_freq = 3.0  # Hz
    filtered_accel = lowpass_filter(accel_mag, cutoff_freq, sampling_rate)

    # Detect peaks (steps)
    # Parameters tuned to detect walking steps
    min_peak_height = np.mean(filtered_accel) + 0.5 * np.std(filtered_accel)
    min_distance = int(0.3 * sampling_rate)  # Minimum 0.3 seconds between steps

    peaks, properties = find_peaks(filtered_accel, height=min_peak_height, distance=min_distance)

    num_steps = len(peaks)

    return timestamps, accel_mag, smoothed_accel, filtered_accel, peaks, num_steps, sampling_rate

def plot_step_detection(timestamps, accel_mag, filtered_accel, peaks, num_steps):
    # Convert timestamps to seconds from start
    time_seconds = (timestamps - timestamps[0]) / 1e9

    plt.figure(figsize=(12, 6))
    plt.plot(time_seconds, accel_mag, label='Raw Acceleration Magnitude', alpha=0.5)
    plt.plot(time_seconds, filtered_accel, label='Filtered Acceleration', linewidth=2)
    plt.plot(time_seconds[peaks], filtered_accel[peaks], 'rx', markersize=10, label=f'Detected Steps ({num_steps})')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration Magnitude (m/s²)')
    plt.title('Step Detection')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plot4_step_detection.png', dpi=300)
    plt.close()

def main():
    print("Part 2: Step Detection")
    print("-" * 50)

    # Detect steps in WALKING.csv
    timestamps, accel_mag, smoothed_accel, filtered_accel, peaks, num_steps, fs = detect_steps('lab9-dataset/WALKING.csv')

    print(f"Detected {num_steps} steps in WALKING.csv")
    print(f"Sampling rate: {fs:.2f} Hz")

    # Create plot
    plot_step_detection(timestamps, accel_mag, filtered_accel, peaks, num_steps)
    print("Step detection plot saved to plot4_step_detection.png")

if __name__ == "__main__":
    main()
