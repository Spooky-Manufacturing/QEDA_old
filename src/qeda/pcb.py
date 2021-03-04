#!/usr/bin/python3
import configparser
import importlib
from math import ceil
from numpy import array


from pykicad.pcb import Net, Via, Segment, Setup, Layer, NetClass, Pcb
from pykicad.module import Module

config = configparser.ConfigParser()
config.read('conf/pcb.conf')


class PCB:
    def __init__(self, verbose=False, title='Quantum PCB Output', comment1='', s='DEFAULT'):
        # Setup verbosity
        self.verbose = str(verbose).lower()
        self.setup_verbosity()
        # Get configurations
        V("Getting configurations")
        V(config[s])
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
        self.num_layers = int(config[s]['layers'])
        self.layers = []
        self.page_type = [int(x) for x in config[s]['page_type'].split(',')]
        self.trace_width = config[s]['trace_width']
        self.coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
        # PCB Info
        V("PCB INFO:")
        self.title = title
        self.comment1 = comment1
        grid_orig = [int(x / 2) for x in self.page_type]
        V("Title: {}\nComment1: {}\nGrid Origin: {}".format(self.title, self.comment1, grid_orig))
        self.setup = Setup(grid_origin=grid_orig)

    def setup_verbosity(self):
        global V
        V = getattr(importlib.import_module("qeda.verbose", self.verbose),
                    self.verbose)
        V("Verbosity setup on PCB prototype complete")

    def _connect_pad(self, comp, pad, net):
        """Connects components pads electrically
            comp - Module, component
            pad - integer, pad number
            net - Net, which net to connect to
        """
        V("Connecting pad {} on component {} to net {}".format(pad, comp, net))
        # r1.pads[0].net = vi
        comp.pads[pad].net = self.nets[net]

    def _place_component(self, comp, x_pos, y_pos):
        """Places component comp at position x,y and adds it to PCB list"""
        V("Placing component at cooridinate ({},{})".format(x_pos, y_pos))
        comp.at = [x_pos, y_pos]
        self.modules.append(comp)

    def _final_compute(self, comp):
        """Computes the positions of vias for quantum optical components"""
        V("Computing final positions of vias for optical components")
        start = array(comp.pads[1].at) + array(comp.at)
        end = array(comp.pads[0].at) + array(comp.at)
        pos = start + (end - start) / 2
        V("Start: {}\nEnd: {}\nPosition: {}".format(start, end, pos))
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
        V("Computing positions of vias for components.")
        start = array(comp1.pads[pads[0]].at) + array(comp1.at)
        end = array(comp2.pads[pads[1]].at) + array(comp2.at)
        pos = start + (end - start) / 2
        V("Start: {}\nEnd: {}\nPosition: {}".format(start, end, pos))

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
        V("Creating Via")
        if via_size is None:
            via_size = self.via_size
        if drill_size is None:
            drill_size = self.drill_size
        V("Position: {}\nNet: {}\nVia Size: {}\nDrill Size: {}".format(pos, net, via_size, drill_size))
        self.vias.append(Via(at=pos.tolist(), size=via_size, drill=drill_size, net=net))

    def _create_segment(self, start, end, net):
        """Creates segments and appends to the list of segments
        net = connected net

        values from self._compute_positions():
        start
        end
        """
        V("Creating Segment.\nStart: {}\nEnd: {}\nNet: {}".format(start, end, net))
        self.segments.append(Segment(
            start=start.tolist(),
            end=end.tolist(),
            net=net.code))

    def _create_zones(self):
        """Creates the zones (layers) of the PCB"""
        # coords = self.coords
        # Unneeded?
        # gndplane_top = Zone(net_name='GND', layer='F.Cu',
        #                    polygon=coords, clearance=self.clearance)
        V("Creating Zones.")
        self.layers = [
            Layer('F.Cu'),
            Layer('Inner1.Cu'),
            Layer('Inner2.Cu'),
            Layer('B.Cu'),
            Layer('Edge.Cuts', type='user')
        ]
        V(self.layers)
        for layer in ['Mask', 'Paste', 'SilkS', 'CrtYd', 'Fab']:
            for side in ['B', 'F']:
                V("Adding layer {} to side {}".format(layer, side))
                self.layers.append(Layer('%s.%s' % (side, layer), type='user'))
        self.net_classes = NetClass('default',
                                    trace_width=self.trace_width,
                                    nets=['VI', 'VO', 'GND'])

    def _create_pcb(self):
        V('Making PCB')
        pcb = Pcb()
        pcb.title = self.title
        V("Title set to {}".format(pcb.title))
        pcb.comment1 = self.comment1
        pcb.page_type = self.page_type
        pcb.num_nets = self.num_nets
        V('setup', self.setup)
        pcb.setup = self.setup
        V('layers', self.layers)
        pcb.layers = self.layers
        pcb.modules = self.modules
        V(pcb.modules)
        V("Setting net classes")
        pcb.net_classes = self.net_classes
        V("Setting nets")
        pcb.nets = self.nets
        V("Setting vias")
        pcb.vias = self.vias
        V("Setting zones")
        pcb.zones = self.zones
        V("Writing to file")
        pcb.to_file('project')


