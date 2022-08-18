import socket
import re

##Proxy server initalization##
proxy_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)

proxy_PORT = 5050 #Port num of proxy server
proxy_IP= socket.gethostbyname(socket.gethostname()) #IP of proxy server
proxy_ADDR= (proxy_IP, proxy_PORT) # Address tuple of the proxy server

proxy_server.bind(proxy_ADDR) #Binding, making this IP and port number the address of proxt server


#Connecting Matlab Server and Obtaining Initial Partial Table#
matlab_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
matlab_PORT = 4000
matlab_IP= "127.0.0.1" #IP value of the matlab.
matlab_ADDR= (matlab_IP, matlab_PORT)

print("Waiting for connection to matlab main server...")
#Proxy connects to the main server#
isConnected = False
while not isConnected:
    try:
        matlab_server.connect(matlab_ADDR)
        isConnected=True
    except:
        continue

#Greeting message
matlab_server.sendall(bytes("Proxy is connected to the main server.", "utf-8"))  # Greeting message. Strings are utf-8 bytes.
print("Connection is established between proxy and matlab main servers.")
#Obtaining first half of the table for initialization#
initial_table = matlab_server.recv(matlab_PORT)
partial_table=initial_table.decode("utf-8")
partial_table_temp =re.split("\s", partial_table)
#The message matlab sends contains some empty strings between actual elements, so I need to remove them.
partial_table = []
for data in partial_table_temp:
    if data !='':
        partial_table.append(data)
# Data are integers. However index values doesn't need to be integer, it doesn't makes any difference. Since the incoming message is string, converting stage is dropped for index values in this way.
proxy_partial_table= {"0":int(partial_table[0]), "1":int(partial_table[1]), "2": int(partial_table[2]), "3": int(partial_table[3]), "4":int(partial_table[4])}
print("Initial partial table:")
for key, value in proxy_partial_table.items():
    print(key, " : ", value)
##End of proxy server initialization##


proxy_server.listen(1)
#Accepting connection from client
client, client_address = proxy_server.accept()  ##client is client socket object. client_address is ip and port number of the client and it is tupple.
print( f"Connection from the client {client_address} has been establisted!\n")  # Client address is the address of client that is connected.
client.sendall(bytes("You connected to the proxy server.\n", "utf-8"))  # Greeting message. Strings are utf-8 bytes.
client_IP = client_address[0]
client_port = client_address[1]

#Instruction functions to call after deciding what incoming instruction is#
#PUT and CLR doesn't send response to client in instruction format, just notifying client by saying it is done.#
def GET(index1, index2=-1, index3=-1,index4=-1, index5=-1):
    extra_indices = []  # Holds the optional additional indices ie indices that are additional to the first two necessary indices.
    for optional in [index2, index3, index4, index5]:
        if optional != -1:  # Means user wants more than one index to get
            extra_indices.append(optional)

    all_indices = [index1] + extra_indices
    not_present = []  # This will hold the indices that are not present in proxy server table.
    for index in all_indices:
        if not (index in proxy_partial_table.keys()):
            not_present.append(index)

    request_to_matlab = "OP=GET;IND="
    if not not_present:  # Means not_present is empty and all entries are already here in proxy partial table, no need to ask for them to matlab server
        request_to_matlab = "DO NOT ASK MATLAB SERVER"
    else:
        for index in not_present:
            if index == not_present[-1]:  # If it is last we should place ";" according to the format
                request_to_matlab = request_to_matlab + f"{index}" + ";"
            else:
                request_to_matlab = request_to_matlab + f"{index}" + ","
        request_to_matlab = request_to_matlab + "DATA=None;"

    # We need to communicate with matlab server if there is at least one index entry that is not written in proxy table
    if request_to_matlab != "DO NOT ASK MATLAB SERVER":
        matlab_server.sendall(bytes(request_to_matlab, "utf-8"))
        print("Proxy to MATLAB: " + request_to_matlab)
        response_from_matlab = matlab_server.recv(matlab_PORT)
        response = response_from_matlab.decode("utf-8")
        print("MATLAB to Proxy: " + response)
        response_list = re.split(";|=", response)
        # Holding indices and data values
        indices_list = re.split(',', response_list[3])
        data_list = re.split(',', response_list[5])
        # Indices list and data list include only the indices and values are not in proxy table
        #this is for making empty space to add newcomers
        proxy_partial_table_indices_list = []
        for index in proxy_partial_table.keys():
            if not (index in all_indices):  # Not to delete any entry that we need for add.
                proxy_partial_table_indices_list.append(index)
        # proxy_partial_table_indices_list has indices that can be overwritten ie they are not needed for the current ADD instruction.
        num_of_newcomers = len(indices_list)
        # We need to delete entries to add one newcomers
        for x in range(0, num_of_newcomers):  # Iterates number of newcomers times
            proxy_partial_table.pop(proxy_partial_table_indices_list[x])

        # Adding new entries
        for x in range(0, num_of_newcomers):
            proxy_partial_table[indices_list[x]] = int(data_list[x])


        str_message_to_client = "OP=GET;IND="
        for index in all_indices:
            if index != all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{index}" + ","
            elif index == all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{index}" + ";"
        str_message_to_client = str_message_to_client + "DATA="

        for index in all_indices:
            if index != all_indices[-1]:
                str_message_to_client  = str_message_to_client + f"{proxy_partial_table[index]}" + ","
            elif index == all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{proxy_partial_table[index]}" + ";"

        print("Updated partial table:")
        for key, value in proxy_partial_table.items():
            print(key, " : ", value)

    elif request_to_matlab == "DO NOT ASK MATLAB SERVER":
        str_message_to_client = "OP=GET;IND="
        for index in all_indices:
            if index != all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{index}" + ","
            elif index == all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{index}" + ";"
        str_message_to_client = str_message_to_client + "DATA="

        for index in all_indices:
            if index != all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{proxy_partial_table[index]}" + ","
            elif index == all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{proxy_partial_table[index]}" + ";"
        print("Partial table is not updated.")

    return str_message_to_client



