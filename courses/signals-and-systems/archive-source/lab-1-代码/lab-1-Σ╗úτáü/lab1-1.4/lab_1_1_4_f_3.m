% (3)	Prove the system is not invertible:
n=[-10:10];
x=[zeros(1,10) 1 zeros(1,10)];
y=n.*x;
subplot(3,1,1);
stem(n,x);xlabel('n');ylabel('x[n]');title('The figure of the signal x[n]');
grid on;
subplot(3,1,2);
stem(n,y);xlabel('n');ylabel('y[n]');title('The figure of the signal y[n]');
grid on;
w=1./n.*y;
subplot(3,1,3);
stem(n,w);xlabel('n');ylabel('w[n]');title('The figure of the signal w[n]');
grid on;