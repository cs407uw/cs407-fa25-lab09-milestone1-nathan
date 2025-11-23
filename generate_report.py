from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def create_report():
    doc = SimpleDocTemplate("report.pdf", pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = styles['Heading2']
    body_style = styles['BodyText']
    body_style.alignment = TA_JUSTIFY

    story.append(Paragraph("Lab 9 Milestone 2: Sensor Data Processing", title_style))
    story.append(Paragraph("Part 1: Understanding Sensor Data Errors", styles['Heading2']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Objective", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "This analysis examines how sensor noise in accelerometer data affects distance estimation. "
        "Using synthetic acceleration data, we integrated acceleration values to compute velocity and distance, "
        "comparing results from clean data versus noisy sensor readings.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Methodology", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The ACCELERATION.csv dataset contains timestamped measurements with both actual and noisy acceleration values. "
        "The analysis used numerical integration with a timestep of 0.1 seconds. "
        "Velocity was computed as v(t) = v(t-1) + a(t-1) * dt, and distance as d(t) = d(t-1) + v(t-1) * dt, "
        "where dt is the time step between measurements.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Results", heading_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Figure 1: Acceleration Comparison", heading_style))
    story.append(Spacer(1, 6))
    img1 = Image('plot1_acceleration.png', width=5.5*inch, height=3.3*inch)
    story.append(img1)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The acceleration plot shows the actual acceleration pattern (a step function with values 0.35, 0, and -0.35 m/s²) "
        "compared to noisy sensor measurements. The noise introduces random variations around the true values.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(PageBreak())

    story.append(Paragraph("Figure 2: Velocity Comparison", heading_style))
    story.append(Spacer(1, 6))
    img2 = Image('plot2_velocity.png', width=5.5*inch, height=3.3*inch)
    story.append(img2)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Integrating acceleration produces velocity. The actual velocity follows a clear triangular pattern, "
        "while the noisy velocity shows cumulative error that grows over time due to noise integration.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Figure 3: Distance Comparison", heading_style))
    story.append(Spacer(1, 6))
    img3 = Image('plot3_distance.png', width=5.5*inch, height=3.3*inch)
    story.append(img3)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Distance traveled shows the most significant error accumulation. The actual distance follows a smooth curve "
        "reaching the final value, while the noisy estimate diverges substantially due to double integration of noise.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(PageBreak())

    story.append(Paragraph("Quantitative Analysis", heading_style))
    story.append(Spacer(1, 12))

    results_text = """
    <b>Final distance using actual acceleration:</b> 26.9430 m<br/>
    <b>Final distance using noisy acceleration:</b> 32.4594 m<br/>
    <b>Difference between estimates:</b> 5.5164 m<br/>
    <b>Percentage error:</b> 20.47%
    """
    story.append(Paragraph(results_text, body_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Discussion", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The analysis demonstrates that sensor noise has a compounding effect when integration is performed. "
        "While the noise in acceleration appears relatively small, integrating once to get velocity and again to get distance "
        "causes errors to accumulate significantly. The 20.47% error in final distance estimation highlights the critical "
        "importance of sensor accuracy in pedestrian dead-reckoning applications.",
        body_style
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "This error accumulation explains why practical PDR systems require additional techniques such as "
        "zero-velocity updates, step detection algorithms, and sensor fusion to maintain accuracy over time. "
        "Without these corrections, raw integration of noisy accelerometer data quickly becomes unreliable for navigation.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Conclusion", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Noisy accelerometer measurements introduce significant errors in distance estimation through double integration. "
        "The 5.5 meter difference over a short movement demonstrates why real-world PDR systems must implement "
        "sophisticated filtering and error correction strategies to achieve useful positioning accuracy.",
        body_style
    ))

    story.append(PageBreak())

    # Part 2: Step Detection
    story.append(Paragraph("Part 2: Step Detection", styles['Heading2']))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Step detection is crucial for pedestrian dead-reckoning systems. By detecting individual steps, "
        "the system can estimate distance traveled by multiplying step count by estimated step length.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Methodology", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The step detection algorithm processes accelerometer data from all three axes by calculating the "
        "acceleration magnitude. A low-pass Butterworth filter (cutoff frequency 3 Hz) smooths the signal "
        "to reduce noise. Peak detection identifies local maxima in the filtered signal that exceed a "
        "threshold based on mean and standard deviation, with a minimum time spacing between detections "
        "to prevent false positives from a single step.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Figure 4: Step Detection Results", heading_style))
    story.append(Spacer(1, 6))
    img4 = Image('plot4_step_detection.png', width=5.5*inch, height=3.3*inch)
    story.append(img4)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The algorithm successfully detected 37 steps in the WALKING.csv dataset. Each peak in the filtered "
        "acceleration magnitude corresponds to one complete step cycle.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(PageBreak())

    # Part 3: Turn Detection
    story.append(Paragraph("Part 3: Turn Detection", styles['Heading2']))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Direction detection complements step detection by tracking changes in heading. This implementation "
        "uses gyroscope data to detect rotational movements and identify 90-degree turns.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Methodology", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The turn detection algorithm processes gyroscope Z-axis data (rotation around the vertical axis). "
        "After applying a low-pass filter (cutoff frequency 1 Hz), the angular velocity is integrated over "
        "time to compute cumulative rotation angle. When the angle crosses an 85-degree threshold (allowing "
        "for sensor noise), a turn is detected. The algorithm distinguishes between clockwise and "
        "counter-clockwise rotations based on the sign of the angle change.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Figure 5: Turn Detection Results", heading_style))
    story.append(Spacer(1, 6))
    img5 = Image('plot5_turn_detection.png', width=5.5*inch, height=3.3*inch)
    story.append(img5)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The algorithm detected 8 turns in TURNING.csv: 4 clockwise turns (completing one full 360-degree rotation) "
        "and 4 counter-clockwise turns (completing another full rotation in the opposite direction). "
        "Each detected turn corresponds to approximately 90 degrees of rotation.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(PageBreak())

    # Part 4: Trajectory Plotting
    story.append(Paragraph("Part 4: Trajectory Reconstruction", styles['Heading2']))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Combining step detection and turn detection enables reconstruction of the complete walking trajectory. "
        "This demonstrates how PDR systems can track position over time without GPS.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Methodology", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The trajectory reconstruction algorithm applies both step detection and turn detection to the "
        "WALKING_AND_TURNING.csv dataset. For each detected step, the algorithm advances the position by "
        "1 meter in the current heading direction. The heading is continuously updated based on the integrated "
        "gyroscope data. Starting from an origin at (0,0) facing north, the algorithm tracks position "
        "changes throughout the walking session.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Figure 6: Reconstructed Trajectory", heading_style))
    story.append(Spacer(1, 6))
    img6 = Image('plot6_trajectory.png', width=4.5*inch, height=4.5*inch)
    story.append(img6)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "The reconstructed trajectory shows 79 detected steps forming a complete walking path. "
        "The green marker indicates the starting position, while the red marker shows the ending position. "
        "The close proximity of start and end points suggests the walking path was designed to return "
        "near the origin.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Overall Conclusion", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "This lab demonstrated the fundamental components of pedestrian dead-reckoning: understanding sensor "
        "error accumulation, detecting steps, identifying turns, and reconstructing trajectories. These techniques "
        "form the basis of indoor navigation systems and fitness tracking applications. The analysis showed that "
        "while raw sensor data contains significant noise, proper filtering and peak detection algorithms can "
        "reliably extract meaningful motion information. Future improvements could include adaptive step length "
        "estimation, zero-velocity updates to reduce drift, and sensor fusion with magnetometer data for "
        "improved heading accuracy.",
        body_style
    ))

    doc.build(story)
    print("Report generated: report.pdf")

if __name__ == "__main__":
    create_report()
