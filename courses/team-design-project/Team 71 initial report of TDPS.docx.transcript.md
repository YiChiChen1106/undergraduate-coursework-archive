# Team 71 initial report of TDPS

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

UESTC3010 Team Design Project and Skills

Initial Design Report

Vortexedge

Team No. 71

No

Team member

GUID

UESTC ID

1

Xu Zijun

[student-id-redacted]

[student-id-redacted]

2

Chen Yichi

[student-id-redacted]

[student-id-redacted]

3

Zhou Hancheng

[student-id-redacted]

[student-id-redacted]

4

Zhou Zhihan

[student-id-redacted]

[student-id-redacted]

5

Li Sihang 

[student-id-redacted]

[student-id-redacted]

6

Liu Junyan

[student-id-redacted]

[student-id-redacted]

REPORT (1445 words)

Our drone system is designed with a modular architecture. The design concept is based on sensor fusion and modular design, ensuring that the drone can efficiently and stably complete all tasks. We have used flight controller to be in charge of the drone's attitude control and stable flight, ensuring actions such as take-offs and hovering. The optical flow sensor provides real-time speed and position information, aiding the drone in maintaining stability in complex environments. The visual recognition module detects the appointed areas through a camera, identifies the location of packages and markers, offering crucial support for the mission. The communication module would be used to send out a "mission accomplished" message via a wireless signal transmitter to fulfil the communication function of the task.

The essence of the system design lies in the collaboration between modules. Consequently, we have chosen the STM32F427 as the core processor for task logic, responsible for processing sensor data and executing mission commands. This ensures that the drone can fly along a predetermined route. The main control board communicates with each module via SPI, I2C, or UART interfaces, guaranteeing efficient data transmission and processing. The optical flow sensor transmits speed and position data to the main control board through the I2C interface. Based on this data, the main control board sends instructions to the flight controller to adjust the flight height and manoeuvres. Subsequently, the visual recognition module captures image data through the camera and relays the processed target location information to the main control board via the SPI interface. Using this information, the main control board determines the package's location and plans a pickup route. Finally, the main control board also exchanges data with the communication module, ensuring that information can be transmitted promptly upon mission completion.

Regarding the power system, we have carefully selected and configured the battery, electronic speed controller (ESC), and motor to ensure the drone has sufficient power to complete all tasks. High-performance lithium batteries, with their high voltage and large capacity, can provide stable power to the entire system. The ESC, as a key component in power transmission, is responsible for efficiently transferring power from the battery to the motor. The flight controller adjusts the motor speed and torque output via PWM signals in accordance with the main control board's instructions, ensuring the drone’s correct flight path. The whole system framework is displayed at the following figure.

Motor

The high-torque brushless motor serves as the propulsion core, directly enabling Task 1 (Vertical Take-off), Task 2 (High-Speed Tunnelling), and Task 5 (Precision Payload Delivery). Its 23mm stator diameter and 6mm height optimize power density, generating 2200KV-class thrust while maintaining a 32g weight—critical for agile manoeuvres in confined spaces. Advanced copper winding and cooling fins ensure thermal stability under 95C battery loads, sustaining performance during Task 3 (Obstacle Avoidance) rapid direction changes.

Compatible with 5" tri-blade propellers (131.8mm diameter, 3.6in pitch), it achieves a 6:1 thrust-to-weight ratio, allowing 15m/s² acceleration for Task 2 (Emergency Tunnel Entry). The anti-vibration shaft design minimizes harmonic interference with flight controllers during Task 4 (Sensor-Based Search). Integrated noise suppression aligns with 20A ESCs, ensuring clean telemetry for Task 6 (Autonomous Landing).

Battery

The 4S 1300mAh LiPo battery delivers mission-critical power consistency across all tasks. Its 95C discharge rate sustains peak thrust demands during Task 1 (Instant Take-off) and Task 2 (Tunnel Sprinting), while graphene-enhanced cells mitigate voltage sag below 14.8V—essential for stable ESC operation during Task 5 (Low-Altitude Hovering).

Weighing 180g, it integrates seamlessly with 5" frames, preserving aerodynamic balance for Task 3 (Collision Recovery). The XT60 connector’s 0.5mΩ resistance ensures 20A current flow with minimal loss, critical for Task 4 (Extended Search Operations). Post-mission, the built-in balancing circuit enables rapid 1C charging, aligning with iterative testing schedules.

ESC

20A electronic speed controller (ESC, peaking at 30A) bridges motor responsiveness and flight controller commands. Its BLHeli_32 firmware dynamically adjusts PWM frequency, eliminating signal jitter during Task 2 (Tunnel Navigation) and Task 5 (Marker-Aligned Drop-off). The 30A burst capacity supports momentary overloads without thermal cutoff—vital for Task 1 (Abortive Landing Recovery).

Operating across 3-4S voltages (11.1~14.8V), it excludes onboard BEC, isolating noise-sensitive components during Task 6 (Wireless Communication Calibration). The 14g weight and 52mm form factor reduce frame clutter, optimizing airflow for Task 4 (high-velocity tracking).

