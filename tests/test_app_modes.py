import unittest
from types import SimpleNamespace

from app import CircleTubeApp, ViewTransform
from editor import CircleEditor
from geometry import Circle


class FakeCanvas:
    def __init__(self):
        self.polygons = []
        self.ovals = []

    def delete(self, _tag):
        self.polygons.clear()
        self.ovals.clear()

    def focus_set(self):
        pass

    def create_polygon(self, *coordinates, **options):
        self.polygons.append((coordinates, options))

    def create_oval(self, *coordinates, **options):
        self.ovals.append((coordinates, options))


class FakeVariable:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class FakeStatus(FakeVariable):
    pass


class CircleTubeModeTests(unittest.TestCase):
    def make_app(self, circles):
        app = CircleTubeApp.__new__(CircleTubeApp)
        app.editor = CircleEditor()
        app.editor.circles.extend(circles)
        app.view = ViewTransform()
        app.curve_mode = FakeVariable(app.DISK_BEZIER_MODE)
        app.status = FakeStatus("")
        app.canvas = FakeCanvas()
        app._handle_angles = []
        app._drag_target = None
        return app

    def test_mode_switch_redraws_without_changing_circles(self):
        app = self.make_app([Circle(0, 0, 2), Circle(8, 0, 2)])
        original_circles = list(app.editor.circles)

        app._redraw()
        disk_bezier_polygon_count = len(app.canvas.polygons)
        app.curve_mode.set(app.SKINNING_MODE)
        app._on_mode_change(None)

        self.assertGreater(disk_bezier_polygon_count, 1)
        self.assertEqual(len(app.canvas.polygons), 1)
        self.assertEqual(app.editor.circles, original_circles)

    def test_skinning_error_preserves_input_and_draws_no_tube(self):
        circles = [Circle(0, 0, 5), Circle(2, 0, 1)]
        app = self.make_app(circles)
        app.curve_mode.set(app.SKINNING_MODE)

        app._redraw()

        self.assertEqual(app.editor.circles, circles)
        self.assertEqual(app.canvas.polygons, [])
        self.assertEqual(len(app.canvas.ovals), 6)
        self.assertEqual(
            sum(
                oval[1].get("fill") == app.TUBE_COLOR
                for oval in app.canvas.ovals
            ),
            2,
        )
        self.assertIn("nem alkalmazható", app.status.get())

        app.curve_mode.set(app.DISK_BEZIER_MODE)
        app._on_mode_change(None)

        self.assertNotIn("nem alkalmazható", app.status.get())
        self.assertGreater(len(app.canvas.ovals), 0)

    def test_sharp_turn_skinning_renders_without_changing_circles(self):
        circles = [
            Circle(0, 0, 10),
            Circle(300, 0, 10),
            Circle(4.56, 52.09, 10),
        ]
        app = self.make_app(circles)
        app.curve_mode.set(app.SKINNING_MODE)

        app._redraw()

        self.assertEqual(len(app.canvas.polygons), 1)
        self.assertEqual(app.editor.circles, circles)
        self.assertNotIn("nem alkalmazható", app.status.get())

    def test_overlapping_circle_skinning_renders_or_reports_without_data_loss(self):
        overlapping_circles = [Circle(0, 0, 2), Circle(3, 0, 2)]
        valid_app = self.make_app(overlapping_circles)
        valid_app.curve_mode.set(valid_app.SKINNING_MODE)

        valid_app._redraw()

        self.assertEqual(len(valid_app.canvas.polygons), 1)
        self.assertEqual(valid_app.editor.circles, overlapping_circles)
        self.assertNotIn("nem alkalmazható", valid_app.status.get())

        invalid_circles = [
            Circle(0, 0, 2),
            Circle(3, 0, 2),
            Circle(2, 3, 2),
        ]
        invalid_app = self.make_app(invalid_circles)
        invalid_app.curve_mode.set(invalid_app.SKINNING_MODE)

        invalid_app._redraw()

        self.assertEqual(invalid_app.canvas.polygons, [])
        self.assertEqual(invalid_app.editor.circles, invalid_circles)
        self.assertGreater(len(invalid_app.canvas.ovals), 0)
        self.assertIn("nem alkalmazható", invalid_app.status.get())

    def test_skinning_mode_explains_when_fewer_than_two_circles_exist(self):
        circles = [Circle(0, 0, 2)]
        app = self.make_app(circles)
        app.curve_mode.set(app.SKINNING_MODE)

        app._on_mode_change(None)

        self.assertIn("legalább két kör", app.status.get())
        self.assertEqual(app.editor.circles, circles)
        self.assertEqual(app.canvas.polygons, [])
        self.assertEqual(len(app.canvas.ovals), 3)

    def test_skinning_mode_fills_each_entire_input_circle(self):
        circles = [Circle(0, 0, 2), Circle(8, 0, 2)]
        app = self.make_app(circles)
        app.curve_mode.set(app.SKINNING_MODE)

        app._redraw()

        filled_circles = [
            oval
            for oval in app.canvas.ovals
            if oval[1].get("fill") == app.TUBE_COLOR
        ]
        self.assertEqual(len(filled_circles), 2)
        self.assertIn(
            (
                (-2, -2, 2, 2),
                {
                    "fill": app.TUBE_COLOR,
                    "outline": app.CIRCLE_COLOR,
                    "width": 2,
                },
            ),
            filled_circles,
        )
        self.assertEqual(app.editor.circles, circles)

        app.curve_mode.set(app.DISK_BEZIER_MODE)
        app._on_mode_change(None)

        disk_bezier_fills = [
            oval
            for oval in app.canvas.ovals
            if oval[1].get("fill") == app.TUBE_COLOR
        ]
        self.assertGreater(len(disk_bezier_fills), len(circles))
        self.assertEqual(app.editor.circles, circles)

    def test_selected_skinning_mode_refreshes_after_add_and_backspace(self):
        original_circles = [Circle(0, 0, 1.5), Circle(8, 0, 1.5)]
        app = self.make_app(original_circles)
        app.curve_mode.set(app.SKINNING_MODE)

        app._redraw()
        initial_contour = app.canvas.polygons[0][0]

        app._on_click(SimpleNamespace(x=12, y=7))
        app._on_click(SimpleNamespace(x=13.5, y=7))
        added_contour = app.canvas.polygons[0][0]

        self.assertEqual(len(app.editor.circles), 3)
        self.assertEqual(app.editor.circles[:2], original_circles)
        self.assertNotEqual(added_contour, initial_contour)
        self.assertEqual(len(app.canvas.polygons), 1)

        app._on_backspace(None)

        self.assertEqual(len(app.editor.circles), 2)
        self.assertEqual(app.editor.circles, original_circles)
        self.assertEqual(len(app.canvas.polygons), 1)
        self.assertEqual(app.canvas.polygons[0][0], initial_contour)


