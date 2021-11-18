color_hex = lambda r, g, b: "#{:0>6}".format(hex(r * 256 * 256 + g * 256 + b)[2:])
to_half_dark = lambda color: tuple(map(lambda x: x // 2, color))
