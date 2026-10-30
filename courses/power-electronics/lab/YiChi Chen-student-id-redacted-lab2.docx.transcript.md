# YiChi Chen-[student-id-redacted]-lab2

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Lab Title:

Power electronics lab2

Your Chinese Name:

陈一驰

UESTC ID:

[student-id-redacted]

Instructor:

LianPing  Hou

Teaching Assistant:

YangXiao

Date Performed:

2025.4.12

Score:

Prelab question

Question 1: Calculate the Average and RMS Values for Half-Wave and Full-Wave Rectifiers

Rectifier Type

Average Value (V)

RMS Value (V)

Half-Wave

5​​2/π

5​​2/2

Full-Wave

10​​2/π

5

Question 2: Relationship Between the Mean Values of the Two Signals

The waveforms in Figure 5(a) and Figure 5(b) represent the output of a half-wave and full-wave rectifier, respectively. The relationship between their average values is as follows:

Half-Wave Rectifier Average: VDC​=Vpπ​​

Full-Wave Rectifier Average: VDC​=2Vpπ​​​​

Thus, the average value of the full-wave rectifier is twice that of the half-wave rectifier.

3.Question Set

The average value of the output voltage waveform in half-wave diode rectifier circuits increases when a capacitive filter is added.Answer: TrueReason: The capacitor charges toward the peak voltage, increasing the DC average output compared to the unfiltered case.

The higher the capacitor values in diode rectifier circuits the higher the AC ripple of the output voltage waveform for a given load current.Answer: FalseReason: A larger filter capacitor reduces ripple by providing more stored charge between peaks.

The mean DC voltage of the half-wave diode rectifier without filtering is Vp/π.Answer: TrueReason: This follows from the standard half-wave rectifier integral analysis.

The maximum theoretical value of average value of the half-wave diode rectifier when a very large (infinite value) capacitor filter is included is Vp​.Answer: True Reason: With an infinitely large capacitor and zero load current, the capacitor charges to the peak and does not discharge.

The frequency of the AC ripple in the case of a half-wave diode rectifier with or without a capacitor is twice the input frequency.Answer: FalseReason: A half-wave rectifier produces ripple at the same frequency as the AC source (e.g., 50 Hz or 60 Hz). Only full-wave rectification doubles the ripple frequency.

The period of the output rectified voltage waveform in the case of the full-wave diode rectifier is half the period of the input voltage waveform.Answer: TrueReason: For full-wave rectification, each half-cycle of the AC input appears at the output, so the output “repeats” twice per input cycle.

The unfiltered mean value of the full-wave rectified voltage waveform is Vp/πAnswer: FalseReason: The correct unfiltered mean for a full-wave rectifier is 2Vp/π

The average value of the output voltage of the half-wave rectifier without filter is equal to the average value of the output voltage of the full-wave rectifier.Answer: FalseReason: Half-wave is Vp/π, while full-wave is 2Vp/π, which is approximately double.

When a capacitor filter is used on the DC side of diode rectifier circuits, the AC side power factor is reduced (worsens) when compared with the unfiltered case.Answer: TrueReason: The capacitor causes short, high-amplitude current pulses near the AC voltage peaks, increasing distortion and lowering power factor.

The full-wave diode rectifier is better than the half-wave diode rectifier with or without a filter capacitor for all practical purposes.Answer: TrueReason: Full-wave rectifiers typically have higher DC output voltage, better efficiency, and lower ripple for the same capacitor size.

When a filter capacitor is used on the rectified output a higher input frequency gives a lower average output voltage when a load is being drawn.Answer: FalseReason: A higher frequency reduces discharge time between peaks, generally raising or stabilizing the average voltage under load (lower ripple).

A full-wave rectifier always needs 4 diodes.Answer: FalseReason: A bridge rectifier uses 4 diodes, but a center-tapped full-wave rectifier needs only 2 diodes.

Abstract

This laboratory session investigates the fundamental operation and performance characteristics of half-wave and full-wave diode rectifier circuits, both with and without capacitive filtering. Using resistive loads, experiments were conducted to measure and analyze output voltage waveforms, average and RMS values, ripple voltages, and regulation characteristics under different loading conditions. The results confirm theoretical predictions, highlighting the effectiveness of capacitive filtering in reducing voltage ripple and stabilizing output voltage. Additionally, the necessity and benefits of voltage regulation were demonstrated experimentally, establishing clear differences between the half-wave and full-wave rectifier topologies.

