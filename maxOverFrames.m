%%
filename = ['V:/Suter_Jul13/GE2/Ti7Test_00017.ge2'];
fp = fopen(filename,'r','n');
offset = 8192;
fseek(fp,offset,'bof');
bg = fread(fp,[2048 2048],'uint16');
fclose(fp);

%%
% loop through images
froot = 'V:/Suter_Jul13/GE2/Ti7_PreHRM_PreLoad__';
%filename = [froot '03048'];
fileno = '00040';
filename = [froot fileno];

fp = fopen(filename,'r','n');

for i = 1:180
    
    i
    offset = 8192 + (i-1)*2048*2048*2;
    fseek(fp,offset,'bof');
    imgcurrent = fread(fp,[2048 2048],'uint16') - bg;
    
    if i==1
        imgmax=imgcurrent;
    end
    imgmax=max(imgmax, imgcurrent);
    

end

fclose(fp);

fileno = '00041';
filename = [froot fileno];
fp = fopen(filename,'r','n');

for i = 1:180
    
    i
    offset = 8192 + (i-1)*2048*2048*2;
    fseek(fp,offset,'bof');
    imgcurrent = fread(fp,[2048 2048],'uint16') - bg;
    imgmax=max(imgmax, imgcurrent);
    

end

fclose(fp);

fileno = '00042';
filename = [froot fileno];
fp = fopen(filename,'r','n');

for i = 1:180
    
    i
    offset = 8192 + (i-1)*2048*2048*2;
    fseek(fp,offset,'bof');
    imgcurrent = fread(fp,[2048 2048],'uint16') - bg;
    imgmax=max(imgmax, imgcurrent);
    

end

fclose(fp);

fileno = '00043';
filename = [froot fileno];
fp = fopen(filename,'r','n');

for i = 1:180
    
    i
    offset = 8192 + (i-1)*2048*2048*2;
    fseek(fp,offset,'bof');
    imgcurrent = fread(fp,[2048 2048],'uint16') - bg;
    imgmax=max(imgmax, imgcurrent);  

end

imgmax = max(imgmax,0*imgmax);

% Plot the image
imagesc(min(imgmax,256+0*imgmax));
NwriteGE('ring1', imgmax)

%%

% offset = 0;
% fseek(fp,offset,'bof');
% hdr = fread(fp,8192,'uint16')
% 
% fclose(fp);

%%
% outname = '/home/beams/S1IDUSER/AJB/summed.ge2'
% fpO = fopen(outname,'w','n')
% % fwrite(fpO,hdr,'uint16')
% fwrite(fpO,imgmax,'uint16')
% fclose(fpO)





