fis = readfis("busscheduler.fis");

while 1
    [pplcount, dispatch_interval] = comp_disp_int(fis);
    disp([pplcount, dispatch_interval]);

    % Open a text file for writing
    fileID = fopen('D:\Projects\crowddetection\dispatch_interval.txt','w+');
    
    % Write the dispatch interval to the file
    fprintf(fileID,'%f',dispatch_interval);
    
    % Close the file
    fclose(fileID);
    pause(1);
end

