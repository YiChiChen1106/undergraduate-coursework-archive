# Control_lab2 Answer sheet

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

s2+cIs+mgl2IΘ(s)=1ITs

So

Ps=ΘsTs=1Is2+cIs+mgl2I

Since

I=ml24

So

Ps=ΘsTs=4ml2s2+4cml2s+2gl=4ml2s2+4cs+2mgl

Using the standard form and the characteristic equation derive expressions for

𝜔𝑛 (undamped natural frequency) and ζ (damping ratio).

Since

Ps=ΘsTs=1Is2+cIs+mgl2I=1Is2+2ξωns+ωn2

So

2ξωn=cI, ωn2=mgl2I

So

ωn=mgl2I, ξ=c22mglI

Since

I=ml24

So

ωn=2gl, ξ=2c2m2gl3

Let’s assume the following physical parameters for the link shown above:

𝑚 = 5 kg (mass);

𝑙 = 0.4 m (length);

𝑐 = 0.5 (damping coefficient);

𝑔 = 9.81 m/s2 (gravity)

Using these parameters and the transfer function derived in #1 above, let’s use Matlab to experiment and investigate how these physical properties relate to the dynamic behaviour of the system and also how they relate to the poles of the system, which, as we know, set the dynamic behaviour.

Open the file “Control_lab2_student.m”

This file contains all the equations and the transfer function definition to allow you to start running the following exp eriments:

Vary the physical parameters one by one (m, l and c) and notice their impact on the step response of the system. Explain clearly why each parameter below is impacted (or maybe not) by the changes you make in each of the physical parameters.

MP, output overshoot.

Since Mp=100e-ξωntp%

When c increases or m, l decreases, Mp decreases

ts, output settling time.

Since ts=3ξωn

When c increases or m, l decreases, ts increases 

tp, time where the maximum output peak occurs.

Since tp=πωd

When c, m decreases or l increases, tp increases 

tr, rise time

Since tr=1ωdtan-11-ζ2ζ

When m, l increases, c decreases, tr increases

𝜔𝑛, the natural undamped frequency.

Since ωn=2gl

When l increases, ωn decreases

𝜔𝑑, the damped frequency.

Since ωd=ωn1-ζ2

When c, l increases,  or m decrease, ωddecrease

Comment on the steady state error of the output for each of the changes you make in the physical parameters. Is this output as expected? Explain why.

According to x∞=Kaωn2,

ess=limt→∞et=r∞-c∞=1-Kaωn2=1-2mgl

So as m or g grows, the steady state error grows, up to 1

By using the “pzplot” function plot the poles and note how their positions vary as you vary the physical parameters. Correlate the position of the poles to the transient response of the output and give full explanations why the pole positions vary as they do and why the correlation to the output behaves accordingly.

Since Ps=ΘsTs=4ml2s2+4cml2s+2gl=4ml2s2+4cs+2mgl

ps=

let qs=ml2s2+4cs+2mgl=0

So the poles are s=-4c+16c2-8m2gl32ml2, s=-4c-16c2-8m2gl32ml2

That is to say, when 2c2≥m2gl3, the poles are real and negative, that is, on the left half of the sigma axis.  When 2c2<m2gl3, the poles are complex, that is, mirrored around a point on the left half of the sigma axis.

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

When Kp changes,

Mp does not change,

ts does not change,

tp does not change,

tr does not change,

ωn does not change,

ωd does not change.

This is because multiplying Kp means scaling the value of the signal in time domain. So parameters related with time are not influenced, and Mp, which is the ratio of maximum overshoot against the steady state value, is also not influenced because the scale operation is eliminated.

Comment on the steady state error of the output for each of the changes you make in the proportional gain, Kp. Is this output as expected? Explain why.

According to x∞=Kaωn2,

ess=limt→∞et=r∞-c∞=1-Kaωn2=1-2Kpmgl

So as Kp grows, the steady state error decreases

By using the “pzplot” function plot the poles and note how their positions vary as you vary the proportional; gain, Kp. Correlate the position of the poles to the transient response of the output and give full explanations why the pole positions vary or not vary.

The poles does not change since the characteristic equation does not change.

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

