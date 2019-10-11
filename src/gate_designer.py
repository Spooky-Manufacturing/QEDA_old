class GateDesigner():
    def __init__(self, name, library, ref=None):
        self.name = name
        self.library = library
        self.component_description = {}
        self.fn = []
        self.arc = []
        self.circ = []
        self.poly = []
        self.rect = []
        self.text = []
        self.pins = []
        if ref == None:
            self.ref = 'U'
        else:
            self.ref = ref

        self._set_def_keys(self.name, self.ref)

        
    def _set_def_keys(self, name, ref=None, offset=0, pinnumber=True,
                      pinname=True, ucount=1, locked=False, flag=False):
        """Sets the component Definition keys
        From Parent Component:
        _DEF_KEYS = ['name','reference','unused','text_offset','draw_pinnumber',
                     'draw_pinname','unit_count','units_locked','option_flag']

        name = name (str)
        ref = reference characters (str)
            default: 'U'
        offset = text offset (int)
            default: 0
        pinnumber = draw pin number (boolean)
            default: True
        pinname = draw pin name (boolean)
            default: True
        ucount = unit count (integer)
            default: 1
        locked = Units locked (boolean)
            default: False
        flag = option flag (boolean)
            default: False
        """
        if ref == None:
            self.ref = 'U'
        else:
            self.ref = ref
        
        self.defs = {
            'name': name,
            'ref': self.ref,
            'offset': offset,
            'pinnumber': pinnumber,
            'pinname': pinname,
            'ucount': ucount,
            'locked': locked,
            'flag': flag
            }
        pass

    def _set_f0_keys(self, posx, posy, vis,
                     hjust, vjust, size=50, orient='H'):
        """Sets the F0 keys.

        From the parent component:
            _F0_KEYS = ['reference','posx','posy','text_size','text_orient',
            'visibility', 'htext_justify','vtext_justify']

        posx = Position x (int)
        posy = Position y (int)
        size = Text size (int)
            default: 50
        orient = Orientation (str)
            options: H(orizontal) | V(ertical)
            default: 'H'
        vis = Visibility (str)
            options: V(isible) | I(nvisible)
            default: 'V'
        hjust = Horizontal Text Justify (str)
        vjust = Vertical Text Justify (str) 
        """
        self.f0 = {
            'ref': self.defs['ref'],
            'posx': posx,
            'posy': posy,
            'size': size,
            'orient': orient,
            'vis': vis,
            'hjust': hjust,
            'vjust': vjust
            }

    def _set_fn_keys(n=1, posx=0, posy=0, size=50,
                     orient='H', vis='V', hjus='R', vjus='C', fieldname=None):
        """Sets the F(n) key names
    _FN_KEYS = ['name','posx','posy','text_size','text_orient','visibility',
                'htext_justify','vtext_justify','fieldname']
                """
        self.fn.append({
            'n': n,
            'name': self.name,
            'posx': posx,
            'posy': posy,
            'size': size,
            'orient': orient,
            'vis': vis,
            'hjus': hjus,
            'vjus': vjus,
            'fieldname': fieldname
        })

    def _add_arc_keys(posx, posy, radius, start_angle, end_angle, unit,
                      convert, thickness, fill, startx, starty, endx, endy):
        """Adds arc key definitions to arc list.
                
    _ARC_KEYS = ['posx','posy','radius','start_angle','end_angle','unit',
                 'convert','thickness','fill','startx','starty','endx','endy']
        """
        self.arc.append({
            'posx': posx,
            'posy': posy,
            'radius': radius,
            'start_angle': start_angle,
            'end_angle': end_angle,
            'unit': unit,
            'convert': convert,
            'thickness': thickness,
            'fill': fill,
            'startx': startx,
            'starty': starty,
            'endx': endx,
            'endy': endy
        })

    def _add_circle_keys(posx, posy, radius, unit, convert, thickness, fill):
        """Adds circle keys to circles list

        _CIRCLE_KEYS = ['posx','posy','radius','unit','convert','thickness',
        'fill']
        """
        self.circle.append({
            'posx': posx,
            'posy': posy,
            'radius': radius,
            'unit': unit,
            'convert': convert,
            'thickness': thickness,
            'fill': fill
        })

    def _add_poly_keys(point_count, unit, convert, thickness, points, fill):
        """Adds poly keys to poly list
    
        _POLY_KEYS = ['point_count','unit','convert','thickness',
        'points','fill']

        """
        self.poly.append({
            'point_count': point_count,
            'unit': unit,
            'convert': convert,
            'thickness': thickness,
            'points': points,
            'fill': fill
        })

    def _add_rect_keys(startx, starty, endx, endy, unit, convert, thickness, fill):
        """Adds rect keys to rect list

        _RECT_KEYS = ['startx','starty','endx','endy','unit','convert',
        'thickness', 'fill']

        """
        self.rect.append({
            'startx': startx,
            'starty': starty,
            'endx': endx,
            'endy': endy,
            'unit': unit,
            'convert': convert,
            'thickness': thickness,
            'fill': fill
        })

    def _add_text_keys(d, posx, posy, tsize, ttype, unit, convert, text,
                       italic, bold, hjus, vjus):
        """Adds text keys to text list

         _TEXT_KEYS = ['direction','posx','posy','text_size','text_type',
         'unit', convert','text', 'italic', 'bold', 'hjustify', 'vjustify']


        """
        self.text.append({
            'direction': d,
            'posx': posx,
            'posy': posy,
            'text_size': tsize,
            'text_type': ttype,
            'unit': unit,
            'convert': convert,
            'text': text,
            'italic': italic,
            'bold': bold,
            'hjustify': hjus,
            'vjustify': vjus
        })

    def _add_pin_keys(name, num, posx, posy, length, d, nsize, tsize,
                      unit, convert, etype, ptype):
        """Adds pin keys to pin list
        
        _PIN_KEYS = ['name','num','posx','posy','length','direction',
                 'num_text_size','name_text_size','unit','convert',
                 'electrical_type','pin_type']
        """
        self.pins.append({
            'name': name,
            'num': num,
            'posx': posx,
            'posy': posy,
            'length': length,
            'direction': d,
            'num_text_size': nsize,
            'name_text_size': tsize,
            'unit': unit,
            'convert': convert,
            'electrical_type': etype,
            'pin_type': ptype
        })
        """
    _DRAW_KEYS = {'A':_ARC_KEYS, 'C':_CIRCLE_KEYS, 'P':_POLY_KEYS,
                  'S':_RECT_KEYS, 'T':_TEXT_KEYS, 'X':_PIN_KEYS}
        """


x = GateDesigner('test', 'lib', 'ref')
print(x, x.defs)
