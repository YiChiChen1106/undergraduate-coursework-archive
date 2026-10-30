clc
clear all
%........(i)......%
b1=[1 5];
a1=[1 2 3];
zs1=roots(b1)
ps1=roots(a1)
figure;
plot(real(zs1),imag(zs1),'o');
xlabel('The real part');
ylabel('The imaginary part');
title('The zero-pole diagram of (i)');
hold on;
plot(real(ps1),imag(ps1),'x');
xlabel('The real part');
ylabel('The imaginary part');
title('The zero-pole diagram of (i)');
axis([-6 6 -6 6]);
grid on;
%........(ii)......%
b2=[2 5 12];
a2=[1 2 10];
zs2=roots(b2)
ps2=roots(a2)
figure;
plot(real(zs2),imag(zs2),'o');
xlabel('The real part');
ylabel('The imaginary part');
title('The zero-pole diagram of (ii)');
hold on;
plot(real(ps2),imag(ps2),'x');
xlabel('The real part');
ylabel('The imaginary part');
title('The zero-pole diagram of (ii)');
axis([-6 6 -6 6]);
grid on;
%........(iii)......%
b3=[2 5 12];
a3=[1 4 14 20];
zs3=roots(b3)
ps3=roots(a3)
figure;
plot(real(zs3),imag(zs3),'o');
xlabel('The real part');
ylabel('The imaginary part');
title('The zero-pole diagram of (iii)');
hold on;
plot(real(ps3),imag(ps3),'x');
xlabel('The real part');
ylabel('The imaginary part');
title('The zero-pole diagram of (iii)');
axis([-6 6 -6 6]);
grid on;