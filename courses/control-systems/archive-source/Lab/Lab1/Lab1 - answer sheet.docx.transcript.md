# Lab1 - answer sheet

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Lab1 - Transients in RLC Networks

Analysis – Step1 (25%)

Write the transfer function in time domain for the voltage across versus the input voltage . 

Convert V1 and Rth into its equivalent current source Ix and parallel resistor

Ix

V1Rth

Rparallel

Rth

Combine the parallel resistor with R2 giving Req

Req

RthR2Rth+R2

Convert Ix and Req into Vx and Req2

Vx

V1R2Rth+R2

Req2

Req   i.e.   RthR2Rth+R2

Rearrange the components so as to get a RLC series circuit – Redraw circuit in Fig1 as instructed.

Figure of the equivalent circuit

Rt= RthR2Rth+R2+ Rparasitic+ R1

Apply mesh analysis to the RLC series

Mesh analysis

Vx=IRt+ L1dIdt+ -∞tI(τ)dτC1

So, V1=I(RthR2Rth+R2+ Rparasitic+ R1)∙Rth+R2R2+ Rth+R2R2∙L1dIdt+ Rth+R2R2∙-∞tI(τ)dτC1

i.e. V1=IRth+ I( Rparasitic+ R1)∙Rth+R2R2+ Rth+R2R2∙L1dIdt+ Rth+R2R2∙-∞tI(τ)dτC1

Give the transfer function of VC1 as a function of V1 and the component values.

Transfer function

VC1V1= -∞tI(τ)dτC1IRth+ I( Rparasitic+ R1)∙Rth+R2R2+ Rth+R2R2∙L1dIdt+ Rth+R2R2∙-∞tI(τ)dτC1

Using the Laplace transform, Vx=IRt+sIL1+ IsC1

So, V1=(IsC1+IRt+sIL1)∙Rth+ R2RthR2

VC1V1= IsC1(IsC1+IRt+sIL1)∙Rth+ R2RthR2= 1sC1∙R2Rth+R2(1sC1+Rt+sL1), where Rt= RthR2Rth+R2+ Rparasitic+ R1

Determine the natural frequency, damping factor, and damping frequency of the circuit shown in Figure 2 where, ,and a)  and b).  Note that you should combine, , , and  into one equivalent resistor before performing these calculations. Be careful with units!!! (Hz and rad/s are not the same)

Req a) 

424.2Ω (with R1)

Req b)

3124.2Ω (with R1)

ω0

3.16×105 rad/s

α a)

21210 rad/s

α b)

1.56×105 rad/s

ζ a)

0.067

ζ b)

0.49

ωd a)

3.15×105 rad/s

ωd b)

2.75×105 rad/s

For the two cases a)  and b), determine the values for A1 and A2 in the equation for a forced response,  when, whereis a unit step function.  Note that .  The solution will be the same as the case where because the transient response is only produced by the step function, not the d.c. component of .  

Determine the initial voltage at t = 0-s, just before the step input. 

ν10- s

2V

νC0- s

νC0- s= R2νC0- sRth+R2 = 0.97V

Determine the steady state voltage at t = ∞s 

ν1∞ s

6V

νC∞ s

νC∞ s= R2νC∞ sRth+R2 = 2.91V

Considering  at t = ∞s, solve VS

VS

Vs= Vc∞s=2.91V

Considering  at t = 0-s, solve A1

A1

Vc0-s= A1+ Vs=0.97V

So, A1= -1.94V

Considering ict at t = 0-s, solve A2 (refer to Hint 2 – derivation needed – A2 depends on R1 so you should have 2 different values for both cases)

derivatiom

i0-s=C∙dVctdt=C∙A2ωd-A1αcosωdt-A1ωd+A2αsinωdt∙e-αt=0

A2 a)

-0.13V

A2 b)

-1.1V

Using Matlab, plot the equations for the voltage across the capacitor developed in Step 3 on the same graph from t = 0 s to t = 0.25 ms.

Insert a screen capture of your code with comments

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

2×0.022ms-0.012ms=20us

foscillation

1T=5×104Hz

ωd

2πf=3.14×105rad/s

Percent difference between theory and simulation

3.14×105rad/s- 3.15×105rad/s3.15×105rad/s × 100%=-0.3%

Toscillation

2×0.025ms-0.013ms=24us

foscillation

1T=4.17×104Hz

ωd

2πf=2.6×105rad/s

Percent difference between theory and simulation

2.6×105rad/s- 2.75×105rad/s2.75×105rad/s × 100%=-0.55%

Conclusion

To reduce the length of time that ringing of the voltage across can be observed: 

Should  increase or decrease? 

α should

increase

Justify your answer

(text, simulation, and/or equations)

It can be shown in previous figures of the simulating results that greater 𝛼 leads to shorter damping time.

If  is held constant, should the value of increase or decrease to reduce the transient response?

L1 should

decrease

Justify your answer (text, simulation, and/or equations)

α= Req2L1, smaller L leads to greater α, thus, the damping time will be shorter

Do you expect that the energy stored in the capacitor will dissipate faster as  increases?  Why or why not? Simulate the power across R1 and comment for R1 = 3kΩ and R1 = 300Ω.

The energy

The energy stored in the capacitor will dissipate faster as R1 increases.

Justify your answer (text, simulation, and/or equations)

R1 = 3kΩ:

R1 = 300Ω:

Given the relationship between energy, charge, voltage, and capacitance, would you expect that the amplitude of the voltage overshoot in the transient response to increase or decrease if the capacitance of is increased while the magnitudes of the other components in the circuit are held constant? Simulate a transient response through R1 before answering.

The overshoot

The overshoot will increase as the capacitance increases

Justify your answer (text, simulation, and/or equations)

C = 1nF:

C = 5nF:

C = 10nF:

If the DC offset is set to 0 V, why would it be inappropriate to use an electrolytic capacitor for?

Electrolytic capacitor

The electrolytic capacitor may be damaged when the across it is negative.

Justify your answer

As shown in the first figure, at 380us, approximately, the voltage across the capacitor is negative.

Student1 - Name

GUID

Student2 - Name

GUID

Tiancheng Li

[student-id-redacted]