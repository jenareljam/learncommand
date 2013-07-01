#!/usr/bin/env python
#
# Copyright (C) 2013 Jeremy Erickson
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import os.path
import re
import imp
import base64

config = None # will be loaded at runtime to retrieve configuration information about the level

def loadConfig():
  cwd = os.getcwd()
  cur_path = cwd
  while cur_path != "/":
    if os.path.isfile(cur_path+"/.config"): # if the config file is in this directory
      global config
      config = imp.load_source("config",cur_path+"/.config") # load it
      if hasattr(config,"BASE_CONFIG"):
        if config.BASE_CONFIG: # if we could only find the config file in the main directory
          print "Error: Could not find local config file. Is the module complete?"
          sys.exit(1)
      return
    else:
      cur_path = os.path.split(cur_path)[0] # go up a directory
  print "Error: Could not find any config file"
  sys.exit(1)

def answerCorrect():
  global config
  if not hasattr(config,"PUZZLE_TYPE"):
    print "Error: No PUZZLE_TYPE specified in configuration."
    sys.exit(1)
  if config.PUZZLE_TYPE == "question":
    return question()
  elif config.PUZZLE_TYPE == "custom":
    return custom()
  elif config.PUZZLE_TYPE == "command_history":
    return commandHistory()
  elif config.PUZZLE_TYPE == "directory_structure":
    return directoryStructure()
  elif config.PUZZLE_TYPE == "interactive":
    return interactive()

def question():
  if not (hasattr(config,"PUZZLE_QUESTION") or hasattr(config,"PUZZLE_ANSWER")):
    print "Error: Interactive puzzle type requires PUZZLE_QUESTIon and PUZZLE_ANSWER arguments"
    sys.exit(1)
  answer = raw_input(config.PUZZLE_QUESTION+" ")
  #print answer
  #print base64.b64encode(answer)
  #print config.PUZZLE_ANSWER
  if base64.b64encode(answer) == config.PUZZLE_ANSWER or base64.b64encode(answer) in config.PUZZLE_ANSWER:
    print "Correct! Unlocking next level."
    return True
  else:
    print "Incorrect. Please try again."
    return False

def custom():
  if not (hasattr(config,"PUZZLE_METHOD") or hasattr(config,"PUZZLE_FAILURE_MESSAGE")):
    print "Error: Interactive puzzle type requires PUZZLE_QUESTIon and PUZZLE_ANSWER arguments"
    sys.exit(1)
  win = config.PUZZLE_METHOD()
  if win:
    print "Well done! Unlocking next level."
  else:
    print config.PUZZLE_FAILURE_MESSAGE
  return win

def commandHistory():
  return False

def directoryStructure():
  return False

def interactive():
  return False

def unlockNext():
  return False

def main():
  # find current module directory and configuration file
  loadConfig()
  if answerCorrect():
    if not unlockNext():
      print "Congratulations! You've passed the module!"
      sys.exit(0)
  else:
    print "If you want to start this level over, use the 'reset' command."

if __name__=="__main__":
  main()
