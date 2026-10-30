# report

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Title：USRP Timed Transmission in GNU Radio: Transmitter-Receiver System Design

Name: YICHI CHEN

Submission date:2024/8/14

Student ID:[student-id-redacted]

Abstract

This project presented the design and implementation of a transmitter-receiver system using GNU Radio, a powerful tool for software-defined radio (SDR) applications. The primary goal was to develop a system capable of reliably transmitting and receiving signals, with a particular focus on timed transmission. The first version of the program established a basic communication link between the transmitter and receiver, utilizing various GNU Radio blocks to manage signal generation, modulation, transmission, reception, and demodulation. The second iteration of the program introduced a timed transmission feature, setting a specific duration for signal transmission. This enhancement allowed the system to operate within predefined time constraints, making it suitable for applications where precise timing was crucial. The system was tested in a controlled environment, and the results indicated that it successfully transmitted and received signals within the set duration, maintaining signal integrity and reliability. This project demonstrated the flexibility and power of GNU Radio in developing custom SDR applications and highlighted the potential for further optimization and application-specific adjustments in future work.

Introduction

Wireless communication has become a crucial part of our daily lives, with technology constantly evolving to meet the growing need for faster and more flexible systems. Traditional radios rely on hardware to process signals, but with the rise of software-defined radio (SDR), these functions can now be managed through software. This shift allows for quicker updates and the ability to easily switch between different communication protocols, making SDR a valuable tool in the development of modern wireless systems.

At the same time, there’s an increasing interest in using technology to monitor human activities without the need for wearable devices or cameras. This type of monitoring is important in areas like healthcare, where tracking a person’s movements can help in detecting falls or other health issues. However, existing systems often require people to wear sensors, which can be uncomfortable, or use cameras, which can invade privacy. SDR offers a promising alternative by using radio waves to detect human activities in a non-intrusive way.

This project focuses on creating a transmitter-receiver system using GNU Radio, a popular open-source platform for SDR. The goal is to design a system that can send and receive signals within a set time period, a feature that’s important for applications where timing is critical, such as monitoring a patient’s movements in real-time. The project also explores how deep learning can be integrated into the system to improve the accuracy of activity detection.

In simpler terms, this work aims to show how SDR can be used to build a reliable communication system that not only transmits and receives signals efficiently but also does so within precise time limits. This has the potential to improve how we monitor and understand human activities, especially in healthcare settings, without the need for intrusive or expensive equipment.

2.Literature Review

The design and implementation of a software-defined radio (SDR) based transmitter-receiver system, particularly with a focus on timed transmission, draws from the extensive research on SDR technologies and their applications in human activity recognition (HAR). Understanding these applications has provided crucial insights into the potential and limitations of SDR, guiding the development of my project.

2.1 SDR and Human Activity Recognition

SDR's flexibility, which allows radio systems to be controlled via software, has made it an ideal tool for applications requiring adaptability and precision, such as HAR. Saeed [1] used SDR for contactless localization and activity recognition, leveraging the Universal Software Radio Peripheral (USRP) to analyze radio frequency signals and classify human activities. This study highlighted SDR's effectiveness in dynamic environments, providing a basis for understanding how to achieve accurate signal transmission and reception in my project.

Khan [2] explored integrating deep learning with SDR to enhance HAR systems, showing how combining SDR with convolutional neural networks (CNN) and long short-term memory (LSTM) networks significantly improves activity classification accuracy. This research suggests future pathways for integrating machine learning into my SDR system to enhance its capabilities.

Taylor [3] demonstrated SDR's role in healthcare, particularly in monitoring patients' movements using machine learning algorithms to classify activities. Their work shows the importance of creating non-invasive, accurate, and adaptable systems, which is directly relevant to the design of my transmitter-receiver system.

2.2 Relevance to My Project

These studies have significantly shaped the development of my SDR-based system. The focus on HAR highlights the critical role of accurate signal transmission and reception, a central aspect of my project. The timed transmission feature aligns with the need for precise synchronization, as emphasized by Saeed et al. [1]. The potential integration of deep learning, as discussed by Khan et al. [2], offers opportunities for enhancing my system's ability to classify and respond to signal patterns.

In conclusion, the literature provides a strong foundation for understanding SDR's potential in HAR. The research from Saeed, Khan [4], and Taylor [5] has informed the design of my system, contributing to existing knowledge and exploring new possibilities for SDR in synchronized communication and activity recognition.

