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
    radius_difference = abs(first.radius - second.radius)
    coordinate_scale = max(
        abs(first.center_x),
        abs(first.center_y),
        abs(second.center_x),
        abs(second.center_y),
        distance,
        first.radius,
        second.radius,
    )
    tolerance = 8 * math.ulp(coordinate_scale)
    if distance <= radius_difference + tolerance:
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


def _circle_arc_segments(
    circle: Circle,
    start: tuple[float, float],
    end: tuple[float, float],
) -> list[HermiteSegment]:
    start_angle = math.atan2(start[1] - circle.center_y, start[0] - circle.center_x)
    end_angle = math.atan2(end[1] - circle.center_y, end[0] - circle.center_x)
    sweep = -((start_angle - end_angle) % (2 * math.pi))
    if sweep == 0:
        return []

    segment_count = max(1, math.ceil(abs(sweep) / (math.pi / 2)))
    angle_step = sweep / segment_count
    tangent_scale = 4 * circle.radius * math.tan(abs(angle_step) / 4)
    segments = []

    for index in range(segment_count):
        first_angle = start_angle + angle_step * index
        second_angle = start_angle + angle_step * (index + 1)
        first_point = (
            start
            if index == 0
            else (
                circle.center_x + circle.radius * math.cos(first_angle),
                circle.center_y + circle.radius * math.sin(first_angle),
            )
        )
        second_point = (
            end
            if index == segment_count - 1
            else (
                circle.center_x + circle.radius * math.cos(second_angle),
                circle.center_y + circle.radius * math.sin(second_angle),
            )
        )
        segments.append(
            HermiteSegment(
                first_point,
                second_point,
                (
                    tangent_scale * math.sin(first_angle),
                    -tangent_scale * math.cos(first_angle),
                ),
                (
                    tangent_scale * math.sin(second_angle),
                    -tangent_scale * math.cos(second_angle),
                ),
            )
        )

    return segments


def _validate_centerline(circles: Sequence[Circle]) -> None:
    directions = []
    for first, second in zip(circles, circles[1:]):
        dx = second.center_x - first.center_x
        dy = second.center_y - first.center_y
        distance = math.hypot(dx, dy)
        if not math.isfinite(distance):
            raise SkinningError(
                "A körök távolsága kívül esik a számítható tartományon."
            )
        if distance == 0:
            raise SkinningError("Két szomszédos kör középpontja egybeesik.")
        directions.append((dx / distance, dy / distance))

    for first_direction, second_direction in zip(directions, directions[1:]):
        cross = (
            first_direction[0] * second_direction[1]
            - first_direction[1] * second_direction[0]
        )
        dot = (
            first_direction[0] * second_direction[0]
            + first_direction[1] * second_direction[1]
        )
        if (
            dot < 0
            and abs(cross) <= 32 * math.ulp(1.0)
        ):
            raise SkinningError(
                "A pontos visszafordulásnál nem határozható meg a kanyar oldala."
            )


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
        coordinate_scale = max(
            abs(point[0]),
            abs(point[1]),
            abs(circle.center_x),
            abs(circle.center_y),
            distance,
            circle.radius,
        )
        tolerance = 8 * math.ulp(coordinate_scale)
        if distance < circle.radius - tolerance:
            return True
    return False


