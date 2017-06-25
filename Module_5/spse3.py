#!/usr/bin/env python
import immlib

DESC = 'SPSE Module 5. Lesson 4. Ex 1. Get Process Content'

def main(args):
  imm = immlib.Debugger()
  td = imm.createTable('Module Information', ['Name', 'Base',
                                              'Entry', 'Size', 'Version'])
  moduleList = imm.getAllModules()
  for module in moduleList.values():
    td.add(0, [entity.getName(),
               '%08X' %entity.getBaseAddress(),
               '%08X' %entity.getEntry(),
               '%08X' %entity.getSize(),
               entity.getVersion()
               ])

  imm.log(str(imm.getRegs()))
  return 'Success'