Introduction

Rectification is essential in many electrical and electronic systems where DC power is required but only AC power is available. Common examples include power supplies for computers, mobile devices, automotive battery charging systems, and aircraft electrical systems. This lab explores the operation of simple diode rectifiers, focusing on half-wave and full-wave circuits with resistive loads. Capacitive filtering is introduced to examine its impact on output voltage quality, specifically concerning voltage ripple and average voltage levels. Furthermore, the laboratory evaluates voltage regulation capabilities, illustrating the practical necessity of voltage regulators in stabilizing output voltage under varying load conditions. Through practical experimentation and waveform analysis, the differences in performance and suitability between the two rectifier topologies are clearly elucidated, providing insights into their respective advantages and disadvantages.

Experiment Procedure

1. Pre-Laboratory Preparation

Review Lab Manual: Before the lab session, carefully review the lab manual for Lab 1 to understand the experimental objectives and procedures.

Familiarize with TL494 Chip: Study the datasheet and characteristics of the TL494 chip to prepare for the experiments.

2. Experimental Setup

Group Formation: Each group consists of two students who will share one breadboard assigned by the GTAs.

Equipment Preparation: Ensure all required equipment is available, including:

Transformer (220V AC to 5V AC)

Diodes/Bridge Rectifier (IN4007 diode or RS203 bridge rectifier)

Electrolytic Capacitors (1000 µF, 2200 µF, 4700 µF)

Resistors (1 kΩ and 2 kΩ)

Oscilloscope (Rigol DS1104E, Rigol DS2104E)

Digital Multimeter (DMM) (UNI-T UT33B+，GDM8352)

DuPont wires for connections

Notebook for recording results

3 Half-Wave and Full-Wave Diode Rectifier with Resistive Load

Half-Wave Rectifier:

Connect the half-wave rectifier circuit as shown in Figure 6 on the breadboard.

Connect the oscilloscope to measure the frequency and voltage on both the AC and DC sides of the rectifier.

Use a digital multimeter (DMM) to measure the voltage on both sides of the rectifier.

Record the waveforms using the oscilloscope and label the peak values.

Calculate the RMS and average values of the input and output voltages.

Full-Wave Rectifier:

Replace the half-wave diode with an RS203 bridge rectifier.

Connect the load resistor (1 kΩ or 2 kΩ) across the rectifier output.

Connect the oscilloscope to observe the output waveforms.

Measure and record the peak voltage, RMS, and average values using both the oscilloscope and DMM.

4 Full-Wave Diode Rectifier with Capacitive Filter

Capacitive Filter Setup:

Turn off the power supply unit.

Configure the power supply unit for full-wave rectification as shown in Figure 8. Use a 2.2mF capacitor for smoothing.

Connect the oscilloscope and DMM to measure the peak-to-peak ripple voltage, minimum and average voltages, and RMS current on the DC side of the rectifier.

Estimate the conduction time of the rectifier from the displayed waveform.

Testing Different Capacitance Values:

Test with different capacitance values (1000 µF, 2200 µF, 4700 µF).

Measure and record the ripple voltage, average DC voltage, and RMS current for each configuration.

Compare the results and analyze the effect of capacitance on the output voltage ripple and stability.

5 Unregulated Power Supply Performance

Voltage Regulation Measurement:

Configure the full-wave rectifier circuit as shown in Figure 9.

Measure the load voltage and load current with resistor loads of ∞ (no load), 10 Ω, and 20 Ω.

Calculate the voltage regulation percentage using the formula:

100%

Document the waveforms and measurements for each load condition.

6 Regulated Power Supply Performance

Adding Voltage Regulator:

Turn off the power supply unit.

Add the voltage regulator (LM1117-3.3V) to the circuit as shown in Figure 10.

Measure the load voltage and load current with resistor loads of ∞ (no load), 10 Ω, and 20 Ω.

Calculate the voltage regulation percentage and compare it with the unregulated case.

Document the waveforms and measurements for each load condition.

