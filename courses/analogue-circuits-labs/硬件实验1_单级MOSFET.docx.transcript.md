# 硬件实验1_单级MOSFET

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Design, implement and test a single MOSFET amplifier circuit

1.Experiment objective

·Learning to master the method to measure and adjust amplifier quiescent point 

·Learning to master the method to measure amplifier dynamic parameter 

·Familiar with the relationship among amplifier quiescent point, voltage gain and distortion

2. Experimental equipment

·Dual trace oscilloscope

·Function Generator

·AC millivoltmeters

·Breadboard

·Multimeter

·Components

3. Experimental principles

(1)Quiescent point analysis 

For IG=0, the calculation is shown as follow:

           UGQ=Rg1Rg1+Rg2VDD

   USQ=IDQRS

   UGSQ=UGQ-USQ=Rg1Rg1+Rg2VDD-IDQRS

And

   IDQ=IDOUGSQUGSth-12

   UDSQ=VDD-IDQ(RD+RS)

(2) Amplifier dynamic index

According to the equivalent circuit, we can obtain AV,Ri,Ro

When the amplifier take appropriate quiescent point，Using Ac millivoltmeter measure the RMS values of ,  

   AV=VOVi=-gmRD//RL

    Ri=Rg1//Rg2 

    RO=RD

 4. Experimental contents

(1) Use millivoltmeter to measure UD,US,UG to the ground respectively when working in quiescent point. And also need to measure ID by measuring the voltage UD across RD and divide UD by  RD.

ID=UDRD

(2) Input an Ac signal () to the amplifier. Observe the input waveform and measure amplifier output voltage  in the condition of output waveform distortionless.

Calculate voltage gain:

(3) Measure the input resistance  

Measure the input resistance by using secondary voltage method: take a resistor R (almost as large as Rg1 or Rg2).Here we choose R=30kΩ.And measure Us and Ui  just like the following method.

Thus, we calculate  by using Ri=UiUs-Ui

(4)Measure the output resistance . 

Measure the input resistance also by using secondary voltage method:

Keep the input voltage as it is, and measure the output voltage Uo' without load RL . And then add the load RL, measure the output voltage Uo across RL .( Here we choose RL=2kΩ)

Thus, we calculate  by using Ro=Uo'Uo-1RL

5. Fill the result in below table

quiescent point

voltage gain

input resistance

output resistance

UGSQ=

IDQ=

UDSQ=

AV=

Ri=

Ro=