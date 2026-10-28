"""Geometry for variable-radius Disk-Bezier curves."""

from dataclasses import dataclass
import math
from typing import Sequence


@dataclass(frozen=True)
class Circle:
    center_x: float
    center_y: float
    radius: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.center_x) or not math.isfinite(self.center_y):
            raise ValueError("Circle center coordinates must be finite.")
        if not math.isfinite(self.radius) or self.radius <= 0:
            raise ValueError("Circle radius must be finite and positive.")


class SkinningError(ValueError):
    """Raised when a safe circle-skinning contour cannot be constructed."""


@dataclass(frozen=True)
class HermiteSegment:
    start: tuple[float, float]
    end: tuple[float, float]
    tangent_start: tuple[float, float]
    tangent_end: tuple[float, float]

    def evaluate(self, t: float) -> tuple[float, float]:
        if not math.isfinite(t) or not 0 <= t <= 1:
            raise ValueError("Hermite parameter t must be between 0 and 1.")

        t2 = t * t
        t3 = t2 * t
        h00 = 2 * t3 - 3 * t2 + 1
        h01 = -2 * t3 + 3 * t2
        h10 = t3 - 2 * t2 + t
        h11 = t3 - t2
        return tuple(
            h00 * self.start[axis]
            + h01 * self.end[axis]
            + h10 * self.tangent_start[axis]
            + h11 * self.tangent_end[axis]
            for axis in range(2)
        )


def _external_tangents(
    first: Circle, second: Circle
) -> tuple[HermiteSegment, HermiteSegment]:
    dx = second.center_x - first.center_x
    dy = second.center_y - first.center_y
    distance = math.hypot(dx, dy)
    if distance <= abs(first.radius - second.radius) + 1e-9:
        raise SkinningError(
            "A szomszédos körök között nem létezik külső közös érintő."
        )

    unit_x = dx / distance
    unit_y = dy / distance
    perpendicular_x = -unit_y
    perpendicular_y = unit_x
    along = (first.radius - second.radius) / distance
    across = math.sqrt(max(0.0, 1 - along * along))
    segments = []
    for side in (1, -1):
        normal_x = along * unit_x + side * across * perpendicular_x
        normal_y = along * unit_y + side * across * perpendicular_y
        start = (
            first.center_x + first.radius * normal_x,
            first.center_y + first.radius * normal_y,
        )
        end = (
            second.center_x + second.radius * normal_x,
            second.center_y + second.radius * normal_y,
        )
        tangent = (end[0] - start[0], end[1] - start[1])
        segments.append(HermiteSegment(start, end, tangent, tangent))
    return segments[0], segments[1]


def _transition(
    start: tuple[float, float],
    end: tuple[float, float],
    tangent_start: tuple[float, float],
    tangent_end: tuple[float, float],
) -> HermiteSegment | None:
    distance = math.hypot(end[0] - start[0], end[1] - start[1])
    if distance <= 1e-9:
        return None

    start_length = math.hypot(*tangent_start)
    end_length = math.hypot(*tangent_end)
    if start_length <= 1e-9 or end_length <= 1e-9:
        raise SkinningError("A körérintési érintő iránya nem határozható meg.")
    start_scale = distance / start_length
    end_scale = distance / end_length
    return HermiteSegment(
        start,
        end,
        (tangent_start[0] * start_scale, tangent_start[1] * start_scale),
        (tangent_end[0] * end_scale, tangent_end[1] * end_scale),
    )


def _validate_centerline(circles: Sequence[Circle]) -> None:
    for first, second in zip(circles, circles[1:]):
        if math.hypot(
            second.center_x - first.center_x,
            second.center_y - first.center_y,
        ) <= 1e-9:
            raise SkinningError("Két szomszédos kör középpontja egybeesik.")

    for first, middle, last in zip(circles, circles[1:], circles[2:]):
        first_x = middle.center_x - first.center_x
        first_y = middle.center_y - first.center_y
        second_x = last.center_x - middle.center_x
        second_y = last.center_y - middle.center_y
        first_length = math.hypot(first_x, first_y)
        second_length = math.hypot(second_x, second_y)
        cross = first_x * second_y - first_y * second_x
        if abs(cross) <= 1e-8 * first_length * second_length:
            raise SkinningError(
                "A három egymást követő kör közel kollineáris; "
                "a bőrözés nem stabil."
            )
        direction_dot = (
            first_x * second_x + first_y * second_y
        ) / (first_length * second_length)
        if direction_dot <= -0.95:
            raise SkinningError("A körök sorrendje éles irányváltást tartalmaz.")


def _point_inside_other_circle(
    point: tuple[float, float], owner: Circle, circles: Sequence[Circle]
) -> bool:
    for circle in circles:
        if circle is owner:
            continue
        distance = math.hypot(
            point[0] - circle.center_x,
            point[1] - circle.center_y,
        )
        if distance < circle.radius - 1e-8:
            return True
    return False


