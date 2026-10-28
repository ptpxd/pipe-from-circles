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
        self.assertEqual(len(app.canvas.ovals), 2)
        self.assertIn("nem alkalmazható", app.status.get())

        app.curve_mode.set(app.DISK_BEZIER_MODE)
        app._on_mode_change(None)

        self.assertNotIn("nem alkalmazható", app.status.get())
        self.assertGreater(len(app.canvas.ovals), 0)

    def test_skinning_mode_explains_when_fewer_than_two_circles_exist(self):
        circles = [Circle(0, 0, 2)]
        app = self.make_app(circles)
        app.curve_mode.set(app.SKINNING_MODE)

        app._on_mode_change(None)

        self.assertIn("legalább két kör", app.status.get())
        self.assertEqual(app.editor.circles, circles)
        self.assertEqual(app.canvas.polygons, [])
        self.assertEqual(len(app.canvas.ovals), 1)

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


if __name__ == "__main__":
    unittest.main()
