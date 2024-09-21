import colorsys


def shift_rgb(rgb_color, shift_amount):
    """Shifts the color in the RGB spectrum by the specified amount.

    :param rgb_color: A tuple of (R, G, B) values where each is in the range
        0-255.
    :param shift_amount: The amount to shift the color in the spectrum.
    :return: A tuple of (R, G, B) representing the shifted color.
    """
    r, g, b, a = [x / 255.0 for x in rgb_color]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + shift_amount) % 1.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = [int(x * 255) for x in (r, g, b)]

    return r, g, b, a


class ColorGradient:
    def __init__(self, color_dict, steps_per_segment=100,
                 use_longest_path=False):
        """Initialize with a dictionary of RGB color tuples and delays."""
        self.rgb_colors = list(color_dict.keys())
        self.delays = list(color_dict.values())
        self.steps_per_segment = steps_per_segment
        self.use_longest_path = use_longest_path

        # Convert RGB to HSL
        self.hsl_colors = [self._rgb_to_hsl(color) for color in self.rgb_colors]

        self.gradient_index = 0
        self.step_index = 0
        self.current_delay = self.delays[0]
        self.direction = 1  # 1 for forward, -1 for backward

    def _interpolate_hue(self, h1, h2, t):
        """Interpolate between two hues, considering shortest or longest path.
        """
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
        """Interpolate between two HSL colors."""
        h1, s1, l1 = start
        h2, s2, l2 = end
        h = self._interpolate_hue(h1, h2, t)
        s = s1 + (s2 - s1) * t
        l = l1 + (l2 - l1) * t
        return h, s, l

    def next_color(self):
        """Generate the next RGB color in the gradient."""
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
        """Reset the gradient to the beginning."""
        self.gradient_index = 0
        self.step_index = 0
        self.current_delay = self.delays[0]
        self.direction = 1  # Reset direction to forward

    @staticmethod
    def _rgb_to_hsl(rgb):
        """Convert an RGB tuple to HSL format."""
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h, s, l

    @staticmethod
    def _hsl_to_rgb(hsl):
        """Convert an HSL tuple back to RGB format."""
        h, s, l = hsl
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)