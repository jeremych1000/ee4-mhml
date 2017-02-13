% Function that computes the Power Spectral Density of an unevenly sampled
% signal, using the Lomb-Scargle Periodogram method.
%
% Inputs:
%
% t - time vector
% rr_intervals - RR Interval vector
% num_samples - number of samples in the PSD
% HFhigh - upper limit of the frequency range of the PSD 
%
% Outputs:
%
% psd - Power Spectral Density (PSD)
% f - frequency vector

function [psd,f] = lomb_scargle(t,rr_intervals,num_samples,HFhigh)

num_samples = num_samples - 1;
y = detrend(rr_intervals,'linear'); % Detrend and normalise signal
f = 0:HFhigh/num_samples:HFhigh;  %define range of frequencies that we are interested in
psd = zeros(1,numel(f)); %initialise periodogram

% Main loop to obtain to the PSD

for n = 1:numel(f)
    
    w = 2*pi*f(n); 
    
    if w>0   
        Sin=sin(2*w*t);
        Cos=cos(2*w*t);
        SumSin = sum(Sin);
        SumCos = sum(Cos);
        tau = atan2(SumSin,SumCos)/2/w;
        wttau = w*(t-tau);
        psd(n) = ((sum(y.*cos(wttau)).^2)/sum(cos(wttau).^2) + ...
                 (sum(y.*sin(wttau)).^2)/sum(sin(wttau).^2))/(2*var(rr_intervals));    
    else         
        psd(n) = (sum(y.*t)^2)/sum(t.^2);   
    end
    
end
