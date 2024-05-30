fis = readfis("busscheduler_3.fis");

while 1
    [pplcount, dispatch_interval] = comp_disp_int(fis);
    disp([pplcount, dispatch_interval]);

    % Open a text file for writing
    f = fopen('D:\Projects\crowddetection\dispatch_interval.txt','w+');
    f_sig = fopen('D:\Projects\crowddetection\done_di.txt','w+');
    % Write the dispatch interval to the file
    fprintf(f,'%f',dispatch_interval);
    fprintf(f_sig, '%f', "Done");

    % Close the file
    fclose(f);
    fclose(f_sig);
end

function [pc, di] = comp_disp_int(fis)
    if exist('D:\Projects\crowddetection\count.txt', 'file')
        pc = str2double(fileread('D:\Projects\crowddetection\count.txt'));
        di = evalfis(fis, pc);
        delete('D:\Projects\crowddetection\done_count.txt');
    else
        error("File not found")
    end
end
