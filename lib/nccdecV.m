function ncc=nccdecV(A,B)

% Requires 2 images

l=size(A);

if sum(size(A)==size(B))==length(l)
    posA=find(A~=0);
    posB=find(B~=0);
    meA=mean(A(posA));
    meB=mean(B(posB));    
%     stA=std(A(posA));
%     stB=std(B(posB));
%     D= (dot(A-meA, B-meB))/(stA*stB);
%     suma=sum(D(:));
    
    ncc=dot(((A(posA)-meA)/norm((A(posA)-meA))),((B(posB)-meB)/norm((B(posB))-meB)))*100;
    
    return
else
    warning('nccdec::Matrix are different size')
    ncc=0;
    return
end
