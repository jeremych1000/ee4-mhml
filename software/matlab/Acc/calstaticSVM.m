%function to calculate the static components of SVM

function staticSVM = calstaticSVM(x ,y ,z)

    order = 2;    %Order of filter
    cfreq = 15;   %Hz cannot be >20Hz. Sampling rate at 40Hz
    fsamp = 40;   %40Hz
    Wn = cfreq/fsamp * 2; 
    
    %current setting on firmeware Wn = 0.9pi, n = 2, Lowpass
    %La = [1, 1.56101807580072, 0.641351538057563];
    %Lb = [0.800592403464570, 1.60118480692914, 0.800592403464570];
    
    [Lb La] = butter(order, Wn, 'low');
    
    Lx = filter(Lb, La, x);
    Ly = filter(Lb, La, y);
    Lz = filter(Lb, La, z);
    
    %staticSVM = abs(Lx)+abs(Ly)+abs(Lz);
    staticSVM = sqrt((Lx.*Lx) + (Ly.*Ly) + (Lz.*Lz));

end

    