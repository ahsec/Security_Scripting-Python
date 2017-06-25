#!/usr/bin/env python

__VERSION__ = '1.0'
import immlib
from immlib import BpHook
imm = immlib.Debugger()

DESC = 'BpHook for SPSE Course Module 5. Lesson 5'

class StrcpyBpHook(BpHook):

  def __init__(self) :
    BpHook.__init__(self)
  
  def run(self, regs):
    imm = immlib.Debugger()
    imm.log('Strcpy BpHook Called')

    # strcpy(char *destination, char *source)

    eipOnStack = imm.readLong(regs['ESP'])
    strcpyFirstArg = imm.readLong(regs['ESP'] + 4)
    strcpySecondArg = imm.readLong(regs['ESP'] + 8)
    imm.log('EIP on Stack: 0x%08x   First Arg: 0x%08x   Second Arg: 0x%08x' %(eipOnStack, strcpyFirstArg, strcpySecondArg))

    # Print the Source String
    recievedString = imm.readString(strcpySecondArg)
#    imm.log(recievedString)
    imm.log('Recieved String Length: %d \nValue: %s' %(len(recievedString), str(recievedString)))

def main(args) :
  # Finding strcpy address
  functionToHook = 'msvcrt.strcpy'
  functionAddress = imm.getAddress(functionToHook)
  newHook = StrcpyBpHook()
  newHook.add(functionToHook, functionAddress)

  imm.log('Hook for %s : 0x%08x added Succesfully!' %(functionToHook, functionAddress))
  return 'Hook Installed'

