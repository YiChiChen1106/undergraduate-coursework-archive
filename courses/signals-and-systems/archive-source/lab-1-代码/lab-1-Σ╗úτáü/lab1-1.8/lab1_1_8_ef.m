x1=sym('cos(pi*t/5)');
x2=sym('sin(pi*t/5)');
x3=sym('exp(i*2*pi*t/3)+exp(i*pi*t)');
syms a;
E1=int(x1^2,[-a,a]);
E2=int(x2^2,[-a,a]);
x3c=subs(x3,'i','-i');
E3=int(x3*x3c,[-a,a]);
P1=E1/2/a;
P2=E2/2/a;
P3=E3/2/a;
subplot(3,1,1);
ezplot(P1,[0.1,60]);xlabel ('a');ylabel('Pa for x1');title('Plot of Pa for x1');
subplot(3,1,2);
ezplot(P2,[0.1,60]);xlabel ('a');ylabel('Pa for x1');title('Plot of Pa for x2');
subplot(3,1,3);
ezplot(P3,[0.1,60]);xlabel ('a');ylabel('Pa for x1');title('Plot of Pa for x3');
sum=P1+P2;
r=simplify(sum)