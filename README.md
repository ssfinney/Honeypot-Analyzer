Honeypot Analyzer
=================

***This is alpha software and is under construction. Use at your own risk.***

**This software isn't functional and is therefore deprecated.**

For a better, open-source log management tool, see [Logstash](http://www.logstash.net).


## Table of Contents<a name="table_of_contents"></a>
* [Introduction & Description](#introduction)
* [Breakdown of System Components](#breakdown)
* [Installation Instructions](#installation)
* [Execution Instructions](#execution)
* [User Functional Walk-through](#walkthrough)
* [Troubleshooting](#troubleshooting)
* [Known Issues](#known_issues)
* [Licensing](#licensing)



### Introduction & Description<a name="introduction"></a>
---

This is a program to retrieve and analyze log entries from a network honeypot. It parses the logs, stores them inside our web application's database, and produces analytics for the log information. 

This program currently works only with log files from [HoneyD's](http://www.honeyd.org) open-source software.

This README acts as the project's user manual and includes the necessary information to install and run the program.

#### What is a Honeypot?

A network honeypot is software that makes your server *look* like a vulnerable machine for hackers. In reality, it's completely isolated from the outside world, but it looks like a hackable machine on a network.

This attracts attackers who want to steal information, data, or place malware on your system. With the honeypot software, you can see where the attackers are attacking from, their IP addresses, and information on which vulnerability was used. With our analyzer, you can visualize this data and really get a feel for what's going on in your network or where your security can be improved.

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

#### Usage

If you want to simply use our software, ***you can do so without any installation!*** Once the web application is complete and live, you'll be able to log in as a user, upload your logs, and see the magic happen right there. We'll keep you posted about developments in this area.

In the meantime, if you want to host this software on *your* machine, then keep reading. We'll walk-through the concepts behind the software, what each piece means, and how to install and run it all. It's pretty long, but you can do it.

### Breakdown of System Components<a name="breakdown"></a>
---

#### Log parser

The log parser is a Python program with a few parameters. The program takes a log file, parses it with the fields described in the last section, and sends it over HTTP to the web application. For now, the code is written to handle only local HTTP traffic, but will be modified in the future to send data to a live website. The program is located at  ```backend/analyzer/parser.py```. Below are the parameters and their meaning:

Command line usage:
       python parser.py

Arguments:
* --user <user name>    
  - What's your username on our website?

* --log <logfile name> 
  - The path to the log file.

* --update <True or False>
  - Is this file an update of one previously parsed? Default: False.

* --static <True or False>
  - Is this a static file, or one that is being updated by HoneyD constantly? Default: True.
                          
                         
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
person hosting the honeypot analyzer and that the server's password will need to be entered after the scp request call.


#### Web Application

We're using Ruby on Rails 4 as our web application (although this will most likely change to Rails 3 in the near future). 


##### MVC 

The framework is an MVC model (which stands for Models, Views, and Controllers) that define and execute on our data.

In the application, we have models for users, logs, and log entries. 

These models are the definitions for what things the database will store.

The views render the data and use embedded Ruby within them to dynamically render information based on user input.

The controllers define the logic for this interaction, and map the HTTP verbs (GET, POST, PUT, & DELETE) to real actions inside of the framework.

##### The Database 

In addition, we're using SQLite as our database model for the website. Since the application is still under heavy development, SQLite's simplicity is very helpful. In the future, this will most likely change to MySQL to accommodate a real user base.

Right now, the database is integrated with Rails' database helper structure called ActiveRecord, which is an ORM (Object-relational mapping) that helps us manipulate and query the database from within the framework. Database migrations are made when changes to the database have to be made. 

##### Purpose of the web application

The web application is designed to facilitate the user's needs with regard to their log files. They can upload their logs or point our code to their server in order to monitor their ongoing Honeypot instance. This is all done through the front-end UI in the web application. User accounts are made for them so they can see their logs and interact with them. They can also see the analytics of their logs as well.

##### Analytics

The app will render different kinds of analytical information for the user to see and interact with. The following are examples of analytics planned for the application:

* Data table - This will be a paginated table of a single log file (the user will select which one it wants to use). The user can then search, filter, and sort the log entries within the table as they desire.

* Charts - There will be a number of Bar and Pie charts visualizing the data, according to whatever parameters the user chooses. Some particularly useful charts will include charts for the top source & target IP addresses and port numbers.

* Maps - There will be a Google Map with the source IP address' geo-location information on it. This information will include city & country information about the source addresses. Later, there may be a heatmap implementation, which would visualize clusters of hits from the same geographical locations.

More information about the web application implementation and UI design can be found in the official design documentation.

### Installation Instructions<a name="installation"></a>
---
#### Back-end Installation

First, open the terminal and execute the following shell command on the intended HoneyPot analyzer host server:
```wget https://raw.github.com/ssfinney/Honeypot-Analyzer/master/backend/backend.tar.gz```

Then, you'll need to decompress it into the directory of your choosing:
```tar -xvf backend.tar.gz```

#### Log monitor

Execute the following command to generate your own personal rsa key:  
```ssh-keygen -t rsa```

You will see the following text:  
```Generating public/private rsa key pair.```  
```Enter file in which to save the key (/home/username/.ssh/id_rsa):```  

The default settings (just hitting enter) are generally acceptable but root may want to change the folder location.  

You will then be asked to enter a passphrase. If you enter one, you will be prompted for it every time you connect
the remote server. You then must verify the passphrase and you will see the following text:

```Enter passphrase (empty for no passphrase):```  
```Enter same passphrase again:```  
```Your identification has been saved in /home/username/.ssh/id_rsa.```  
```Your public key has been saved in /home/username/.ssh/id_rsa.pub.```  
```The key fingerprint is:```  
```bf:7b:63:a8:91:29:76:2b:03:ac:21:8c:91:4a:fa:11 username@server.domain.com```  

The passphrase can be changed at anytime with ```sshkeygen -p```  

Next type the following commands:  
```cd ~/.ssh```  
```cp id_rsa.pub authorized_keys```  
Note that if you changed the initial location, you will need to go to that folder first.

Then type:  
```mv authorized_keys /home/<username>/analyzer/keys/```  
Note that the <username> will need to be changed to your account's username.

#### Log parser

The parser is included in the tarball file you downloaded, so there's no need to do anything else for it right now.


#### Web application installation

This is a Rails app, so you'll need to install Ruby on Rails on your machine. Again, just like for the back-end code above, we're assuming that you're running this on a Linux machine.

First, you need to install Ruby on your machine. [Here](https://www.ruby-lang.org/en/downloads) is a good guide for setting it up.

When Ruby is done installing, you'll have access to a great tool for Ruby applications, called rubygems. This will let you install Ruby packages (like Rails and *many* of the packages you'll use in Rails) with a simple command.

Run ```gem install rails``` on the command line to install Rails with all of its dependencies. Easy!

Once Rails is done installing, you need to download the source code from here on GitHub. To do that, you'll need to pull the code down using git. Install git (if you don't have it already; you probably do and don't know it) using this: 
```git clone https://github.com/ssfinney/Honeypot-Analyzer.git```

Done! You've finished installing Rails. Now, we need to install the dependencies for the app. First, you need to run ```bundler``` to install the rubygems we need to run the app. That's it; just type ```bundler```. 

After that's done, we need to migrate the database. If you didn't already, you now have SQLite. Rails uses a tool called "rake" to do stuff to the database for you. So, all you need to do is: ```rake db:migrate``` and you're done!

### Execution Instructions<a name="execution"></a>
---

#### Log monitor

When starting the log monitor, you're effectively creating a new user for the program. The monitor program is called ```newUser``` and is located inside the tarball that you downloaded. The usage for the monitor is defined as: ```newUser <user@hostname> <location> <userID>```

Here's what the parameters mean:
* user@hostname - The user's name and the domain host name that he/she is on. This is the server that the HoneyD Honeypot software is running on, so make sure you point it in the right place. 
     - Example: smith@host.servername.com

* location - This is the path on that server to the log file that HoneyD is updating. It's the full path from root. Make sure it's correct. 
     - Example: /home/smith/Honeypot/Logs/log.log

* userID - This is the user's name that he signed up with on the web application. Don't worry, we'll go over how to set that up below in a little bit.
     - Example: JohnSmith

#### Log Parser

The web application and the log monitor above both execute the log parser when they have logs to process. If the log monitor is running, it will execute an instance of the parser to process the files that it's retrieving. 

The web application executes it when a user uploads some static log files to the server to process them. In this case, the parser dies when finished but it will continue running if it's processing a log file that is being updated by the monitor.

#### Web Application

Now, we have to initialize the app before we use it. Fortunately, this takes almost no effort whatsoever. You already learned to [install the Rails framework and its dependencies](#installation). You also migrated the database already, so all that's left to do it start the Rails server. 

Just run ```rails server```. When you do that, you can run the web application out of your browser by going to ```http://localhost:3000``` and you're done!

### User Functional Walk-through<a name="walkthrough"></a>
---

As we mentioned in [the Usage section](#introduction), to use the software without hosting it yourself, simply use the live website! Right now, we don't have a live site up and running and the web application isn't finished. You can see our progress here on the GitHub page.

When the website is live, users can go to it, sign up for an account, and start monitoring & uploading log files to be analyzed. After signing up, they will be able to select a log file to look at and perform any analysis that they wish on it. Maps, charts, data tables, and custom searching/sorting will all be supported. 

It's that simple! No installation required.

### Troubleshooting<a name="troubleshooting"></a>
---

If you're having trouble getting this set up on your machine, then it's possible there's a bug in our code. Please submit issues on this GitHub site, or submit pull requests with your own fix for our code! We welcome both.

If you need help, please don't hesitate to submit an issue or contact Stephen Finney at stephen.s.finney@gmail.com.

In general, make sure that your monitor is running and pointed to the correct location and server, and that your Rails server is running and is working correctly.

### Known Issues<a name="known_issues"></a>
---

There is a list of known issues on the Issues page here on GitHub. Just go to the right-hand side of the page and click "Issues" to see what's been reported so far. Feel free to add your own!

### Licensing<a name="licensing"></a>
---

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/InteractiveResource" property="dct:title" rel="dct:type">Honeypot Analyzer</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Thai-Son Le, Stephen Antalis, and Stephen Finney</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://www.github.com/ssfinney/Honeypot-Analyzer" rel="dct:source">https://www.github.com/ssfinney/Honeypot-Analyzer</a>
