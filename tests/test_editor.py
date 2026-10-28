import unittest

from editor import CircleEditor


class CircleEditorUndoTests(unittest.TestCase):
    def setUp(self):
        self.editor = CircleEditor()
        self.editor.add_click(0, 0)
        self.editor.add_click(3, 0)
        self.editor.add_click(10, 0)
        self.editor.add_click(10, 4)

    def test_undo_removes_only_last_circle_and_preserves_order(self):
        previous = self.editor.circles[0]

        removed = self.editor.remove_last_circle()

        self.assertTrue(removed)
        self.assertEqual(len(self.editor.circles), 1)
        self.assertIs(self.editor.circles[0], previous)
        self.assertIsNone(self.editor.pending_center)

    def test_undo_cancels_pending_center_before_removing_circle(self):
        self.editor.add_click(20, 20)
        circle_count = len(self.editor.circles)

        removed = self.editor.remove_last_circle()

        self.assertFalse(removed)
        self.assertEqual(len(self.editor.circles), circle_count)
        self.assertIsNone(self.editor.pending_center)

    def test_undo_on_empty_editor_is_harmless(self):
        editor = CircleEditor()

        self.assertFalse(editor.remove_last_circle())
        self.assertEqual(editor.circles, [])


if __name__ == "__main__":
    unittest.main()
