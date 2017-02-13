function [MeanRR, MeanHR, MaxRR, MinRR, SDNN, RMSSD, pNN50, HRVResult1] = slidingHRV1(ECG)
    window_s = 120; %10 secs
    fsamp = 250;
    overlap = 30000-25;

    MeanRR(1) = 0; 
    MeanHR (1) = 0; 
    MaxRR (1) = 0; 
    MinRR (1) = 0; 
    SDNN (1) = 0; 
    RMSSD(1) = 0; 
    pNN50 (1) = 0; 
    HRVResult1{1} = 0; 

    window_size = fsamp * window_s; 
   % window = zeros(window_size);
    
    len = length(ECG); 
    
    idx = bsxfun(@plus, (1:window_size)', 1+(0:(fix((len-overlap)/(window_size-overlap))-1))*(window_size-overlap))-1;

     for k=3:size(idx,2)
            slidingWindowRR = ECG(idx(:,k));
            [pks, locs] = findpeaks(slidingWindowRR);
            difflocs = diff(locs);
            diffRR = difflocs./fsamp;
            numRpeak = length(locs);
            rrs = slidingWindowRR(slidingWindowRR ~= 0);

           if isempty(rrs) == 0;
          
               rrs(1) = [];

               rrs = rrs/250;
               t = zeros(size(rrs));
               for i=2:length(t)
                    t(i) = rrs(i) + t(i-1); 

               end
               HRVResult = HRV(rrs, t);
               HRVResult1{k+1} = HRVResult;
               MeanHR(k+1) = numRpeak*(60/window_s);
               MeanRR(k+1) = mean(diffRR);
               MaxRR(k+1) = max(diffRR); 
               MinRR(k+1) = min(diffRR);  
               SDNN(k+1) = HRVResult.timeHRV.SDNN;
               RMSSD(k+1) = HRVResult.timeHRV.rMSSD;
               pNN50(k+1) = HRVResult.timeHRV.pNNx;
            else
            MeanHR(k+1) = 0
            MeanRR(k+1) = 0
            MaxRR(k+1) = 0
            MinRR(k+1) = 0 
            SDNN(k+1) = 0
            RMSSD(k+1) = 0
            pNN50(k+1) = 0
            end


     end
end
