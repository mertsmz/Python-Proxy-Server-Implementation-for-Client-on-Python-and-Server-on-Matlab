# Python Proxy Server Implementation for Client on Python and Server on Matlab
 The server holds a table of 10 indexed integer values and the proxy server has a cached table that holds 5 values. The client asks to get some operations done by sending string messages.  
 
 The message format is **OP=XXX;IND=Ind1,Ind2,..;DATA=Dat1,Dat2,...;** 

**GET:** Request for the values of the specified indices. Response contains the values in the DATA field. Order of the values match order of the indices.  
**PUT:** Request for updating the values of the specified indices. Request contains the values in the DATA field. Order of the values match the order of the indices.  
**CLR:** Clear the whole table for both the proxy and the back endserver.  
**ADD:** Add the values of the specified indices. Response contains the added value in the data field. For simplicity, maximum of 5 indices can be added.  