def _orientation(
    first: tuple[float, float],
    second: tuple[float, float],
    third: tuple[float, float],
) -> float:
    return (second[0] - first[0]) * (third[1] - first[1]) - (
        second[1] - first[1]
    ) * (third[0] - first[0])


def _segments_intersect(
    first_start: tuple[float, float],
    first_end: tuple[float, float],
    second_start: tuple[float, float],
    second_end: tuple[float, float],
) -> bool:
    tolerance = 1e-9
    first_a = _orientation(first_start, first_end, second_start)
    first_b = _orientation(first_start, first_end, second_end)
    second_a = _orientation(second_start, second_end, first_start)
    second_b = _orientation(second_start, second_end, first_end)

    def on_segment(
        start: tuple[float, float],
        end: tuple[float, float],
        point: tuple[float, float],
    ) -> bool:
        return (
            min(start[0], end[0]) - tolerance
            <= point[0]
            <= max(start[0], end[0]) + tolerance
            and min(start[1], end[1]) - tolerance
            <= point[1]
            <= max(start[1], end[1]) + tolerance
        )

    if first_a * first_b < -tolerance and second_a * second_b < -tolerance:
        return True
    return (
        abs(first_a) <= tolerance and on_segment(first_start, first_end, second_start)
    ) or (
        abs(first_b) <= tolerance and on_segment(first_start, first_end, second_end)
    ) or (
        abs(second_a) <= tolerance
        and on_segment(second_start, second_end, first_start)
    ) or (
        abs(second_b) <= tolerance
        and on_segment(second_start, second_end, first_end)
    )


def _sample_segments(
    segments: Sequence[HermiteSegment], steps_per_segment: int
) -> list[tuple[float, float]]:
    points = []
    for segment in segments:
        for step in range(steps_per_segment + 1):
            if points and step == 0:
                continue
            points.append(segment.evaluate(step / steps_per_segment))
    return points


def _validate_simple_contour(points: Sequence[tuple[float, float]]) -> None:
    edge_count = len(points) - 1
    for first_index in range(edge_count):
        for second_index in range(first_index + 2, edge_count):
            if first_index == 0 and second_index == edge_count - 1:
                continue
            if _segments_intersect(
                points[first_index],
                points[first_index + 1],
                points[second_index],
                points[second_index + 1],
            ):
                raise SkinningError(
                    "A bőrözési kontúr önmetsző; válassz más körkonfigurációt."
                )


def build_skinning_segments(
    circles: Sequence[Circle],
) -> list[HermiteSegment]:
    """Build a closed, tangent Hermite contour around an ordered circle chain."""
    if len(circles) < 2:
        raise SkinningError("A bőrözéshez legalább két kör szükséges.")
    _validate_centerline(circles)

    if len(circles) == 2:
        upper_bridge, lower_bridge = _external_tangents(circles[0], circles[1])
        upper = [upper_bridge]
        lower = [lower_bridge]
    else:
        directions = []
        for first, second in zip(circles, circles[1:]):
            dx = second.center_x - first.center_x
            dy = second.center_y - first.center_y
            distance = math.hypot(dx, dy)
            directions.append((dx / distance, dy / distance))

        centerline_tangents = [directions[0]]
        for previous, following in zip(directions, directions[1:]):
            tangent_x = previous[0] + following[0]
            tangent_y = previous[1] + following[1]
            tangent_length = math.hypot(tangent_x, tangent_y)
            if tangent_length <= 1e-8:
                raise SkinningError(
                    "A körök sorrendje éles irányváltást tartalmaz."
                )
            centerline_tangents.append(
                (tangent_x / tangent_length, tangent_y / tangent_length)
            )
        centerline_tangents.append(directions[-1])

        upper_points = []
        lower_points = []
        for circle, tangent in zip(circles, centerline_tangents):
            normal = (-tangent[1], tangent[0])
            upper_points.append(
                (
                    circle.center_x + circle.radius * normal[0],
                    circle.center_y + circle.radius * normal[1],
                )
            )
            lower_points.append(
                (
                    circle.center_x - circle.radius * normal[0],
                    circle.center_y - circle.radius * normal[1],
                )
            )

        upper = []
        lower = []
        for index, (first, second) in enumerate(zip(circles, circles[1:])):
            distance = math.hypot(
                second.center_x - first.center_x,
                second.center_y - first.center_y,
            )
            upper.append(
                HermiteSegment(
                    upper_points[index],
                    upper_points[index + 1],
                    (
                        centerline_tangents[index][0] * distance,
                        centerline_tangents[index][1] * distance,
                    ),
                    (
                        centerline_tangents[index + 1][0] * distance,
                        centerline_tangents[index + 1][1] * distance,
                    ),
                )
            )
            lower.append(
                HermiteSegment(
                    lower_points[index],
                    lower_points[index + 1],
                    (
                        centerline_tangents[index][0] * distance,
                        centerline_tangents[index][1] * distance,
                    ),
                    (
                        centerline_tangents[index + 1][0] * distance,
                        centerline_tangents[index + 1][1] * distance,
                    ),
                )
            )

    tangent_pairs = list(zip(upper, lower))
    for pair_index, pair in enumerate(tangent_pairs):
        first_circle = circles[pair_index]
        second_circle = circles[pair_index + 1]
        for segment in pair:
            if _point_inside_other_circle(segment.start, first_circle, circles):
                raise SkinningError(
                    "Egy érintési pont másik kör belsejébe esik."
                )
            if _point_inside_other_circle(segment.end, second_circle, circles):
                raise SkinningError(
                    "Egy érintési pont másik kör belsejébe esik."
                )

    segments: list[HermiteSegment] = []

    for bridge in upper:
        segments.append(bridge)

    end_cap = _transition(
        upper[-1].end,
        lower[-1].end,
        upper[-1].tangent_end,
        (-lower[-1].tangent_end[0], -lower[-1].tangent_end[1]),
    )
    if end_cap is not None:
        segments.append(end_cap)

    for index in range(len(lower) - 1, -1, -1):
        bridge = lower[index]
        reversed_bridge = HermiteSegment(
            bridge.end,
            bridge.start,
            (-bridge.tangent_end[0], -bridge.tangent_end[1]),
            (-bridge.tangent_start[0], -bridge.tangent_start[1]),
        )
        segments.append(reversed_bridge)

    start_cap = _transition(
        lower[0].start,
        upper[0].start,
        (-lower[0].tangent_start[0], -lower[0].tangent_start[1]),
        upper[0].tangent_start,
    )
    if start_cap is not None:
        segments.append(start_cap)

    contour = _sample_segments(segments, steps_per_segment=12)
    if not contour or contour[0] != contour[-1]:
        raise SkinningError("A bőrözési kontúr nem zárható biztonságosan.")
    _validate_simple_contour(contour)
    return segments


