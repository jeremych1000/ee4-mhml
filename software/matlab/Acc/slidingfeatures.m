function [Detrend Mean Max Min DIFF VEL VAR STD SKE KUR] = slidingfeatures(inputSVM)
    fsamp = 40;
    overlap = 29;
    window_size = 30;
    window = zeros(window_size);
    
    len = length(inputSVM); 
    
    idx = bsxfun(@plus, (1:window_size)', 1+(0:(fix((len-overlap)/(window_size-overlap))-1))*(window_size-overlap))-1;
   
    for k=1:size(idx,2)
        slidingWindow = inputSVM(idx(:,k));
        Mean(k+1) = mean(slidingWindow);
        Max(k+1) = max(slidingWindow);
        Min(k+1) = min(slidingWindow); 
        STD(k+1) = std(slidingWindow);
        VAR(k+1) = var(slidingWindow);
        SKE(k+1) = skewness(slidingWindow);
        KUR(k+1) = kurtosis(slidingWindow); 
        VEL(k+1) = trapz(slidingWindow - 256)*window_size/fsamp;
      
    end
    
    for i = window_size+1:length(inputSVM);
        Detrend(i) = inputSVM(i)- Mean(i-(window_size-1)); 
    end
    
    
    Detrend = abs(Detrend);
    
    
    Mean(1) = Mean(2);
    Max(1) = Max(2);
    Min(1) = Min(2);
    STD(1) = STD(2);
    VAR(1) = VAR(2);
    SKE(1) = SKE(2); 
    VEL(1) = VEL(2);
    KUR(1) = KUR(2); 
    
    if overlap == 0
        overlap = 1;
    end
    
    %xq = 1:(len/(1200-1)):len +1;
    xq = 1:(length(Mean)-1)/(length(inputSVM)-1):length(Mean);
    x = 1:size(idx,2)+1; 
    Mean = interp1(Mean, xq); 
    Max = interp1(Max, xq);
    Min = interp1(Min, xq);
    STD = interp1(STD, xq);
    VEL = interp1(VEL, xq);
    VAR = interp1(VAR, xq);
    SKE = interp1(SKE, xq);
    KUR = interp1(KUR, xq); 
    DIFF = Max - Min; 
    
end