def _segments_intersect(
    first_start: tuple[float, float],
    first_end: tuple[float, float],
    second_start: tuple[float, float],
    second_end: tuple[float, float],
) -> bool:
    def normalized_orientation(
        start: tuple[float, float],
        end: tuple[float, float],
        point: tuple[float, float],
    ) -> float:
        first_x = end[0] - start[0]
        first_y = end[1] - start[1]
        second_x = point[0] - start[0]
        second_y = point[1] - start[1]
        first_length = math.hypot(first_x, first_y)
        second_length = math.hypot(second_x, second_y)
        if first_length == 0 or second_length == 0:
            return 0.0
        return (
            (first_x / first_length) * (second_y / second_length)
            - (first_y / first_length) * (second_x / second_length)
        )

    tolerance = 32 * math.ulp(1.0)
    first_a = normalized_orientation(first_start, first_end, second_start)
    first_b = normalized_orientation(first_start, first_end, second_end)
    second_a = normalized_orientation(second_start, second_end, first_start)
    second_b = normalized_orientation(second_start, second_end, first_end)

    def on_segment(
        start: tuple[float, float],
        end: tuple[float, float],
        point: tuple[float, float],
    ) -> bool:
        scale = max(
            math.hypot(end[0] - start[0], end[1] - start[1]),
            1e-300,
        )
        coordinate_scale = max(
            abs(start[0]),
            abs(start[1]),
            abs(end[0]),
            abs(end[1]),
            abs(point[0]),
            abs(point[1]),
        )
        position_tolerance = max(
            scale * 32 * math.ulp(1.0),
            8 * math.ulp(coordinate_scale),
        )
        return (
            min(start[0], end[0]) - position_tolerance
            <= point[0]
            <= max(start[0], end[0]) + position_tolerance
            and min(start[1], end[1]) - position_tolerance
            <= point[1]
            <= max(start[1], end[1]) + position_tolerance
        )

    def sign(value: float) -> int:
        if value > tolerance:
            return 1
        if value < -tolerance:
            return -1
        return 0

    first_a_sign = sign(first_a)
    first_b_sign = sign(first_b)
    second_a_sign = sign(second_a)
    second_b_sign = sign(second_b)
    if (
        first_a_sign * first_b_sign < 0
        and second_a_sign * second_b_sign < 0
    ):
        return True
    return (
        first_a_sign == 0 and on_segment(first_start, first_end, second_start)
    ) or (
        first_b_sign == 0 and on_segment(first_start, first_end, second_end)
    ) or (
        second_a_sign == 0 and on_segment(second_start, second_end, first_start)
    ) or (
        second_b_sign == 0 and on_segment(second_start, second_end, first_end)
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
    ordered_edges = []
    for index in range(edge_count):
        start = points[index]
        end = points[index + 1]
        coordinate_scale = max(
            abs(start[0]),
            abs(start[1]),
            abs(end[0]),
            abs(end[1]),
        )
        length = math.hypot(end[0] - start[0], end[1] - start[1])
        tolerance = max(
            length * 32 * math.ulp(1.0),
            8 * math.ulp(coordinate_scale),
        )
        ordered_edges.append(
            (
                min(start[0], end[0]) - tolerance,
                max(start[0], end[0]) + tolerance,
                min(start[1], end[1]) - tolerance,
                max(start[1], end[1]) + tolerance,
                index,
            )
        )

    ordered_edges.sort(key=lambda edge: edge[0])
    active_edges = []
    for current in ordered_edges:
        min_x, max_x, min_y, max_y, current_index = current
        active_edges = [
            edge for edge in active_edges if edge[1] >= min_x
        ]
        for other in active_edges:
            if other[3] < min_y or max_y < other[2]:
                continue
            other_index = other[4]
            if (
                abs(current_index - other_index) <= 1
                or {current_index, other_index} == {0, edge_count - 1}
            ):
                continue
            if _segments_intersect(
                points[current_index],
                points[current_index + 1],
                points[other_index],
                points[other_index + 1],
            ):
                raise SkinningError(
                    "A bőrözési kontúr önmetsző; válassz más körkonfigurációt."
                )
        active_edges.append(current)


def _point_inside_contour(
    point: tuple[float, float],
    contour: Sequence[tuple[float, float]],
) -> bool:
    x, y = point
    inside = False
    for start, end in zip(contour, contour[1:]):
        if (start[1] > y) != (end[1] > y):
            crossing_x = start[0] + (y - start[1]) * (
                end[0] - start[0]
            ) / (end[1] - start[1])
            if x < crossing_x:
                inside = not inside
    return inside


def _distance_to_segment(
    point: tuple[float, float],
    start: tuple[float, float],
    end: tuple[float, float],
) -> float:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return math.hypot(point[0] - start[0], point[1] - start[1])

    projection = (
        (point[0] - start[0]) * dx + (point[1] - start[1]) * dy
    ) / length_squared
    projection = min(1.0, max(0.0, projection))
    closest = (start[0] + projection * dx, start[1] + projection * dy)
    return math.hypot(point[0] - closest[0], point[1] - closest[1])


def _validate_circle_containment(
    contour: Sequence[tuple[float, float]],
    circles: Sequence[Circle],
) -> None:
    for circle in circles:
        center = (circle.center_x, circle.center_y)
        if not _point_inside_contour(center, contour):
            raise SkinningError(
                "A bőrözési kontúr nem foglalja magában az összes bemeneti kört."
            )

        boundary_distance = math.inf
        for start, end in zip(contour, contour[1:]):
            min_x = min(start[0], end[0])
            max_x = max(start[0], end[0])
            min_y = min(start[1], end[1])
            max_y = max(start[1], end[1])
            dx = max(min_x - center[0], 0, center[0] - max_x)
            dy = max(min_y - center[1], 0, center[1] - max_y)
            if dx * dx + dy * dy >= boundary_distance * boundary_distance:
                continue
            boundary_distance = _distance_to_segment(center, start, end)
        coordinate_scale = max(
            abs(circle.center_x),
            abs(circle.center_y),
            circle.radius,
        )
        tolerance = max(
            circle.radius * 64 * math.ulp(1.0),
            8 * math.ulp(coordinate_scale),
        )
        if boundary_distance < circle.radius - tolerance:
            raise SkinningError(
                "A bőrözési kontúr nem foglalja magában az összes bemeneti kört."
            )


def _enclose_circles(
    contour: Sequence[tuple[float, float]],
    circles: Sequence[Circle],
) -> list[tuple[float, float]]:
    if not contour or contour[0] != contour[-1]:
        raise SkinningError("A bőrözési kontúr nem zárható biztonságosan.")

    points = list(contour[:-1])
    if len(points) < 3:
        raise SkinningError("A bőrözési kontúr nem alkot zárt tartományt.")

    for _ in range(32):
        adjusted = False
        for index in range(len(points)):
            next_index = (index + 1) % len(points)
            for circle in circles:
                start = points[index]
                end = points[next_index]
                center = (circle.center_x, circle.center_y)
                coordinate_scale = max(
                    abs(circle.center_x),
                    abs(circle.center_y),
                    circle.radius,
                )
                tolerance = max(
                    circle.radius * 64 * math.ulp(1.0),
                    8 * math.ulp(coordinate_scale),
                )
                if (
                    max(start[0], end[0]) < center[0] - circle.radius - tolerance
                    or min(start[0], end[0])
                    > center[0] + circle.radius + tolerance
                    or max(start[1], end[1])
                    < center[1] - circle.radius - tolerance
                    or min(start[1], end[1])
                    > center[1] + circle.radius + tolerance
                ):
                    continue
                distance = _distance_to_segment(center, start, end)
                if distance >= circle.radius - tolerance:
                    continue
                if distance == 0:
                    raise SkinningError(
                        "A kontúr nem kerülhető biztonságosan a kör középpontja körül."
                    )

                factor = (circle.radius + tolerance) / distance
                points[index] = (
                    center[0] + (start[0] - center[0]) * factor,
                    center[1] + (start[1] - center[1]) * factor,
                )
                points[next_index] = (
                    center[0] + (end[0] - center[0]) * factor,
                    center[1] + (end[1] - center[1]) * factor,
                )
                adjusted = True
        if not adjusted:
            result = points + [points[0]]
            _validate_simple_contour(result)
            _validate_circle_containment(result, circles)
            return result

    raise SkinningError(
        "A bemeneti köröket nem lehet egyszerű skinning kontúrral körülvenni."
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
            turn_cross = previous[0] * following[1] - previous[1] * following[0]
            turn_dot = previous[0] * following[0] + previous[1] * following[1]
            if turn_cross == 0.0 and turn_dot < 0.0:
                raise SkinningError(
                    "A pontos visszafordulásnál nem határozható meg a kanyar oldala."
                )
            half_turn = 0.5 * math.atan2(turn_cross, turn_dot)
            cosine = math.cos(half_turn)
            sine = math.sin(half_turn)
            centerline_tangents.append(
                (
                    previous[0] * cosine - previous[1] * sine,
                    previous[0] * sine + previous[1] * cosine,
                )
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

    segments.extend(
        _circle_arc_segments(
            circles[-1],
            upper[-1].end,
            lower[-1].end,
        )
    )

    for index in range(len(lower) - 1, -1, -1):
        bridge = lower[index]
        reversed_bridge = HermiteSegment(
            bridge.end,
            bridge.start,
            (-bridge.tangent_end[0], -bridge.tangent_end[1]),
            (-bridge.tangent_start[0], -bridge.tangent_start[1]),
        )
        segments.append(reversed_bridge)

    segments.extend(
        _circle_arc_segments(
            circles[0],
            lower[0].start,
            upper[0].start,
        )
    )

    contour = _sample_segments(segments, steps_per_segment=32)
    if not contour or contour[0] != contour[-1]:
        raise SkinningError("A bőrözési kontúr nem zárható biztonságosan.")
    _validate_simple_contour(contour)
    _enclose_circles(contour, circles)
    return segments


def sample_skinning(
    circles: Sequence[Circle], steps_per_segment: int = 32
) -> list[tuple[float, float]]:
    """Sample a validated circle-skinning contour for rendering."""
    if steps_per_segment < 2:
        raise ValueError("At least two steps per segment are required.")
    segments = build_skinning_segments(circles)
    points = _sample_segments(segments, steps_per_segment)
    return _enclose_circles(points, circles)


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
