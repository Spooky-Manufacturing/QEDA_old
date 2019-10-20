#!/usr/bin/python3
from math import ceil as CEIL
from pcb import PCB, Segment
from pykicad.module import Module

class Automaker():
    def __init__(self):
        self.pcb = PCB()
        x = Module.from_library('Resistors_SMD', 'R_0805')
        x.set_reference('x')
        y = Module.from_library('Resistors_SMD', 'R_0805')
        y.set_reference('y')
        z = Module.from_library('Resistors_SMD', 'R_0805')
        z.set_reference('z')
        a = Module.from_library('Resistors_SMD', 'R_0805')
        a.set_reference('a')
        b = Module.from_library('Resistors_SMD', 'R_0805')
        b.set_reference('b')
        c = Module.from_library('Resistors_SMD', 'R_0805')
        c.set_reference('c')
        qcode = [[a,b,c], [x,y], [z]]
        self.automake(qcode)
        pass

    def _find_max_x(self, comp):
        """Returns the maximal X size as an integer"""
        global CEIL
        max_x = 0
        geo = comp.geometry()
        x = [each for each in geo]
        for each in x:
            if each.start == None and each.end != None:
                y = abs(0 - each.end[0])
            elif each.end == None and each.start != None:
                y = abs(each.start)
            elif each.start == each.end == None:
                pass
            else:
                y = abs(each.start[0] - each.end[0])
                if y > max_x:
                    max_x = y
        return CEIL(max_x)

    def _find_max_y(self, comp):
        """Return maximal Y size as an integer"""
        global CEIL
        max_y = 0
        geo = comp.geometry()
        x = [each for each in geo]
        for each in x:
            if each.start == None and each.end != None:
                y = abs(0 - each.end)
            if each.end == None and each.start != None:
                y = abs(each.start)
            elif each.start == each.end == None:
                pass
            else:
                y = abs(each.start[1] - each.end[1])
                if y > max_y:
                    max_y = y
        return CEIL(max_y)

    def _find_maxes(self, comp):
        """Returns the maximal x and y value of a component (starting at 0,0)"""
        x = self._find_max_x(comp)
        y = self._find_max_y(comp)
        return int(x), int(y)

    def _find_x(self, pos, maxx):
        """Returns the x coordinates"""
        return pos[0] + maxx

    def _find_y(sef, pos, maxy):
        return pos[1] + maxy
        
    def _autoplace_unitary_gates(self, qcode):
        pos = {
            'X': 0,
            'Y': 0
            }
        max_y = 0
        for qubit in qcode:
            for i in range(len(qubit)):
                # Place component (horizontal line)
                self.pcb._place_component(qubit[i], pos['X'], pos['Y'])
                print('Component is at ', qubit[i].at)
                x, y = self._find_maxes(qubit[i])
                #update x, y values
                pos['X'] = pos['X'] + x
                if y > max_y:
                    max_y += y
                #loop
            # Step down y by max_x
            pos['X'] = 0
            pos['Y'] = pos['Y'] + max_y


#                if i == len(qubit)-1:
#                    start, end, np_pos = self.pcb._final_compute(qubit[i])
#                else:
#                    start, end, np_pos = self.pcb._compute_positions(
#                        qubit[i], qubit[i+1])
#                # Create segments
#                self.pcb._create_segment(start, end, self.pcb.nets[1])

    def _autoplace_controlled_gates(self, qcode):
        pos = {
            'X': 0,
            'Y': 0
            }
        max_y = 0
    
        
    
    def _autoplace3(self, qcode):
        """Automagically places components where they need to be"""
        pos = {
            'X': 0,
            'Y': 0
            }
        cur_x = 0
        cur_y = 0
        for qubit in qcode:
            for i in range(len(qubit)):
                # Connect pads
#                self.pcb._connect_pad(qubit[i], 1, 1)
                # Find maxes
                x, y = self._find_maxes(qubit[i])
                print(x)
                # Place component
                cur_x += x
                pos['X'] = cur_x
                cur_y += y
                print("Placing Component: ", qubit[i].name, ' at coordinates', pos)
                self.pcb._place_component(qubit[i], pos['X'], pos['Y'])
                print('Component is at ', qubit[i].at)
                # compute and place vias
                if i == len(qubit)-1:
                    start, end, pos_np = self.pcb._final_compute(qubit[i])
                else:
                    start, end, pos_np = self.pcb._compute_positions(
                        qubit[i], qubit[i+1])
                # Create segments
                self.pcb._create_segment(start, end, self.pcb.nets[1])
                print('Rechecking, component is at ', qubit[i].at)
            cur_x = 0
            pos['X'] = cur_x
            pos['Y'] = cur_y
            
    def automake(self, qcode):
        """Attempts to automagically make a PCB from modules

        To start, we have our qcode which is in list format:
        1,H,CX,...,MEASURE
        2,I,I,..., MEASURE
        3,I,CX,...,MEASURE
        ... etc
        pass

        For quantum gates, we only need to place footprints.

        For electrical/analog gates we will need to computer positions, vias, etc"""
        #Place components
        self._autoplace(qcode)
        # Create PCB Zones
        self.pcb._create_zones()
        # Make the PCB
        self.pcb._create_pcb()

if __name__ == '__main__':
    a = Automaker()
