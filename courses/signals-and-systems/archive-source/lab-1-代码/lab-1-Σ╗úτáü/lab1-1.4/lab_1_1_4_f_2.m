% (2)	Prove the system is not stable:
n=[-10:10];
x=[ones(1,21)];
subplot(2,1,1);
stem(n,x);xlabel('n');ylabel('x[n]');title('The figure of the signal x[n]');
grid on;
y=n.*x;
subplot(2,1,2);
stem(n,y);xlabel('n');ylabel('y[n]');title('The figure of the signal y[n]');
grid on;
