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
***Stephen, this is the RSync section***


### Web Application


**Dependencies:**
- Python 3

  - Python Requests module - For windows, see [this](http://stackoverflow.com/questions/1449494/how-do-i-install-python-packages-on-windows).


- Ruby on Rails 4

  - See the Gemfile for app specific dependencies.


*NOTES*

Bulk inserts: http://stackoverflow.com/questions/7965949/best-practice-for-bulk-update-in-controller

RailsCast on Devise (Authentication): http://railscasts.com/episodes/209-devise-revised
***REMEMBER: Set action mailer URL in production environment with actual host***

Alternative Charts - http://railscasts.com/episodes/223-charts

Also, look at custom rake tasks! There's a railscast. #66 I believe.

Should we use a SQL DB now?
If not, it's gonna be hard to do this in rails...
But if we use a NoSQL DB, using another framework will be harder to implement and take more time.

Yep, let's just do a regular SQL db...:(
