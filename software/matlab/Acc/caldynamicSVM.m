function dynamicSVM = caldynamicSVM(x ,y ,z)

    order = 6;    %Order of filter
    cfreq = 0.25;   %Hz cannot be >20Hz. Sampling rate at 40Hz
    fsamp = 40;   %40Hz
    Wn = (cfreq/fsamp) * 2; 
    
    %current setting on firmeware Wn = 0.9pi, n = 2, highpass
    %Ha = [1.0000000000000000,-5.8482746375593901,14.2528406664852128,-18.5280691624172142,13.5499271756970803,-5.2856359973981224,0.8592119585945107];
    %Hb = [0.9269368687211177,-5.5616212123267061,13.9040530308167654,-18.5387373744223538,13.9040530308167654,-5.5616212123267061,0.9269368687211177];
    
    [Hb Ha] = butter(order, Wn, 'high');
    
    Hx = filter(Hb, Ha, x);
    Hy = filter(Hb, Ha, y);
    Hz = filter(Hb, Ha, z);
    
    %dynamicSVM = abs(Hx)+abs(Hy)+abs(Hz);
    dynamicSVM = sqrt((Hx.*Hx)+(Hy.*Hy)+(Hz.*Hz));

end
