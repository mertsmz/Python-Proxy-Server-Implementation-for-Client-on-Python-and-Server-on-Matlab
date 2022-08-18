# Python Proxy Server Implementation for Client on Python and Server on Matlab
 The server holds a table of 10 indexed integer values and the proxy server has a cached table that holds 5 values. The client asks to get some operations done by sending string messages.  
 
 The message format is **OP=XXX;IND=Ind1,Ind2,..;DATA=Dat1,Dat2,...;** 

**GET:** Request for the values of the specified indices. Response contains the values in the DATA field. Order of the values match order of the indices.  
**PUT:** Request for updating the values of the specified indices. Request contains the values in the DATA field. Order of the values match the order of the indices.  
**CLR:** Clear the whole table for both the proxy and the back endserver.  
**ADD:** Add the values of the specified indices. Response contains the added value in the data field. For simplicity, maximum of 5 indices can be added.  






![Screenshot_5](https://user-images.githubusercontent.com/32621628/185416168-fe6f596e-2b06-4268-9726-7e48c3d2cb2c.jpg)  

**Initial Connections:**
![Screenshot_1](https://user-images.githubusercontent.com/32621628/185417678-faba0a4b-e64c-471d-8fa6-867f64131108.jpg)  


**Examples**   

![Screenshot_5](https://user-images.githubusercontent.com/32621628/185418319-0ce8bdf7-93cf-4d3a-8cf5-4a4fa2d2b64d.jpg)  


![Screenshot_3](https://user-images.githubusercontent.com/32621628/185417911-86a32c39-6cd0-4c0b-917e-d2a8e33d0f52.jpg)  


![Screenshot_4](https://user-images.githubusercontent.com/32621628/185418053-32107cef-8a47-4070-91a2-a51edfb34fd7.jpg)  
