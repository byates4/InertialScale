% % Use only time period which all sensors have values
% timeStop = min([tVis(end) tImu(end)]);
% tVis = tVis(tVis <= timeStop);
% tImu = tImu(tImu <= timeStop);
% 
% qtVis = qtVis(1:length(tVis),:);
% angImu = angImu(1:length(tImu),:);
% 
% % Upsample visual-data to match the sampling of the IMU
% t = tImu;
% dt = mean(diff(t));
% qtVis = interp1(tVis,qtVis,t,'linear','extrap'); % Consider using SLERP
% 
% % Compute visual angular velocities
% qtDiffs = diff(qtVis);
% qtDiffs = [qtDiffs; qtDiffs(end,:)]';
% angVis = -(2/dt)*qt_mul(qtDiffs, qt_inv(qtVis'));
% angVis = angVis(2:4,:)';
% 
% % Smooth angular velocities
% angVis(:,1) = smooth(angVis(:,1),15);
% angVis(:,2) = smooth(angVis(:,2),15);
% angVis(:,3) = smooth(angVis(:,3),15);
% angImu(:,1) = smooth(angImu(:,1),15);
% angImu(:,2) = smooth(angImu(:,2),15);
% angImu(:,3) = smooth(angImu(:,3),15);

iter = 1;
tds = -10:.01:10;
flist = []
for td =  -10:.01:10
    angVis1 = interp1(t-td,angVis,t,'linear',0);
    angImu1 = angImu;
    for i = 1:length(angVis1(:,1))
        if angVis1(i,1) == 0
            angImu1(i,:) = 0;
        end
    end
    N = size(angVis1,1);

    % Compute mean vectors
    meanImu = repmat(mean(angImu),N,1);
    meanVis = repmat(mean(angVis1),N,1);

    % Compute centralized point sets
    P = angImu - meanImu;
    Q = angVis - meanVis;

    % Singular value decomposition
    [U,S,V] = svd(P'*Q);

    % Ensure a right handed coordinate system and correct if necessary
    C = eye(3);
    if (det(V*U') < 0)
        C(3,3) = -1;
    end

    Rs = V*C*U'
    D = angVis1 - angImu1*Rs;
    f = sum(D(:).^2)/length(D(:,1));
    flist(iter) = f;
    iter = iter +1
end

plot(tds,flist)
    
