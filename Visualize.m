rotg = gravity
accImu1 = accImu + bias'


tiledlayout(3,1)
nexttile
plot(t,accImu1(:,1),t-td,accVis(:,1)*scale)
title('xvars')
nexttile
plot(t,accImu1(:,2),t-td,accVis(:,2)*scale)
title('yvars')
nexttile
plot(t,accImu(:,3),t-td,accVis(:,3)*scale)
title('zvars')

% angImup = angImu*Rs;
% 
% 
% tiledlayout(3,1)
% nexttile
% plot(t,angImup(:,1),t-td,angVis(:,1))
% title('xvars rot')
% nexttile
% plot(t,angImup(:,2),t-td,angVis(:,2))
% title('yvars rot')
% nexttile
% plot(t,angImup(:,3),t-td,angVis(:,3))
% title('zvars rot')

% tiledlayout(4,1)
% nexttile
% itlist = 1:30
% plot(itlist,plist)
% title('c')
% nexttile
% plot(itlist,flist)
% title('f')
% nexttile
% plot(itlist,dlist)
% title('d')
% nexttile
% plot(plist,flist)
