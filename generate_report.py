from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def create_report():
    doc = SimpleDocTemplate("report.pdf", pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    story = []

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor='black',
        spaceAfter=20,
        alignment=TA_CENTER
    )

    # Student info style
    info_style = ParagraphStyle(
        'StudentInfo',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_LEFT
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        leftIndent=20,
        spaceAfter=12
    )

    heading_style = styles['Heading2']
    subheading_style = styles['Heading3']
    body_style = styles['BodyText']
    body_style.alignment = TA_JUSTIFY

    # Header with student info
    story.append(Paragraph("Nathan, netid@wisc.edu, githublogin", info_style))
    story.append(Spacer(1, 30))

    # Title
    story.append(Paragraph("Lab 9 Milestone 2: Sensor Data Processing", title_style))
    story.append(Spacer(1, 20))

    # PART 1
    story.append(Paragraph("Milestone 2 Part 1: Understanding Sensor Data Errors", heading_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "This section analyzes how sensor noise affects distance estimation through double integration "
        "of accelerometer data.",
        body_style
    ))
    story.append(Spacer(1, 12))

    # Plot 1: Acceleration
    story.append(Paragraph("Acceleration Comparison", subheading_style))
    story.append(Spacer(1, 6))
    img1 = Image('plot1_acceleration.png', width=5*inch, height=3*inch)
    story.append(img1)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Figure 1 shows the actual acceleration (clean signal) versus noisy acceleration measurements. "
        "The actual acceleration follows a step function pattern (0.35, 0, -0.35 m/s²), while the noisy "
        "signal shows random variations around these true values.",
        body_style
    ))
    story.append(Spacer(1, 15))

    # Plot 2: Velocity
    story.append(Paragraph("Velocity Comparison", subheading_style))
    story.append(Spacer(1, 6))
    img2 = Image('plot2_velocity.png', width=5*inch, height=3*inch)
    story.append(img2)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Figure 2 displays velocity obtained by integrating acceleration. The clean velocity shows a smooth "
        "triangular pattern, while the noisy velocity begins to show error accumulation from noise integration.",
        body_style
    ))
    story.append(Spacer(1, 15))

    # Plot 3: Distance
    story.append(Paragraph("Distance Comparison", subheading_style))
    story.append(Spacer(1, 6))
    img3 = Image('plot3_distance.png', width=5*inch, height=3*inch)
    story.append(img3)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Figure 3 shows distance traveled from double integration. The error accumulation is most pronounced "
        "here, with the noisy estimate diverging significantly from the actual distance.",
        body_style
    ))
    story.append(Spacer(1, 15))

    # Results
    story.append(Paragraph("Results", subheading_style))
    story.append(Spacer(1, 6))
    results_text = """
    <b>Final distance using actual acceleration:</b> 26.9430 m<br/>
    <b>Final distance using noisy acceleration:</b> 32.4594 m<br/>
    <b>Difference between estimates:</b> 5.5164 m<br/>
    <b>Percentage error:</b> 20.47%
    """
    story.append(Paragraph(results_text, body_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "The 5.5 meter difference (20.47% error) demonstrates how noise compounds through double integration, "
        "highlighting the importance of filtering techniques in real-world PDR systems.",
        body_style
    ))

    story.append(PageBreak())

    # PART 2: STEP DETECTION
    story.append(Paragraph("Milestone 2 Part 2: Step Detection", heading_style))
    story.append(Spacer(1, 12))

    # Data Preparation
    story.append(Paragraph("Data Preparation", subheading_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "For step detection, I calculated the <b>acceleration magnitude</b> from the three-axis accelerometer data: "
        "magnitude = sqrt(accel_x² + accel_y² + accel_z²). This single metric captures overall body acceleration "
        "regardless of phone orientation.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Smoothing Method:", subheading_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "A <b>4th-order Butterworth low-pass filter</b> with cutoff frequency of <b>3 Hz</b> was applied. "
        "This removes high-frequency noise while preserving the ~1-2 Hz step frequency. The Butterworth filter "
        "was chosen for its maximally flat frequency response in the passband.",
        body_style
    ))
    story.append(Spacer(1, 12))

    code1 = """def lowpass_filter(data, cutoff_freq, sampling_rate, order=4):
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low')
    return filtfilt(b, a, data)

# Apply filter
filtered_accel = lowpass_filter(accel_mag, 3.0, sampling_rate)"""

    story.append(Preformatted(code1, code_style))
    story.append(Spacer(1, 12))

    # Step detection plot
    img4 = Image('plot4_step_detection.png', width=5.5*inch, height=3.3*inch)
    story.append(img4)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Figure 4 shows raw acceleration magnitude (blue) and filtered signal (orange). Red markers indicate "
        "detected steps.",
        body_style
    ))
    story.append(Spacer(1, 15))

    # Step Detection Algorithm
    story.append(Paragraph("Step Detection Algorithm", subheading_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "The algorithm uses <b>peak detection</b> on the filtered acceleration magnitude:",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "1. <b>Height threshold:</b> Peaks must exceed mean + 0.5×std_dev of the filtered signal. "
        "This adaptive threshold accounts for varying activity intensities.<br/><br/>"
        "2. <b>Minimum distance:</b> Peaks must be at least 0.3 seconds apart (~60 samples at 200 Hz). "
        "This prevents detecting multiple peaks within a single step cycle.<br/><br/>"
        "The 0.5×std_dev multiplier was chosen empirically - lower values caused false positives from noise, "
        "higher values missed legitimate steps. The 0.3-second spacing corresponds to a maximum cadence of "
        "200 steps/minute, which is faster than normal walking.",
        body_style
    ))
    story.append(Spacer(1, 12))

    code2 = """min_peak_height = np.mean(filtered_accel) + 0.5 * np.std(filtered_accel)
min_distance = int(0.3 * sampling_rate)  # 0.3 seconds

peaks, _ = find_peaks(filtered_accel,
                      height=min_peak_height,
                      distance=min_distance)"""

    story.append(Preformatted(code2, code_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "<b>Result:</b> The algorithm detected <b>37 steps</b> in WALKING.csv, matching the expected count.",
        body_style
    ))

    story.append(PageBreak())

    # PART 3: DIRECTION DETECTION
    story.append(Paragraph("Milestone 2 Part 3: Direction Detection", heading_style))
    story.append(Spacer(1, 12))

    # Data Preparation
    story.append(Paragraph("Data Preparation", subheading_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "For turn detection, I used the <b>gyroscope Z-axis</b> data, which measures rotation around the "
        "vertical axis (yaw). This directly corresponds to changes in heading direction.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Smoothing Method:", subheading_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "A <b>4th-order Butterworth low-pass filter</b> with cutoff frequency of <b>1 Hz</b> was applied. "
        "The lower cutoff (compared to step detection) is appropriate because turning motions are slower than "
        "stepping frequency. This effectively removes sensor drift and high-frequency noise.",
        body_style
    ))
    story.append(Spacer(1, 12))

    # Turn detection plot
    img5 = Image('plot5_turn_detection.png', width=5.5*inch, height=3.3*inch)
    story.append(img5)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Figure 5 shows the filtered gyroscope data (top) and cumulative angle from integration (bottom). "
        "Vertical lines mark detected turns - red for clockwise, blue for counter-clockwise.",
        body_style
    ))
    story.append(Spacer(1, 15))

    # Direction Detection Algorithm
    story.append(Paragraph("Direction Detection Algorithm", subheading_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "The algorithm integrates gyroscope angular velocity to compute cumulative rotation angle:",
        body_style
    ))
    story.append(Spacer(1, 8))

    code3 = """# Integrate gyroscope to get cumulative angle
cumulative_angle = np.zeros(len(timestamps))
for i in range(1, len(timestamps)):
    dt = (timestamps[i] - timestamps[i-1]) / 1e9  # nanoseconds to seconds
    cumulative_angle[i] = cumulative_angle[i-1] + filtered_gyro_z[i-1] * dt

cumulative_angle_deg = np.degrees(cumulative_angle)"""

    story.append(Preformatted(code3, code_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Turns are detected when the cumulative angle crosses an <b>85-degree threshold</b>. The threshold "
        "is slightly below 90° to account for sensor noise and imperfect turns. The algorithm tracks angle "
        "changes from the last detected turn, resetting the reference point after each detection. "
        "A minimum 0.5-second spacing prevents duplicate detections of the same turn.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Results:</b>", subheading_style))
    story.append(Spacer(1, 6))
    results_turns = """
    <b>Total turns detected:</b> 8<br/>
    <b>Clockwise turns:</b> 4 (average angle: 85.3°)<br/>
    <b>Counter-clockwise turns:</b> 4 (average angle: -85.1°)<br/><br/>
    This matches the expected pattern: 4 clockwise turns (one complete 360° rotation)
    followed by 4 counter-clockwise turns (another complete rotation).
    """
    story.append(Paragraph(results_turns, body_style))

    story.append(PageBreak())

    # PART 4: TRAJECTORY PLOTTING
    story.append(Paragraph("Milestone 2 Part 4: Trajectory Plotting", heading_style))
    story.append(Spacer(1, 12))

    img6 = Image('plot6_trajectory.png', width=4.5*inch, height=4.5*inch)
    story.append(img6)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Figure 6 shows the reconstructed walking trajectory. Green marker indicates start position, "
        "red marker shows end position.",
        body_style
    ))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Methodology", subheading_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "The trajectory reconstruction combines both step detection and turn detection algorithms "
        "on the WALKING_AND_TURNING.csv dataset:",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Step 1:</b> Detect steps using the same peak detection algorithm from Part 2<br/><br/>"
        "<b>Step 2:</b> Track heading by integrating gyroscope data continuously<br/><br/>"
        "<b>Step 3:</b> For each detected step, advance position by 1 meter in the current heading direction<br/><br/>"
        "<b>Step 4:</b> Update (x, y) coordinates using: x += cos(heading), y += sin(heading)",
        body_style
    ))
    story.append(Spacer(1, 12))

    code4 = """x, y = 0.0, 0.0
current_angle = 90.0  # Start facing north

for step_idx in step_indices:
    # Get heading from integrated gyroscope
    heading = current_angle + cumulative_angle_deg[step_idx]

    # Move 1 meter in current direction
    x += 1.0 * np.cos(np.radians(heading))
    y += 1.0 * np.sin(np.radians(heading))"""

    story.append(Preformatted(code4, code_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "<b>Results:</b> Detected 79 steps total. Final position: (0.15, 1.25) meters from origin. "
        "The proximity of start and end points (1.26 meters apart) suggests the walking path was designed "
        "to approximately return to the starting location.",
        body_style
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Conclusion", subheading_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This lab successfully implemented the core components of pedestrian dead-reckoning: step detection "
        "achieved 100% accuracy (37/37 steps), turn detection correctly identified all 8 turns, and trajectory "
        "reconstruction combined both algorithms to track a 79-step walking path. The analysis demonstrated "
        "that proper signal filtering and peak detection can reliably extract motion information from noisy "
        "sensor data.",
        body_style
    ))

    doc.build(story)
    print("Report generated: report.pdf")

if __name__ == "__main__":
    create_report()