It is clear that there is a faint oscillation of 0.2 even after a long time as it should be steady, which is introduced by the disturbance. That is because a open loop system do not have the ability to eliminate noise.

Modify the gain, Kp, and note if changing the gain has any impact on the output behaviour during the disturbance.

Compared to the above result at Kp=100, setting Kp to 5 amplifies the impact of disturbance, although the value is same. This is because the signal noise ratio decreases.

Modify parameter, c and observe the behaviour of the system output. Explain why the output behaves the way it does.

As c increases, the system changes from overdamped to underdamped, the steady state value does not change.

This is because the steady state value is given by x∞=Kaωn2, which is not related with c, while c will influences the poles.

Explain what you are observing and if this behaviour is as you would expect and why.

Here we see how disturbance impact a open loop second order system and how the impact changes when modifying Kp and c.

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

ts, output settling time.

tp, time where the maximum output peak occurs.

tr, rise time.

𝜔𝑛, the natural undamped frequency.

𝜔𝑑, the damped frequency.

Since CLTF=1Is2+cIs+mgl+22I, compared to sys=1Is2+cIs+mgl2I, ωn increases and ξdecreases

So Mp, tp, tr, ts decreases and ωd increases

Comment on the steady state error.

ess=1-Kωn2, since ωn increases so ess increases compared to sys

Type “CLTF” in the command window and note the transfer function.

CLTF =

           5 s^2 + 17.5 s + 245.2

  ----------------------------------------

  s^4 + 7 s^3 + 115.3 s^2 + 360.8 s + 2651

Type “sys” in the command window and note the transfer function.

sys =

           5

  -------------------

  s^2 + 3.5 s + 49.05

What do you observe about the difference between the denominator of “CLTF” and “sys”?

CLTF can be simplified to 5s2+3.5s+54.05, so densCLTF=denssys+numssys

Calculate the transfer function by hand and enter it in MATLAB compare it with what MATLAB gave you. Plot the step response of both functions on the same graph. What do you observe?

Comparing CLTF=5s2+17.5s+245.2s4+7s3+115.3s2+360.8s+2651 with CLTF=5s2+3.5s+54.05, their response has no difference.

Use the functions pole(sys), zero(sys) on the transfer function you calculated, and the closed-loop transfer function given by MATLAB. What can you say about the poles and zeros of the closed-loop transfer function given by MATLAB and your calculation? Are they the same? What does that tell you about your simulation software?

Using pzplot() on both system we could  see there is a difference that my version missed two poles and two zeros, which are introduced by the numerator of MATLAB’s CLTF, however, I eliminated it without considering whether it could be zero in some circumstances. So a simulation software could be really helpful. (with the default parameter values)

By looking at the position of the poles, have the poles varied in position compared to the open loop case? Why do you so answer?

Compared to poles of the open loop system, the closed loop system has two more poles with same real part and larger imaginary part, which is introduced by denssys+numssys=0

Vary the parameters “c” (the damping coefficient) and “l” (the length) and note the impact on the transient response and pole positions. Try and have the system go into oscillation, explain how you did it and how this impacted the position of the system poles.

When all poles have no imaginary part a system is critically damped or overdamped, so to have the system go into oscillation, we just let b2-4ac<0, that is to say, by increasing c or decreasing l.

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

MP, output overshoot.

ts, output settling time.

tp, time where the maximum output peak occurs.

tr, rise time.

𝜔𝑛, the natural undamped frequency.

𝜔𝑑, the damped frequency.

The Mp, ts, tp, tr OF CLTF is always smaller than the ones of OLTF, the ωn, ωd of CLTF is always larger than the ones of OLTF.

And as Kp grows, the difference between parameters of CLTF and parameters of OLTF becomes larger.

Comment on the steady state error. Why is it different if we vary Kp?

Since  ess=1Kp+1

So when Kp increases, ess decreases

Type “sys” in the command window and note the transfer function.

sys =

           5

  -------------------

  s^2 + 3.5 s + 49.05

Continuous-time transfer function.

Type “CLTF” in the command window and note the transfer function.

CLTF =

           50 s^2 + 175 s + 2452

  ----------------------------------------

  s^4 + 7 s^3 + 160.3 s^2 + 518.3 s + 4858

Continuous-time transfer function.