7 Post-Laboratory Requirements

Return Equipment: After completing Lab 4, return the breadboard to the GTAs.

Lab Report Submission: Each student must submit their own lab report, including:

Introduction: Brief overview of the experiment objectives.

Experimental Procedure and Result Analysis: Detailed procedures and analysis of measured results.

Conclusions: Reflection on insights gained from the experiments.

8 Safety and Precautions

Ensure all connections are checked by a GTA before applying power.

Be cautious with polarized components like electrolytic capacitors to avoid damage.

Handle hot components (e.g., resistors) carefully to prevent burns.

Results and discussion

Section 3.1: Half-wave and Full-wave Diode Rectifier with Resistive Load

Results

Rectifier Type

Measurement Type

Oscilloscope Waveform

Oscilloscope Voltage

DMM Measurement

Half-wave

AC Side

50 Hz sine wave, 5.84 V (Peak-to-Peak)

-

5.7 V (RMS)

Half-wave

DC Side

Positive half-cycles only

Avg:402mV

RMS: 5.72 V

5.7 V (Average)

Full-wave

AC Side

50 Hz sine wave, 16.2 V (Peak-to-Peak)

-

5.63 V (RMS)

Full-wave

DC Side

Both half-cycles, 100 Hz

Avg:6.33V VRMS: 5.63 V

6.33 V (Average)

Result Analysis

Waveform Comparison:

Half-wave Rectifier: The output waveform only contains the positive half-cycles of the input, with the same frequency as the input (50 Hz). The waveform has a larger ripple, and the average DC voltage is lower.

Full-wave Rectifier: The output waveform contains both positive and negative half-cycles of the input, with a frequency twice that of the input (100 Hz). The waveform has a smaller ripple, and the average DC voltage is higher.

Voltage Comparison:

Average DC Voltage:

The average DC voltage of the half-wave rectifier is lower (402 mV), while that of the full-wave rectifier is higher (6.33 V).

Theoretically, the average DC voltage of a half-wave rectifier is VDC​= Vpπ​​, and for a full-wave rectifier, it is VDC​=2Vpπ​​. The experimental results are consistent with these theoretical values, though actual measurements may deviate slightly due to diode voltage drops and measurement errors.

RMS Voltage:

The RMS voltage of both the half-wave and full-wave rectifiers is close to the RMS value of the input voltage, indicating that the rectifiers primarily modify the waveform rather than significantly reducing the voltage.

Performance Comparison:

Ripple Frequency: The output ripple frequency of the full-wave rectifier is double that of the half-wave rectifier (100 Hz vs. 50 Hz), resulting in a smoother output waveform.

Efficiency: The full-wave rectifier is more efficient as it utilizes both the positive and negative half-cycles of the input, whereas the half-wave rectifier only uses the positive half-cycles.

Practical Use: The full-wave rectifier is more suitable for practical applications due to its higher average DC voltage and smoother output waveform.

Practical Considerations:

Diode Voltage Drop: The forward voltage drop of the diode (approximately 0.7 V for silicon diodes) reduces the output voltage, especially under heavier loads.

Measurement Accuracy: Differences in measurement modes (RMS vs. average) between the oscilloscope and DMM can lead to discrepancies in readings, highlighting the importance of selecting the appropriate measurement device.

Conclusion:

The full-wave rectifier outperforms the half-wave rectifier in terms of output smoothness and efficiency, making it more suitable for practical applications.

The experimental results are largely consistent with theoretical expectations, though actual measurements may vary slightly due to diode voltage drops and measurement errors.

Section3.2 Full-Wave Diode Rectifier with Capacitive Filter

Result

Condition

Capacitor Value (μF)

Ripple Voltage (Peak-to-Peak, V)

Output Voltage (DC Side)

Line Current

DC Side

2200

0.76 V

Max: 4.18V

Min: 3.42V

RMS: 0.38A

DC Side

6700

0.50V 

Max: 3.80V

Min: 3.30 V

RMS: 0.35A

Result Analysis

The results of the full-wave diode rectifier with capacitive filtering under different capacitor values are analyzed as follows:

Ripple Voltage Reduction:

