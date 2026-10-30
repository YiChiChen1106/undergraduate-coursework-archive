clc
clear
nh=[0:9];
nx0=[0:49];
nx1=[50:99];
nx00=[-9:49];
nx01=[41:99];
ny=[0:99];
x0=[cos(nx00.^2).*sin(2*pi*nx00/5)];
x1=[cos(nx01.^2).*sin(2*pi*nx01/5)];
h=[(0.9).^nh];
y00=conv(h,x0);
y01=conv(h,x1);
y10=[y00 zeros(1,41)];
y11=[zeros(1,40) y01];
y2=[];
for k0=0:49
y2(end+1)=y10(k0+10);
end
y0=[y2 zeros(1,50)];
y3=[];
for k1=50:99
y3(end+1)=y11(k1);
end
y1=[zeros(1,50) y3];
y=y0+y1;
figure(1);
subplot(2,1,1);
stem(ny,y0,'fill');
xlabel('n');
ylabel('y0[n]');
title('The figure of y0[n]');
grid on;
subplot(2,1,2);
stem(ny,y1,'fill');
xlabel('n');
ylabel('y1[n]');
title('The figure of The figure of y1[n]');
grid on;
figure(2);
stem(ny,y,'fill');
xlabel('n');
ylabel('y[n]');
title('The figure of  y[n]=y0[n]+y1[n]');
grid on;
%.........compare the result of (d)and（e）......%
nx=[-9:99];
x=[cos(nx.^2).*sin(2*pi*nx/5)];
yd0=conv(h,x);
yd=[];
for k=0:99
yd(end+1)=yd0(k+10);
end
t=yd-y;
figure(3);
stem(ny,t,'fill');
xlabel('n');
ylabel('difference value');
title('the result of (d) subtract the result of (e)');
grid on;
