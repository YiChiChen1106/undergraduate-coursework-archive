n1=-5:9;
x=[zeros(1,5) ones(1,10)];
figure(1)
subplot(2,1,1);
stem(n1,x);xlabel('n1');ylabel('x[n]');title('The figure of the signal x[n]');
grid on;
n2=-6:9;
x1=[zeros(1,6) ones(1,10)];
x2=[zeros(1,5) ones(1,11)];
subplot(2,1,2);
stem(n2,x2);xlabel('n2');ylabel('x2[n]');title('The figure of the signal x2[n]');
y=x1+x2;
figure(2);
stem(n2,y);xlabel('n2');ylabel('y[n]');title('The figure of the signal y[n]');
grid on;
