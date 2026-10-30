clc
clear all
n=-20:100;
a=[1 -0.25];
b=[1 0.9];
x1=exp(1i*pi*n/4);
x2=sin(pi*n/8+pi/16);
x3=(9/10).^n;
x4=n+1;
y1=filter(b,a,x1);
y2=filter(b,a,x2);
y3=filter(b,a,x3);
y4=filter(b,a,x4);
figure(1);
Y1=[];
for k=0:100
Y1(end+1)=y1(k+21);
end
subplot(2,1,1);
stem([0:100],real(Y1));
xlabel('n');
ylabel('The real component of y1[n]');
title('The figure of the real component of the signal y1[n]');
grid on;
subplot(2,1,2);
stem([0:100],imag(Y1));
xlabel('n');
ylabel('The imaginary component of y1[n]');
title('The figure of the imaginary component of the signal y1[n]');
grid on;
figure(2);
Y2=[];
for k=0:100
Y2(end+1)=y2(k+21);
end
stem([0:100],Y2);
xlabel('n');
ylabel('y2[n]');
title('The figure of the signal y2[n]');
grid on;
figure(3);
Y3=[];
for k=0:100
Y3(end+1)=y3(k+21);
end
stem([0:100],Y3);
xlabel('n');
ylabel('y3[n]');
title('The figure of the signal y3[n]');
grid on;
figure(4);
Y4=[];
for k=0:100
Y4(end+1)=y4(k+21);
end
stem([0:100],Y4);
xlabel('n');
ylabel('y4[n]');
title('The figure of the signal y4[n]');
grid on;
%..........(c)...............%
X1=[];
for k=0:100
X1(end+1)=x1(k+21);
end
X2=[];
for k=0:100
X2(end+1)=x2(k+21);
end
X3=[];
for k=0:100
X3(end+1)=x3(k+21);
end
X4=[];
for k=0:100
X4(end+1)=x4(k+21);
end
H1=Y1./X1;
H2=Y2./X2;
H3=Y3./X3;
H4=Y4./X4;
figure(5);
subplot(2,1,1);
stem([0:100],real(H1));
xlabel('n'),ylabel('The real component of H1');
title('The figure of the real component of the vector H1');
grid on;
subplot(2,1,2);
stem([0:100],imag(H1));
xlabel('n'),ylabel('The imaginary component of H1');
title('The figure of the imaginary component of the vector H1');
grid on;
figure(6);
stem([0:100],H2);
xlabel('n');
ylabel('H2');
title('The figure of the vector H2');
grid on;
figure(7);
stem([0:100],H3);
xlabel('n');
ylabel('H3');
title('The figure of the vector H3');
grid on;
figure(8);
stem([0:100],H4);
xlabel('n');
ylabel('H4');
title('The figure of the vector H4');
grid on;

