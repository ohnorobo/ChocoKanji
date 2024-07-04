from svgpathtools import Line, CubicBezier, QuadraticBezier, Arc
from pprint import pprint


# This is a modified version of the d function from svgpathtools.path.Path.d
# It allows rounding the float outputs
def alternative_d(self, useSandT=False, use_closed_attrib=False, rel=False, round_decimal_places=None):
    """Returns a path d-string for the path object.
    For an explanation of useSandT and use_closed_attrib, see the
    compatibility notes in the README.
    round_decimal_places sets the number of decimal places to output."""
    if len(self) == 0:
        return ''
    if use_closed_attrib:
        self_closed = self.iscontinuous() and self.isclosed()
        if self_closed:
            segments = self[:-1]
        else:
            segments = self[:]
    else:
        self_closed = False
        segments = self[:]

    current_pos = None
    parts = []
    previous_segment = None
    end = self[-1].end

    # Format string to round floating point numbers to a specific number of decimal places.
    if round_decimal_places:
        f = f'.{round_decimal_places}f'
    else:
        f = 'g'

    for segment in segments:
        seg_start = segment.start
        # If the start of this segment does not coincide with the end of
        # the last segment or if this segment is actually the close point
        # of a closed path, then we should start a new subpath here.
        if current_pos != seg_start or \
                (self_closed and seg_start == end and use_closed_attrib):
            if rel:
                _seg_start = seg_start - current_pos if current_pos is not None else seg_start
            else:
                _seg_start = seg_start
            a0, a1 = (_seg_start.real, _seg_start.imag)
            parts.append(f'M {a0:g},{a1:g}')

        if isinstance(segment, Line):
            if rel:
                _seg_end = segment.end - seg_start
            else:
                _seg_end = segment.end
            a0, a1 = (_seg_end.real, _seg_end.imag)
            parts.append(f'L {a0:g},{a1:g}')
        elif isinstance(segment, CubicBezier):
            if useSandT and segment.is_smooth_from(previous_segment,
                                                    warning_on=False):
                if rel:
                    _seg_control2 = segment.control2 - seg_start
                    _seg_end = segment.end - seg_start
                else:
                    _seg_control2 = segment.control2
                    _seg_end = segment.end
                a, b, c, d = (_seg_control2.real, _seg_control2.imag,
                              _seg_end.real, _seg_end.imag)
                parts.append(f'S {a0:{f}},{a1:{f}} {b0:{f}},{b1:{f}}')
            else:
                if rel:
                    _seg_control1 = segment.control1 - seg_start
                    _seg_control2 = segment.control2 - seg_start
                    _seg_end = segment.end - seg_start
                else:
                    _seg_control1 = segment.control1
                    _seg_control2 = segment.control2
                    _seg_end = segment.end
                a0, a1, b0, b1, c0, c1 = (_seg_control1.real, _seg_control1.imag,
                                          _seg_control2.real, _seg_control2.imag,
                                          _seg_end.real, _seg_end.imag)
                parts.append(f'C {a0:{f}},{a1:{f}} {b0:{f}},{b1:{f}} {c0:{f}},{c1:{f}}')
        elif isinstance(segment, QuadraticBezier):
            if useSandT and segment.is_smooth_from(previous_segment,
                                                    warning_on=False):
                if rel:
                    _seg_end = segment.end - seg_start
                else:
                    _seg_end = segment.end
                a0, a1 = (_seg_end.real, _seg_end.imag)
                parts.append(f'T {a0:{f}},{a1:{f}}')
            else:
                if rel:
                    _seg_control = segment.control - seg_start
                    _seg_end = segment.end - seg_start
                else:
                    _seg_control = segment.control
                    _seg_end = segment.end
                a0, a1, b0, b1 = (_seg_control.real, _seg_control.imag,
                              _seg_end.real, _seg_end.imag)
                parts.append(f'Q {a0:{f}},{a1:{f}} {b0:{f}},{b1:{f}}')

        elif isinstance(segment, Arc):
            if rel:
                _seg_end = segment.end - seg_start
            else:
                _seg_end = segment.end
            a0, a1, b, c, d, e0, e1 = (segment.radius.real, segment.radius.imag,
                                       segment.rotation,int(segment.large_arc),
                                       int(segment.sweep),_seg_end.real, _seg_end.imag)
            parts.append(f'A {a0:{f}},{a1:{f}} {b:{f}} {c:d},{d:d} {e0:{f}},{e1:{f}}')
        current_pos = segment.end
        previous_segment = segment

    if self_closed:
        parts.append('Z')

    s = ' '.join(parts)
    return s if not rel else s.lower()