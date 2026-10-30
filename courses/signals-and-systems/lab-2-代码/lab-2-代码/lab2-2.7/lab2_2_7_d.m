clc
clear
nh=[0:9];
nx=[-9:99];
h=[(0.9).^nh];
x=[cos(nx.^2).*sin(2*pi*nx/5)];
y0=conv(h,x);
ny=[0:99];
y=[];
for k=0:99
y(end+1)=y0(k+10);
end
stem(ny,y,'fill');
xlabel('n');
ylabel('y[n]');
title('The figure of the signal y[n]=h[n]*x[n]');
grid on;