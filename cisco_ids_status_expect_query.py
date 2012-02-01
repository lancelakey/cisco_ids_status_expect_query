#!/usr/bin/env python

# Use xterm not xterm-color                                                                                                                              
# I can't figure out how to make this work
# export TERM=xterm

import os, sys, time, re
import pexpect

user = ("your_username")

password = ("your_password")

prompt = ".*#"

ip_list = [
  "10.1.1.1",
  "10.1.1.2",
  "10.1.1.3",
  "10.1.1.4",
  "10.1.1.5"
  ]

cmd_list = [
  "show e a p 23:00"
  ]

print "Starting up now..."

for ip in ip_list: 
  p = pexpect.spawn("ssh %s@%s"%(user, ip), timeout=5, logfile=sys.stdout)

  passq = p.expect (["[Pp]assword: ", pexpect.EOF, pexpect.TIMEOUT])
  if passq == 0:
    p.sendline (password)
  if passq == 1:
    print "%s is unresponsive." % ip
    continue
  if passq == 2:
    print "%s is unresponsive." % ip
    continue

  for cmd in cmd_list: 
    p.expect (prompt) 
    p.sendline (cmd)

    alertq = p.expect (["evIdsAlert", pexpect.EOF, pexpect.TIMEOUT])
    if alertq == 0:
      p.sendline ("q")
      print "\n%s has produced at least 1 alert in the past 23 hours\n" % ip
    elif alertq == 1:
      p.sendline ("q")
      print "%s has produced at least 0 alerts in the past 23 hours" % ip
    elif alertq == 2:
      p.sendline ("q")
      print "%s has produced at least 0 alerts in the past 23 hours" % ip
    
    p.expect (prompt)
    p.sendline ("exit")

    continue

print "\nAll done.\n"
