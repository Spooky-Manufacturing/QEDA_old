#!/usr/bin/python3
import configparser
from numpy import array
from math import ceil as CEIL

from pykicad.pcb import Net, Via, Segment, Setup, Layer, NetClass, Pcb
from pykicad.module import *

config = configparser.ConfigParser()
config.read('configs/pcb.conf')

class PCB():
    def __init__(self, title='Quantum PCB Output', comment1='', s='DEFAULT'):
        # Get configurations
        # Define nets
        vi_net, vo_net, gnd_net = Net('VI'), Net('VO'), Net('GND')
        # Init variables
        self.num_nets = 4
        self.modules = []
        self.net_classes = None
        self.nets = [vi_net, vo_net, gnd_net]
        self.vias = []
        self.zones = []
        self.segments = []
        self.via_size = float(config[s]['via_size'])
        self.drill_size = float(config[s]['drill_size'])
        self.clearance = float(config[s]['clearance'])
        self.layers = [] #int(config[s]['layers'])
        self.page_type = [int(x) for x in config[s]['page_type'].split(',')]
        self.trace_width = config[s]['trace_width']
        self.coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        # PCB Info
        self.title = title
        self.comment1 = comment1
        grid_orig = [int(x/2) for x in self.page_type]
        self.setup = Setup(grid_origin=grid_orig)

    def _connect_pad(self, comp, pad, net):
        """Connects components pads electrically
            comp - Module, component
            pad - integer, pad number
            net - Net, which net to connect to
        """
        # r1.pads[0].net = vi
        comp.pads[pad].net = self.nets[net]

    def _place_component(self, comp, x_pos, y_pos):
        """Places component comp at position x,y and adds it to PCB list"""
        comp.at = [x_pos, y_pos]
        self.modules.append(comp)

    def _final_compute(self, comp):
        """Computes the positions of vias for quantum optical components"""
        start = array(comp.pads[1].at) + array(comp.at)
        end = array(comp.pads[0].at) + array(comp.at)
        pos = start + (end - start) / 2
        self._create_via(pos, self.nets[1].code)

        return start, end, pos

    def _compute_positions(self, comp1, comp2, pads=[1, 0], create_vias=True):
        """Computes the positions of vias
        comp1 - Module for component 1
        comp2 - Module for component 2
        pads - list of integers of pads, only 2 pads can be connected at a time
        create_vias - Boolean, create vias as well
        Notes:
            comp1 and comp2 can be the same.
        """
        start = array(comp1.pads[pads[0]].at) + array(comp1.at)
        end = array(comp2.pads[pads[1]].at) + array(comp2.at)
        pos = start + (end-start)/2

        if create_vias:
            self._create_via(pos, self.nets[1].code)
        return start, end, pos

    def _create_via(self, pos, net=None, via_size=None, drill_size=None):
        """Creates the vias
        pos = Position
        net = Net
        via_size = Size of via (default 0.8)
        drill_size = Size of drill (default 0.6)
        """
        if via_size is None:
            via_size = self.via_size
        if drill_size is None:
            drill_size = self.drill_size
        self.vias.append(Via(at=pos.tolist(), size=via_size, drill=drill_size, net=net))

    def _create_segment(self, start, end, net):
        """Creates segments and appends to the list of segments
        net = connected net

        values from self._compute_positions():
        start
        end
        """
        self.segments.append(Segment(
            start=start.tolist(),
            end=end.tolist(),
            net=net.code))

    def _create_zones(self):
        """Creates the zones (layers) of the PCB"""
        #coords = self.coords
        # Unneeded?
        #gndplane_top = Zone(net_name='GND', layer='F.Cu',
        #                    polygon=coords, clearance=self.clearance)

        layers = [
            Layer('F.Cu'),
            Layer('Inner1.Cu'),
            Layer('Inner2.Cu'),
            Layer('B.Cu'),
            Layer('Edge.Cuts', type='user')
            ]
        for layer in ['Mask', 'Paste', 'SilkS', 'CrtYd', 'Fab']:
            for side in ['B', 'F']:
                layers.append(Layer('%s.%s' % (side, layer), type='user'))
        self.net_classes = NetClass('default',
                                    trace_width=self.trace_width,
                                    nets=['VI', 'VO', 'GND'])

    def _create_pcb(self):
        print('Making PCB')
        pcb = Pcb()
        pcb.title = self.title
        pcb.comment1 = self.comment1
        pcb.page_type = self.page_type
        pcb.num_nets = self.num_nets
        pcb.setup = self.setup
        pcb.layers = self.layers
        pcb.modules = self.modules
        print([x.at for x in self.modules])
        print([x.at for x in pcb.modules])
        pcb.net_classes = self.net_classes
        pcb.nets = self.nets
        pcb.vias = self.vias
        pcb.zones = self.zones
        pcb.to_file('project')
        
        
class PCBBuilder:
    def __init__(self,qcode={}):
        self.pcb=PCB()
        self.qcode={}
        for i in range(1,len(qcode)+1):
            for each in qcode[i]:
                print(each[0],each[1])
                if i not in self.qcode.keys():
                    self.qcode[i] = [Module.from_library(each[0],each[1])]
                else:
                    self.qcode[i].append(Module.from_library(each[0],each[1]))
        print("PCB BUILDER QCODE")
        print(qcode)
        self._autoplace_()
        self.pcb._create_zones()
        self.pcb._create_pcb()
    def _find_max_x(self, comp):
        """Return the maximal X size of a component as an interger"""
        max_x = 0
        geo = comp.geometry()
        x = [each for each in geo]
        for each in x:
            if each.start == None and each.end != None:
                y = abs(0-each.end[0])
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
        """Return the maximal X size of a component as an interger"""
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
        
    def _place_component(self, comp, x, y):
        """Places the component at x,y"""
        print("Placing component {} at ({}, {})".format(comp.name, x,y))
        self.pcb._place_component(comp, x, y)
        print("Component {} is at {}".format(comp.name, comp.at))
        
    def _autoplace_(self):
        pos = {
            'X': 0,
            'Y': 0}
        cur_x = 0
        cur_y = 0
        for qubit, gates in self.qcode.items():
            print("Creating qubit {}".format(qubit))
            # Iterate over qubits
            for i in range(len(gates)):
                # Iterate over gates
                # Find maxes
                x, y = self._find_maxes(gates[i])
                # Place component
                cur_x += x
                pos['X'] = cur_x
                if y > cur_y:            
                    cur_y = y
                self._place_component(gates[i], pos['X'], pos['Y'])
            cur_x = 0
            pos['X'] = cur_x
            pos['Y'] += cur_y

if __name__ == '__main__':
    x = PCB()