3.Methodology

As a second-year student with no prior experience in software-defined radio (SDR) or related technologies, setting up the environment for this project was a challenging yet rewarding experience. With guidance from Dr. Zakir and Dr. William Taylor, I embarked on learning how to configure a complex SDR system using a Universal Software Radio Peripheral (USRP) and GNU Radio within a virtualized environment.

The first step was setting up a virtual machine (VM) on my personal computer to run Ubuntu, an open-source operating system essential for SDR development. This was my first time working with virtual machines, so I needed to learn how to install and configure VirtualBox, allocate the right resources like CPU and memory, and ensure Ubuntu ran smoothly. With Dr. Zakir’s help, I optimized these settings to balance the VM’s performance with my computer’s capabilities.

Once Ubuntu was up and running, the next task was installing the necessary development tools, including GNU Radio and Visual Studio Code (VSCode). Installing GNU Radio was particularly tricky because it involved adding repositories and managing dependencies through the command line. Dr. Taylor guided me through these steps, ensuring that everything was correctly installed. Setting up VSCode was more straightforward, but I had to make sure it was configured to work well with Python, the language used for the SDR programs.

The most technically challenging part was setting up the network configuration to connect the USRP to my computer via Ethernet. This involved manually setting IP addresses and other network settings, something I had never done before. Dr. Zakir walked me through the process, explaining each step and helping me troubleshoot issues as they arose. After several attempts and adjustments, I was able to establish a stable connection between the USRP and the computer.

With the environment fully set up, I moved on to running the provided Python programs, "Transmitter_Receiver.py" and "Transmitter_Receiver_3_secs.py", in GNU Radio. These programs were designed to create a basic transmitter-receiver system, with the second program introducing a timed transmission feature. Running these programs involved understanding how GNU Radio interfaces with the USRP and how to manage the transmission and reception of signals within the software.

This entire process, from setting up the virtual machine to running the SDR programs, was a significant learning curve. However, with the support of Dr. Zakir and Dr. Taylor, I successfully configured and operated a complex SDR system, gaining valuable technical skills along the way. This experience has provided me with a solid foundation in SDR technology and has prepared me for more advanced projects in the future.

4.Result

After successfully setting up the software-defined radio (SDR) environment and running the provided Python programs, the next crucial step was to analyze the output data and validate the performance of the transmitter-receiver system. The images above represent different human activities, the X-axis representing time or packet index, while the Y-axis indicating signal amplitude, showing how signal strength varies over time or across data packets, captured using the USRP's single omnidirectional Tx and Rx antennas. The following activities were performed:

Activities

4.1.1 Empty Room (EmptyL1Z1_9): The room was empty, and no human presence was detected. The received signals showed minimal fluctuations, with all subcarriers maintaining consistent behavior. This baseline is critical for comparing how the presence of a human or activity affects the signal.

4.1.2 Leaning (LeaningL1Z2_19): In this scenario, a person leaned forward. The signal showed a noticeable increase in variation, particularly around the middle of the time frame. This indicates that the system was sensitive enough to detect the subtle movement of leaning, with certain subcarriers reflecting significant changes due to the human body's proximity to the Tx and Rx antennas.

4.1.3 No Activity (NoActivityL1Z2_48.png): The subject was seated without movement. The signal variation was minimal, slightly higher than the empty room scenario but still consistent. This suggests that while the system can detect the presence of a person, the absence of significant movement results in relatively stable signals. 

4.1.4 Sitting Down (SittingL1Z2_50.png): The subject transitioned from standing to sitting. This action caused a moderate spike in signal variation as the person moved. The variations are clearly seen in the graph, especially at the points where the action begins and ends, demonstrating the system’s ability to capture dynamic changes in human posture.

4.1.5 Standing Up (StandingL2Z2_42.png): Here, the subject stood up from a seated position. Similar to the sitting scenario, the signal variation increased as the action was performed. The data shows a significant shift in signal behavior corresponding to the movement, indicating that the system is responsive to vertical movements. 

4.1.6 Walking from Rx to Tx (WalkingRxTxZ2_88.png): The subject walked from the Rx antenna toward the Tx antenna. This resulted in a pronounced increase in signal variability, with distinct peaks and valleys corresponding to the subject's movement across the room. The system captured the complex interaction of the body with the signal as the distance between the subject and the antennas changed. 