What do you observe about the difference between the denominator of “sys” and “CLTF”?

densCLTF=denssys×(denssys+Kp×numssys)

What differences in the denominator of the transfer function occur as you increase Kp? For this example, create another polynomial, OLTF, in your script, which is merely the pendulum transfer function multiplied by Kp.

OLTF =

          50

  -------------------

  s^2 + 3.5 s + 49.05

Continuous-time transfer function.

By looking at the position of the poles, have the poles varied in position compared to the open loop case and the closed loop case with unity gain?

When Kp=1, the case is same with exercise IV.

How do the pole positions change as Kp is varied?

Since densCLTF=denssys×(denssys+Kp×numssys)

So the two poles introduced by denssys=0 will not change as Kp changes, while the two poles introduced by denssys+Kp×numssys=0 get further from the real axis as Kp increases.

Will this be the reason for the change in dynamic performance as Kp is varied?

The above statement show out why a too big Kp may cause oscillation.

GTA’s Signature

Closed-loop transfer function with disturbance

For this lab exercise, we are now going to add a step disturbance to the output on previous exercise we carried out in section V.

Make the appropriate edit to the file “Control_lab2_ex6b.m”.

Modify “Control_lab2_ex3.slx” so that the closed-loop system resembles what is shown below and save it as “Control_lab2_ex6.slx” as shown below:

Figure 5

Run your Control_lab2_ex6b.m file as this will set up all of your variables. When changing any variables change using this script and rerun the script before rerunning the Simulink simulation.

By observing the output response, as before to a unit step input, what do you observe about the output of the system during the times that the disturbance is applied and then removed?

The disturbance will active the steady state response and there will be a oscillation of the disturbance. So even the disturbance is removed, there could still be error.

Modify the gain, Kp, and note if changing the gain has any impact on the output behaviour during the disturbance. Please explain why changing the gain, Kp, has influence on the response to disturbance, if any.

Since the disturbance will also be a input, how Kp works on the reference input also works for the disturbance.

Tie in your response for question 7 by plotting the poles and tying in the pole positions to what you see on the transient response due to a step input and the output disturbance, for various physical parameters such as Kp, c, etc.

As c increases, the system changes from overdamped to underdamped, the steady state value does not change.

This is because the steady state value is given by x(∞)=Ka/(ω_n^2 ), which is not related with c, while c will influences the poles.

And as Kp increases, the impact of disturbance seems become smaller, although the value is same. This is because the signal noise ratio increases.

Modify parameter, c and observe the behaviour of the system output. Explain why the output behaves the way it does.

As c increases, the system changes from overdamped to underdamped, the steady state value does not change.

This is because the steady state value is given by x(∞)=Ka/(ω_n^2 ), which is not related with c, while c will influences the poles.

Explain what you are observing and if this behaviour is as you would expect and why.

Here we see how disturbance impact a closed loop second order system and how the impact changes when modifying Kp and c.

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

Kp has the largest impact on the rise time, steady state error and overshoot since the proportional control introduce a steady state error, and scale the system, while integrational control is mainly for steady state error elimination.

As you vary the gains in the system please take note of how this impacts the pole and zero positions and give explanations as to the behaviour of the time-domain response.

Except from the two poles introduced by sys, increasing Ki will increase the real part of the poles.

You should observe the transfer function, “CLTF”, as you vary the gains. You can print “CLTF” in the console window to verify this.

CLTF =

            150 s^4 + 1700 s^3 + 9357 s^2 + 9810 s

  -----------------------------------------------------------

  s^6 + 20 s^5 + 348.1 s^4 + 2681 s^3 + 1.176e04 s^2 + 9810 s

Continuous-time transfer function.

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

Kd has the largest impact on the overshoot, settling time as it predict the trend.

Kp has the largest impact on the others.

As you vary the gains in the system please take note of how this impacts the pole and zero positions and give explanations as to the behaviour.

As Kd increases the two poles reaches the real axis and the real part becomes smaller.

You should observe the transfer function, “CLTF”, as you vary the gains. You can print CLTF in the console window to verify this.

CLTF =

       100 s^3 + 1500 s^2 + 9905 s + 2.452e04

  ------------------------------------------------

  s^4 + 120 s^3 + 1698 s^2 + 1.089e04 s + 2.693e04

