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
    def test_two_circles_are_connected_by_tangent_hermite_segments(self):
        circles = [Circle(0, 0, 2), Circle(8, 1, 1)]

        segments = build_skinning_segments(circles)

        self.assertEqual(len(segments), 4)
        for segment, endpoint_circles in (
            (segments[0], circles),
            (segments[2], list(reversed(circles))),
        ):
            for point, center, tangent in (
                (segment.start, endpoint_circles[0], segment.tangent_start),
                (segment.end, endpoint_circles[1], segment.tangent_end),
            ):
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

        contour = sample_skinning(circles, steps_per_segment=12)

        self.assertGreater(len(contour), 20)
        self.assertEqual(contour[0], contour[-1])

    def test_three_circle_skinning_touches_each_circle_with_tangent_vectors(self):
        circles = [
            Circle(0, 0, 1.5),
            Circle(8, 0, 1.5),
            Circle(12, 7, 1.5),
        ]
        segments = build_skinning_segments(circles)
        boundary_segments = [
            (segments[0], circles[0], circles[1]),
            (segments[1], circles[1], circles[2]),
            (segments[3], circles[2], circles[1]),
            (segments[4], circles[1], circles[0]),
        ]

        for segment, start_circle, end_circle in boundary_segments:
            for point, circle, tangent in (
                (segment.start, start_circle, segment.tangent_start),
                (segment.end, end_circle, segment.tangent_end),
            ):
                radial = (
                    point[0] - circle.center_x,
                    point[1] - circle.center_y,
                )
                self.assertAlmostEqual(math.hypot(*radial), circle.radius)
                self.assertAlmostEqual(
                    radial[0] * tangent[0] + radial[1] * tangent[1],
                    0,
                    places=7,
                )

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

        original_contour = sample_skinning(circles, steps_per_segment=8)
        transformed_contour = sample_skinning(transformed, steps_per_segment=8)

        self.assertEqual(len(original_contour), len(transformed_contour))
        for original, actual in zip(original_contour, transformed_contour):
            self.assertAlmostEqual(actual[0], original[0] * 2 + 5, places=6)
            self.assertAlmostEqual(actual[1], original[1] * 2 - 3, places=6)

    def test_impossible_and_unsupported_configurations_are_rejected(self):
        with self.assertRaises(SkinningError):
            build_skinning_segments([Circle(0, 0, 1)])
        with self.assertRaises(SkinningError):
            build_skinning_segments([Circle(0, 0, 5), Circle(2, 0, 1)])
        with self.assertRaises(SkinningError):
            build_skinning_segments(
                [Circle(0, 0, 1), Circle(5, 0, 1), Circle(10, 0, 1)]
            )
        with self.assertRaises(SkinningError):
            build_skinning_segments(
                [Circle(0, 0, 1), Circle(5, 0, 1), Circle(0, 1, 1)]
            )
        with self.assertRaises(SkinningError):
            build_skinning_segments(
                [Circle(0, 0, 1), Circle(6, 0, 1), Circle(0, 0, 1)]
            )


if __name__ == "__main__":
    unittest.main()
