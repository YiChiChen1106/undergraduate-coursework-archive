# Lab1 - answer sheet 19-20

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Lab1 - Transients in RLC Networks

Analysis – Step1 (25%)

Write the transfer function in time domain for the voltage across versus the input voltage . 

Convert V1 and Rth into its equivalent current source Ix and parallel resistor

Ix

Ix=V1Rth

Rparallel

Rparallel=Rth

Combine the parallel resistor with R2 giving Req

Req

Req=RthR2Rth+R2

Convert Ix and Req into Vx and Req2

Vx

Vx=V1R2Rth+R2

Req2

Req2=Req=RthR2Rth+R2

Rearrange the components so as to get a RLC series circuit – Redraw circuit in Fig1 as instructed.

Figure of the equivalent circuit

Apply mesh analysis to the RLC series

Mesh analysis

We have:

-Vx+VR+VL1+VC1=0

-Vx+Req2×I+L1×dIdt+1C1-∞τ=tIτdτ=0

V_1=IR_{th}⍁{L_1 (R_{th}+R_2)}R_2×⍁{dI}{dt}}

V1=IRth+L1 Rth+R2R2×dIdt+Rth+R2C1R2-∞τ=tIτdτ

Give the transfer function of VC1 as a function of V1 and the component values.

Transfer function

Since V1=IRth+L1 Rth+R2R2×dIdt+Rth+R2C1R2-∞τ=tIτdτ

VC1=1C1-∞τ=tIτdτ

So 

VC1V1=1C1-∞τ=tIτdτIRth+L1 Rth+R2R2×dIdt+Rth+R2C1R2-∞τ=tIτdτ

Determine the natural frequency, damping factor, and damping frequency of the circuit shown in Figure 2 where, ,and a)  and b).  Note that you should combine, , , and  into one equivalent resistor before performing these calculations. Be careful with units!!! (Hz and rad/s are not the same)

Req a) 

Req=RthR2Rth+R2+Rparasitic+R1=50×4750+47+100+300=424.2Ω

Req b)

Req=RthR2Rth+R2+Rparasitic+R1=50×4750+47+100+3000=3124.2Ω

ω0

ω0=1LC=3.16×105rad/s

α a)

α=Req2L=21210rad/s

α b)

α=Req2L=1.56×105rad/s

ζ a)

ζ=R2CL=424.221×10-910×10-3=0.067

ζ b)

ζ=R2CL=3124.221×10-910×10-3=0.49

ωd a)

ωd=ω02-α2=3.16×1052-212102=3.15×105rad/s

ωd b)

ωd=ω02-α2=3.16×1052-1.56×1052=2.75×105rad/s

For the two cases a)  and b), determine the values for A1 and A2 in the equation for a forced response,  when, whereis a unit step function.  Note that .  The solution will be the same as the case where because the transient response is only produced by the step function, not the d.c. component of .  

Determine the initial voltage at t = 0-s, just before the step input. 

ν10- s

v10-s=2V

νC0- s

vC0- s=R2Rth+R2v10-=4750+47×2=0.97V

Determine the steady state voltage at t = ∞s 

ν1∞ s

6V

νC∞ s

2.91V

Considering  at t = ∞s, solve VS

VS

VS=vC∞s=2.91V

Considering  at t = 0-s, solve A1

A1

A1=-1.94V, since vC0s=A1+VS=A1+2.91=0.97

Considering ict at t = 0-s, solve A2 (refer to Hint 2 – derivation needed – A2 depends on R1 so you should have 2 different values for both cases)

derivation

ict

=Cdvctdt=A2ωd-A1αcosωdt-A1ωd+A2αsinωdte-αtC

Since ic0s=0, we have A2ωd-A1α=0,

So A2=αωdA1

A2 a)

A2=αωdA1=212103.15×105×-1.94=-0.13V

A2 b)

A2=αωdA1=1.56×1052.75×105×-1.94=-1.1V

