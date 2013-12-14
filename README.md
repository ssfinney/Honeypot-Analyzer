Honeypot Analyzer
=================

***Under construction. Use at your own risk.***


## Table of Contents
* Introduction & Description
* Breakdown of System Components
* Installation Instructions
* Execution Instructions
* User Functional Walk-through
* Troubleshooting
* Known Issues



### Introduction & Description
---

This is a program to retrieve and analyze log entries from a network honeypot. It parses the logs, stores them inside our web application's database, and produces analytics for the log information. 

This program currently works only with log files from [HoneyD's](http://www.honeyd.org) open-source software.


#### What is a Honeypot?

A network honeypot is software that makes your server *look* like a vulnerable machine for hackers. In reality, it's completely isolated from the outside world, but it looks like a hackable machine on a network.

This attracts attackers who want to steal information, data, or place malware on your system. With the honeypot software, you can see where the attackers are attacking from, their IP addresses, and information on which vulnerability was used.

#### The Honeypot Log File

Our system gets these logs and analyzes the data inside them. HoneyD log files have the following fields in them, and we'll parse them.

For the TCP or UDP protocol, the following fields exist:

 - date 
 - time 
 - protocol 
 - connection type 
 - source IP 
 - target IP 
 - source port 
 - target port 
 - other information 
 - environment information

For the ICMP protocol, the entries are the same except for the port fields, which are omitted.


#### Our System

Our analyzer is a combination of a log parser, a log monitor, and a web application. These parts work together to create the analytics for the log information. In the next section, we'll discuss the system's components and each of their roles in this project.

### Breakdown of System Components
---

#### Log parser

The log parser is a Python program with a few parameters. The program takes a log file, parses it with the fields described in the last section, and sends it over HTTP to the web application. For now, the code is written to handle only local HTTP traffic, but will be modified in the future to send data to a live website. The program is located at  ```backend/app.py```. Below are the parameters and their meaning:

Command line usage:
       python app.py

        Arguments:
                --user <user name> What's your username on our website?

                --log <logfile name> 
                         The path to the log file.

                --update <True or False>
                          Is this file an update of one previously parsed? Default: False.
                          
                --static <True or False>
                          Is this a static file, or one that is being updated by HoneyD constantly? Default: True.
                          
                         
This file will *not* be run by the end user. Instead, it will be called by the two other components of the program, which are described below.


#### Log monitor
This executable bash program will link a remote server to the honeypot analyzer's server and copy over then update the web user's honeypot log file on the host's server indefinately.

The user file will use a previously created public key saved in the file ```authorized_keys``` located at ```/home/<hostUser>/analyzer/keys/authorized_keys``` on the analyzer server to install RSA encrypted ssh keys onto a remote server and then will use the rsync command to first pull a log file from that server and update that file every 10 seconds if needed. It assumes that the HoneyPot analyzer is stored at /home/<hostUser>/analyzer/ and that it is already setup with the folder 'users' inside. See the rest of the README for help.

This file must be created as an executable bash file. 

Required Input fields:
```newUser <user@host.servername.com> <location> <userID>```

newUser is the executable
```<user@host.servername.com>``` is the user account with the log file and server or ip address
```<location>``` is the specific path to the log file on the server
```<userID>``` is the user id of the user on the web server. 

example execution call:
```newUser smith@host.servername.com /home/smith/Honeypot/Logs/log.log JohnSmith```

Note that in the below code, the ```<hostUser>``` field needs to be modified to be the account of the
person hosting the honeyput analyzer and that the server's password will need to be entered after the scp request call.


#### Web Application

### Installation Instructions
---
#### Back-end Installation

Open the terminal and execute the following shell command on the intended HoneyPot analyzer host server:
```wget --link--```

Execute the following command to generate your own personal rsa key:
```ssh-keygen -t rsa```
