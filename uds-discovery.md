
<b> Challenge: </b></br>
[EASY] - 20 pts You have encountered a wild module with no home! It has a wiring harness, but it misses its vehicle. The first flag is to identify which car this module came from! Bonus points if you can tell me where it was manufactured.

[HARD] - 100 pts One of the UDS servers on this module has security in place. Find the diagnostic ID and see if you can unlock it. The flag will be in this format: FLAG{...}

<b> Walkthrough: </b></br>

sudo ./uds-server vcan0

cc.py uds discovery

![image](https://user-images.githubusercontent.com/47937620/234049005-82d56a83-7235-4bcc-b5e8-34cb723e4c00.png)

cc.py uds services 0x710 0x77a

![image](https://user-images.githubusercontent.com/47937620/234050031-c17c9ba0-d15e-411d-8c17-556d4c8516f6.png)

cc.py uds services 0x780 0x786

![image](https://user-images.githubusercontent.com/47937620/234052366-b2e80854-6595-45ab-840a-a579a65266df.png)

cc.py uds services 0x7df 0x77a

![image](https://user-images.githubusercontent.com/47937620/234061217-eb4783eb-1e24-4b6d-87b2-fe6bb51efba0.png)

cc.py uds services 0x7e0 0x77a

![image](https://user-images.githubusercontent.com/47937620/234061895-2da16588-f701-4014-a794-d7395c7ed684.png)


In order to identify which vehicle this module came from we can request to read the VIN number by using the ReadDataByIdentifier request 0x22 and VIN request F190

isotprecv -s 780 -d 786 vcan0

cansend vcan0 780#0222F19000000000

Response: 62 F1 90 31 46 54 56 57 31 45 4C 37 4E 57 47 30 30 36 37

Data:
31 46 54 56 57 31 45 4C 37 4E 57 47 30 30 36 37

By converting the hex to ascii we get:
1FTVW1EL7NWG0067

With a quick search online we know now the vehicle and manufacturer:
1  - North America
FT - FORD

UDS Server 0x786 has security and place via 0x27 security access service identifier


