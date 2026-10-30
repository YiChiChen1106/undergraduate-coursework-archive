# YiChi Chen-[student-id-redacted]-lab1

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Lab Title:

Power electronics

Your Chinese Name:

陈一驰

UESTC ID:

[student-id-redacted]

Instructor:

Lian Ping

Teaching Assistant:

Hu Zhenghao

Date Performed:

2025.4.4

Score:

Abstract

This laboratory session aimed to familiarize us students with fundamental voltage and current waveform measurements common in power electronics, emphasizing waveform analysis through key parameters such as frequency, peak voltage (Vpk), mean, and root mean square (RMS) values. The experiments utilized essential electronic testing equipment, including a digital storage oscilloscope, digital multimeter (DMM), and function generator. Specifically, students explored the characteristics of sinusoidal and pulse-width modulation (PWM) waveforms, gaining practical skills in accurate measurement techniques and parameter calculation. Additionally, the lab incorporated hands-on experience in generating PWM signals using the TL494 PWM control integrated circuit, highlighting its practical application in power electronic systems.

Introduction

The intersection of Electrical/Electronic, Aerospace, and Mechanical Engineering disciplines is prevalent in modern engineering applications. Engineers across these fields require foundational knowledge of power electronics technology to effectively contribute to multidisciplinary projects. In power electronic circuits operating under steady-state conditions, voltages and currents typically exhibit periodic behavior. Understanding these periodic waveforms—beyond traditional sinusoidal forms—is essential due to their frequent occurrence in real-world applications. Consequently, measuring and analyzing parameters like peak voltage (Vpk), mean voltage, and RMS voltage become critical, given their practical implications on component design and system efficiency.

The experiments conducted aimed to enhance proficiency in waveform analysis, focusing explicitly on measuring waveform characteristics using equipment such as oscilloscopes and DMMs. Moreover, the laboratory sessions provided exposure to PWM techniques, widely utilized in controlling power electronic devices, by employing the TL494 integrated circuit. PWM techniques are fundamental in controlling voltage levels efficiently in various industrial applications, including motor speed control, lighting control, and power supply regulation. Thus, this laboratory offered both theoretical insights and practical skills necessary for advanced studies and professional practices in power electronics engineering.

Methodology

Experiment 1: Measurement of Waveform Period and Calculation of Frequency

In this experiment, waveform period and frequency measurements were performed using a digital storage oscilloscope (GDS 2104E) and a function generator (Rigol DG4082). Initially, a sinusoidal waveform was generated at selected frequencies of 500 Hz, 1000 Hz, and 2000 Hz.10V For each frequency, the waveform was carefully adjusted using the oscilloscope’s volts/div, time base, and triggering level controls to ensure a stable and clear display.

The period of each waveform was measured manually by observing the waveform display on the oscilloscope and calculating the frequency accordingly. These manually calculated frequencies were subsequently cross-verified using the oscilloscope’s built-in automatic frequency measurement feature to ensure accuracy. All measurement results, including both manually calculated and automatically measured frequencies, were recorded using a mobile phone memo application for subsequent analysis.

This systematic procedure allowed for a precise evaluation of the oscilloscope measurement accuracy compared with the function generator's nominal frequency settings.

Experiment 2: Measurement of Peak/RMS Value of a Sinusoidal Waveform

In this experiment, peak and RMS values of sinusoidal waveforms were measured and analyzed. The sinusoidal signals were generated at a fixed frequency of 1000 Hz using the Rigol DG4082 function generator at three different voltage amplitudes: 3V, 5V, and 8V. Measurements of peak voltage (Vpk) were manually conducted using the Keysight 2104E oscilloscope, and corresponding RMS values were calculated using the standard sinusoidal RMS relationship (Vrms = Vpk/√2).

The calculated RMS values were then validated by measuring the RMS directly using a digital multimeter (GW Instek GDM-8352) set to the AC measurement mode. To enhance accuracy and consistency, oscilloscope automatic measurement functions were employed as an additional reference. All experimental data, including peak and RMS values, were consistently recorded using a mobile phone memo application.

Experiment 3: Measurement of RMS Value of Sinusoidal Waveform with DC Offset

In this experiment, RMS values of sinusoidal waveforms with DC offsets were investigated. The function generator (Rigol DG4082) was set to generate a sinusoidal waveform at a fixed frequency of 1 kHz with three distinct amplitude and DC offset combinations: AC 5V with DC 1V, AC 3V with DC 1V, and AC 5V with DC 2V.