Using Matlab, plot the equations for the voltage across the capacitor developed in Step 3 on the same graph from t = 0 s to t = 0.25 ms.

Insert a screen capture of your code with comments

t = linspace(0, 0.25, 100) / 1000;

Vca = [-1.94 * cos(315000*t) - 0.13 * sin(315000*t)] .* exp(-21210*t);

Vcb = [-1.94 * cos(274000*t) - 0.13 * sin(274000*t)] .* exp(-156000*t);

plot(t, Vca, Vcb);

Insert the resulting graph with appropriate annotations, units and legends.

Modeling – Step2 (25%)

In PSpice, simulate the transient response of the circuit shown in Figure 2 where, ,when a)  and b).   Set the amplitude of the voltage source V1 such that it is a square wave with an amplitude that varies from 2 V to 6 V.  The pulse width should be 0.25 ms and the period should be 0.5 ms. 

Insert the resulting schematic 

Graph the voltage across , the voltage across, and the voltage across  for one period of the square wave.  Either scale the curves so that the magnitude and shape of each signal is readable or add plots to obtain a stack of graphs of the signals.

Insert the resulting graph with appropriate annotations, units and legends.

Graph the current flowing out of to show that the voltage source is always a power generating element in the circuit.

Insert the resulting graph with appropriate annotations, units and legends.

Measure the period of the underdamped response of the voltage across the capacitor when a)  and b).   Calculate the damped frequency d using the period measured. Determine the percent difference between the expected value of d calculated in Step 1 and the damped frequency calculated from the data graphed in PSpice. Don’t forget units.

Toscillation

Toscillation=150.74-9.567=20.17μs

foscillation

foscillation=1Toscillation=120.17=5×104Hz

ωd

ωd=2πf=3.14×105rad/s

Percent difference between theory and simulation

3.14×105-3.15×1053.15×105×100\%=0.32\%

Toscillation

Toscillation=26.84-4.04=22.8μs

foscillation

foscillation=1Toscillation=122.8=4.4×104Hz

ωd

ωd=2πf=2.8×105rad/s

Percent difference between theory and simulation

2.8×105-2.75×1052.75×105×100%=1.8%

Conclusion

To reduce the length of time that ringing of the voltage across can be observed: 

Should  increase or decrease? 

α should

Increase 

Justify your answer

(text, simulation, and/or equations)

From the simulation we can see that greater α leads to shorter damping time

If  is held constant, should the value of increase or decrease to reduce the transient response?

L1 should

Decrease 

Justify your answer (text, simulation, and/or equations)

Since α=Req2L, and according to a, a greater α is needed to reduce the transient response, so L1 has to decrease.

Do you expect that the energy stored in the capacitor will dissipate faster as  increases?  Why or why not? Simulate the power across R1 and comment for R1 = 3kΩ and R1 = 300Ω.

The energy

The energy stored in the capacitor will dissipate faster as R1 increases.

Justify your answer (text, simulation, and/or equations)

Since E=12CU2, and C is constant, we can compare the two situations by showing VC12

Figures above proves the statement.

Given the relationship between energy, charge, voltage, and capacitance, would you expect that the amplitude of the voltage overshoot in the transient response to increase or decrease if the capacitance of is increased while the magnitudes of the other components in the circuit are held constant? Simulate a transient response through R1 before answering.

The overshoot

The overshoot will increase as the capacitance increases

Justify your answer (text, simulation, and/or equations)

The green, blue, red line are VR1 when C1 is 1nF , 5nF, 10nF respectly, which proves the statement.

If the DC offset is set to 0 V, why would it be inappropriate to use an electrolytic capacitor for?

Electrolytic capacitor

Electrolytic capacitor could be easily burnt when the voltage across it is negative. 

Justify your answer

The simulation shows that there are moments when voltage across C1 becomes negative, when pulse of V1 is set to 0V to 4V.

Student1 - Name

GUID

Student2 - Name

GUID

Zhuheng Song

[student-id-redacted]

/

/