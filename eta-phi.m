%%
clear all
close all
clc

%% eta-phi map
% Add proj/Sector1-MATLAB/imagereading to the path
PATH('/home/tempuser/proj/Sector1-MATLAB/imagereading',PATH);

filenum = 253; % files 

file_def.GE.imgpath = '/home/tempuser/Nov11/Data/UIUC_March11/';
file_def.GE.prefix  = 'BsLoc2';
file_def.param.path = '/home/tempuser/Nov11/Data/UIUC_Mar11/';
file_def.param.file = 'sweep2.par';
file_def.GE.background  = 'Bs1_00502';

% Load the fastscan image
img = load_img([2416:2555],file_def,'GE_NEW',[],[],1,1);

%% polar coordinate trafo
cenC = 1024;
cenR = 1024;

% The arrays radius and ee give "radius" and "eta", respectively
% based on the center pixel given above.  They can be checked with the plot
% commands.
cc = repmat([1:2048],2048,1);
rr = repmat([1:2048]',1,2048);
radius = sqrt((cc-cenC).^2 + (rr-cenR).^2);
ee = atan2(-cc+cenC, rr-cenR)*180/pi+180;

figure(2); imagesc(radius);colorbar
figure(3); imagesc(ee);colorbar

% Pick off the radius corresponding to the 2theta of interest, and create a
% mask ii

ii = radius > 920 & radius < 960; %331
% ii = radius > 550 & radius < 650; %220
% ii = radius > 405 & radius < 445; %200
% ii = radius > 345 & radius < 390; %111
imm = zeros(2048, 2048);
im_ = [];

% ee(ii) is a vector of eta values for pixels in the ring of interest
% After calling histc, "n" will contain a vector that gives the number of
% pixels which contribute to a particular (integral) value of 2theta (not
% so very interesting).  The variable "bin" is the more interesting one:
% it gives the value of eta for a particular pixel from the vector of
% pixels indexed by "ii"
etaInt = zeros(360, 140);
[n, bin] = histc(ee(ii),[0:1:360]);
n(end-1) = n(end-1) + n(end);
bin(bin == 361) = 360;
n = n(1:end-1);

% Loop for each phi (Argonne), or omega (Fable)
for i = 1:1:140
    imgcurrent = img.im(:,:,i);
    imc = imgcurrent(ii);
    
    % Loop through the pixels in 2theta window, summing contributions for a
    % particular value of "eta"
    for j = 1:length(imc)
        etaInt(bin(j),i) = imc(j) + etaInt(bin(j),i);
    end
end

figure(4)
imagesc([-69:70], [0 359], etaInt)
xlabel('\phi (deg)')
ylabel('\eta (deg)')
grid on
return
