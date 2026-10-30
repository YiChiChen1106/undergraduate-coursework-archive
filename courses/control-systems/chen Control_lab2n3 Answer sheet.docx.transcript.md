# chen Control_lab2n3 Answer sheet

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

A second order pendulum system

Figure 1

Likening the leg to a link, referring Figure.1 above. It has a length, l, and is free to rotate about 𝑂, as shown. The mass is 𝑚 and the centre of mass is located at 𝐺 which in turn is situated at 1/2 , in the middle of the link. The moment of inertia, l, about the pivot point, 𝑂, is given by the relationship:

I = ml2

as the mass is centred at 𝑙 then we have I = m(1/2)2. The knee-extensor muscles contract to hold the system in equilibrium at angle 𝜃𝑒, by application of a torque, 𝜏𝑒, acting around 𝑂. The moment (force x distance) required to maintain equilibrium, 𝜏𝑒, is:

Assume now that the knee moves to a new angle of displacement, 𝜃. There will be a damping coefficient, 𝑐, as shown in Figure.1. This damping occurs naturally and is caused by physical properties of the muscle and tendon-bone connection. When the body is moving there is now a viscous damping moment that’s proportional to the object velocity, or 𝜃̇ . This damping moment is 𝑐𝜃̇ . The displacement angle is shown in Figure. 2

Figure 2

Let’s now derive the differential equation that describes this system. From Newton’s Law: 𝑀 = 𝐼𝛼, where 𝑀 is the sum of all external moments about the centre of mass, 𝐼 is the moment of inertia of the mass and 𝛼 is the angular acceleration of the mass. The knee displacement is 𝜃, angular acceleration is 𝜃̈ and therefore the total inertial moment is 𝐼𝜃̈. Balancing all moments:

Convert the equation of motion from the time, 𝑡, domain to 𝑠 domain and rewrite the transfer function as shown above but in the 𝑠 domain.

Using the standard form and the characteristic equation derive expressions for

𝜔𝑛 (undamped natural frequency) and ζ (damping ratio).

ωn=mgl2I

ζ=c2Iωn=c12mglI

Let’s assume the following physical parameters for the link shown above:

𝑚 = 5 kg (mass);

𝑙 = 0.4 m (length);

𝑐 = 0.5 (damping coefficient);

𝑔 = 9.81 m/s2 (gravity)

Using these parameters and the transfer function derived in #1 above, let’s use Matlab to experiment and investigate how these physical properties relate to the dynamic behaviour of the system and also how they relate to the poles of the system, which, as we know, set the dynamic behaviour.

Open the file “Control_lab2_student.m”

This file contains all the equations and the transfer function definition to allow you to start running the following experiments:

Vary the physical parameters one by one (m, l and c) and notice their impact on the step response of the system. Explain clearly why each parameter below is impacted (or maybe not) by the changes you make in each of the physical parameters.

MP, output overshoot.

ts, output settling time.

tp, time where the maximum output peak occurs.

tr, rise time

𝜔𝑛, the natural undamped frequency.

𝜔𝑑, the damped frequency.

Comment on the steady state error of the output for each of the changes you make in the physical parameters. Is this output as expected? Explain why.

By using the “pzplot” function plot the poles and note how their positions vary as you vary the physical parameters. Correlate the position of the poles to the transient response of the output and give full explanations why the pole positions vary as they do and why the correlation to the output behaves accordingly.

You can also display the transfer function or any other variable just by

directly typing the variable name in this window: for example, note from the following screenshot how to display the transfer function:

GTA’s Signature

Proportional gain – Open loop transfer function

For this lab exercise, we are now going to add proportional gain, Kp, to the plant pendulum transfer function and notice the impact of this on open loop behaviour.

Make the appropriate edit to the file “Control_lab2_ex1.m” and remember to save the new file to another name, such as “Control_lab2_ex2.m” or something appropriate.

Hint: add a new variable called Kp to the script: The plant transfer function is:

sys = tf (1/I,[1 2*xi*wn wn^2]

Now create a new variable called sysKp, which will be the transfer function of the gain Kp

Kp=100; (this value will be part of your experiments) sysKp = tf(Kp,1)

The new transfer function will be the product of the original transfer function sys and the newly added proportional gain sysKp

sysP = sys*sysKp

In block diagram form, you are now making the system look like Figure 3 below:

Figure 3

Vary the proportional gain, Kp, and notice its impact on the step response of the system. Explain clearly, why each parameter below is impacted (or maybe not) by the changes made in each of the physical parameters.

MP, output overshoot.

ts, output settling time.

tp, time where the maximum output peak occurs.

tr, rise time.

𝜔𝑛, the natural undamped frequency.

𝜔𝑑, the damped frequency.

From the simulation data, when​ Kp increases from 1 to 500, the system’s dynamic characteristics remain unchanged: 𝜔𝑛 ​, 𝜔𝑑 ​, tr​, tp​, ts​, and MP ​ all stay the same.

Reason:

The Kp​ gain was applied in the open-loop system, simply scaling the output without introducing feedback control. 

The system poles remain unchanged, so the natural frequency, damping ratio, and all dynamic behaviors stay the same. Kp​ only changes the amplitude of the system output, not its dynamics.

Comment on the steady state error of the output for each of the changes you make in the proportional gain, Kp. Is this output as expected? Explain why.

Increasing Kp​ scales the response but does not eliminate the steady-state error.

There is no error correction in an open-loop system, so no matter how Kp​ changes, the steady-state error remains. To eliminate steady-state error, we need closed-loop feedback control

By using the “pzplot” function plot the poles and note how their positions vary as you vary the proportional; gain, Kp. Correlate the position of the poles to the transient response of the output and give full explanations why the pole positions vary or not vary.

From pzplot, it is clear that the pole locations remain unchanged when varying Kp.

Kp​ here is just a forward gain; it does not affect the system poles, which are determined by the denominator of the transfer function. Since the pole locations are unchanged, the system dynamics remain the same.

GTA’s Signature

Disturbance

For this lab exercise, we are now going to add a step disturbance to the output of our open loop plant system as developed in section II.

Launch “simulink”

Open the file “Control_lab2_ex3.slx”, it will automatically use the variable values from Matlab workspace so you don’t need to specify the values for wn, xi or Kp. If you cleared the memory run the previous Matlab script to repopulate the workspace.

Go to the tab simulation> Model configuration parameters

Enter the following parameters and apply to configure your model

Read the help documentation on simulink:

– Simulink_user_guide

– Simuling_guide_to_blocks

For an overview of the functions available in Simulink.

Make sure you explore the model so that you understand how it is setup. And where to find the blocks in the Simulink libraries

Hint: only 4 libraries used for this model: Sources, Sinks, Math operations and Continuous

For this exercise, we are now going to use Simulink in Matlab. The schematic you are going to create will look something like that shown in Figure 4 below:

Figure 4

The above setup will impress a disturbance on the output of the plant which has an amplitude of 0.1V with a period of 1s and 50% duty cycle.

Make a copy of your previous script and call it “Control_lab2_ex3b.m”. You should then run this script before you run the simulation in Simulink. This is because the script will define all variables shown in the Simulink schematic such as Kp, wn and so on. You should change the values in the script for your experiments, run the script and then run the simulink simulation each time you make the change to the script to see the changes.

Hint: don’t name the script and the m-file the same, Matlab will not like it

By observing the output response, as before to a unit step input, what do you observe about the output of the system during the times that the disturbance is applied and then removed?

Modify the gain, Kp, and note if changing the gain has any impact on the output behaviour during the disturbance.

Modify parameter, c and observe the behaviour of the system output. Explain why the output behaves the way it does.

Explain what you are observing and if this behaviour is as you would expect and why.

GTA’s Signature

Closed-loop transfer function

For this lab exercise, we are now going to close the loop and add a step disturbance to the output of our closed loop plant system as developed in Control Lab 3.

Make the appropriate edit to the file “Control_lab2_ex3b.m” and remember to save the new file to another name, such as “Control_lab2_ex4.m” or something appropriate.

Hint: The edit you need to make is to create another transfer function in the script which can be done in different ways as illustrated below:

The original open loop transfer for the plant is given as:

sys = tf (1/I,[1 2*xi*wn wn^2]

CLTF = sys/(1+sys);

Edit the script to plot both the transient step response and the poles of the loop in order to be able to analyse the following questions:

By observing the output response, as before to a unit step input, what do you observe about the following compared to that measured in Control_lab2_ex1?

MP, output overshoot.

Feedback with high Kp​ leads to higher overshoot due to increased response speed.

ts, output settling time.

Settling time is shorter because feedback stabilizes the system more effectively.

tp, time where the maximum output peak occurs.

Peak time decreases because of faster response in closed-loop control.

tr, rise time.

Rise time is shorter because closed-loop response is faster.

𝜔𝑛, the natural undamped frequency.

Natural frequency is determined by the physical system and remains unchanged.

𝜔𝑑, the damped frequency.

Damped frequency of the original mode is the same, but closed-loop introduces additional higher-frequency poles.

Comment on the steady state error.

In the closed-loop system (CLTF), steady-state error is zero. The system output eventually reaches the unit step input (final value = 1), with no steady-state deviation.

Closed-loop control system is Type 1, which ensures zero steady-state error for a step input. 

In Control_lab2_ex4, feedback improves error correction, eliminating steady-state error.

Type “CLTF” in the command window and note the transfer function.

Type “sys” in the command window and note the transfer function.

What do you observe about the difference between the denominator of “CLTF” and “sys”?

The closed-loop system denominator increased from second-order to fourth-order due to the feedback loop. The system dynamics are more complex but stability is enhanced.

Calculate the transfer function by hand and enter it in MATLAB compare it with what MATLAB gave you. Plot the step response of both functions on the same graph. What do you observe?

The MATLAB result matches the theoretical calculation.

Figure 1

The CLTF response is faster, with more overshoot but a shorter settling time.

Use the functions pole(sys), zero(sys) on the transfer function you calculated, and the closed-loop transfer function given by MATLAB. What can you say about the poles and zeros of the closed-loop transfer function given by MATLAB and your calculation? Are they the same? What does that tell you about your simulation software?

The poles and zeros of the closed-loop transfer function from MATLAB are exactly the same as those from your manual calculation.

This shows that MATLAB's simulation software is accurate and reliable in calculating transfer functions and solving poles/zeros.

By looking at the position of the poles, have the poles varied in position compared to the open loop case? Why do you so answer?

Figure 2

The CLTF poles move further left or to higher frequencies in the left-half plane, making the closed-loop system more stable and faster in response.

New poles appeared at higher frequencies, indicating faster dynamic behavior due to feedback control. 

The real part remains the same (-1.75), but the higher frequency poles show enhanced dynamic performance.

The feedback introduced new dynamics, with the proportional gain Kp=10 enhancing the feedback effect and introducing higher-frequency poles.

Vary the parameters “c” (the damping coefficient) and “l” (the length) and note the impact on the transient response and pole positions. Try and have the system go into oscillation, explain how you did it and how this impacted the position of the system poles.

Figure 3

Increased damping reduces overshoot, slows down response, and improves stability.

Figure 4

Increasing link length increases inertia, reducing natural frequency, slowing down response.

Figure 5

Increase Kp ​ to a very high value (e.g., Kp=100) .

Closed-loop poles move toward the imaginary axis, possibly crossing into the right-half plane.

System becomes unstable, resulting in divergent oscillations.

Insufficient damping leads to high oscillation frequency and large overshoot. 

Excessive gain strengthens feedback, causing aggressive response, poles nearing instability.

GTA’s Signature

Closed-loop transfer function with proportional gain

For this lab exercise, we are now going to close the loop and we will also add proportional gain, Kp to the closed-loop system.

Make the appropriate edit to the file “Control_lab2_ex5”.

sys = tf (1/I,[1 2*xi*wn wn^2]

So you can add loop gain, Kp, in the following way:

Kp=100;

sysKp = tf(Kp,1) 

OLTF = sysKp*sys

CLTF = OLTF/(1+OLTF)

Edit the script to plot both the transient step response from the OLTF and CLTF and the poles of the open and closed loops loop in order to be able to analyse the following questions:

Vary Kp and observe the following:

Mp, output overshoot.

ts, output settling time.

tp, time where the maximum output peak occurs.

tr, rise time from 10%-90% of final output value.

𝜔𝑛, the natural undamped frequency.

𝜔𝑑, the damped frequency.

Comment on the steady state error. Why is it different if we vary Kp?

Type “sys” in the command window and note the transfer function.

Type “CLTF” in the command window and note the transfer function.

What do you observe about the difference between the denominator of “sys” and “CLTF”?

What differences in the denominator of the transfer function occur as you increase Kp? For this example, create another polynomial, OLTF, in your script, which is merely the pendulum transfer function multiplied by Kp.

By looking at the position of the poles, have the poles varied in position compared to the open loop case and the closed loop case with unity gain?

How do the pole positions change as Kp is varied?

Will this be the reason for the change in dynamic performance as Kp is varied?

GTA’s Signature

Closed-loop transfer function with disturbance

For this lab exercise, we are now going to add a step disturbance to the output on previous exercise we carried out in section V.

Make the appropriate edit to the file “Control_lab2_ex6b.m”.

Modify “Control_lab2_ex3.slx” so that the closed-loop system resembles what is shown below and save it as “Control_lab2_ex6.slx” as shown below:

Figure 5

Run your Control_lab2_ex6b.m file as this will set up all of your variables. When changing any variables change using this script and rerun the script before rerunning the Simulink simulation.

By observing the output response, as before to a unit step input, what do you observe about the output of the system during the times that the disturbance is applied and then removed?

Modify the gain, Kp, and note if changing the gain has any impact on the output behaviour during the disturbance. Please explain why changing the gain, Kp, has influence on the response to disturbance, if any.

Tie in your response for question 7 by plotting the poles and tying in the pole positions to what you see on the transient response due to a step input and the output disturbance, for various physical parameters such as Kp, c, etc.

Modify parameter, c and observe the behaviour of the system output. Explain why the output behaves the way it does.

Explain what you are observing and if this behaviour is as you would expect and why.

GTA’s Signature

PI controller in closed-loop system

For this lab exercise, we are now going to add integral gain, Ki, to our proportional gain, Kp, in a closed loop system.

Make the appropriate edit to the file “Control_lab2_ex7b.m”.

The original open loop transfer for the plant is given as:

sys = tf (1/I,[1 2*xi*wn wn^2]

So you can assign two variables now, Kp and Ki. You should keep the script written in such a way that you can independently vary Kp and Ki to note the impact on the system response and the pole/zero positions.

For example:

Kp=1;

sysKp = tf(Kp,1) Ki=1;

sysKi = tf(Ki,[1 0])

OLTF = (sysKp+sysKi)*sys 

CLTF=OLTF/(1+OLTF)

CLTF is the closed loop transfer function, Kp and Ki can be varied separately.

Edit the script to plot both the transient step response and the poles of the loop in order to be able to analyse the following questions:

Note the response on the output as you vary both Kp and Ki for the following parameters:

Rise timeOvershootSettling TimeSteady State error

Please show which gain has the largest impact on which parameter and give clear reasons why this should be the case.

As you vary the gains in the system please take note of how this impacts the pole and zero positions and give explanations as to the behaviour of the time-domain response.

You should observe the transfer function, “CLTF”, as you vary the gains. You can print “CLTF” in the console window to verify this.

GTA’s Signature

PD controller in closed-loop system

For this lab exercise, we are now going to add derivative gain, Kd, to our proportional gain, Kp, in a closed loop system.

Make the appropriate edit to the file “Control_lab2_ex8”

The original open loop transfer for the plant is given as:

sys = tf (1/I,[1 2*xi*wn wn^2]

So you can assign two variables now, Kp and Kd. You should keep the script written in such a way that you can independently vary Kp and Kd to note the impact on the system response and the pole/zero positions.

Kp=10;

sysKp = tf(Kp,1) Kd=1;

sysKd = tf([Kd 0],1)

OLTF = (sysKp+sysKd)*sys 

CLTF=OLTF/(1+OLTF)

CLTF is the closed loop transfer function, Kp and Kd can be varied separately.

Edit the script to plot both the transient step response and the poles of the loop in order to be able to analyse the following questions:

Note the response on the output as you vary both Kp and Kd for the following parameters:

Rise timeOvershootSettling TimeSteady State error

Please show which gain has the largest impact on which parameter and give clear reasons why this should be the case.

As you vary the gains in the system please take note of how this impacts the pole and zero positions and give explanations as to the behaviour.

You should observe the transfer function, “CLTF”, as you vary the gains. You can print CLTF in the console window to verify this.

GTA’s Signature

PID controller in closed-loop system

For this lab exercise, we are now going to simulate a PID system, with Kp, Ki and Kd gains operating together.

Make the appropriate edit to the file “Control_lab2_ex9”

The original open loop transfer for the plant is given as:

sys = tf (1/I,[1 2*xi*wn wn^2]

So you can assign 3 variables now, Kp, Kd and Ki. You should keep the script written in such a way that you can independently vary Kp, Kd and Ki to note the impact on the system response and the pole/zero positions.

Kp=10;

sysKp = tf(Kp,1) Kd=1;

sysKd = tf([Kd 0],1)

Ki=1;

sysKi = tf(Ki,[1 0])

OLTF = (sysKp+sysKd+sysKi)*sys 

CLTF=OLTF/(1+OLTF)

CLTF is the closed loop transfer function, Kp, Kd and Ki can be varied separately.

Edit the script to plot both the transient step response and the poles of the loop in order to be able to analyse the following questions:

Note the response on the output as you vary both Kp and Ki for the following parameters:

Rise timeOvershootSettling TimeSteady State error

Please show which gain has the largest impact on which parameter and give clear reasons why this should be the case.

As you vary the gains in the system please take note of how this impacts the pole and zero positions and give explanations as to the behaviour.

You should observe the transfer function, “CLTF”, as you vary the gains. You can print CLTF in the Console window to verify this.

GTA’s Signature

PID controller – Simulink

For this lab exercise, we are going to use Simulink and the available blocks that can be dragged from the Palette Browser under the “Continuous time systems” tab. You are going to create a schematic as shown in Figure 6.

Figure 6

The PID block will allow you to enter the Kp, Ki and Kd gains directly and allow experimentation to quickly ascertain how each influences the output.

Let’s have a quick reminder of how each gain influences the output:

The proportional gain, Kp, is always assigned a non-zero value and plays a part in setting the rise time and steady state error, although it will never on its own remove the steady state error.

The derivative gain, Kd, reacts to changes in the controller input and therefore helps to reach steady state quicker. However, setting this gain too high could lead to stability issues.

The integral gain, Ki, eliminates the steady state error, but as it creates a pole at DC then if set too high could lead to oscillation and ultimately instability.

All 3 can be varied independently from each other to provide an optimal output and this is why PID controllers are so popular today.

As a first experiment, assume the controller transfer function above. By setting Kd and Ki to zero and influencing Kp, note what happens to the output response. Why does the output behave like this?

What happens:

Steady-State Error: With only Kp active, the system will always exhibit some steady-state error (the difference between the desired setpoint and the actual output). This occurs because the proportional controller can only reduce the error but cannot completely eliminate it.

Response Speed: Increasing Kp will make the system respond faster (shorter rise time) because the controller reacts more aggressively to any error. However, too high a Kp can cause overshoot.

No Oscillation Damping: Without the derivative term (Kd=0), there's no mechanism to dampen oscillations, so the system might oscillate more before settling.

No Error Elimination: Without the integral term (Ki=0), there's no mechanism to "remember" and accumulate past errors, so any persistent error remains uncorrected.

Why:

Proportional control alone provides an immediate response proportional to the current error

It cannot account for how quickly the error is changing (needs derivative)

It cannot account for how long the error has persisted (needs integral)

It reaches a point where the control action balances the system's response, leaving residual error

Figure 7

Hint: by calculating the Characteristic equation of the above loop you can plot the poles of the equation and understand the system behaviour.

“pole(Characteristic Equation)” in OLTF and CLTF

Alternatively, you can create a script that will plot the poles to allow you to visualise easily where the poles move to depending on the system gain configuration.

So from this what do you conclude is the reason for the output behaving as it does with Kp=1, Ki and Kd=0?

With Kp=1 and Ki=Kd=0, the system exhibits steady-state error because the proportional controller alone cannot eliminate residual error (no integral action) and may show oscillatory response (no derivative damping). The poles remain in the left-half plane (stable), but their placement explains the compromise between response speed and precision in pure P-control—faster than low-gain systems yet inherently inaccurate due to missing integral pole at the origin.

Kp = 1, Kd = Ki = 0:

Figure 7

 , when Kp = 1, the steady error is 0.5

Now in addition to Kp=1, add derivative gain, Kd=1 and note the change in behaviour. Explain this by again looking at the poles and zeros in the system

using the console or edit your script that you generated above. Note also in this case the steady-state output error and explain this based on the closed loop transfer function calculated in the Console.

With Kd​=1, the system responds faster, with reduced peak time tp and rise time tr. However, too large ​ Kd​ could lead to oscillation.

Using pzplot(CLTF), you'll see the system adds a zero, poles shift left (more stable), but with increased imaginary part, indicating faster yet potentially more oscillatory response.

The system still exhibits steady-state error for step input, because it lacks integral action.

Figure 8

Figure 9

Finally add integral gain and experiment with the system output.

Kp = Ki = Kd = 1:

With integral action, steady-state error is eliminated. But large Ki may cause low-frequency oscillation or increased overshoot.

Figure 10

Figure 11

Outline your conclusions on how each of the gains impacts the system as outlined in points 4-7.

Kp:Increases speed, reduces steady-state error, may cause overshoot

Kd:Suppresses overshoot, improves stability, accelerates response

Ki:Eliminates steady-state error, but may introduce low-frequency oscillation

Now make a change to the transfer function that will ensure all poles are on the LHP and repeat the experiments from 4 to 7.

Let us now setup a somewhat more complex system and check disturbance and tracking attenuation and performance. Create a schematic in Simulink that represents the system as shown in Figure 7. This could be a joint that’s subject to an external force N(s). J is the joint inertia and B is the frictional

 𝐾 𝐾resistance.

𝐾

𝐾

𝑑𝐾   ++ 𝐾 𝑠𝑑𝐾   ++ 𝐾 𝑠1 𝑠2 + 𝑠1 𝑠2 + 𝑠𝑠𝑠𝑝𝑝 (𝑠)

𝑑

𝐾   ++ 𝐾 𝑠

𝑑

𝐾   ++ 𝐾 𝑠

1

 𝑠2 + 𝑠

1

 𝑠2 + 𝑠

𝑠

𝑠

𝑝

𝑝

 (𝑠)

𝜃 (𝑠)+

𝜃(𝑠)

Let’s assume J=10 and B=0.1.

Figure 7

Set the N(s) disturbance to 20V and apply at 40s.

Apply the reference input, 𝜃 , at 20s.

Set the Kp gain to 1 and all others to zero.

Observe the output and explain what is happening and why. You can plot the poles using the Console by entering the characteristic closed loop equation or use a script to plot the poles and zeros.

Kp = 1, Kd = Ki = 0:

Figure 12

At 20 seconds, the system responds to the reference input 𝜃, but since there is only proportional control, the system output fails to reach the reference fully (i.e., steady-state error exists).

At 40 seconds, a disturbance N(s)=20V is applied at the output. This causes a sudden shift in the output, which remains afterwards.

Because the system lacks integral action, it cannot reject the disturbance or correct the steady-state error.

Thus, the system is sensitive to disturbances, and cannot restore output to the reference without additional control terms.

What happens to the steady state error as you increase the gain Kp to say 100? Does it change the transient behaviour?

Figure 13

Increasing Kp to 100:

Reduces the steady-state error significantly, since the controller reacts more strongly to error.

However, it does not eliminate the error completely, because the system is still Type 0 (no integrator in the loop).

The transient response becomes faster (shorter rise time), possibly with slight overshoot.

Larger Kp​ improves the performance, but is not sufficient to eliminate steady-state error or reject disturbances.

What change in the plant transfer function would need to take place to change this behaviour?

Let us now start to calculate the optimal gains for this system. Let us set the integral gain, Ki to 0. This can be added at the end to remove any steady state error. Let us select optimal Kp and Kd gains. Let’s assume we want an overall critically damped system with ζ = 1 and let us select a natural frequency,

𝜔𝑛 of 10 rad/sec.

Firstly, calculate the Closed Loop Characteristic Equation. This isn’t too difficult as we know the plant – in some cases the plant is unknown, and the controller would have to be designed using the Zeigler Nichols method.

Then equating the coefficients calculate the required Kp and Kd to provide the required specification as above.

Using the values you have calculated simulate your system in Simulink and then try some experiments by selecting new values of 𝜔𝑛 (and hence Kd and Kp) and note how this changes the response of the output.

Comment on the steady state error when using only a PD controller (Kp and Kd gain only). Can it be completely removed only using PD control?

Figure 14

    and    

In order to get  as 1 and  as 10, then Kp = 1000 and Kd = 199.9

as a result, the steady state error is 0.

Now introduce integral control, Ki. Calculate the new closed loop Characteristic equation. Note that the integrator raises the order of the system. What is the best method for calculating the maximum allowable gain, Ki, before instability occurs?

Use the Routh–Hurwitz criterion，The characteristic equation turns to , Ki needs to be less than 20000.

Ki = 18000:

Figure 15

Ki = 21220:

Figure 16

Ki = 25000:

Figure 17

Use this method and simulate with the calculated gain values in Simulink to verify your calculation.

Observe any ringing that occurs during the disturbance – does the frequency match your target 𝜔𝑛?

Kp= 4000，Kd= 399.9, Ki = 160000

Figure 18

From simulation result, we observe clear ringing in the output signal after the disturbance is applied at around t = 40s.

The frequency measured from the Scope isΔT=50s for 1000 cycles. So, 𝑓=20Hz and 𝜔=2𝜋𝑓≈125.66 rad/s

Compared to your target natural frequency ωn=10 rad/s, the actual oscillation frequency is much higher, indicating that the ringing does not match the target frequency, and suggests that:

The gain values, especially high Ki =160000, are causing the system to enter a high-frequency oscillatory mode

The system is likely overcompensating and generating undesired high-frequency dynamics, possibly on the verge of instability

Does the output respond faster or slower as you increase 𝜔𝑛?

Increasing ωn makes the system faster, with reduced rise and peak time, but may increase overshoot or cause minor oscillations.

** You will be required to include answers (and programs) from this Lab in your final report for assessment. The specific instructions will be communicated to you at the end of Lab 4.

1010

10

10

UESTC 3001/UESTCHN 3007 Lab 2 and 3 (2024/2025)