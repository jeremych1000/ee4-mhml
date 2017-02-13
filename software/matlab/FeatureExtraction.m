DataPath='../../data/TH_sleep_data/MSBand2_ALL_data_10.02.17.csv';
[num,text,raw]=xlsread(DataPath,1);
[m n] = size(raw)
win_size = 600
n_win = round(m/win_size)
raw= raw(2:end,:);
for index = 1: n_win-1
    slice= raw((index-1)*win_size+1:index*win_size,:);
    mean_hr(index) = mean(cell2mat(slice(:,2)));
    std_hr(index) = std(cell2mat(slice(:,2)));
    mean_rr(index) = mean(cell2mat(slice(:,3)));
    std_rr(index) = std(cell2mat(slice(:,3)));
    mean_gsr(index)= mean(cell2mat(slice(:,5)));
    std_gsr(index) =std(cell2mat(slice(:,5)));
    mean_temp(index)= mean(cell2mat(slice(:,6)));
    std_temp(index)= std(cell2mat(slice(:,6)));
    mean_acc(index)= abs(mean(cell2mat(slice(:,7))))^2 +abs(mean(cell2mat(slice(:,8))))^2+abs(mean(cell2mat(slice(:,9))))^2;
end
feature_vec=[mean_hr,std_hr,mean_rr,std_rr,mean_gsr,std_gsr,mean_temp,std_temp,mean_acc]