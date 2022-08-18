%Port number of server is 4000
%IP adress of the server on the matlab is 127.0.0.1.Still I get it with resolvehost func at the beginning.
%In tcpserer func one directly write "localhost" instead of server_IP however I prefer to hold adress value in a seperate variable server_IP
[name,server_IP] = resolvehost("localhost");
server_PORT=4000;
%Timeout is 2 seconds. After two seconds it terminates read function. 2 sec is enough for to catch incoming string
main_server = tcpserver(server_IP,4000, "Timeout",2); 

%Table initialization with 10 values corresponding to 10 index values from 0 to 10
main_table = [2 24 5 12 26 90 115 1080 4 7];
disp(strcat("Initial main table is [", num2str(main_table), "]."));
%This is for surpass warnings. Otherwise it will try to read and it goes timeout when there is no data on socket to read, so it will give warning messages repeatedly in that case.
warning('off');
%Establishing connection between proxy and the main server
%Proxy sends the string "Proxy is connected to server." if connection is successful.
isConnected = 0;
while ~isConnected
        %count value is necessary.I put a high value, so since the count value won't be reached, timeout mechanism will be effective and the incoming message will be recieved without loss. If I set it low, matlab reads incoming message partially.  
        message = read(main_server, 9999, "string"); 
        if strcmp(message,"Proxy is connected to the main server.")
            disp(message);
            isConnected = 1;
        end
end

%Sending the first half of the table(index0 to index4 values are sent) to initialize the partial table in proxy.
write(main_server, num2str(main_table(1:5)));

%At this point proxy server table initialization is done.%

%Infinite loop to handle proxy requests%
while 1
    try 
        %Incoming message from proxy is read and it becomes a list% 
        request_from_proxy = read(main_server, 9999, "string");
        request_from_proxy_list = split(request_from_proxy , ["=",";"]);
        p_to_m= "Proxy to MATLAB: ";
        disp(strcat(p_to_m, request_from_proxy));
        m_to_p="MATLAB to Proxy: ";

        %GET instruction comes from proxy%
        if strcmp("GET", request_from_proxy_list(2))
            indices_list= split(request_from_proxy_list(4) , [","]);
            response_to_proxy = "OP=GET;IND=";
            
            %If five value is asked 
            if length(indices_list)==5
                index1_int=str2num(indices_list(1))+1 ;
                index2_int=str2num(indices_list(2))+1 ;
                index3_int=str2num(indices_list(3))+1 ;
                index4_int=str2num(indices_list(4))+1 ;
                index5_int=str2num(indices_list(5))+1 ;
                
                data1=num2str(main_table(index1_int));
                data2=num2str(main_table(index2_int));
                data3=num2str(main_table(index3_int));
                data4=num2str(main_table(index4_int));
                data5=num2str(main_table(index5_int));


                %Merging strings and forming final response message
                response_to_proxy = strcat(response_to_proxy,indices_list(1),",",indices_list(2),",",indices_list(3),",",indices_list(4),",",indices_list(5),";", "DATA=", data1,",",data2,",",data3,",",data4,",",data5,";");
                write(main_server, response_to_proxy);

            %If 4 values are asked  
            elseif length(indices_list)==4
                index1_int=str2num(indices_list(1))+1 ;
                index2_int=str2num(indices_list(2))+1;
                index3_int=str2num(indices_list(3))+1;
                index4_int=str2num(indices_list(4))+1;
                
                data1=num2str(main_table(index1_int));
                data2=num2str(main_table(index2_int));
                data3=num2str(main_table(index3_int));
                data4=num2str(main_table(index4_int));


                %Merging strings and forming final response message
                response_to_proxy = strcat(response_to_proxy,indices_list(1),",",indices_list(2),",",indices_list(3),",",indices_list(4),";", "DATA=", data1,",",data2,",",data3,",",data4,";");
                write(main_server, response_to_proxy);

            %If three values are asked    
            elseif length(indices_list)==3
                index1_int=str2num(indices_list(1))+1 ;
                index2_int=str2num(indices_list(2))+1;
                index3_int=str2num(indices_list(3))+1;
                
                data1=num2str(main_table(index1_int));
                data2=num2str(main_table(index2_int));
                data3=num2str(main_table(index3_int));


                %Merging strings and forming final response message
                response_to_proxy = strcat(response_to_proxy,indices_list(1),",",indices_list(2),",",indices_list(3),";", "DATA=", data1,",",data2,",",data3,";");
                write(main_server, response_to_proxy);
            
            
            
            %Two values are asked.
            elseif length(indices_list)==2
                index1_int=str2num(indices_list(1))+1; %In matlab indexing starts from 1.
                index2_int=str2num(indices_list(2))+1;
                
                data1=num2str(main_table(index1_int));
                data2=num2str(main_table(index2_int));
                %Merging strings and forming final response message
                response_to_proxy = strcat(response_to_proxy,indices_list(1),",",indices_list(2),";", "DATA=", data1,",",data2,";");
                write(main_server, response_to_proxy);
  
            %Only one value is asked.
            elseif length(indices_list)==1
                index1_int=str2num(indices_list(1))+1;
                data1=num2str(main_table(index1_int));
                response_to_proxy=strcat(response_to_proxy, indices_list(1), ";","DATA=", data1,";");
                write(main_server, response_to_proxy);
            end

        
        %PUT instruction comes from proxy%
        elseif strcmp("PUT", request_from_proxy_list(2));
            indices_list= split(request_from_proxy_list(4) , [","]);
            data_list= split(request_from_proxy_list(6) , [","]);
            response_to_proxy = "OP=PUT;IND=";
            
            index1_int=str2num(indices_list(1))+1 ;
            index2_int=str2num(indices_list(2))+1;

            data1_int=str2num(data_list(1));
            data2_int=str2num(data_list(2));

                
            %Updating main table%
            main_table(index1_int) =  data1_int;
            main_table(index2_int) = data2_int;
            %Forming response to proxy by using main table%
            data1=num2str(main_table(index1_int));
            data2=num2str(main_table(index2_int));
            response_to_proxy = strcat(response_to_proxy,indices_list(1),",",indices_list(2),";", "DATA=", data1,",",data2,";");
            write(main_server, response_to_proxy);
            disp(strcat("Updated main table is [", num2str(main_table), "]."));
            
        
        elseif strcmp("CLR", request_from_proxy_list(2))
            %Clear main table
            main_table = [0 0 0 0 0 0 0 0 0 0];
            %Responsing proxy to indicated we cleared the main table%
            response_to_proxy = "OP=CLR;IND=None;DATA=None;";
            write(main_server, response_to_proxy);
            disp(strcat("Updated main table is [", num2str(main_table), "]."));
         %Since summation operation is conducted in proxy server for ADD,
         %an ADD instruction never comes matlab server. If user choose ADD,
         %a GET instruction from porxy may come here since there may be
         %missing entries for ADD operation in proxy table.
        end
        disp(strcat(m_to_p,response_to_proxy));

    catch
        continue
    end

end