class PCBBuilder:
    def __init__(self, qcode={}, verbose=False):
        self.verbose = str(verbose).lower()
        self.setup_verbosity()
        self.pcb = PCB(self.verbose)
        self.qcode = {}
        self.oldq = qcode
        for i in range(1, len(qcode) + 1):
            self.qcode[i] = []
            self.qcode[i].append(Module.from_file(qcode[i][0][0] + 'Photon-Source.kicad_mod'))
            for each in qcode[i]:
                self.qcode[i].append(Module.from_file(each[0] + each[1] + '.kicad_mod'))
        V("PCB BUILDER QCODE")
        self._autoplace_()
        self.pcb._create_zones()
        self.pcb._create_pcb()

    def setup_verbosity(self):
        global V
        V = getattr(importlib.import_module("qeda.verbose", self.verbose), self.verbose)
        V("Verbosity setup on PCBBuilder complete")

    def _find_max_x(self, comp):
        """Return the maximal X size of a component as an interger"""
        max_x = 0
        geo = comp.geometry()
        x = [each for each in geo]
        for each in x:
            if each.start is None and each.end is not None:
                y = abs(0 - each.end[0])
            elif each.end is None and each.start is not None:
                y = abs(each.start)
            elif each.start == each.end is None:
                pass
            else:
                y = abs(each.start[0] - each.end[0])
                if y > max_x:
                    max_x = y
        return ceil(max_x)

    def _find_max_y(self, comp):
        """Return the maximal X size of a component as an interger"""
        max_y = 0
        geo = comp.geometry()
        x = [each for each in geo]
        for each in x:
            if each.start is None and each.end is not None:
                y = abs(0 - each.end)
            if each.end is None and each.start is not None:
                y = abs(each.start)
            elif each.start == each.end is None:
                pass
            else:
                y = abs(each.start[1] - each.end[1])
                if y > max_y:
                    max_y = y
        return ceil(max_y)

    def _find_maxes(self, comp):
        """Returns the maximal x and y value of a component (starting at 0,0)"""
        x = self._find_max_x(comp)
        y = self._find_max_y(comp)
        return int(x), int(y)

    def _place_component(self, comp, x, y):
        """Places the component at x,y"""
        V("Placing component {} at ({}, {})".format(comp.name, x, y))
        self.pcb._place_component(comp, x, y)
        V("Component {} is at {}".format(comp.name, comp.at))

    def _autoplace_(self):
        V("Running auto-placer")
        pos = {
            'X': 0,
            'Y': 0}
        cur_x = 0
        cur_y = 0
        V("Mapping Qubits")
        for qubit, gates in self.qcode.items():
            V("Creating qubit {}".format(qubit))
            # Iterate over qubits
            for i in range(len(gates)):
                # Iterate over gates
                V("Processing component {} of qubit {}".format(i, qubit))
                # Find maxes
                V("Finding maximum geometry of component.")
                x, y = self._find_maxes(gates[i])
                # Place component
                V("Placing component.")
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
