%function to detrend a signal
%not being used

function Detrend = Detrend1(inputSVM)
    fsamp = 40;
    overlap = 31;
    window_size = 32;
    window = zeros(window_size);
    
    len = length(inputSVM); 
    
    idx = bsxfun(@plus, (1:window_size)', 1+(0:(fix((len-overlap)/(window_size-overlap))-1))*(window_size-overlap))-1;
 
    for k=1:size(idx,2)
        slidingWindow = inputSVM(idx(:,k));
        Mean(k+1) = mean(slidingWindow);
    end
    
    for i = window_size+1:length(inputSVM);
        Detrend(i) = inputSVM(i)- Mean(i-(window_size-1)); 
    end
    
    
    Detrend = abs(Detrend);
    
    
    Mean(1) = Mean(2);
   
    
    if overlap == 0
        overlap = 1;
    end
    
end