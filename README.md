# S7conn_extender
 connects more S7-PLC to SCADA then allowed
 ******************************************
 
 According to this Siemens forum threads:
 https://support.industry.siemens.com/tf//ww/en/posts/maximum-allowable-number-of-connections-in-wincc/62699
 https://support.industry.siemens.com/tf/WW/en/posts/limitation-in-number-of-connections-in-wincc/182503
 
 Windows can't handle more then 10 PLC connections.
 
 Script Snap7Server.py uses snap7 library to start virtual PLC server. 
 SCADA software is configured just for one connection to the virtual server.
 
 Script S7Exchanger uses snap7 library to exchange data from physical PLCs to virtual server one by one, not simultaneously.
 
 Installation and run:
 * expected installed SCADA software
 1) download latest snap7-full from `https://sourceforge.net/projects/snap7/files/ `
 2) extract from \build\bin\win64 files snap7.dll and snap7.lib into windows/system32/
 3) start Snap7Server.py with administrator rights
 4) configure config.ini file
 5) start S7Exchanger.py
 
 Tested with WinCC Advanced V13. There is Cyclic operation checkbox in connections - must be unchecked.