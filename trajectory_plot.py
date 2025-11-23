import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
from scipy.signal import butter, filtfilt, find_peaks

def lowpass_filter(data, cutoff_freq, sampling_rate, order=4):
    # Butterworth low-pass filter
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def detect_steps_and_turns(filename):
    # Read data - trailing commas cause pandas to use first column as index
    df = pd.read_csv(filename)
    df = df.reset_index()
    # After reset: 'index' has timestamps, other columns are shifted left by 1
    timestamps = df['index'].values
    accel_x = df['timestamp'].values  # Actually accel_x
    accel_y = df['accel_x'].values   # Actually accel_y
    accel_z = df['accel_y'].values   # Actually accel_z
    gyro_z = df['gyro_y'].values     # Actually gyro_z

    # Calculate sampling rate
    dt = np.mean(np.diff(timestamps)) / 1e9
    sampling_rate = 1.0 / dt

    # Step detection
    accel_mag = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
    filtered_accel = lowpass_filter(accel_mag, 3.0, sampling_rate)

    min_peak_height = np.mean(filtered_accel) + 0.5 * np.std(filtered_accel)
    min_distance = int(0.3 * sampling_rate)
    step_indices, _ = find_peaks(filtered_accel, height=min_peak_height, distance=min_distance)

    # Turn detection using gyroscope
    filtered_gyro_z = lowpass_filter(gyro_z, 1.0, sampling_rate)

    # Integrate gyroscope to get cumulative angle
    cumulative_angle = np.zeros(len(timestamps))
    dt_array = np.diff(timestamps) / 1e9
    for i in range(1, len(timestamps)):
        cumulative_angle[i] = cumulative_angle[i-1] + filtered_gyro_z[i-1] * dt_array[i-1]

    cumulative_angle_deg = np.degrees(cumulative_angle)

    return timestamps, step_indices, cumulative_angle_deg, sampling_rate

def create_trajectory(step_indices, cumulative_angle_deg):
    # Start at origin facing north (90 degrees)
    x, y = 0.0, 0.0
    current_angle = 90.0  # degrees, 0=East, 90=North

    trajectory_x = [x]
    trajectory_y = [y]

    for step_idx in step_indices:
        # Get current heading from cumulative angle
        # Cumulative angle starts at 0, we start facing North (90 deg)
        heading = current_angle + cumulative_angle_deg[step_idx]

        # Move 1 meter in the current direction
        dx = 1.0 * np.cos(np.radians(heading))
        dy = 1.0 * np.sin(np.radians(heading))

        x += dx
        y += dy

        trajectory_x.append(x)
        trajectory_y.append(y)

    return trajectory_x, trajectory_y

def plot_trajectory(trajectory_x, trajectory_y, num_steps):
    plt.figure(figsize=(10, 10))
    plt.plot(trajectory_x, trajectory_y, 'b-', linewidth=2, label='Walking Path')
    plt.plot(trajectory_x[0], trajectory_y[0], 'go', markersize=15, label='Start')
    plt.plot(trajectory_x[-1], trajectory_y[-1], 'ro', markersize=15, label='End')

    # Mark every 5th step
    for i in range(0, len(trajectory_x), 5):
        plt.plot(trajectory_x[i], trajectory_y[i], 'k.', markersize=8)

    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.title(f'Walking Trajectory ({num_steps} steps)')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('plot6_trajectory.png', dpi=300)
    plt.close()

def main():
    print("Part 4: Trajectory Plotting")
    print("-" * 50)

    # Process WALKING_AND_TURNING.csv
    timestamps, step_indices, cumulative_angle_deg, fs = detect_steps_and_turns('lab9-dataset/WALKING_AND_TURNING.csv')

    num_steps = len(step_indices)
    print(f"Detected {num_steps} steps")
    print(f"Sampling rate: {fs:.2f} Hz")

    # Create trajectory
    trajectory_x, trajectory_y = create_trajectory(step_indices, cumulative_angle_deg)

    # Plot trajectory
    plot_trajectory(trajectory_x, trajectory_y, num_steps)

    print(f"Trajectory plot saved to plot6_trajectory.png")
    print(f"Final position: ({trajectory_x[-1]:.2f}, {trajectory_y[-1]:.2f}) meters")

if __name__ == "__main__":
    main()