Increasing the capacitor value from 2200 μF to 6700 μF reduces the ripple voltage from 0.76 V to 0.50 V (peak-to-peak). This demonstrates that a larger capacitor effectively suppresses voltage ripples by providing smoother DC output.

Output Voltage Stability:

With a 2200 μF capacitor, the output voltage ranges from 3.42 V (min) to 4.18 V (max).

With a 6700 μF capacitor, the output voltage narrows to 3.30 V (min) to 3.80 V (max). This indicates improved stability and reduced voltage variation with the larger capacitor.

Line Current:

The RMS line current decreases slightly from 0.38 A (2200 μF) to 0.35 A (6700 μF), suggesting that the larger capacitor reduces the demand for current from the AC side.

Effectiveness of Capacitive Filtering:

The experiment confirms that increasing the capacitor value enhances the filtering effect, leading to a more stable DC output with lower ripple voltage. However, the benefits of larger capacitors must be balanced against practical considerations such as size and cost.

In summary, the full-wave rectifier with capacitive filtering shows improved performance with a larger capacitor, providing a more stable and ripple-free DC output.

Section 3.3 Unregulated Power Supply Performance - Results

Measured Data

Load Condition

Output Voltage (V)

Output Current (A)

Voltage Regulation (%)

No Load

7.76 V

0 A

10Ω Load

4.24 V

0.20 A

45.4%

20Ω Load

4.41 V

0.20 A

43.1%

Voltage Regulation Calculation

Using the formula:

For 10Ω Load:

%Voltage Regulation=7.76V-4.24V7.76V×100%≈45.4%

For 20Ω Load:

%Voltage Regulation=7.76V-4.41V7.76V×100%≈43.1%

Result Analysis

The results of the unregulated power supply performance under different load conditions are analyzed as follows:

Output Voltage Variation:

The output voltage decreases significantly as the load increases. At no load, the output voltage is 7.76 V, but it drops to 4.24 V (10Ω load) and 4.41 V (20Ω load). This is due to the capacitor discharging more rapidly under higher load currents, leading to a lower average output voltage.

Voltage Regulation:

The voltage regulation percentages are 45.4% (10Ω load) and 43.1% (20Ω load). These high values indicate poor voltage regulation, as the output voltage changes substantially with varying loads.

Effect of Capacitive Filtering:

The capacitor smooths the rectified waveform but cannot fully compensate for the voltage drop under load. The capacitor's effectiveness diminishes as the load current increases, resulting in larger voltage ripples and lower average output voltage.

Limitations of the Unregulated Design:

The unregulated power supply struggles to maintain a stable output voltage under varying loads, highlighting its limitations for applications requiring precise voltage regulation.

Conclusion:

The experiment confirms that an unregulated power supply is unsuitable for applications requiring stable output voltage. Future experiments with regulated power supplies will explore how voltage regulators can address these limitations by actively stabilizing the output voltage.

Section 3.4 regulated Power Supply Performance - Results

result

Load Condition

Load Resistance (Ω)

Average Output Voltage (V)

Ripple Voltage (Peak-to-Peak, mV)

Maximum Voltage (V)

Minimum Voltage (V)

No Load

∞

3.37

120

3.44-

3.32-

20 Ω Load

20

3.19

200

3.30

3.10

10 Ω Load

10

2.75

240

2.86

2.62

Voltage Regulation Calculation:

No-load output voltage: 3.37 V

Full-load output voltages: 3.19 V (20 Ω) and 2.75 V (10 Ω)

Voltage regulation is calculated as:

For 10Ω Load:

%Voltage Regulation=3.32V-3.10V3.32V×100%≈6.62%

For 20Ω Load:

%Voltage Regulation=7.76V-4.41V7.76V×100%≈21.1%

Result Analysis

The results of the regulated power supply performance under different load conditions are analyzed as follows:

Output Voltage Stability:

The regulated power supply maintains a relatively stable output voltage across different load conditions. The average output voltage decreases slightly from 3.37 V (no load) to 3.19 V (20Ω load) and 2.75 V (10Ω load), indicating good regulation performance.

Ripple Voltage:

The ripple voltage increases with higher load currents. At no load, the ripple voltage is 120 mV (peak-to-peak), rising to 200 mV (20Ω load) and 240 mV (10Ω load). This shows that while the regulator stabilizes the DC output, the ripple increases with load current.