def sample_skinning(
    circles: Sequence[Circle], steps_per_segment: int = 16
) -> list[tuple[float, float]]:
    """Sample a validated circle-skinning contour for rendering."""
    if steps_per_segment < 2:
        raise ValueError("At least two steps per segment are required.")
    segments = build_skinning_segments(circles)
    points = _sample_segments(segments, steps_per_segment)
    _validate_simple_contour(points)
    return points


def evaluate_disk_bezier(circles: Sequence[Circle], t: float) -> Circle:
    """Evaluate the Bezier center and radius using the same parameter weights."""
    if not circles:
        raise ValueError("At least one control circle is required.")
    if not math.isfinite(t) or not 0 <= t <= 1:
        raise ValueError("Curve parameter t must be between 0 and 1.")

    points = [
        [circle.center_x, circle.center_y, circle.radius]
        for circle in circles
    ]

    for level in range(1, len(points)):
        for index in range(len(points) - level):
            for axis in range(3):
                points[index][axis] = (
                    (1 - t) * points[index][axis]
                    + t * points[index + 1][axis]
                )

    center_x, center_y, radius = points[0]
    return Circle(center_x, center_y, radius)


def sample_disk_bezier(
    circles: Sequence[Circle], steps: int = 120
) -> list[Circle]:
    """Return disks along the curve for drawing their filled union."""
    if len(circles) < 2:
        return []
    if steps < 1:
        raise ValueError("At least one sampling step is required.")

    return [
        evaluate_disk_bezier(circles, step / steps)
        for step in range(steps + 1)
    ]


def disk_bridge(
    first: Circle, second: Circle
) -> tuple[tuple[float, float], ...] | None:
    """Return a quadrilateral joining two disks along their common tangents."""
    dx = second.center_x - first.center_x
    dy = second.center_y - first.center_y
    distance = math.hypot(dx, dy)
    radius_difference = first.radius - second.radius

    if distance <= abs(radius_difference):
        return None

    unit_x = dx / distance
    unit_y = dy / distance
    tangent_x = radius_difference / distance
    tangent_y = math.sqrt(1 - tangent_x * tangent_x)

    points = []
    for side in (-1, 1):
        normal_x = tangent_x * unit_x - side * tangent_y * unit_y
        normal_y = tangent_x * unit_y + side * tangent_y * unit_x
        points.append(
            (
                first.center_x + first.radius * normal_x,
                first.center_y + first.radius * normal_y,
            )
        )
        points.append(
            (
                second.center_x + second.radius * normal_x,
                second.center_y + second.radius * normal_y,
            )
        )

    return points[0], points[1], points[3], points[2]
