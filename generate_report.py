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

    doc.build(story)
    print("Report generated: report.pdf")

if __name__ == "__main__":
    create_report()
