x1=sym('cos(pi*t/5)');
x2=sym('sin(pi*t/5)');
x3=sym('exp(i*2*pi*t/3)+exp(i*pi*t)');
syms a;
E1=int(x1^2,[-a,a]);
E2=int(x2^2,[-a,a]);
x3c=subs(x3,'i','-i');
E3=int(x3*x3c,[-a,a]);
subplot(3,1,1);
ezplot(E1,[0,30]);xlabel ('a');ylabel('Ea for x1');title('Plot of Ea for x1');
subplot(3,1,2);
ezplot(E2,[0,30]);xlabel ('a');ylabel('Ea for x2');title('Plot of Ea for x2');
subplot(3,1,3);
ezplot(E3,[0,30]);xlabel ('a');ylabel('Ea for x3');title('Plot of Ea for x3');
Et1=int(x1^2,[-5,5])
Et2=int(x2^2,[-5,5])
ET3=int(x3*x3c,[-3,3]);
Et3=eval(ET3)

