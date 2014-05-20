% Modify the five values below
lowerID = 362 % Enter the ID of the first file (362,40, or 553)
upperID = 379 % Enter the ID of the last file (379,43, or 570)
omegamin = 0 % Enter the value for the minimum of the range of omega (0 or -180)
omegamax = 180 % Enter the value for the maximum of the range of omega (180)
noRings = 11 % Enter the number of rings (11)
% No need to modify anything below

fileprefix = strcat('Data/',num2str(lowerID),'-',num2str(upperID),'/eta-phi-map-arr-');
filetype = '.csv';
saveimprefix = strcat('Images/',num2str(lowerID),'-',num2str(upperID),'/eta-phi-map-');
saveimtype = '.fig';
for i = 1:noRings
    filei = strcat(fileprefix, num2str(i),filetype);
    saveimi = strcat(saveimprefix,num2str(i),saveimtype);
    titlei = strcat('Eta-Phi Map Ring-',num2str(i));
    arri = csvread(filei);
    % arri = interp2(arri,3);
    f = figure();
    imagesc(omegamin:omegamax,[0 359],arri);
    grid()
    xlabel('\phi (\circ)');
    ylabel('\eta (\circ)');
    title(titlei);
    axis xy;
    saveas(f,saveimi);
    close all;
end