from numpy import array
from pykicad.pcb import *
from pykicad.module import *

# Define nets
vi, vo, gnd = Net('VI'), Net('VO'), Net('GND')

# Load footprints
r1 = Module.from_library('Resistors_SMD', 'R_0805')
r2 = Module.from_library('Resistors_SMD', 'R_0805')

# Connect pads
"""
r1.pads[0].net = vi
r1.pads[1].net = vo
r2.pads[0].net = vo
r2.pads[1].net = gnd
"""
# Place components
r1.at = [0, 0]
r2.at = [5, 0]

# Compute positions
start = array(r1.pads[1].at) + array(r1.at)
end = array(r2.pads[0].at) + array(r2.at)
pos = start + (end - start) / 2


# Create vias
v1 = Via(at=pos.tolist(), size=.8, drill=.6, net=vo.code)

# Create segments
s1 = Segment(start=start.tolist(), end=pos.tolist(), net=vo.code)
s2 = Segment(start=pos.tolist(), end=end.tolist(), net=vo.code)

# Create zones
coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
gndplane_top = Zone(net_name='GND', layer='F.Cu', polygon=coords, clearance=0.3)


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

nc1 = NetClass('default', trace_width=1, nets=['VI', 'VO', 'GND'])

# Create PCB
pcb = Pcb()
pcb.title = 'A title'
pcb.comment1 = 'Comment 1'
pcb.page_type = [20, 20]
pcb.num_nets = 5
pcb.setup = Setup(grid_origin=[10, 10])
pcb.layers = layers
pcb.modules += [r1, r2]
print([x.at for x in pcb.modules])
pcb.net_classes += [nc1]
pcb.nets += [vi, vo, gnd]
pcb.segments += [s1, s2]
pcb.vias += [v1]
pcb.zones += [gndplane_top]
pcb.to_file('project2')
