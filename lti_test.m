


q = 45;
A1 = expm(F*dt);

n   = size(F,1);
Phi = [F L*q*L'; zeros(n,n) -F'];
ab1 = expm(Phi*dt)
AB  = expm(Phi*dt)*[zeros(n,n);eye(n)];
Q   = AB(1:n,:)/AB((n+1):(2*n),:);
