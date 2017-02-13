%function for butterworth low pass filter 

function output = butterlowpass(input);
    order = 4;    %Order of filter
    cfreq = 19;   %Hz cannot be >20Hz. Sampling rate at 40Hz
    fsamp = 40;   %40Hz
    Wn = cfreq/fsamp * 2; 
    
    %current setting on firmeware Wn = 0.9pi, n = 2, Lowpass
    %La = [1, 1.56101807580072, 0.641351538057563];
    %Lb = [0.800592403464570, 1.60118480692914, 0.800592403464570];
    
    [Lb La] = butter(order, Wn, 'low');
    
    output = filter(Lb, La, input);
    
end 