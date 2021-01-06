function [Rs,td,bg,angVis,angImu,rslist] = estimateAlignment2(qtVis,tVis,angImu,tImu)
% Estimate temporal and spatial alignment between the camera and IMU.
% Gyroscope bias is also estimated in the process.
%
% INPUT:    qtVis   : Visual orientations (Nx4 matrix)
%           tVis    : Visual timestamps in seconds (Nx1 vector)
%           angImu  : Inertial angular velocities [rad/s] (Mx3 matrix)
%           tImu    : Inertial timestamps in seconds (Mx1 vector)
%
% OUTPUT:   Rs      : Rotation between the camera and IMU (3x3 matrix)
%           td      : Time offset between the camera and IMU (scalar)
%           bg      : Gyroscope bias [rad/s] (1x3 vector)
%

fprintf('%s', repmat('-', 1, 60));
fprintf('\nTemporal and spatial alignment\n');
tic;

% Use only time period which all sensors have values
timeStop = min([tVis(end) tImu(end)]);
tVis = tVis(tVis <= timeStop);
tImu = tImu(tImu <= timeStop);

qtVis = qtVis(1:length(tVis),:);
angImu = angImu(1:length(tImu),:);

% Upsample visual-data to match the sampling of the IMU
t = tImu;
dt = mean(diff(t));
qtVis = interp1(tVis,qtVis,t,'linear','extrap'); % Consider using SLERP

% Compute visual angular velocities
qtDiffs = diff(qtVis);
qtDiffs = [qtDiffs; qtDiffs(end,:)]';
angVis = -(2/dt)*qt_mul(qtDiffs, qt_inv(qtVis'));
angVis = angVis(2:4,:)';

% Smooth angular velocities
angVis(:,1) = smooth(angVis(:,1),15);
angVis(:,2) = smooth(angVis(:,2),15);
angVis(:,3) = smooth(angVis(:,3),15);
angImu(:,1) = smooth(angImu(:,1),15);
angImu(:,2) = smooth(angImu(:,2),15);
angImu(:,3) = smooth(angImu(:,3),15);

iter = 1;
tds = -3:.01:3;
flist = [];
blist = {};
Rslist = {};
tic
for td =  -3:.01:3
    %interpolate intermediate values, extrapolated values are set to zero
    angVis1 = interp1(t-td,angVis,t,'linear',0);
    angImu1 = angImu;
    %remove extrapolated vis values and corresponding imu values
    for i = 1:length(angVis1(:,1))
        try
            if angVis1(i,1) == 0
                angImu1(i,:) = [];
                angVis1(i,:) = [];
            end
        catch
            continue
        end
    end
    % Compute mean vectors
    N = size(angVis1,1);

    % Compute mean vectors
    meanImu = repmat(mean(angImu1),N,1);
    meanVis = repmat(mean(angVis1),N,1);
    
    % Compute centralized point sets
    P = angImu1 - meanImu;
    Q = angVis1 - meanVis;

    % Singular value decomposition
    [U,S,V] = svd(P'*Q);

    % Ensure a right handed coordinate system and correct if necessary
    C = eye(3);
    if (det(V*U') < 0)
        C(3,3) = -1;
    end
    
    Rs = V*C*U';
    
    bias = mean(angVis1) - mean(angImu1)*Rs;
    D = angVis1 - angImu1*Rs;
        
    f = sum(D(:).^2)/length(D(:,1));
    flist(iter) = f;
    blist{iter} = bias;
    rslist{iter} = Rs;
    iter = iter +1;
end
toc
plot(tds,flist)
title('loss function')
[mincost,minindex] = min(flist)
td = tds(minindex);
bg = blist{minindex};
Rs = rslist{minindex};
end


