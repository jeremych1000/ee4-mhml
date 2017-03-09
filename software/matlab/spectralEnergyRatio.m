function ratio=bandEnergyRatio(hr_vec)
HR_FFT=fft(hr_vec);
LF_size=length(HR_FFT)/4;
lf_power=abs([HR_FFT(1:LF_size);HR_FFT(length(HR_FFT)-LF_size:end)]).^2;
hf_power=abs(HR_FFT(LF_size+1:length(HR_FFT)-LF_size-1)).^2;
ratio=sum(lf_power)/sum(hf_power);
end