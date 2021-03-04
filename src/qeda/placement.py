# The placement algorithm
import configparser


class Placement:
    def __init__(self, specs, qcode):
        self.spec_conf = specs
        self.qcode = qcode
        self.conf = get_conf()
        self.import_specs()
        pass

    def get_conf(self):
        """Grabs the config file"""
        conf = configparser.ConfigParser()
        conf.read(self.spec_conf)
        return conf

    def import_specs(self):
        """imports specifications"""
        self.comp_max_x = self.conf['Maxes']['X']
        self.comp_min_x = self.conf['Mins']['X']
        self.comp_max_y = self.conf['Maxes']['Y']
        self.comp_min_y = self.conf['Mins']['Y']
        self.comp_mode_V_top_margin = self.conf['Modes']['V']
        self.comp_mode_H_bottom_margin = self.conf['Modes']['H']
        self.comp_X_spacing = self.conf['Spacing']['X']
        self.comp_y_spacing = self.conf['Spacing']['Y']
        pass

    def placement_algorithm(self):
        """Runs the placement algorithm"""
        pos = {'X': 0, 'Y': 0}  # First component is placed at (0,0)
        cur_x = 0
        cur_y = 0
        # cur_x = Current X, init at 0 or x origin
        # cur_y = CUrrent Y, init at 0 or y origin
        # Place first component at (cur_x, cur_y)
        # Calculate first component length:
        # Max(X) - Min(X) = First Component Length
        # Verify within circuit specs - throw an error if component length is
        # greater than comp_max_x.
        # Calculate the component height of first component
        # Max(Y) - Min(Y)
        # Verify within circuit specs - throw an error if component height is
        # greater than comp_max_y.
        # Calculate V and H points for the first component
        V_Points = {'X': 0, 'Y': 0}
        H_Points = {'X': 0, 'Y': 0}
        # To calculate the X, use the Min(X) and Max(X) of the component found
        # earlier.
        # To calculate the V(Y), take the Max(y) and subtract comp_mode_V_top_margin
        # To calculate the H(Y), take the Min(y) and add comp_mode_H_bottom_margin
        # When placing a single-qubit component:
        # Calculate the V and H points for component to be placed
        # Place component such that it aligns with the top (V) rail.
        # Place(component, x,y):
        # X = max_x + comp_x_spacing
        # Y = max_y - comp_mode_V_top_margin
        # When placing a multi-qubit component like CX:
        # Calculate the V and H points for component to be placed.
        # If component is the "Control" component, place it aligned to the
        # top (V) rail.
        # If "Target" component, place it aligned to the bottom (H) rail.
        pass
