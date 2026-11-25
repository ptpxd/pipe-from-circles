import math
import unittest

from geometry import (
    Circle,
    SkinningError,
    build_skinning_segments,
    disk_bridge,
    evaluate_disk_bezier,
    sample_skinning,
    sample_disk_bezier,
)


class CircleSkinningTests(unittest.TestCase):
    @staticmethod
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

    @staticmethod
    def _point_inside_contour(
        point: tuple[float, float],
        contour: list[tuple[float, float]],
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

    def assert_contour_contains_circles(
        self,
        contour: list[tuple[float, float]],
        circles: list[Circle],
    ) -> None:
        for circle in circles:
            center = (circle.center_x, circle.center_y)
            self.assertTrue(
                self._point_inside_contour(center, contour),
                f"Contour does not enclose circle at {center}.",
            )
            minimum_boundary_distance = min(
                self._distance_to_segment(center, start, end)
                for start, end in zip(contour, contour[1:])
            )
            tolerance = max(
                circle.radius * 1e-12,
                8 * math.ulp(max(abs(center[0]), abs(center[1]), circle.radius)),
            )
            self.assertGreaterEqual(
                minimum_boundary_distance + tolerance,
                circle.radius,
                f"Contour cuts through circle at {center}.",
            )

    def test_sharp_170_degree_turn_produces_a_simple_enclosing_contour(self):
        circles = [
            Circle(0, 0, 10),
            Circle(300, 0, 10),
            Circle(4.56, 52.09, 10),
        ]

        contour = sample_skinning(circles)

        self.assertEqual(contour[0], contour[-1])
        self.assertGreater(len(contour), 20)
        self.assert_contour_contains_circles(contour, circles)

    def test_variable_radii_and_overlapping_or_nearly_touching_circles(self):
        cases = [
            [
                Circle(0, 0, 1),
                Circle(20, 0, 5),
                Circle(40, 8, 2),
            ],
            [Circle(0, 0, 1), Circle(2.01, 0, 1)],
            [Circle(0, 0, 2), Circle(3, 0, 2)],
        ]

        for circles in cases:
            with self.subTest(circles=circles):
                original_circles = list(circles)
                contour = sample_skinning(circles)

                self.assertEqual(contour[0], contour[-1])
                self.assert_contour_contains_circles(contour, circles)
                self.assertEqual(circles, original_circles)

    def test_nearly_straight_and_extreme_uniform_scales_are_supported(self):
        nearly_straight = [
            Circle(0, 0, 1),
            Circle(5, 0, 1),
            Circle(10, 1e-5, 1),
        ]
        base = [
            Circle(0, 0, 1.5),
            Circle(8, 0, 1.5),
            Circle(12, 7, 1.5),
        ]

        cases = [nearly_straight] + [
            [
                Circle(
                    circle.center_x * scale,
                    circle.center_y * scale,
                    circle.radius * scale,
                )
                for circle in base
            ]
            for scale in (1e-12, 1e12)
        ]
        for circles in cases:
            with self.subTest(circles=circles):
                contour = sample_skinning(circles)
                self.assertEqual(contour[0], contour[-1])
                self.assert_contour_contains_circles(contour, circles)

    def test_two_circles_are_connected_by_tangent_hermite_segments(self):
        circles = [Circle(0, 0, 2), Circle(8, 1, 1)]

        segments = build_skinning_segments(circles)

        def circle_at(point):
            return next(
                (
                    circle
                    for circle in circles
                    if math.isclose(
                        math.hypot(
                            point[0] - circle.center_x,
                            point[1] - circle.center_y,
                        ),
                        circle.radius,
                        abs_tol=1e-7,
                    )
                ),
                None,
            )

        bridges = [
            segment
            for segment in segments
            if circle_at(segment.start) is not circle_at(segment.end)
        ]
        self.assertEqual(len(bridges), 2)
        for segment in bridges:
            for point, tangent in (
                (segment.start, segment.tangent_start),
                (segment.end, segment.tangent_end),
            ):
                center = circle_at(point)
                self.assertIsNotNone(center)
                radial = (
                    point[0] - center.center_x,
                    point[1] - center.center_y,
                )
                self.assertAlmostEqual(
                    math.hypot(*radial),
                    center.radius,
                )
                self.assertAlmostEqual(
                    radial[0] * tangent[0] + radial[1] * tangent[1],
                    0,
                    places=7,
                )

    def test_existing_disk_bezier_endpoints_and_sampling_are_preserved(self):
        circles = [Circle(0, 0, 2), Circle(8, 4, 3)]

        self.assertEqual(evaluate_disk_bezier(circles, 0), circles[0])
        self.assertEqual(evaluate_disk_bezier(circles, 1), circles[1])
        self.assertEqual(len(sample_disk_bezier(circles)), 121)
        self.assertEqual(len(disk_bridge(circles[0], circles[1])), 4)

    def test_three_non_collinear_circles_produce_a_closed_sampled_contour(self):
        circles = [
            Circle(0, 0, 1.5),
            Circle(8, 0, 1.5),
            Circle(12, 7, 1.5),
        ]

        contour = sample_skinning(circles, steps_per_segment=16)

        self.assertGreater(len(contour), 20)
        self.assertEqual(contour[0], contour[-1])

    def test_three_circle_skinning_touches_each_circle_with_tangent_vectors(self):
        circles = [
            Circle(0, 0, 1.5),
            Circle(8, 0, 1.5),
            Circle(12, 7, 1.5),
        ]
        segments = build_skinning_segments(circles)
        contacts = {circle: 0 for circle in circles}
        for segment in segments:
            for point, tangent in (
                (segment.start, segment.tangent_start),
                (segment.end, segment.tangent_end),
            ):
                for circle in circles:
                    radial = (
                        point[0] - circle.center_x,
                        point[1] - circle.center_y,
                    )
                    if math.isclose(
                        math.hypot(*radial),
                        circle.radius,
                        abs_tol=1e-7,
                    ):
                        self.assertAlmostEqual(
                            radial[0] * tangent[0] + radial[1] * tangent[1],
                            0,
                            places=7,
                        )
                        contacts[circle] += 1
                        break

        for circle in circles:
            self.assertGreaterEqual(contacts[circle], 2)

    def test_skinning_is_translation_and_uniform_scale_invariant(self):
        circles = [
            Circle(0, 0, 1.5),
            Circle(8, 0, 1.5),
            Circle(12, 7, 1.5),
        ]
        transformed = [
            Circle(circle.center_x * 2 + 5, circle.center_y * 2 - 3, circle.radius * 2)
            for circle in circles
        ]

        original_contour = sample_skinning(circles, steps_per_segment=16)
        transformed_contour = sample_skinning(transformed, steps_per_segment=16)

        self.assertEqual(len(original_contour), len(transformed_contour))
        for original, actual in zip(original_contour, transformed_contour):
            self.assertAlmostEqual(actual[0], original[0] * 2 + 5, places=6)
            self.assertAlmostEqual(actual[1], original[1] * 2 - 3, places=6)

    def test_impossible_and_unsupported_configurations_are_rejected(self):
        with self.assertRaises(SkinningError):
            build_skinning_segments([Circle(0, 0, 1)])
        with self.assertRaises(SkinningError):
            build_skinning_segments([Circle(0, 0, 5), Circle(2, 0, 1)])
        straight_contour = sample_skinning(
            [Circle(0, 0, 1), Circle(5, 0, 1), Circle(10, 0, 1)]
        )
        self.assertEqual(straight_contour[0], straight_contour[-1])
        with self.assertRaises(SkinningError):
            build_skinning_segments(
                [
                    Circle(0, 0, 1),
                    Circle(5, 0, 1),
                    Circle(5 + 1e-12, 1e-12, 1),
                ]
            )
        with self.assertRaises(SkinningError):
            build_skinning_segments(
                [Circle(0, 0, 1), Circle(5, 0, 1), Circle(0, 1, 1)]
            )
        with self.assertRaisesRegex(SkinningError, "önmetsző"):
            sample_skinning(
                [
                    Circle(0, 0, 1),
                    Circle(30, 0, 5),
                    Circle(26, 4, 2),
                ]
            )
        with self.assertRaises(SkinningError):
            build_skinning_segments(
                [Circle(0, 0, 1), Circle(6, 0, 1), Circle(0, 0, 1)]
            )


if __name__ == "__main__":
    unittest.main()
