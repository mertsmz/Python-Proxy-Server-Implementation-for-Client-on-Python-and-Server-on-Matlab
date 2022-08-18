import socket
import re

#The information of the proxy server that client will connect.#
proxy_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None)
proxy_PORT = 5050
proxy_IP= socket.gethostbyname(socket.gethostname())
proxy_ADDR= (proxy_IP, proxy_PORT)

print("Waiting for connection to proxy server...")
#Client connects to the proxy#
isConnected = False
while not isConnected:
    try:
        proxy_server.connect(proxy_ADDR)
        isConnected=1
    except:
        continue

greeting_message = proxy_server.recv(proxy_PORT)
print(greeting_message.decode("utf-8"))

##Functions that send messages(requests) to the proxy server##
#Message Format## OP=XXX;IND=Ind1,Ind2,..;DATA=Dat1,Dat2,...;#
#In message format, if one field is unnecessary, its value is written as "None" #
def GET(index1, index2=-1, index3=-1, index4=-1, index5=-1):
    extra_indices = []  # Holds the optional additional indices ie indices that are additional to the first index
    for optional in [index2, index3, index4, index5]:
        if optional != -1:  # Means user wants more than two indices for add
            extra_indices.append(optional)

    str_message = f"OP=GET;IND={index1}"
    for index in extra_indices:
        str_message = str_message + "," + index
    str_message = str_message + ";DATA=None;"
    proxy_server.sendall(bytes(str_message, "utf-8"))  # Sending the instruction in the specified format
    print('You to proxy: ' + str_message)
    print('Proxy to you: ' + proxy_server.recv(proxy_PORT).decode("utf-8"))


def PUT(index1, index2, data1, data2):
    str_message = f"OP=PUT;IND={index1},{index2};DATA={data1},{data2};"
    proxy_server.sendall(bytes(str_message, "utf-8")) #strings are utf-8 bytes.
    print('You to proxy: ' + str_message)
    print('Proxy to you: ' + proxy_server.recv(proxy_PORT).decode("utf-8"))


def CLR():
    str_message = "OP=CLR;IND=None;DATA=None;"
    proxy_server.sendall(bytes(str_message, "utf-8")) #strings are utf-8 bytes.
    print('You to proxy: ' + str_message)
    print('Proxy to you: ' + proxy_server.recv(proxy_PORT).decode("utf-8"))


#For ADD index1 and index2 is necessary but index3, index4, index5 is optional.
def ADD(index1,index2,index3=-1,index4=-1,index5=-1):
    extra_indices = [] #Holds the optional additional indices ie indices that are additional to the first two necessary indices.
    for optional in [index3, index4, index5]:
        if optional!=-1:#Means user wants more than two indices for add
            extra_indices.append(optional)
    str_message = f"OP=ADD;IND={index1},{index2}"
    for index in extra_indices:
        str_message = str_message +"," + index
    str_message = str_message + ";DATA=None;"
    proxy_server.sendall(bytes(str_message, "utf-8")) #Sending the instruction in the specified format
    print('You to proxy: ' + str_message)
    print('Proxy to you: ' + proxy_server.recv(proxy_PORT).decode("utf-8"))
##End of message sender functions##





##Interface##
def interface():
    choice = input("1) GET\n2) PUT\n3) CLR\n4) ADD\n")
    #GET#
    #With GET, user can ask from number of 0 to 5 indices values.
    if choice == "1":
        indices = input("Enter number of between 0-5 indices whose values are between 0 and 9 by separating them with space characters.\n")
        indices_list=re.split("\s", indices)
        #Invalidity check#
        if len(indices_list) > 5:
            print("You entered more than 5 indices!")
            interface()
        elif len(indices_list) == 0:
            print("You didn't enter any index value!")
            interface()
        for strindex in indices_list:
            if int(strindex) < 0 or int(strindex) > 9:
                print("You entered invalid index values!")
                interface()
        #End of invalidity check#

        if len(indices_list) == 1:
            GET(indices_list[0])
            interface()
        elif len(indices_list) == 2:
            GET(indices_list[0], indices_list[1])
            interface()
        elif len(indices_list) == 3:
            GET(indices_list[0], indices_list[1], indices_list[2])
            interface()
        elif len(indices_list) == 4:
            GET(indices_list[0], indices_list[1], indices_list[2], indices_list[3])
            interface()
        elif len(indices_list) == 5:
            GET(indices_list[0], indices_list[1], indices_list[2], indices_list[3], indices_list[4])
            interface()


    #PUT#
    elif choice=="2":
        two_indices_and_data = input("Enter two indices between 0 and 9  and two corresponding data value respectively by separating them with space character.\n")
        two_indices_and_data_list = re.split("\s", two_indices_and_data)

        #Invalidity check#
        if len(two_indices_and_data_list)!=4:
            print("You didn't enter appropriate number of inputs!")
            interface()

        for strindex in two_indices_and_data_list[0:2]:
            if int(strindex) < 0 or int(strindex) > 9:
                print("You entered invalid index values!")
                interface()
        #End of invalidity check#

        ##i1,i2,d1,d2 ile işlem yapılcak func çağırılıp.
        i1 = (two_indices_and_data_list)[0]
        i2 = (two_indices_and_data_list)[1]
        d1 = (two_indices_and_data_list)[2]
        d2 = (two_indices_and_data_list)[3]
        PUT(i1, i2, d1, d2)
        interface()


    #CLR#
    elif choice=="3":
        CLR()
        interface()


    #ADD#
    elif choice=="4":
        indices = input("Enter maximum number of 5 indices between 0 and 9  by separating them with space character.\n")
        indices_list = re.split("\s", indices)

        #Invalidity check#
        if len(indices_list)>5:
            print("You entered more than 5 indices!")
            interface()
        elif len( indices_list)==1:
            print("You entered only one index value")
            interface()
        for strindex in indices_list :
            if int(strindex)<0 or int(strindex)>9:
                print("You entered invalid index values!")
                interface()
        #End of invalidty check#

        if len(indices_list)==2:
            ADD(indices_list[0], indices_list[1])
            interface()
        elif len(indices_list)==3:
            ADD(indices_list[0], indices_list[1], indices_list[2])
            interface()
        elif len(indices_list)==4:
            ADD(indices_list[0], indices_list[1], indices_list[2], indices_list[3])
            interface()
        elif len(indices_list)==5:
            ADD(indices_list[0], indices_list[1], indices_list[2], indices_list[3], indices_list[4])
            interface()
    else:
        print("Invalid option!")
        interface()

interface()
##End of Interface##
