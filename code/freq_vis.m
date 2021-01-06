Av = A*x; % Visual accelerations
Ai = b;    % Inertial accelerations

Av = [Av(1:3:end) Av(2:3:end) Av(3:3:end)];
Ai = [Ai(1:3:end) Ai(2:3:end) Ai(3:3:end)];

Fv = abs(fft(Av));
Fi = abs(fft(Ai));

Fv = Fv(freqRange,:);
Fi = Fi(freqRange,:);

plot(1:length(Fv),Fv(:,1),1:length(Fi),Fi(:,1))