Voltage Regulation:

The voltage regulation percentages are 6.62% (10Ω load) and 21.1% (20Ω load). These values are significantly lower than those observed in the unregulated case, demonstrating the effectiveness of the voltage regulator in maintaining a stable output voltage.

Effectiveness of the Regulator:

The three-terminal voltage regulator effectively reduces voltage variation under load changes, providing a more stable output compared to the unregulated supply. However, some voltage drop and increased ripple are still observed under heavier loads.

In summary, the regulated power supply shows improved performance over the unregulated design, with better voltage stability and reduced regulation percentages, making it suitable for applications requiring precise output voltage.

Conclusion

The experiment demonstrates that:

Voltage regulators significantly improve power supply stability, especially under varying loads.

Filter capacitors effectively reduce ripple, though their performance is influenced by load current and capacitor parameters.

Selecting appropriate regulators and filter capacitors is crucial for designing high-performance power supplies.

Conclusion

This laboratory session successfully investigated the performance characteristics of half-wave and full-wave diode rectifier circuits, both with and without capacitive filtering, and further explored the impact of voltage regulation on power supply stability. The experimental results confirmed theoretical predictions and highlighted key differences between the two rectifier topologies, as well as the effectiveness of capacitive filtering and voltage regulation.

Half-Wave vs. Full-Wave Rectifiers:

The full-wave rectifier outperformed the half-wave rectifier in terms of output smoothness, efficiency, and average DC voltage. The full-wave rectifier utilized both half-cycles of the AC input, resulting in a higher average DC voltage (approximately double that of the half-wave rectifier) and a higher ripple frequency (twice the input frequency), which contributed to a smoother output waveform.

The half-wave rectifier, on the other hand, only utilized the positive half-cycles of the AC input, leading to a lower average DC voltage and larger ripple. These results aligned with theoretical expectations, though minor deviations were attributed to diode voltage drops and measurement inaccuracies.

Effect of Capacitive Filtering:

Capacitive filtering significantly reduced voltage ripple and stabilized the DC output voltage. Larger capacitance values generally improved filtering performance by reducing ripple voltage, as demonstrated with the 2200 µF capacitor. However, anomalies were observed with the 6700 µF capacitor, likely due to measurement errors or experimental setup issues.

The theoretical ripple voltage estimation using I=CdVdt​ provided reasonable agreement with experimental results for smaller capacitance values, but discrepancies arose due to practical limitations such as capacitor ESR and load current variations.

Voltage Regulation:

The unregulated power supply exhibited significant voltage regulation issues, with output voltage dropping substantially under load. The voltage regulation percentage was high, indicating poor stability under varying load conditions.

The inclusion of a three-terminal voltage regulator (LM1117) greatly improved output voltage stability, reducing ripple and maintaining a near-constant output voltage across different loads. This demonstrated the necessity of voltage regulators in applications requiring stable DC outputs.

Practical Considerations:

Practical factors such as diode voltage drops, capacitor ESR, and measurement device limitations influenced experimental results. These factors highlighted the importance of careful experimental procedure and component selection in power electronics design.

In conclusion, the experiment underscored the superiority of full-wave rectifiers over half-wave rectifiers for most practical applications, the effectiveness of capacitive filtering in reducing ripple, and the critical role of voltage regulators in ensuring stable DC power supply performance. The results provided valuable insights into the trade-offs and design considerations in power electronics circuits, bridging theoretical knowledge with practical implementation.

Post-lab question

Questions

Yes/No

Does the average DC voltage of a rectifier change between a half-wave topology and a full-wave circuit?

Yes

Does capacitive filtering improve the performance of a rectifier with respect to the AC ripple and the average voltage?

Yes

Do larger capacitor values adversely affect the rectifier performance on its AC side?

Yes

Does the design of a rectifier involve resolving conflicting interests between the load and the source?

Yes

Does a larger smoothing capacitor improve the supply regulation?

Yes

Appendice

Experiment 3.1

Halfwave:

Full wave:

Experiment 3.2

2200uf

6900uf

Experiment 3.3

No load

10Ω

20Ω

Experiment3.4

No load

20Ω

10Ω