def PUT(index1, index2, data1, data2):

    is_index1_here = True
    is_index2_here = True

    if not (index1 in proxy_partial_table.keys()):
        is_index1_here = False

    if not (index2 in proxy_partial_table.keys()):
        is_index2_here = False
    # Decision is done at this point#
    #This message is common for all cases since the updates need to be matlab server as well.
    request_to_matlab = f"OP=PUT;IND={index1},{index2};DATA={data1},{data2};"
    matlab_server.sendall(bytes(request_to_matlab, "utf-8"))
    print("Proxy to MATLAB: " + request_to_matlab)
    response_from_matlab = matlab_server.recv(matlab_PORT)
    response = response_from_matlab.decode("utf-8")
    print("MATLAB to Proxy: " + response)
    response_list = re.split(";|=", response)
    # Holding indice and data values from the message coming from matlab, These are updated values (PUT executed in matlab)
    indice_list = re.split(',', response_list[3])
    data_list = re.split(',', response_list[5])
    #After this point new entries are overwritten if the indices are not here or if they are here only data values will be updated.
    #If they are not here, they are updated in matlab server and new values sent to the proxy from matlab server.
    if (not is_index1_here) and (not is_index2_here):
        proxy_partial_table_indices_list = []  # holds the present indices before update
        # To obtain keys, I used these to delete two index and its data from the partial table to make empty space for incoming new two indices and their values.
        for index in proxy_partial_table.keys():
            proxy_partial_table_indices_list.append(index)
        #Delete two oldest elements to overwrite.
        proxy_partial_table.pop(proxy_partial_table_indices_list[0])
        proxy_partial_table.pop(proxy_partial_table_indices_list[1])

        proxy_partial_table[indice_list[0]] =  int(data_list[0])
        proxy_partial_table[indice_list[1]] =  int(data_list[1])

        print("Updated partial table:")
        for key, value in proxy_partial_table.items():
            print(key, " : ", value)

    # Only index1 is not present, index2 is here
    elif (not is_index1_here):
        proxy_partial_table_indices_list = []
        for index in proxy_partial_table.keys():
            if index != index2:  # This is for not to overwrite presented and asked one by accident
                proxy_partial_table_indices_list.append(index)

        proxy_partial_table.pop(proxy_partial_table_indices_list[0])
        #Adding index1 and updating index2
        proxy_partial_table[index1] = int(data_list[0])
        proxy_partial_table[index2] = int(data_list[1])

        print("Updated partial table:")
        for key, value in proxy_partial_table.items():
            print(key, " : ", value)

    elif (not is_index2_here):
        proxy_partial_table_indices_list = []
        for index in proxy_partial_table.keys():
            if index != index1:  # This is for not to overwrite presented and asked one by accident
                proxy_partial_table_indices_list.append(index)

        proxy_partial_table.pop(proxy_partial_table_indices_list[0])

        #Adding index2 and updating index1
        proxy_partial_table[index1] = int(data_list[0])
        proxy_partial_table[index2] = int(data_list[1])

        print("Updated partial table:")
        for key, value in proxy_partial_table.items():
            print(key, " : ", value)

    elif is_index1_here and is_index2_here:
        #Updating existing indices values without deleting an entry
        proxy_partial_table[indice_list[0]] = int(data_list[0])
        proxy_partial_table[indice_list[1]] = int(data_list[1])

        print("Updated partial table:")
        for key, value in proxy_partial_table.items():
            print(key, " : ", value)

    #Response to client is formed from the new values from the proxy partial table, and it indicates PUT is executed successfully.
    response_to_client = f"OP=PUT;IND={index1},{index2};DATA={proxy_partial_table[index1]},{proxy_partial_table[index2]};" + " is executed successfully!"
    return response_to_client