Frame & Propellers

Unibody carbon fibre frame (220mm wheelbase) combines torsional rigidity and 25mm stack clearance, accommodating flight controllers and sensors for Task 3 (Multi-Directional Collision Avoidance). Tool-less arm swaps enable rapid propeller adjustments during Task 1 (Thrust Profile Optimization).

Tri-blade propellers (PC material, 4.2g each) leverage 15mm blade width and 3.6in pitch to maximize lift-to-drag efficiency—critical for Task 5 (Sub-1m Altitude Precision). The 5mm hub bore ensures vibration-free coupling with motor shafts, while crash-resistant geometry aids Task 2 (Post-Impact Tunnel Re-entry). Combined with the motor-ESC chain, this system achieves 6:1 thrust-to-weight ratios, enabling mission-grade agility.

Flight Controller

The PIX2.4.8 flight controller is central to this drone design project, responsible for Task 1 (Take-off), Task 2 (Tunnelling), Task 3 (Obstacle avoidance), Task 4 (Package search and pickup), Task 5 (Marker search and precise package drop-off), and Task 6 (Landing and wireless communication). Its advanced sensor fusion and robust control algorithms enable the drone to efficiently handle complex environmental situations, greatly enhancing mission success.

Based on the PX4 platform—originally developed from the PIXHAWK project at ETH Zurich—PIX2.4.8 is acclaimed as a leading open-source flight controller, providing cost-effective yet high-performance autopilot solutions for academia, hobbyists, and industry. Managed by the Dronecode Foundation under the BSD license, it supports commercial applications in visual navigation, multi-drone coordination, and target tracking.

Compared to our previously considered F4V3SPLUS, PIX2.4.8 offers superior computational power, enhanced sensor integration, and greater flight stability. Its mature firmware and comprehensive mission-planning tools simplify development, significantly improving project reliability and efficiency.

Optical Flow Sensor

The major reason why we picked PX4FLOW v1.3.1 optical flow sensor is that it has an ability to deliver precise ground velocity measurements and stable positioning even in low-GPS environment, which is quite suitable for the in-door test site. This ability is achieved by using high-resolution imaging paired with a built-in 3-axis gyroscope to calculate motion along the X and Y axes, ensuring accurate hovering and navigation.  

To be more specific, the PX4FLOW sensor contributes to these key tasks in our project:

Task 1 (Take-off): It enables a smooth vertical take-off and rapid stabilization into a hover.

Task 2 (Tunnelling): It ensures the drone maintains a precise trajectory through narrow spaces.

Task 3 (Obstacle Avoidance): It supports accurate horizontal positioning, allowing the drone to safely navigate around obstacles.

Tasks 4 & 5 (Package Search, Pickup, and Drop-off): It provides the precision needed for accurate package handling.

Task 6 (Landing and Communication): It assists in controlled descent and stable landing, ensuring reliable communication post-landing.

Overall, its ability to operate without GPS, combined with its high-precision and robust performance, makes the PX4FLOW sensor indispensable for our project.

Remote Control

We selected the Radiolink AT9S Pro primarily for its reliability and comprehensive control features during the initial flight tests. With 12 full-function channels, it provides enough flexibility to evaluate manoeuvres necessary for various mission tasks—such as Task 1 (Take-off), Task 3 (Obstacle Avoidance), or Tasks 4 & 5 (Package Search, Pickup, and Drop-off)—before moving on to autonomous, program-based control. Its advanced FHSS and DSSS16 frequency-hopping protocols provide robust anti-interference capabilities, ensuring stable communication and more accurate test results.

Beyond signal stability, the AT9S Pro also integrates a 32-bit ARM MCU and TI’s CC2533 wireless module for heightened responsiveness and range, which is especially helpful in early-stage trials when adjustments and troubleshooting are common. Once these tests confirm the drone’s ability to perform each required task, the remote is no longer needed, and the flight controller transitions to fully automated operation.

Receiver

We chose the R9DS receiver for its compact size (just 10.5g) and the option of 9 or 10 channels, depending on whether it’s set to PWM or SBUS mode. This setup pairs well with the Radiolink AT9S Pro transmitter we selected and delivers the precision we need during initial tests for Task 1 (Take-off), Task 3 (Obstacle Avoidance) and Task 4 & 5 (Package Search, Pickup, and Drop-off).

Moreover, a standout feature of the R9DS is its dependable range—reaching up to 4000 meters under optimal conditions—thanks to FHSS frequency hopping on the 2.4GHz ISM band. This method ensures a stable signal and reduces interference, improving control consistency across different testing environments. The receiver can also relay telemetry data, such as battery voltage, when paired with a PRM module, and it accommodates a wide input voltage range (3.6–12V). These attributes provide stable flight performance, easier troubleshooting, and a smoother transition from manual flight tests to fully autonomous missions.

GANTT CHART