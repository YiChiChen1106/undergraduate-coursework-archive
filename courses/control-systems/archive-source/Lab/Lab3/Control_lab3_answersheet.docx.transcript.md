# Control_lab3_answersheet

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Control lab 2

A second order pendulum system

Figure 1

Likening the leg to a link, referring Figure.1 above. It has a length, l, and is free to rotate about O, as shown. The mass is m and the centre of mass is located at G which in turn is situated at l2, in the middle of the link. The moment of inertia, I, about the pivot point, O, is given by the relationship:

I=ml2

as  the mass is centred at l2 then we have I=ml22. The knee-extensor muscles contract to hold the system in equilibrium at angle θe, by application of a torque, τe, acting around O. The moment (force x distance) required to maintain equilibrium, τe, is:

τe=mgl2sinθe

Assume now that the knee moves to a new angle of displacement, θ. There will be a damping coefficient, c, as shown in Figure.1. This damping occurs naturally and is caused by physical properties of the muscle and tendon-bone connection.

When the body is moving there is now a viscous damping moment that’s proportional to the object velocity, or θ. This damping moment is cθ. The displacement angle is shown in Figure. 2

Figure 2

Let’s now derive the differential equation that describes this system. From Newton’s Law: M=Iα, where M is the sum of all external moments about the centre of mass, I is the moment of inertia of the mass and α is the angular acceleration of the mass. The knee displacement is θ, angular acceleration is θ and therefore the total inertial moment is Iθ. Balancing all moments:

The final equation of motion is:

The transfer function of this system in standard form is therefore:

Convert the equation of motion from the time,t, domain to s domain and rewrite the transfer function as shown above but in the s domain.

Using the standard form and the characteristic equation derive expressions for ωn (undamped natural frequency) and ζ (damping ratio).

ζ=c2Iωn    ωn=mgl2I

Let’s assume the following physical parameters for the link shown above:

m=5 kg (mass);

l=0.4 m (length);

c=0.5 (damping coefficient);

g=9.81 m/s2 (gravity)

Using these parameters and the transfer function derived in #1 above, let’s use Matlab to experiment and investigate how these physical properties relate to the dynamic behaviour of the system and also how they relate to the poles of the system, which, as we know, set the dynamic behaviour.

Open the file “Control_lab2_ex1.m”

This file contains all the equations and the transfer function definition to allow you to start running the following experiments:

Vary the physical parameters one by one (m, l and c) and notice their impact on the step response of the system. Explain clearly why each parameter below is impacted (or maybe not) by the changes you make in each of the physical parameters.

MP, output overshoot.

ts, output settling time.

tp, time where the maximum output peak occurs.

tr, rise time 

ωn, the natural undamped frequency.

ωd, the damped frequency.

PID controller in closed-loop system

For this lab exercise, we are now going to simulate a PID system, with Kp, Ki and Kd gains operating together.

Make the appropriate edit to the file “Control_lab2_ex9” 

The original open loop transfer for the plant is given as:

sys = tf (1/I,[1 2*xi*wn wn^2]

So you can assign 3 variables now, Kp, Kd and Ki. You should keep the script written in such a way that you can independently vary Kp, Kd and Ki to note the impact on the system response and the pole/zero positions.

Kp=10;

sysKp = tf(Kp,1)

Kd=1;

sysKd = tf([Kd 0],1)

Ki=1;

sysKi = tf(Ki,[1 0])

OLTF = (sysKp+sysKd+sysKi)*sys

CLTF=OLTF/(1+OLTF)

CLTF is the closed loop transfer function, Kp, Kd and Ki can be varied separately.

Edit the script to plot both the transient step response and the poles of the loop in order to be able to analyse the following questions:

Note the response on the output as you vary both Kp and Ki for the following parameters:

Rise time          Overshoot          Settling Time           Steady State error

Please show which gain has the largest impact on which parameter and give clear reasons why this should be the case.

As you vary the gains in the system please take note of how this impacts the pole and zero positions and give explanations as to the behaviour.

You should observe the transfer function, “CLTF”, as you vary the gains. You can print CLTF in the Console window to verify this.

GTA’s signature

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

Hint: by calculating the Characteristic equation of the above loop you can plot the poles of the equation and understand the system behaviour. 

“pole(Characteristic Equation)” in OLTF and CLTF

Alternatively, you can create a script that will plot the poles to allow you to visualise easily where the poles move to depending on the system gain configuration. 

So from this what do you conclude is the reason for the output behaving as it does with Kp=1, Ki and Kd=0?

Now in addition to Kp=1, add derivative gain, Kd=1 and note the change in behaviour. Explain this by again looking at the poles and zeros in the system using the console or edit your script that you generated above. Note also in this case the steady-state output error and explain this based on the closed loop transfer function calculated in the Console.

Finally add integral gain and experiment with the system output. 

Outline your conclusions on how each of the gains impacts the system as outlined in points 4-7.

Now make a change to the transfer function that will ensure all poles are on the LHP and repeat the experiments from 4 to 7.

Let us now setup a somewhat more complex system and check disturbance and tracking attenuation and performance. Create a schematic in Simulink that represents the system as shown in Figure 7. This could be a joint that’s subject to an external force N(s). J is the joint inertia and B is the frictional resistance.

Figure 7

Let’s assume J=10 and B=0.1.

Set the N(s) disturbance to 20V and apply at 40s.

Apply the reference input, θr, at 20s.

Set the Kp gain to 1 and all others to zero.

Observe the output and explain what is happening and why. You can plot the poles using the Console by entering the characteristic closed loop equation or use a script to plot the poles and zeros.

What happens to the steady state error as you increase the gain Kp to say 100? Does it change the transient behaviour? 

What change in the plant transfer function would need to take place to change this behaviour?

Let us now start to calculate the optimal gains for this system. Let us set the integral gain, Ki to 0. This can be added at the end to remove any steady state error. Let us select optimal Kp and Kd gains. Let’s assume we want an overall critically damped system with ζ = 1 and let us select a natural frequency, ωn of 10 rad/sec.

Firstly, calculate the Closed Loop Characteristic Equation. This isn’t too difficult as we know the plant – in some cases the plant is unknown and the controller would have to be designed using the Zeigler Nichols method.

Then equating the coefficients calculate the required Kp and Kd to provide the required specification as above.

Using the values you have calculated simulate your system in Simulink and then try some experiments by selecting new values of ωn (and hence Kd and Kp)and note how this changes the response of the output.

Comment on the steady state error when using only a PD controller (Kp and Kd gain only). Can it be completely removed only using PD control?

Now introduce integral control, Ki. Calculate the new closed loop Characteristic equation. Note that the integrator raises the order of the system. What is the best method for calculating the maximum allowable gain, Ki, before instability occurs?

Use this method and simulate with the calculated gain values in Simulink to verify your calculation.

Observe any ringing that occurs during the disturbance – does the frequency match your target ωn?

Does the output respond faster or slower as you increase ωn?

GTA’s signature

4

Student 1 Name

GUID

Student 2 Name

GUID