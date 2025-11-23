import subprocess
import sys

def main():
    print("=" * 60)
    print("Lab 9 Milestone 2: Sensor Data Processing")
    print("=" * 60)
    print()

    scripts = [
        ('analyze_acceleration.py', 'Part 1: Acceleration Error Analysis'),
        ('step_detection.py', 'Part 2: Step Detection'),
        ('turn_detection.py', 'Part 3: Turn Detection'),
        ('trajectory_plot.py', 'Part 4: Trajectory Plotting'),
        ('generate_report.py', 'Generating PDF Report')
    ]

    for script, description in scripts:
        print(f"\nRunning: {description}")
        print("-" * 60)
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors/Warnings:", result.stderr)

    print("\n" + "=" * 60)
    print("All analyses complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - report.pdf (comprehensive report)")
    print("  - plot1_acceleration.png")
    print("  - plot2_velocity.png")
    print("  - plot3_distance.png")
    print("  - plot4_step_detection.png")
    print("  - plot5_turn_detection.png")
    print("  - plot6_trajectory.png")

if __name__ == "__main__":
    main()
