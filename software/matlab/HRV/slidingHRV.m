%function used to calualte meanHR and meanRR in a window
%pass argument as RR interval file generated in OSEA
%50ms = 
% input ECGRR straight from OSEA.  0 0 0 0 peak  0 0 0 0 

function [MeanRR, MeanHR, MaxRR, MinRR, SDNN, RMSSD, pNN50] = slidingHRV(ECG)
    window_s = 10; %10 secs
    fsamp = 250;
    overlap = 0;

    window_size = fsamp * window_s; 
    window = zeros(window_size);
    
    len = length(ECG); 
    
    idx = bsxfun(@plus, (1:window_size)', 1+(0:(fix((len-overlap)/(window_size-overlap))-1))*(window_size-overlap))-1;

     for k=1:size(idx,2)
        slidingWindow = ECG(idx(:,k));
        [pks, locs] = findpeaks(slidingWindow);
        difflocs = diff(locs);
        diffRR = difflocs./fsamp;
       
        numRpeak = length(locs);

        if numRpeak == 0;
                MeanHR(k+1) = 0
                MeanRR(k+1) = 0
                MaxRR(k+1) = 0
                MinRR(k+1) = 0 
                SDNN(k+1) = 0
                RMSSD(k+1) = 0
                pNN50(k+1) = 0
        else 
        
        MeanHR(k+1) = numRpeak*(60/window_s);
        MeanRR(k+1) = mean(diffRR);
        MaxRR(k+1) = max(diffRR); 
        MinRR(k+1) = min(diffRR);  

%noramlly used in long term, 5 mins or 24 hours, standard recordings,
%inappropiate to compare SDNN of different recording lengths
        SDNN(k+1) = std(diffRR); 
        
        %below features are apparently better at 30second windwos
        RMSSD(k+1) = sqrt(mean(difflocs.*difflocs));
        pNN50(k+1) = length(find(diffRR>0.005))/(length(pks));
        end
    end

end
