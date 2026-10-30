# Control lab 2

| Student Name | GUID     |
| ------------ | -------- |
| Zhuheng Song | [student-id-redacted] |

## A second order pendulum system

![image-20200505034009757](lab3/image-20200505034009757.png)

Likening the leg to a link, referring Figure 1 above. It has a length, **l**, and is free to rotate about 𝑂, as shown. The mass is **m** and the center of mass is located at 𝐺 which in turn is situated at 1/2, in the middle of the link. The moment of inertia, **l**, about the pivot point, 𝑂, is given by the relationship:

- $I=ml^2$

as the mass is centered at **l** then we have $I=m(\frac{l}{2})^2$. The knee-extensor muscles contract to hold the system in equilibrium at angle **$\theta_e$**, by application of a toorque, **$\tau_e$**, acting around $O$. The moment ($force \times distance$) required to maintain equilibrium, $\tau_e$, is:

- $\tau_e=(mg\frac{l}{2})sin \theta_e$

Assume now that the knee moves to a new angle of displacement, **$\theta$**. There will be a damping coefficient, $c$, as shown in Figure 1. This damping occurs naturally and is caused by physical properties of the muscle and tendon-bone connection. When the body is moving there is now a viscous damping moment that's proportional to the object velocity, or $\theta$. This damping moment is $c\theta$. The displacement angle is shown in Figure 2.

![image-20200505040443068](lab3/image-20200505040443068.png)

Let's now derive the differential equation that describes this system. From Newton's Law: $M=l\alpha$, where $M$ is the sum of all external moments about the center of mass, $I$ is the moment of inertia of the mass and 

## Proportional gain – Open loop transfer function

## Disturbance

## Closed-loop transfer function

## Closed-loop transfer function with proportional gain

## Closed-loop transfer function with disturbance

## PI controller in closed-loop system

## PD controller in closed-loop system

## PID controller in closed-loop system

## PID controller –Simulink