function [frames]=getFramesfromFolderG2(filefolder,etiqueta,extension)

direco=dir(filefolder);
kv={direco.name};
pattern=[etiqueta];
TF = contains(kv,pattern) & endsWith(kv,extension);
cind=find(TF==1);
framesd=kv(cind);

A=[(regexp(framesd,'\d*','Match'))];
NumbSL=cat(1,A{1,:});
if size(NumbSL,2)<2
    [B,I]=sort(str2double(NumbSL));
else
    for k=1:size(NumbSL,2)
        cc(k)=length(unique(NumbSL(:,k)));
    end
    [vmax,pmax]=max(cc);
    [B,I]=sort(str2double(NumbSL(:,pmax(1))));
end
frames={framesd{I}};