For each waveform configuration, peak-to-peak voltages (Vpk-pk) and DC offset levels were measured using the Keysight 2104E oscilloscope. The corresponding AC RMS and DC RMS voltages were calculated separately, and the total RMS voltage was determined using the relationship Vrms-total=Vrms-AC2+Vrms-DC2. These calculated RMS values were cross-validated using the digital multimeter (GW Instek GDM-8352) set for both DC and AC voltage measurements.

Automatic measurement functions and input coupling options (AC and DC coupling) of the oscilloscope were employed to ensure measurement accuracy. All measurement data were consistently recorded using the mobile phone memo application for further analysis.

Experiment 4: Measurement of Square Wave Duty Cycle(1K hz)

In this experiment, the duty cycle of square wave signals was measured. A square waveform with an amplitude of approximately 2V and a DC offset ensuring a 0V baseline was generated using the Rigol DG4082 function generator. Three distinct duty cycle settings (40%, 50%, and 80%) were selected and measured using the Keysight 2104E oscilloscope.

Measurements of the duty cycle were conducted manually using the oscilloscope display and subsequently cross-verified using the oscilloscope’s automatic measurement functionality for enhanced accuracy. All duty cycle measurement data were recorded consistently in the mobile phone memo application for analysis and comparison.

Experiment 5: Relationship between Mean Voltage and Duty Cycle

This experiment aimed to verify the relationship between mean voltage and duty cycle in square wave signals. A square waveform with a peak voltage of approximately 2V and a 0V baseline was generated using the Rigol DG4082 function generator. Three different duty cycle settings (40%, 50%, and 80%) were selected for investigation.

For each duty cycle setting, the mean (average) voltage was measured directly using the GW Instek GDM-8352 digital multimeter set to DC voltage measurement mode. The corresponding duty cycle values were confirmed using the Keysight 2104E oscilloscope’s automatic measurement features. All experimental data, including the measured mean voltages and corresponding duty cycles, were recorded using the mobile phone memo application for subsequent analysis and validation of the theoretical relationship Vmain=D×Vpk.

Experiment 6: TL494-based PWM Signal Generator

In this experiment, a PWM signal generator circuit based on the TL494 IC was constructed and tested according to the provided schematic. A Rigol DP832 adjustable DC power supply provided the necessary operating voltage (+12V) for the TL494 circuit. The circuit was configured with a timing capacitor (CT = 0.01 μF) and a timing resistor (RT = 2.2 kΩ), calculated to achieve an oscillator frequency of approximately 50 kHz using the relationship f=1.1RT×CT..

The circuit was assembled as follows:

Connect +12V DC from Rigol DP832 to Vcc (pin 12) and ground to GND (pin 7).

Connect the timing capacitor (CT = 0.01 μF) from pin 5 to ground.

Connect the timing resistor (RT = 2.2 kΩ) between pins 5 and 6.

Connect pins 4 (deadtime control) and 13 (output control) to ground for maximum duty cycle and single-ended output mode.

Connect pin 14 (reference voltage output, +5V) through a resistor divider to create adjustable control voltages between 0.5V and 3.5V, feeding into pin 1.

Ensure pins 2 and 3 are connected to form a voltage follower, and connect pin 15 (error amp 2) to pin 14 through a 50 kΩ resistor.

Connect output pins (9 and 10) through appropriate pull-up resistors to +12V DC and measure the PWM output signals.

During the test, three specific control voltages (1V, 2V, and 3V) were applied. The resulting PWM output duty cycles from pins 9 and 10 were observed and measured using the Keysight 2104E oscilloscope with automatic measurement functions for accuracy. All experimental data, including control voltages and corresponding PWM duty cycles, were consistently recorded in the mobile phone memo application.

Result

Experiment1

Table 1. Measurement Results of Waveform Frequency and Period

Nominal Frequency (Hz)

Measured Period (ms)

Measured Frequency (Hz)

Percentage Error (%)

500

1.990

502

0.4%

1000

1.000

1000

0.0%

2000

0.502

1992

0.4%

Note: The results above were obtained directly from oscilloscope screenshots.

