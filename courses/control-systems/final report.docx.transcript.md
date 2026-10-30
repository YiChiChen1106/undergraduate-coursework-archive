# final report

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Lab1.Q2G

Code General_characteristics.m

function general_charateristics(L1,C1,alpha,A1,A2)

    t = 0:1e-6:0.5e-3;

    omega_n = 1/sqrt(L1*C1);

    wd = sqrt(omega_n^2 - alpha^2);

    vc = A1*exp((-alpha+1j*wd)*t) + A2*exp((-alpha-1j*wd)*t);

    plot(t*1e3, real(vc), 'LineWidth', 2);

    grid on;

    xlabel('time (ms)');

    ylabel('Vc (V)');

    title('Effects of L, C, α');

    grid minor

    axis tight

end

Below each plot corresponds to one of the parameter sets in our table. In all cases, C1=7.9×10−8 F, and the curves show vC(t) over the first 0.5 ms.

Case 1: L1=0.01H, α=20,000 s⁻¹ (ζ≈0.56, underdamped)

Oscillatory behavior: Since ζ<1 we see clear sinusoidal oscillations around zero.

Frequency: The damped frequency   ωd=ωn1-ζ2≈29,400 gives a period T≈0.21ms; the first positive peak occurs at ≈0.06 ms.

Envelope decay: The exponential envelope decays with time constant τ=1/α=50 µs, so successive peaks shrink rapidly.

Peak amplitude: The first overshoot reaches about +0.55 V.

Case 2: L1=0.01H, α=25,000s⁻¹ (ζ≈0.70, still underdamped)

Reduced oscillations: Raising α increases damping; oscillations persist but with smaller amplitude (~0.40 V first peak).

Faster decay: Envelope decays more quickly (τ=40 µs), so the waveform settles to zero in fewer cycles.

Same period: Because L1 and C1 are unchanged, the oscillation period remains ~0.21 ms.

Case 3: L1=0.0202H, α=25,000s⁻¹ (ζ≈1.00, critically damped)

No oscillation: At ζ=1, the response shows a single exponential rise to steady state without overshoot.

Fastest non-oscillatory settle: This curve reaches the final value more quickly than any overdamped case—ideal for fastest monotonic response.

Case 4: L1=0.032H, α=25,000s⁻¹ (ζ≈1.26, overdamped)

Monotonic, sluggish: With ζ>1, the system no longer oscillates, but the rise is slower than in the critically damped case.

Lower natural frequency: Increasing L1 reduces ωn (from ≈35 570 to ≈19 900 rad/s), so the overall response is stretched in time.

Overall Conclusions

Damping ratio ζ: Controls whether the response oscillates (ζ<1), is perfectly non-oscillatory and fastest (ζ=1), or is over-damped and slow (ζ>1).

Damping constant α: Increasing αat fixed L,C reduces oscillation amplitude and speeds up decay, but does not change the oscillation period.

Inductance LLL: For constant α,C, larger L lowers ωn, lengthening the period (or time-scale) of the response and, if α\alphaα is unchanged, increasing ζ.

These slider-based experiments vividly confirm the textbook relations for a second-order RLC circuit’s transient behavior.

Q3

A. Effect of α

Increasing the damping constant α\alphaα always reduces the amplitude of the oscillations.

Reason: The damping ratio is

ζ=αωn,ωn=1L C

A larger α⇒ larger ζ⇒ smaller peak overshoot(for underdamped, 0<ζ<10 the overshoot Mp=exp-π ζ1-ζ2 falls as ζ rises).

Conclusion: To suppress oscillations, increase α.

B. Effect of L1​ (with R1​ fixed)

Because α=R1/(2L1), if R1 is held constant then

ζ=R1/2L11/L1C1=R1C12 L1

As L1 increases, the denominator L1​​ grows ⇒ ζ decreases ⇒ more oscillatory.

As L1 decreases, ζ increases ⇒ oscillations damp out faster.

Conclusion: To reduce oscillations with R1​ fixed, decrease L1​.

C. Effect of C1​ (with R1​ fixed)

Still holding R1​ constant,

ζ=R1C12 L1

As C1​ increases, C1​​ grows ⇒ ζgrows ⇒ stronger damping.

Conversely, decreasing C1​ lowers ζ and lets oscillations persist.

Conclusion: To suppress oscillations, increase C1​.

D. Energy Dissipation vs. R1​

Stored energy in the capacitor:EC=12C1VC2.\displaystyle E_C=\tfrac12 C_1 V_C^2.EC​=21​C1​VC2​.

Instantaneous power dissipated in R1R_1R1​:PR=VC2R1.\displaystyle P_R = \tfrac{V_C^2}{R_1}.PR​=R1​VC2​​.

Time‐constant for energy decay in a second‐order RLC is τ=1/α=2L1/R1\tau = 1/\alpha = 2L_1/R_1τ=1/α=2L1​/R1​.

As R1R_1R1​ increases ⇒ α\alphaα increases ⇒ τ\tauτ decreases ⇒ energy is dissipated faster.

Conclusion: Yes, larger R1R_1R1​ causes the capacitor’s stored energy to dissipate more quickly.

E. Overshoot Amplitude vs. Capacitance

From EC=12C1V2E_C=\tfrac12C_1V^2EC​=21​C1​V2, a larger C1C_1C1​ stores more energy for the same VVV.

However, increasing C1C_1C1​ also increases ζ\zetaζ (see part C), which reduces the normalized overshoot MpM_pMp​.

Net effect: Even though the capacitor can hold more energy, the voltage overshoot decreases when C1C_1C1​ is increased (all else held constant).