Continuous-time transfer function.

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

Kp has the largest impact on rise time, settling time

Kd has the largest impact on overshoot

Ki has the largest impact on steady state error

As you vary the gains in the system please take note of how this impacts the pole and zero positions and give explanations as to the behaviour.

Increasing Kp will increase the imaginary part of the poles.

Increasing Ki will increase the real part of the poles.

Increasing Kd will decrease both the real part of the poles and imaginary part.

You should observe the transfer function, “CLTF”, as you vary the gains. You can print CLTF in the Console window to verify this.

CLTF =

     200 s^5 + 5250 s^4 + 4.306e04 s^3 + 1.669e05 s^2 + 3.679e04 s

  -------------------------------------------------------------------

  s^6 + 220 s^5 + 5448 s^4 + 4.404e04 s^3 + 1.693e05 s^2 + 3.679e04 s

Continuous-time transfer function.

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

By setting Kd and Ki to zero we are getting a Proportional control, so as Kp increases, the settling time decreases, steady state error increases, and may becomes to oscillate.

Hint: by calculating the Characteristic equation of the above loop you can plot the poles of the equation and understand the system behaviour.

“pole(Characteristic Equation)” in OLTF and CLTF

Alternatively, you can create a script that will plot the poles to allow you to visualise easily where the poles move to depending on the system gain configuration.

So from this what do you conclude is the reason for the output behaving as it does with Kp=1, Ki and Kd=0?

Since ess=11+Kp , that is why there is a ess of 0.5 with Kp=1, Ki and Kd = 0

And since when Kp increase, the system becomes underdamped, that is why when Kp = 1, the system is overdamped

Now in addition to Kp=1, add derivative gain, Kd=1 and note the change in behaviour. Explain this by again looking at the poles and zeros in the system

using the console or edit your script that you generated above. Note also in this case the steady-state output error and explain this based on the closed loop transfer function calculated in the Console.

Finally add integral gain and experiment with the system output.

Outline your conclusions on how each of the gains impacts the system as outlined in points 4-7.

So Kp impacts the rise time

Kd impact the damping quality

Ki impact the steady state error.

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

What happens to the steady state error as you increase the gain Kp to say 100? Does it change the transient behaviour?

The system starts to oscillates very much.

What change in the plant transfer function would need to take place to change this behaviour?

Increase B or decrease J to increase ξ, so it becomes overdamped.

Let us now start to calculate the optimal gains for this system. Let us set the integral gain, Ki to 0. This can be added at the end to remove any steady state error. Let us select optimal Kp and Kd gains. Let’s assume we want an overall critically damped system with ζ = 1 and let us select a natural frequency,

𝜔𝑛 of 10 rad/sec.

Firstly, calculate the Closed Loop Characteristic Equation. This isn’t too difficult as we know the plant – in some cases the plant is unknown, and the controller would have to be designed using the Zeigler Nichols method.

Then equating the coefficients calculate the required Kp and Kd to provide the required specification as above.

Using the values you have calculated simulate your system in Simulink and then try some experiments by selecting new values of 𝜔𝑛 (and hence Kd and Kp) and note how this changes the response of the output.

Comment on the steady state error when using only a PD controller (Kp and Kd gain only). Can it be completely removed only using PD control?

Kp=100, Kd=19.9

The steady state error can not be removed but only decrease using only PD and it could be big.

Now introduce integral control, Ki. Calculate the new closed loop Characteristic equation. Note that the integrator raises the order of the system. What is the best method for calculating the maximum allowable gain, Ki, before instability occurs?

The equation becomes Js3+B+Kds2+Kps+Ki=0

When pole appears in the right half plane, the system becomes unstable. So let s=aj

We have -10a3j-20a2+100aj+Ki=0

So Kimax=200

Use this method and simulate with the calculated gain values in Simulink to verify your calculation.

Observe any ringing that occurs during the disturbance – does the frequency match your target 𝜔𝑛?

Does the output respond faster or slower as you increase 𝜔𝑛?

It respond faster as ωn increases.

GTA’s Signature

1010

10

10

  Control lab 2

Student1-Name

GUID

Student2-Name

GUID

Zhuheng Song

[student-id-redacted]