def CLR():
    #Asking matlab server to clear its table
    request_to_matlab = "OP=CLR;IND=None;DATA=None;"
    matlab_server.sendall(bytes(request_to_matlab, "utf-8"))
    print("Proxy to MATLAB: " + request_to_matlab)
    response_from_matlab = matlab_server.recv(matlab_PORT)
    response = response_from_matlab.decode("utf-8")
    print("MATLAB to Proxy: " + response)
    #If matlab sends the message "OP=CLR;IND=None;DATA=None;" we understand matlab cleared its table and we can clear the partial table placed in proxy server, here.
    if response == "OP=CLR;IND=None;DATA=None;":
        #Clearing all entries.
        for index in proxy_partial_table.keys():
            proxy_partial_table[index] = 0

    print("Updated partial table:")
    for key, value in proxy_partial_table.items():
        print(key, " : ", value)

    return "OP=CLR;IND=None;DATA=None;" + " is executed successfully!"


#For ADD index1 and index2 is necessary but index3, index4, index5 is optional.
def ADD(index1, index2, index3=-1, index4=-1, index5=-1):
    extra_indices = []  # Holds the optional additional indices ie indices that are additional to the first two necessary indices.
    for optional in [index3, index4, index5]:
        if optional != -1:  # Means user wants more than two indices for add
            extra_indices.append(optional)


    all_indices = [index1, index2] + extra_indices

    not_present = [] #This will hold the indices that are not present in proxy server table.
    for index in all_indices:
        if not (index in proxy_partial_table.keys()):
            not_present.append(index)

    request_to_matlab = "OP=GET;IND="

    if not not_present: #Means not_present is empty and all entries are already here in proxy partial table, no need to ask for them to matlab server
        request_to_matlab = "DO NOT ASK MATLAB SERVER"
    else:
        for index in not_present:
            if index == not_present[-1]: #If it is last we should place ";" according to the format
                request_to_matlab = request_to_matlab + f"{index}" + ";"
            else:
                request_to_matlab = request_to_matlab + f"{index}" + ","
        request_to_matlab = request_to_matlab + "DATA=None;"

    # We need to communicate with matlab server if there is at least one index entry that is not written in proxy table
    if request_to_matlab != "DO NOT ASK MATLAB SERVER":
        matlab_server.sendall(bytes(request_to_matlab, "utf-8"))
        print("Proxy to MATLAB: " + request_to_matlab)
        response_from_matlab = matlab_server.recv(matlab_PORT)
        response = response_from_matlab.decode("utf-8")
        print("MATLAB to Proxy: " + response)
        response_list = re.split(";|=", response)
        # Holding indices and data values
        indices_list = re.split(',', response_list[3])
        data_list = re.split(',', response_list[5])

        #Indices list and data list include only the indices and values are not in proxy table



        #Again, this is for making empty space to add newcomers
        proxy_partial_table_indices_list = []
        for index in proxy_partial_table.keys():
            if not (index in all_indices): #Not to delete any entry that we need for add.
                proxy_partial_table_indices_list.append(index)
        #proxy_partial_table_indices_list has indices that can be overwritten ie they are not needed for the current ADD instruction.
        num_of_newcomers = len(indices_list)
        #We need to delete entries to add newcomers
        for x in range(0, num_of_newcomers): #Iterates number of newcomers times
            proxy_partial_table.pop(proxy_partial_table_indices_list[x])

        #Adding new entries
        for x in range(0, num_of_newcomers):
            proxy_partial_table[indices_list[x]] = int(data_list[x])

        #We have all entries asked by the user, we can calculate the sum.
        sum=0
        str_message_to_client="OP=ADD;IND="
        for index in all_indices:
            sum = sum + proxy_partial_table[index]
            if index != all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{index}" + ","
            elif index == all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{index}" + ";"

        print("Updated partial table:")
        for key, value in proxy_partial_table.items():
            print(key, " : ", value)


        str_message_to_client =str_message_to_client+ f"DATA={sum};"


    #We don't need to communicate with the matlab server.
    elif request_to_matlab == "DO NOT ASK MATLAB SERVER":
        sum = 0
        str_message_to_client = "OP=ADD;IND="
        for index in all_indices:
            sum = sum + proxy_partial_table[index]
            if index != all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{index}" + ","
            elif index == all_indices[-1]:
                str_message_to_client = str_message_to_client + f"{index}" + ";"

        print("Partial table is not updated.")
        str_message_to_client =str_message_to_client+ f"DATA={sum};"


    return str_message_to_client

