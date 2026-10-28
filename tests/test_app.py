import unittest
from types import SimpleNamespace

from app import CircleTubeApp, ViewTransform
from editor import CircleEditor
from geometry import Circle


class FakeCanvas:
    def delete(self, _tag):
        pass

    def focus_set(self):
        pass

    def create_oval(self, *_coordinates, **_options):
        pass


class FakeVariable:
    def __init__(self):
        self.value = ""

    def set(self, value):
        self.value = value


class ViewTransformTests(unittest.TestCase):
    def test_world_and_screen_coordinates_round_trip(self):
        view = ViewTransform(scale=2.5, offset_x=30, offset_y=-12)

        screen = view.to_screen(4, 8)

        self.assertEqual(screen, (40, 8))
        self.assertEqual(view.to_world(*screen), (4, 8))

    def test_zoom_keeps_world_point_under_cursor_fixed(self):
        view = ViewTransform(scale=1, offset_x=20, offset_y=40)
        cursor = (160, 100)
        world_before = view.to_world(*cursor)

        view.zoom_at(2, *cursor)

        self.assertEqual(view.to_screen(*world_before), cursor)
        self.assertEqual(view.scale, 2)

    def test_zoom_clamps_scale_without_moving_anchor(self):
        view = ViewTransform(scale=20, offset_x=3, offset_y=7)
        cursor = (25, 30)
        world_before = view.to_world(*cursor)

        view.zoom_at(2, *cursor)

        self.assertEqual(view.scale, view.MAX_SCALE)
        self.assertEqual(view.to_screen(*world_before), cursor)

    def test_pan_moves_every_world_point_by_the_same_offset(self):
        view = ViewTransform(scale=1.5, offset_x=4, offset_y=9)

        view.pan(12, -6)

        self.assertEqual(view.to_screen(0, 0), (16, 3))
        self.assertEqual(view.to_screen(8, 3), (28, 7.5))

    def test_clicks_after_view_transform_create_world_space_circle(self):
        app = CircleTubeApp.__new__(CircleTubeApp)
        app.view = ViewTransform(scale=2, offset_x=10, offset_y=20)
        app.editor = CircleEditor()
        app.canvas = FakeCanvas()
        app.status = FakeVariable()

        app._on_click(SimpleNamespace(x=14, y=26))
        app._on_click(SimpleNamespace(x=20, y=26))

        self.assertEqual(app.editor.circles, [Circle(2, 3, 3)])


if __name__ == "__main__":
    unittest.main()
