import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd

def process_acceleration_data(filename):
    # Read CSV file
    df = pd.read_csv(filename)

    timestamps = df['timestamp'].values
    acceleration = df['acceleration'].values
    noisy_acceleration = df['noisyacceleration'].values

    # Calculate time step
    dt = timestamps[1] - timestamps[0]

    # Initialize arrays for velocity and distance
    velocity = np.zeros(len(timestamps))
    noisy_velocity = np.zeros(len(timestamps))

    distance = np.zeros(len(timestamps))
    noisy_distance = np.zeros(len(timestamps))

    # Integrate acceleration to get velocity, then integrate velocity to get distance
    for i in range(1, len(timestamps)):
        # v = v0 + a*dt
        velocity[i] = velocity[i-1] + acceleration[i-1] * dt
        noisy_velocity[i] = noisy_velocity[i-1] + noisy_acceleration[i-1] * dt

        # d = d0 + v*dt
        distance[i] = distance[i-1] + velocity[i-1] * dt
        noisy_distance[i] = noisy_distance[i-1] + noisy_velocity[i-1] * dt

    return timestamps, acceleration, noisy_acceleration, velocity, noisy_velocity, distance, noisy_distance

def create_plots(timestamps, acceleration, noisy_acceleration, velocity, noisy_velocity, distance, noisy_distance):
    # Plot 1: Acceleration
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, acceleration, label='Actual Acceleration', linewidth=2)
    plt.plot(timestamps, noisy_acceleration, label='Noisy Acceleration', alpha=0.7)
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.title('Acceleration Comparison')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plot1_acceleration.png', dpi=300)
    plt.close()

    # Plot 2: Velocity
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, velocity, label='Actual Velocity', linewidth=2)
    plt.plot(timestamps, noisy_velocity, label='Noisy Velocity', alpha=0.7)
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Velocity Comparison')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plot2_velocity.png', dpi=300)
    plt.close()

    # Plot 3: Distance
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, distance, label='Actual Distance', linewidth=2)
    plt.plot(timestamps, noisy_distance, label='Noisy Distance', alpha=0.7)
    plt.xlabel('Time (s)')
    plt.ylabel('Distance (m)')
    plt.title('Distance Comparison')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plot3_distance.png', dpi=300)
    plt.close()

    print("Plots saved: plot1_acceleration.png, plot2_velocity.png, plot3_distance.png")

def main():
    # Process the data
    timestamps, acceleration, noisy_acceleration, velocity, noisy_velocity, distance, noisy_distance = process_acceleration_data('lab9-dataset/ACCELERATION.csv')

    # Create plots
    create_plots(timestamps, acceleration, noisy_acceleration, velocity, noisy_velocity, distance, noisy_distance)

    # Calculate final distances
    final_distance_actual = distance[-1]
    final_distance_noisy = noisy_distance[-1]
    difference = abs(final_distance_actual - final_distance_noisy)

    print(f"Final distance using actual acceleration: {final_distance_actual:.4f} m")
    print(f"Final distance using noisy acceleration: {final_distance_noisy:.4f} m")
    print(f"Difference between estimates: {difference:.4f} m")
    print(f"Percentage error: {(difference / final_distance_actual * 100):.2f}%")

if __name__ == "__main__":
    main()