The measured frequencies showed high consistency with the nominal values set by the function generator, with errors maintained within ±0.4%. Specifically, the largest observed deviation was at the frequency of 2000 Hz, where the measured value was approximately 1992 Hz, resulting in a minimal error of 0.4%.

Experiment2

Table 2. Measurement of Peak and RMS Voltages

Nominal Peak Voltage (V)

Oscilloscope Peak-to-Peak Voltage (Vpp)

Calculated RMS Voltage (Vrms)

DMM Measured RMS Voltage (Vrms)

Percentage Error (%)

3

6.04

2.135

2.1169

0.85%

5

10.2

3.606

3.5237

2.28%

8

16.0

5.657

5.6500

0.12%

Note: Calculated RMS Voltage (Vrms) = (Vpp/2) / √2.

The measurements showed good agreement between the calculated RMS values and the RMS values measured directly by the digital multimeter. The largest deviation observed was 2.28% at the 5 V nominal peak voltage, indicating overall accuracy in the measurement procedures.

Experiment3

Table 3. Measurement of RMS Voltages with DC Offset

Configuration (AC/DC)

Oscilloscope Vpp (V)

DMM Measured RMS Voltage (Vrms)

AC 5V / DC 1V

10.1

3.6644

AC 3V / DC 1V

6.00

2.3421

AC 5V / DC 2V

10.1

4.0577

Note: Oscilloscope measured Vpp includes AC amplitude only.

The RMS voltages measured using the digital multimeter reflect the combined effects of both AC amplitude and DC offset, matching theoretical expectations closely. The observed results confirm the correctness of the RMS voltage formula for waveforms with DC offsets:

Vtotal-rms2=VAC-rms2+VDC-rms2

Experiment4

Table 4. Measurement of Square Wave Duty Cycle

Nominal Duty Cycle (%)

Oscilloscope Measured Duty Cycle (%)

Measurement Error (%)

40

39.80

0.50%

50

50.00

0.00%

80

80.00

0.00%

The measurements closely match the nominal settings, showing very high accuracy in duty cycle generation and measurement. The maximum deviation observed was only 0.50% at the 40% nominal duty cycle setting.

Experiment5

Table 5. Measurement of Mean Voltage with Varying Duty Cycles

Duty Cycle (%)

Theoretical Mean Voltage (V)

DMM Measured Mean Voltage (V)

Percentage Error (%)

40

1.60

1.6001

0.01%

50

2.00

2.0002

0.01%

80

3.20

3.2001

0.00%

Note: Theoretical mean voltage calculated as Vmean=Duty cycle×Vpeak

The measurements demonstrated extremely high precision, closely aligning with the theoretical values. The maximum observed deviation was minimal at 0.01%, confirming the direct proportionality between duty cycle and mean voltage.

Experiment 6 

Table 6. TL494 PWM Duty Cycle vs. Control Voltage

Pin 1 Voltage (V)

PWM Output Duty Cycle (Q1, %)

PWM Output Duty Cycle (Q2, %)

Measured Oscillator Frequency (kHz)

0.5

95.02

95.05

52.8

1.0

94.23

94.24

52.8

1.5

77.44

77.51

52.8

2.0

60.60

60.65

52.8

2.5

43.74

43.81

52.8

3.0

26.90

27.01

52.8

3.5

10.10

10.16

52.8

Sawtooth Wave Observation:A sawtooth waveform was captured at pin 5 (timing capacitor node). The waveform exhibits a linear rising ramp followed by a rapid reset, which is characteristic of the TL494 oscillator. The measured frequency of this sawtooth waveform is approximately 52.8 kHz, closely matching the designed target of 50 kHz (considering component tolerances).

Discussion

Experiment 1: Measurement of Waveform Period and Calculation of Frequency

The measured frequencies were found to be in very close agreement with the nominal values provided by the function generator. The slight deviations (approximately 0.4% error) can be attributed to inherent instrument limitations, minor human reading errors, and potential environmental interference. The consistency between manually calculated frequencies and those obtained via the oscilloscope's automatic measurement functionality validates the accuracy and reliability of the measurement method.

Experiment 2: Measurement of Peak/RMS Value of a Sinusoidal Waveform

In Experiment 2, both the calculated RMS values (derived from the measured peak-to-peak voltage) and the directly measured RMS values using the digital multimeter showed strong concordance. The minor discrepancies, with the largest error being around 2.28% at a 5 V nominal peak, indicate that the theoretical relationship Vrms=VPK2 ​​ holds well under practical conditions. These small differences may arise from the resolution limits of the oscilloscope and multimeter, as well as potential variations in the waveform amplitude due to circuit tolerances.