class CircleResizeInteractionTests(unittest.TestCase):
    def test_resize_handles_are_drawn_and_drag_uses_world_coordinates(self):
        app = CircleTubeModeTests().make_app(
            [Circle(0, 0, 2), Circle(8, 0, 2)]
        )
        app.view = ViewTransform(scale=2, offset_x=10, offset_y=20)
        app._redraw()
        initial_contour = app.canvas.polygons[0][0]

        handles = [
            oval
            for oval in app.canvas.ovals
            if oval[1].get("fill") == app.HANDLE_COLOR
        ]
        self.assertEqual(len(handles), 4)

        app._on_canvas_press(SimpleNamespace(x=14, y=20))
        app._on_canvas_drag(SimpleNamespace(x=18, y=20))
        app._on_canvas_release(None)
        app._on_canvas_press(SimpleNamespace(x=2, y=20))
        app._on_canvas_drag(SimpleNamespace(x=0, y=20))
        app._on_canvas_release(None)

        self.assertEqual(app.editor.circles[0], Circle(0, 0, 5))
        self.assertEqual(app.editor.circles[1], Circle(8, 0, 2))
        self.assertNotEqual(app.canvas.polygons[0][0], initial_contour)


class CircleMoveInteractionTests(unittest.TestCase):
    def test_dragging_circle_body_moves_it_and_blank_click_still_adds(self):
        app = CircleTubeModeTests().make_app(
            [Circle(0, 0, 2), Circle(12, 0, 2)]
        )
        app.view = ViewTransform(scale=2, offset_x=10, offset_y=20)
        app._redraw()
        initial_contour = app.canvas.polygons[0][0]

        app._on_canvas_press(SimpleNamespace(x=10, y=20))
        app._on_canvas_drag(SimpleNamespace(x=18, y=26))
        app._on_canvas_release(None)

        self.assertEqual(app.editor.circles[0], Circle(4, 3, 2))
        self.assertEqual(app.editor.circles[1], Circle(12, 0, 2))
        self.assertNotEqual(app.canvas.polygons[0][0], initial_contour)

        app._on_canvas_press(SimpleNamespace(x=100, y=100))
        self.assertEqual(app.editor.pending_center, (45, 40))

    def test_clicking_inside_circle_still_completes_two_click_circle_entry(self):
        original = Circle(0, 0, 5)
        app = CircleTubeModeTests().make_app([original])

        app._on_canvas_press(SimpleNamespace(x=1, y=0))
        app._on_canvas_release(SimpleNamespace(x=1, y=0))

        self.assertEqual(app.editor.circles, [original])
        self.assertEqual(app.editor.pending_center, (1, 0))

        app._on_canvas_press(SimpleNamespace(x=2, y=0))
        app._on_canvas_release(SimpleNamespace(x=2, y=0))

        self.assertEqual(app.editor.circles, [original, Circle(1, 0, 1)])
        self.assertIsNone(app.editor.pending_center)


if __name__ == "__main__":
    unittest.main()
