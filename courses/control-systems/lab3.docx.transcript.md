# lab3

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

1.For this lab exercise, we are going to use Simulink and the available blocks that can be dragged from the Palette Browser under the “Continuous time systems” tab. You are going to create a schematic as shown in Figure 6.

Figure 6

2.The PID block will allow you to enter the Kp, Ki and Kd gains directly and allow experimentation to quickly ascertain how each influences the output.

3.Let’s have a quick reminder of how each gain influences the output:

The proportional gain, Kp, is always assigned a non-zero value and plays a part in setting the rise time and steady state error, although it will never on its own remove the steady state error.

The derivative gain, Kd, reacts to changes in the controller input and therefore helps to reach steady state quicker. However, setting this gain too high could lead to stability issue.

The integral gain, Ki, eliminates the steady state error, but as it creates a pole at DC then if set too high could lead to oscillation and ultimately instability.

All 3 can be varied independently from each other to provide an optimal output and this is why PID controllers are so popular today.

4.As a first experiment, assume the controller transfer function above. By setting Kd and Ki to zero and influencing Kp, note what happens to the output response. Why does the output behave like this?

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

5.Alternatively, you can create a script that will plot the poles to allow you to visualise easily where the poles move to depending on the system gain configuration.

So from this what do you conclude is the reason for the output behaving as it does with Kp=1, Ki and Kd=0?

With Kp=1 and Ki=Kd=0, the system exhibits steady-state error because the proportional controller alone cannot eliminate residual error (no integral action) and may show oscillatory response (no derivative damping). The poles remain in the left-half plane (stable), but their placement explains the compromise between response speed and precision in pure P-control—faster than low-gain systems yet inherently inaccurate due to missing integral pole at the origin.

Kp = 1, Kd = Ki = 0:

Figure 7

 , when Kp = 1, the steady error is 0.5

6.Now in addition to Kp=1, add derivative gain, Kd=1 and note the change in behaviour. Explain this by again looking at the poles and zeros in the system

using the console or edit your script that you generated above. Note also in this case the steady-state output error and explain this based on the closed loop transfer function calculated in the Console.

With Kd​=1, the system responds faster, with reduced peak time tp and rise time tr. However, too large ​ Kd​ could lead to oscillation.

Using pzplot(CLTF), you'll see the system adds a zero, poles shift left (more stable), but with increased imaginary part, indicating faster yet potentially more oscillatory response.

The system still exhibits steady-state error for step input, because it lacks integral action.

Figure 8

Figure 9

7.Finally add integral gain and experiment with the system output.

Kp = Ki = Kd = 1:

With integral action, steady-state error is eliminated. But large Ki may cause low-frequency oscillation or increased overshoot.

Figure 10

Figure 11

8.Outline your conclusions on how each of the gains impacts the system as outlined in points 4-7.

Kp:Increases speed, reduces steady-state error, may cause overshoot

Kd:Suppresses overshoot, improves stability, accelerates response

Ki:Eliminates steady-state error, but may introduce low-frequency oscillation