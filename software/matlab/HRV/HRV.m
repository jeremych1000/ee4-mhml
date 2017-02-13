% Function that computes short-term (ST) and long-term (LT) Heart Rate 
% Variability (HRV) parameters, using Time-Domain and Frequency-Domain methods

% Inputs: 
%
% rr_intervals - RR Interval vector
% t - time vector
% condition - ST vs. LT
% configSetting - configuration window settings
% 
% Outputs:
%
% HRV - Structure containing relevant HRV parameters

%function HRV = HRV(rr_intervals,t,condition,configSetting,psdMethod)
function HRV = HRV(rr_intervals,t)

% Store configuration window settings

%% Condition setting.
condition = 'ST';
configSetting.points_PSD = 1024;
psdMethod = 'Welch';
%psdMethod = 'LS';
%psdMethod = 'Burg';
%% 

if strcmp(condition,'ST')
    num_samples = configSetting.points_PSD;
else
    num_samples = configSetting.points_PSD_LT;
end

%% configSetting
configSetting.pnnx = 0.05;      % seconds
configSetting.sdann = 300;      % seconds
configSetting.sdnni = 300;      % seconds
configSetting.HRVTi = 100;      % seconds
configSetting.ULFlo = 0;        % Hz.
configSetting.ULFhigh = 0.003;  % Hz
configSetting.VLFlo = 0.003;    % Hz
configSetting.VLFhigh = 0.04;   % Hz
configSetting.LFlo = 0.04;      % Hz
configSetting.LFhigh = 0.15;    % Hz
configSetting.HFlo = 0.15;      % Hz
configSetting.HFhigh = 0.4;     % Hz
%%

x = configSetting.pnnx;
block_length1 = configSetting.sdann;
block_length2 = configSetting.sdnni;
numBins = configSetting.HRVTi;
ULFlo = configSetting.ULFlo;
ULFhigh = configSetting.ULFhigh;
VLFlo = configSetting.VLFlo;
VLFhigh = configSetting.VLFhigh;
LFlo = configSetting.LFlo;
LFhigh = configSetting.LFhigh;
HFlo = configSetting.HFlo;
HFhigh = configSetting.HFhigh;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%% Time - Domain HRV %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Compute and store short-term HRV measures

HRV.timeHRV.SDNN = sdnn(rr_intervals);
[HRV.timeHRV.SD1, HRV.timeHRV.SD2, HRV.timeHRV.SD1_SD2Ratio] = poincare(rr_intervals);
HRV.timeHRV.SDSD = sdsd(rr_intervals);
HRV.timeHRV.rMSSD = rmssd(rr_intervals);
HRV.timeHRV.pNNx = pnnx(rr_intervals,x);

% If operation in long-term mode, compute long-term HRV measures. Round to
% three decimal places.

