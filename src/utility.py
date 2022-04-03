color_hex = lambda r, g, b: "#{:0>6}".format(hex(r * 256 * 256 + g * 256 + b)[2:])
to_half_dark = lambda color: tuple(map(lambda x: x // 2, color))
same_pos = lambda x1, y1, x2, y2: x1 == x2 and y1 == y2
