import colorsys


def shift_rgb(rgb_color, shift_amount):
    r, g, b, a = [x / 255.0 for x in rgb_color]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + shift_amount) % 1.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = [int(x * 255) for x in (r, g, b)]

    return r, g, b, a


class ColorGradient:
    def __init__(self, color_dict, steps_per_segment=100,
                 use_longest_path=False):
        self.rgb_colors = list(color_dict.keys())
        self.delays = list(color_dict.values())
        self.steps_per_segment = steps_per_segment
        self.use_longest_path = use_longest_path

        # Convert RGB to HSL
        self.hsl_colors = [self._rgb_to_hsl(color) for color in
                           self.rgb_colors]

        self.gradient_index = 0
        self.step_index = 0
        self.current_delay = self.delays[0]
        self.direction = 1  # 1 for forward, -1 for backward

    def _interpolate_hue(self, h1, h2, t):
        if self.use_longest_path:
            if h2 > h1:
                h1 += 1  # Move to the next hue circle (wrap around)
            else:
                h2 += 1
        else:  # Shortest path
            if abs(h2 - h1) > 0.5:
                if h1 > h2:
                    h2 += 1
                else:
                    h1 += 1

        hue = h1 + (h2 - h1) * t
        return hue % 1.0

    def _interpolate(self, start, end, t):
        h1, s1, l1 = start
        h2, s2, l2 = end
        h = self._interpolate_hue(h1, h2, t)
        s = s1 + (s2 - s1) * t
        l = l1 + (l2 - l1) * t
        return h, s, l

    def next_color(self):
        if self.current_delay > 0:
            self.current_delay -= 1
            return self._hsl_to_rgb(self.hsl_colors[self.gradient_index])

        start_hsl = self.hsl_colors[self.gradient_index]
        end_hsl = self.hsl_colors[
            (self.gradient_index + self.direction) % len(self.hsl_colors)]
        t = self.step_index / self.steps_per_segment

        current_hsl = self._interpolate(start_hsl, end_hsl, t)
        current_rgb = self._hsl_to_rgb(current_hsl)

        self.step_index += 1
        if self.step_index > self.steps_per_segment:
            self.step_index = 0
            self.gradient_index = (self.gradient_index + self.direction) % len(
                self.hsl_colors)
            self.current_delay = self.delays[self.gradient_index]

            # Check if we've reached the end of the gradient in either direction
            if self.gradient_index == len(
                    self.hsl_colors) - 1 and self.direction == 1:
                self.direction = -1
            elif self.gradient_index == 0 and self.direction == -1:
                self.direction = 1

        return current_rgb

    def reset(self):
        self.gradient_index = 0
        self.step_index = 0
        self.current_delay = self.delays[0]
        self.direction = 1  # Reset direction to forward

    @staticmethod
    def _rgb_to_hsl(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h, s, l

    @staticmethod
    def _hsl_to_rgb(hsl):
        h, s, l = hsl
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)