if (strcmp(condition,'LT'))
 
   HRV.timeHRV.SDANN = round(sdann(rr_intervals,block_length1)*1000)/1000; 
   HRV.timeHRV.SDNNi = round(sdnni(rr_intervals,block_length2)*1000)/1000;
   HRV.timeHRV.HRVTi = round(triangularIndex(rr_intervals,numBins)*1000)/1000; 
   
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%% Frequency - Domain HRV %%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Obtain the PSD and frequency vector using the Lomb-Scargle periodogram /
% Welch periodogram / Autoregression (Burg's) methods.

switch psdMethod
    case 'LS'        
        [psd,f] = lomb_scargle(t,rr_intervals,num_samples,HFhigh);
    
    
    case 'Welch'
        fs = 4;
        window_size = 256;
        noverlap = window_size*0.5;
        %num_samples = num_samples*(fs/HFhigh)-1;
        nfft = window_size * 2 - 1;
        
%         if (num_samples < window_size)
%             nfft = window_size;
%             disp('Specified number of samples in PSD is too small');
%             disp('Number of samples = 256');
%         else
%             nfft = num_samples;
%         end
        
        t_new = t(1):1/fs:t(end);
        rr_intervals = detrend(rr_intervals,'linear');
        RRIntervals_new = interp1(t,rr_intervals,t_new,'spline'); 
            
        %zero padding    
        L = length(RRIntervals_new);        
        if(L < window_size)
          RRIntervals_new = [RRIntervals_new,zeros(1,window_size-L)];  
        end
        
        % PSD
        windowing = hamming(window_size)';        
        windowing(isnan(windowing)) = 1; %Fixing MATLAB bug    
        
        [psd,f] = pwelch(RRIntervals_new,windowing,noverlap,nfft,fs,'onesided');
        f = f(f <= HFhigh);
        psd = psd(1:length(f));        
    case 'Burg'
        fs = 4;
        ar_order = 16;
        num_samples=num_samples*(fs/HFhigh)-1;
        
        t_new = t(1):1/fs:t(end);
        rr_intervals = detrend(rr_intervals,'linear');
        RRIntervals_new = interp1(t,rr_intervals,t_new,'spline'); 
                
        windowing = hamming(length(RRIntervals_new))';        
        windowing(isnan(windowing)) = 1; %Fixing MATLAB bug       
        RRIntervals_new = windowing.*RRIntervals_new;
        
        L = length(RRIntervals_new);
        if num_samples < L
            num_samples = L;
        end
        
        [psd,f] = pburg(RRIntervals_new,ar_order,num_samples,fs);
        f = f(f <= HFhigh);
        psd = psd(1:length(f));   
    otherwise
       disp('invalid psd method.');
       return;
end

% psd = psd/max(psd); %normalise PSD

% if ~isempty(f(isnan(f)))
%      disp('f NaN');
% end
% 
% if ~isempty(psd(isnan(psd)))
%     disp('psd NaN');
% end

% Find indeces of relevant frequency bands

ULFi = find((f>=ULFlo) & (f<=ULFhigh));
VLFi = find((f>VLFlo) & (f<=VLFhigh));
LFi = find((f>LFlo) & (f<=LFhigh));
HFi = find((f>HFlo));

HRV.FreqIndex.ULFi = ULFi;
HRV.FreqIndex.VLFi = VLFi;
HRV.FreqIndex.LFi = LFi;
HRV.FreqIndex.HFi = HFi;

% Fixing MATLAB bug using mean values (replacing NaN with mean of relevant region)

tmp=psd(ULFi);
tmp(isnan(tmp))=mean(tmp(~isnan(tmp)));
psd(ULFi)=tmp;

tmp=psd(VLFi);
tmp(isnan(tmp))=mean(tmp(~isnan(tmp)));
psd(VLFi)=tmp;

tmp=psd(LFi);
tmp(isnan(tmp))=mean(tmp(~isnan(tmp)));
psd(LFi)=tmp;

tmp=psd(HFi);
tmp(isnan(tmp))=mean(tmp(~isnan(tmp)));
psd(HFi)=tmp;

% Compute areas using trapezoidal numerical integration

if (length(ULFi)==1 || isempty(ULFi))
    areaULF=0;
else
    areaULF = trapz(f(ULFi),psd(ULFi))*(10^6);
end

if (length(VLFi)==1 || isempty(VLFi))
    areaVLF=0;
else
    areaVLF = trapz(f(VLFi),psd(VLFi))*(10^6);
end

if (length(LFi)==1 || isempty(LFi))
    areaLF=0;
else
    areaLF = trapz(f(LFi),psd(LFi))*(10^6);
end

if (length(HFi)==1 || isempty(HFi))
    areaHF=0;
else
    areaHF = trapz(f(HFi),psd(HFi))*(10^6);
end


areaTP = areaULF + areaVLF + areaLF + areaHF;
areaNorm = areaLF + areaHF;

% Calculate powers as percentage of Total Power

ULF = (areaULF/areaTP)*100;
VLF = (areaVLF/areaTP)*100;
LF = (areaLF/areaTP)*100;
HF = (areaHF/areaTP)*100;

% Calculate normalised LF and HF Powers

LF_Norm = areaLF/areaNorm;
HF_Norm = areaHF/areaNorm;

LFHF_Ratio = areaLF/areaHF;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Populate frequency-domain HRV structure

HRV.freqHRV.freq_vector = f;
HRV.freqHRV.PSD = psd;
HRV.freqHRV.LFraw = areaLF;
HRV.freqHRV.HFraw = areaHF;
HRV.freqHRV.LFp = round(LF*1000)/1000;
HRV.freqHRV.HFp = round(HF*1000)/1000;
HRV.freqHRV.LFn = round(LF_Norm*1000)/1000;
HRV.freqHRV.HFn = round(HF_Norm*1000)/1000;
HRV.freqHRV.LFHF_Ratio = round(LFHF_Ratio*1000)/1000;
HRV.freqHRV.TP = round(areaTP*1000)/1000;

% If operating in long-term mode, store long-term HRV measures

if (strcmp(condition,'LT'))

HRV.freqHRV.ULFp = round(ULF*1000)/1000;
HRV.freqHRV.VLFp = round(VLF*1000)/1000;    

end

end %end main function

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% Time-Domain HRV Functions %%%%%%%%%%%%%%%%%%%%%%%%%%

% Function that computes the Standard Deviation of all NN-Intervals (SDNN),
% accurate to three decimal places.
%
% Inputs:
%
% rr_intervals - RR Interval vector
%
% Outputs:
%
% sdnn1 - SDNN

function sdnn1 = sdnn(rr_intervals)

sdnn1 = round(std(rr_intervals)*1000)/1000;

end

function sdsd1 = sdsd(rr_intervals)

RR_diff = abs(diff(rr_intervals));
r = sqrt(sum((RR_diff-mean(RR_diff)).^2)/length(RR_diff));
sdsd1 = round(r*1000)/1000;

end

function [sd1, sd2, sd1_sd2_ratio] = poincare(rr_intervals)

Cos45 = (1/(2^0.5));

tmp1 = rr_intervals(1:end-1) - rr_intervals(2:end);
tmp2 = rr_intervals(1:end-1) + rr_intervals(2:end);

sd1 = Cos45*std(tmp1);
sd2 = Cos45*std(tmp2);
sd1_sd2_ratio = sd1/sd2;

end

% Function that computes the Root Mean Square Successive Differences of all
% NN-Intervals (rMSSD), accurate to three decimal places.
%
% Inputs:
%
% rr_intervals - RR Interval vector
%
% Outputs:
%
% rmssd1 = rMSSD
%

function rmssd1 = rmssd(rr_intervals)

RR_diff = abs(diff(rr_intervals));
r = sqrt(sum(RR_diff.^2)/length(RR_diff));
rmssd1 = round(r*1000)/1000;

end

% Function that computes the Percentage of NN-Interval differences greater
% than x (ms) (pNNx), accurate to three decimal places.
%
% Inputs:
%
% rr_intervals - RR Interval vector
%
% Outputs:
%
% pnnx1 = pNNx


function pnnx1 = pnnx(rr_intervals,x)

RR_diff = abs(diff(rr_intervals));
num_diff_x = sum(RR_diff > x);
num_diff = numel(rr_intervals);
p = (num_diff_x/num_diff)*100;
pnnx1 = round(p*1000)/1000;

end

% Function that computes the Standard Deviation of the Mean of NN-Intervals
% for all 5 minute segments of the long-term ECG recording (SDANN),
% accurate to three decimal places.
%
% Inputs:
%
% rr_intervals - RR Interval vector
%
% Outputs:
%
% sdann1 = SDANN

function sdann1 = sdann(rr_intervals,block_length)

 i = 0;
 count1 = 1;
 temp = zeros(ceil(sum(rr_intervals)/block_length),1);
 
 for count2 = 1:length(rr_intervals)
        if (sum(rr_intervals(count1:count2)) >= block_length)
            i = i+1;
            temp(i) = mean(rr_intervals(count1:count2));
            count1 = count2;
        end
 end

 sdann1 = std(temp);

end

% Function that computes the Mean of the Standard Deviations of all NN-Intervals
% for all 5 minute segments of a long-term ECG recording (SDNNi), accurate to
% three decimal places.
%
% Inputs:
%
% rr_intervals - RR Interval vector
%
% Outputs:
%
% sdnni1 = SDNNi

function sdnni1 = sdnni(rr_intervals,block_length)

i = 0;
count1 = 1;
temp = zeros(ceil(sum(rr_intervals)/block_length),1);

for count2 = 1:length(rr_intervals)
        if sum(rr_intervals(count1:count2)) >= block_length
            i = i+1;
            temp(i) = std(rr_intervals(count1:count2));
            count1 = count2;
        end
end

sdnni1 = mean(temp);
    
end