4.1.7Walking from Tx to Rx (WalkingTxRxZ2_99): The subject walked from the Tx antenna toward the Rx antenna. Similar to the previous walking scenario, the signal demonstrated substantial variation. The pattern of peaks and troughs was consistent with the previous walking scenario but mirrored due to the reversed direction of movement. 

4.2 Analysis and Validation

The plots illustrate the system's ability to capture and differentiate between various human activities based on the signal fluctuations caused by movement. The system maintained consistent performance across multiple tests, with each activity showing distinct signal patterns. These patterns can be used to classify different activities, making the system a strong candidate for applications in human activity recognition.

4.3 Strengths and Areas for Improvement

4.3.1 Strengths:

Accurate Activity Detection: The system successfully detected and distinguished between various human activities, with clear differences in signal behavior corresponding to each activity.

Consistent Signal Transmission: Across all tests, the system demonstrated reliable signal transmission, even in scenarios involving significant movement.

4.3.2 Areas for Improvement:

Handling of Environmental Variability: While the system performed well, environmental factors such as room layout or the presence of other objects could impact signal quality. Further tuning may be needed to improve robustness against such factors.

Advanced Classification: Incorporating machine learning algorithms could enhance the system's ability to classify activities automatically, improving its effectiveness in real-world applications.

5.Conclusions and Future Work

This project successfully implemented a transmitter-receiver system using GNU Radio and USRP, focusing on timed transmission. The results showed that the system could reliably transmit and receive signals across multiple subcarriers with consistent performance, even when faced with minor environmental variations. The timed transmission feature worked as intended, accurately controlling the duration of signal transmission, which is crucial for applications requiring precise synchronization. The findings align with existing research, confirming the potential of SDR technology in modern communication and sensing systems.

If given more time, several improvements could be pursued. First, enhancing the system's robustness to environmental changes would make it more reliable in diverse real-world conditions. Developing automated tools for signal analysis would also streamline the validation process, making it more efficient. Additionally, expanding testing to include more varied environments would provide deeper insights into the system's performance under different conditions.

Integrating machine learning models for activity recognition or anomaly detection could significantly enhance the system's functionality, aligning with ongoing research in healthcare and human activity monitoring. Finally, scaling the system to support multiple communication channels would broaden its application, particularly in areas like IoT and smart environments.

In summary, while the project successfully achieved its primary objectives, further development could unlock even greater potential, transforming the system into a versatile tool for a wide range of applications.

6.References

[1] U. Saeed, Q. H. Abbasi, S. A. Shah, A. H. Naqvi, and M. Imran, "Software-Defined Radio-Based Contactless Localization for Diverse Human Activity Recognition," IEEE Sensors Journal, vol. 23, no. 11, pp. 12041-12048, June 2023, doi: 10.1109/JSEN.2023.3265867.

[2] M. Z. Khan, J. Ahmad, W. Boulila, M. Broadbent, S. A. Shah, A. Koubaa, and Q. H. Abbasi, "Contactless Human Activity Recognition using Deep Learning with Flexible and Scalable Software Defined Radio," in 2023 International Wireless Communications and Mobile Computing (IWCMC), Marrakesh, Morocco, 2023, pp. 126-131, doi: 10.1109/IWCMC58020.2023.10182652.

[3] W. Taylor, A. M. A. Ashleibta, S. A. Shah, M. Imran, and Q. Abbasi, “Software Defined Radio Based Activity Recognition for Remote Healthcare Driven by Machine Learning,” in Proc. 9th IEEE Asia-Pacific Conf. Antennas and Propagation (APCAP), Xiamen, China, Aug. 2020, pp. 1-6.

[4] M. Z. Khan, A. Taha, W. Taylor, A. Alomainy, M. A. Imran, and Q. H. Abbasi, "Indoor localization using software defined radio: A non-invasive approach," in 2022 3rd URSI Atlantic and Asia Pacific Radio Science Meeting (AT-AP-RASC), Gran Canaria, Spain, 2022, pp. 1-4, doi: 10.23919/AT-AP-RASC54737.2022.9814250.

[5] M. Z. Khan, T. Althobaiti, M. Almutiry, and N. Ramzan, "Empowering the Blind: Contactless Activity Recognition with Commodity Software-Defined Radio and Ultra-High-Frequency Radio Frequency Identification," Sensors, vol. 24, no. 11, p. 3645, June 2024, doi: 10.3390/s24113645.

2