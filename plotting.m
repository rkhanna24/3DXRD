fileprefix = 'Data/eta-phi-map-arr-';
filetype = '.csv';
saveimprefix = 'Images/eta-phi-map-';
saveimtype = '.fig';
for i = 1:11
    filei = strcat(fileprefix, num2str(i),filetype);
    saveimi = strcat(saveimprefix,num2str(i),saveimtype);
    titlei = strcat('Eta-Phi Map Ring-',num2str(i));
    arri = csvread(filei);
    % arri = interp2(arri,3);
    f = figure();
    imagesc(0:180,[0 359],arri);
    grid()
    xlabel('\phi (\circ)');
    ylabel('\eta (\circ)');
    title(titlei);
    axis xy;
    saveas(f,saveimi);
    close all;
end