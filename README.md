python tcp server to forward command as osc to Disguise d3 software. 

simply put that on a device on your network and send it commands and it will resend it to the server as osc. 

e.g. Sending cue :
create telnet device with port 12345
create control string : cue \$
create remote transport receiving on port 12346
send command with variable 0
('cue 0')
receive osc command /d3/showcontrol/cue 0

any /d3/showcontrol command show work out of the box. 

