"""Mouse input state for placing ordered control circles."""

import math

from geometry import Circle


class CircleEditor:
    def __init__(self) -> None:
        self.circles: list[Circle] = []
        self.pending_center: tuple[float, float] | None = None

    def add_click(self, x: float, y: float) -> bool:
        """Record a center or complete its circle; return True when completed."""
        if not math.isfinite(x) or not math.isfinite(y):
            raise ValueError("Click coordinates must be finite.")

        if self.pending_center is None:
            self.pending_center = (x, y)
            return False

        center_x, center_y = self.pending_center
        radius = math.hypot(x - center_x, y - center_y)
        if radius == 0:
            return False

        self.circles.append(Circle(center_x, center_y, radius))
        self.pending_center = None
        return True

    def remove_last_circle(self) -> bool:
        """Cancel a pending center, or remove the last completed circle."""
        if self.pending_center is not None:
            self.pending_center = None
            return False
        if not self.circles:
            return False
        self.circles.pop()
        return True

    def resize_circle(self, index: int, radius: float) -> None:
        """Replace one circle with the requested positive radius."""
        circle = self.circles[index]
        self.circles[index] = Circle(
            circle.center_x,
            circle.center_y,
            radius,
        )

    def move_circle(
        self, index: int, center_x: float, center_y: float
    ) -> None:
        """Replace one circle at a new center while preserving its radius."""
        circle = self.circles[index]
        self.circles[index] = Circle(
            center_x,
            center_y,
            circle.radius,
        )