#Interacting with client incoming messages and handling them.
while True:
    incoming_message = client.recv(client_port) #Receiving string messages
    str_received_message = (incoming_message.decode("utf-8")) #Strings are utf-8 bytes. Decoding to convert them regular strings.
    print("User to proxy: " + str_received_message)

    #The resulting list is in the form ["OP=XXX", "IND", "Ind1,Ind2,..", "DATA", "Dat1,Dat2,..."]
    splitted_message = re.split(';|=', str_received_message)


    #Deciding which operation will be executed according to incoming message.#
    #Handle GET op#
    if "GET" in splitted_message[1]:
        # in splitted_message list, 2. element is indices seperated by commas if it is get, put or add
        indices_list= re.split(',', splitted_message[3])
        if len(indices_list) ==1 :
            response_to_client = GET(indices_list[0])
            print("Proxy to user: " + response_to_client + "\n")
            client.sendall(bytes(response_to_client, "utf-8"))
        elif len(indices_list) ==2 :
            response_to_client = GET(indices_list[0],indices_list[1])
            print("Proxy to user: " + response_to_client + "\n")
            client.sendall(bytes(response_to_client, "utf-8"))
        elif len(indices_list) ==3 :
            response_to_client = GET(indices_list[0],indices_list[1],indices_list[2])
            print("Proxy to user: " + response_to_client + "\n")
            client.sendall(bytes(response_to_client, "utf-8"))
        elif len(indices_list) ==4 :
            response_to_client = GET(indices_list[0],indices_list[1],indices_list[2],indices_list[3])
            print("Proxy to user: " + response_to_client + "\n")
            client.sendall(bytes(response_to_client, "utf-8"))
        elif len(indices_list) ==5 :
            response_to_client = GET(indices_list[0],indices_list[1],indices_list[2],indices_list[3],indices_list[4])
            print("Proxy to user: " + response_to_client + "\n")
            client.sendall(bytes(response_to_client, "utf-8"))




    #Handle PUT op#
    elif "PUT" in splitted_message[1]:
        # in splitted_message list, 2. element is indices seperated by commas if it is get, put or add
        indices_list = re.split(',', splitted_message[3])
        # in splitted_message list, 4. element is data seperated by commas if it is put
        data_list = re.split(',', splitted_message[5])
        response_to_client = PUT(indices_list[0], indices_list[1], data_list[0], data_list[1])
        client.sendall(bytes(response_to_client, "utf-8"))
        print("Proxy to user: " + response_to_client+ "\n")

    # Handle CLR op#
    elif "CLR" in splitted_message[1]:
        response_to_client = CLR()
        client.sendall(bytes(response_to_client, "utf-8"))
        print("Proxy to user: " + response_to_client+ "\n")

    #Handle ADD op#
    elif "ADD" in splitted_message[1]:
        # in splitted_message list, 2. element is indices seperated by commas if it is get, put or add
        indices_list = re.split(',', splitted_message[3])
        if len(indices_list) == 2:
            response_to_client = ADD(indices_list[0], indices_list[1])
            print("Proxy to user: " + response_to_client+ "\n")
            client.sendall(bytes(response_to_client, "utf-8"))
        elif len(indices_list) == 3:
            response_to_client = ADD(indices_list[0], indices_list[1], indices_list[2])
            print("Proxy to user: " + response_to_client+ "\n")
            client.sendall(bytes(response_to_client, "utf-8"))
        elif len(indices_list) == 4:
            response_to_client = ADD(indices_list[0], indices_list[1], indices_list[2], indices_list[3])
            print("Proxy to user: " + response_to_client+ "\n")
            client.sendall(bytes(response_to_client, "utf-8"))
        elif len(indices_list) == 5:
            response_to_client = ADD(indices_list[0], indices_list[1], indices_list[2], indices_list[3], indices_list[4])
            print("Proxy to user: " + response_to_client+ "\n")
            client.sendall(bytes(response_to_client, "utf-8"))