Experiment 3: Measurement of RMS Value of Sinusoidal Waveform with DC Offset

The experiments involving waveforms with a DC offset demonstrated the expected behavior where the total RMS voltage is a combination of both the AC and DC components, as given by:

Vtotal-rms2=VAC-rms2+VDC-rms2

The measured results closely matched theoretical predictions, indicating that the method for separating and calculating the AC and DC contributions was effective. Any slight discrepancies might be due to measurement resolution or small interference effects, yet overall the results confirm the validity of the RMS calculation method for combined AC and DC signals.

Experiment 4: Measurement of Square Wave Duty Cycle

The square wave duty cycle measurements were very accurate, with the measured values nearly identical to the nominal settings. For example, the measured duty cycle for the 40% setting deviated by only 0.50%. This high level of precision indicates that both the signal generation and the measurement techniques are reliable. The minimal error observed can be attributed to factors such as the oscilloscope’s resolution and potential slight variations in the waveform due to inherent device tolerances.

Experiment 5: Relationship between Mean Voltage and Duty Cycle

The relationship  Vmean=Duty cycle×Vpeak​ was clearly validated by the experimental data. The measured mean voltages at duty cycles of 40%, 50%, and 80% were almost identical to the theoretical values, with errors of less than 0.01%. This strong correlation reinforces the direct proportionality between duty cycle and average output voltage in PWM signals. Such results not only confirm the theoretical predictions but also highlight the effectiveness of the experimental setup and measurement procedures used.

Experiment 6: TL494-based PWM Signal Generator Discussion

The experimental results show that the TL494 PWM circuit responds as expected to variations in the control voltage. As the control voltage applied at pin 1 increases from 0.5 V to 3.5 V, the observed duty cycles at outputs Q1 and Q2 decrease consistently—from approximately 95% at 0.5 V to around 10% at 3.5 V. This inverse relationship confirms the TL494's design, where higher control voltages result in shorter on-times due to the comparator and error amplifier configurations.

Additionally, the sawtooth waveform captured at pin 5 validates the proper operation of the oscillator circuit. The measured frequency of approximately 52.8 kHz is very close to the target design frequency of 50 kHz, considering component tolerances (with RT = 2.2 kΩ and CT = 0.01 μF). This agreement indicates that the timing network is functioning correctly and that the TL494 is operating within the expected parameters.

Minor deviations in the measured duty cycles (typically within 0.1–0.5%) can be attributed to instrument resolution, slight variations in component values, and environmental factors such as wiring noise. Overall, the experiment confirms that the TL494 is capable of generating stable PWM signals over a wide range of duty cycles, which is essential for applications in switching power supplies and motor control systems.

Conclusion

This series of experiments provided a comprehensive understanding of various waveform measurement techniques and PWM generation, highlighting both theoretical and practical aspects of power electronics. In Experiment 1, the close agreement between the manually calculated and oscilloscope-measured frequencies validated the accuracy of our measurement approach. Experiment 2 demonstrated that the theoretical relationship between peak voltage and RMS voltage holds true in practice, with minimal errors between calculated and directly measured RMS values.

Experiment 3 extended these findings to waveforms with DC offsets, confirming that the total RMS voltage can be accurately determined by considering both AC and DC components. In Experiment 4 and Experiment 5, the precise control of duty cycle and its direct impact on the mean voltage were clearly established, reinforcing the theoretical relationship Vmean=Duty cycle×Vpeak

Finally, Experiment 6 showcased the effective operation of a TL494-based PWM signal generator. The observed inverse relationship between control voltage and duty cycle, along with the stable sawtooth waveform at the oscillator pin, confirmed that the circuit met the design expectations, despite minor deviations due to component tolerances and environmental factors.

Overall, the experiments not only confirmed the theoretical principles underlying waveform measurement and PWM control but also provided practical insights into instrument usage, circuit assembly, and data analysis. The techniques and results demonstrated here lay a solid foundation for further exploration in power electronics and control systems. Future work may involve optimizing circuit layouts to reduce interference and exploring advanced modulation techniques for enhanced performance.

Appendices

Experiment1

Experiment2

Experiment3

Experiment 4

Experiment 5

Experiment 6