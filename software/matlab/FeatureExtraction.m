filelist =dir('./*.csv');
featureVec=[];
for file_i =1:length(filelist)
DataPath=[filelist(file_i).folder,'/',filelist(file_i).name];
[num,text,raw]=xlsread(DataPath,1);
[m n] = size(raw)
win_size = 600
n_win = round(m/win_size)
raw= raw(2:end,:);
label = raw{1,end};
for index = 1: n_win-1
    slice= raw((index-1)*win_size+1:index*win_size,:);
    feature_vec(index,1) = mean(cell2mat(slice(:,2)));
    feature_vec(index,2) = std(cell2mat(slice(:,2)));
    feature_vec(index,3) = mean(cell2mat(slice(:,3)));
    feature_vec(index,4) = std(cell2mat(slice(:,3)));
    feature_vec(index,5)= mean(cell2mat(slice(:,5)));
    feature_vec(index,6) =std(cell2mat(slice(:,5)));
    feature_vec(index,7)= mean(cell2mat(slice(:,6)));
    feature_vec(index,8)= std(cell2mat(slice(:,6)));
    feature_vec(index,9)= abs(mean(cell2mat(slice(:,7))))^2 +abs(mean(cell2mat(slice(:,8))))^2+abs(mean(cell2mat(slice(:,9))))^2;
    feature_vec(index,10) = label;
end
    featureVec = [featureVec;feature_vec];
%feature_vec=[mean_hr,std_hr,mean_rr,std_rr,mean_gsr,std_gsr,mean_temp,std_temp,mean_acc]
end