import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
from scipy.signal import butter, filtfilt

def lowpass_filter(data, cutoff_freq, sampling_rate, order=4):
    # Butterworth low-pass filter
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def detect_turns(filename):
    # Read only specific columns we need to avoid inconsistent column issues
    df = pd.read_csv(filename, usecols=['timestamp', 'gyro_z'])

    timestamps = df['timestamp'].values
    gyro_z = df['gyro_z'].values

    # Calculate sampling rate
    dt_ns = np.diff(timestamps)
    dt = dt_ns / 1e9  # Convert to seconds
    sampling_rate = 1.0 / np.mean(dt)

    # Apply smoothing to gyroscope data
    cutoff_freq = 1.0  # Hz
    filtered_gyro_z = lowpass_filter(gyro_z, cutoff_freq, sampling_rate)

    # Integrate gyroscope to get angle (in radians)
    cumulative_angle = np.zeros(len(timestamps))
    for i in range(1, len(timestamps)):
        cumulative_angle[i] = cumulative_angle[i-1] + filtered_gyro_z[i-1] * dt[i-1]

    # Convert to degrees
    cumulative_angle_deg = np.degrees(cumulative_angle)

    # Detect 90-degree turns
    turns = []
    turn_threshold = 85  # degrees (slightly less than 90 to account for noise)
    last_turn_index = 0
    current_turn_start = 0

    for i in range(1, len(cumulative_angle_deg)):
        angle_change = cumulative_angle_deg[i] - cumulative_angle_deg[current_turn_start]

        # Check for clockwise turn (positive)
        if angle_change >= turn_threshold:
            if i - last_turn_index > 0.5 * sampling_rate:  # At least 0.5 seconds since last turn
                turns.append({
                    'index': i,
                    'time': (timestamps[i] - timestamps[0]) / 1e9,
                    'angle': angle_change,
                    'direction': 'clockwise'
                })
                current_turn_start = i
                last_turn_index = i

        # Check for counter-clockwise turn (negative)
        elif angle_change <= -turn_threshold:
            if i - last_turn_index > 0.5 * sampling_rate:
                turns.append({
                    'index': i,
                    'time': (timestamps[i] - timestamps[0]) / 1e9,
                    'angle': angle_change,
                    'direction': 'counter-clockwise'
                })
                current_turn_start = i
                last_turn_index = i

    return timestamps, gyro_z, filtered_gyro_z, cumulative_angle_deg, turns, sampling_rate

def plot_turn_detection(timestamps, gyro_z, filtered_gyro_z, cumulative_angle_deg, turns):
    # Convert timestamps to seconds
    time_seconds = (timestamps - timestamps[0]) / 1e9

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Plot gyroscope data
    ax1.plot(time_seconds, gyro_z, label='Raw Gyroscope Z', alpha=0.5)
    ax1.plot(time_seconds, filtered_gyro_z, label='Filtered Gyroscope Z', linewidth=2)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Angular Velocity (rad/s)')
    ax1.set_title('Gyroscope Data (Z-axis)')
    ax1.legend()
    ax1.grid(True)

    # Plot cumulative angle with turn markers
    ax2.plot(time_seconds, cumulative_angle_deg, label='Cumulative Angle', linewidth=2)

    for turn in turns:
        color = 'red' if turn['direction'] == 'clockwise' else 'blue'
        ax2.axvline(turn['time'], color=color, linestyle='--', alpha=0.7)
        ax2.plot(turn['time'], cumulative_angle_deg[turn['index']], 'o', color=color, markersize=8)

    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Cumulative Angle (degrees)')
    ax2.set_title(f'Turn Detection ({len(turns)} turns detected)')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('plot5_turn_detection.png', dpi=300)
    plt.close()

def main():
    print("Part 3: Turn Detection")
    print("-" * 50)

    # Detect turns in TURNING.csv
    timestamps, gyro_z, filtered_gyro_z, cumulative_angle_deg, turns, fs = detect_turns('lab9-dataset/TURNING.csv')

    print(f"Sampling rate: {fs:.2f} Hz")
    print(f"Detected {len(turns)} turns:")
    for i, turn in enumerate(turns):
        print(f"  Turn {i+1}: {turn['direction']}, angle = {turn['angle']:.1f}°, time = {turn['time']:.2f}s")

    # Create plot
    plot_turn_detection(timestamps, gyro_z, filtered_gyro_z, cumulative_angle_deg, turns)
    print("\nTurn detection plot saved to plot5_turn_detection.png")

if __name__ == "__main__":
    main()
