"""Tkinter interface for the interactive circle tube editor."""

from dataclasses import dataclass
import math
import tkinter as tk
from tkinter import ttk

from editor import CircleEditor
from geometry import (
    SkinningError,
    disk_bridge,
    sample_disk_bezier,
    sample_skinning,
)


@dataclass
class ViewTransform:
    scale: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0

    MIN_SCALE = 0.1
    MAX_SCALE = 20.0

    def __post_init__(self) -> None:
        if (
            not math.isfinite(self.scale)
            or not self.MIN_SCALE <= self.scale <= self.MAX_SCALE
        ):
            raise ValueError("View scale is outside its supported range.")
        if not math.isfinite(self.offset_x) or not math.isfinite(self.offset_y):
            raise ValueError("View offsets must be finite.")

    def to_screen(self, x: float, y: float) -> tuple[float, float]:
        return (
            self.offset_x + self.scale * x,
            self.offset_y + self.scale * y,
        )

    def to_world(self, x: float, y: float) -> tuple[float, float]:
        return (
            (x - self.offset_x) / self.scale,
            (y - self.offset_y) / self.scale,
        )

    def zoom_at(self, factor: float, x: float, y: float) -> None:
        if not math.isfinite(factor) or factor <= 0:
            raise ValueError("Zoom factor must be finite and positive.")

        world_x, world_y = self.to_world(x, y)
        self.scale = min(
            self.MAX_SCALE,
            max(self.MIN_SCALE, self.scale * factor),
        )
        self.offset_x = x - self.scale * world_x
        self.offset_y = y - self.scale * world_y

    def pan(self, delta_x: float, delta_y: float) -> None:
        self.offset_x += delta_x
        self.offset_y += delta_y


class CircleTubeApp:
    TUBE_COLOR = "#8ecae6"
    CIRCLE_COLOR = "#1d3557"
    PENDING_COLOR = "#e63946"
    DISK_BEZIER_MODE = "Disk-Bézier"
    SKINNING_MODE = "Skinning mode"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Körökből képzett cső")
        self.root.geometry("1000x700")
        self.root.minsize(480, 360)

        self.editor = CircleEditor()
        self.view = ViewTransform()
        self._pan_last: tuple[int, int] | None = None
        self.status = tk.StringVar(
            value="Kattints a rajzfelületre az első kör középpontjához."
        )
        self.curve_mode = tk.StringVar(
            root,
            value=self.DISK_BEZIER_MODE,
        )

        controls = tk.Frame(root, padx=8, pady=6)
        controls.pack(fill=tk.X)
        tk.Label(controls, text="Görbemód:").pack(side=tk.LEFT)
        mode_selector = ttk.Combobox(
            controls,
            textvariable=self.curve_mode,
            values=(self.DISK_BEZIER_MODE, self.SKINNING_MODE),
            state="readonly",
            width=18,
        )
        mode_selector.pack(side=tk.LEFT, padx=(6, 0))
        mode_selector.bind("<<ComboboxSelected>>", self._on_mode_change)

        reset_button = tk.Button(
            controls, text="Reset", command=self._reset
        )
        reset_button.pack(side=tk.LEFT, padx=(6, 0))

        self.canvas = tk.Canvas(root, background="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<BackSpace>", self._on_backspace)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<ButtonPress-2>", self._on_pan_start)
        self.canvas.bind("<B2-Motion>", self._on_pan_motion)
        self.canvas.bind("<ButtonRelease-2>", self._on_pan_end)

        status_bar = tk.Label(
            root,
            textvariable=self.status,
            anchor=tk.W,
            padx=10,
            pady=6,
        )
        status_bar.pack(fill=tk.X)



    def _on_click(self, event: tk.Event) -> None:
        self.canvas.focus_set()
        was_setting_radius = self.editor.pending_center is not None
        world_x, world_y = self.view.to_world(event.x, event.y)
        completed = self.editor.add_click(world_x, world_y)
        if not self._redraw():
            return

        if not completed:
            if self.editor.pending_center is None:
                self.status.set("Kattints a következő kör középpontjához.")
            elif was_setting_radius:
                self.status.set(
                    "A sugár legyen pozitív. Kattints távolabb a középponttól."
                )
            else:
                self.status.set(
                    "Kattints egy másik helyre a kör sugarának megadásához."
                )
            return

        self.status.set(
            f"{len(self.editor.circles)} kör megadva. "
            "Kattints a következő középponthoz."
        )

    def _on_backspace(self, _event: tk.Event) -> str:
        removed = self.editor.remove_last_circle()
        if not self._redraw():
            return "break"
        if self.editor.pending_center is None:
            if removed:
                self.status.set(
                    f"{len(self.editor.circles)} kör maradt. "
                    "Kattints a következő középponthoz."
                )
            else:
                self.status.set("Kattints a kör középpontjához.")
        else:
            self.status.set("Kattints egy másik helyre a kör sugarához.")
        return "break"

    def _reset(self) -> None:
        """Reset the editor and clear all circles."""
        self.editor.circles.clear()
        self.editor.pending_center = None
        self.status.set("Kattints a kör középpontjához.")
        self._redraw()

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        factor = 1.1 ** (event.delta / 120)
        self.view.zoom_at(factor, event.x, event.y)
        self._redraw()

    def _on_pan_start(self, event: tk.Event) -> None:
        self._pan_last = (event.x, event.y)

    def _on_pan_motion(self, event: tk.Event) -> None:
        if self._pan_last is None:
            return
        previous_x, previous_y = self._pan_last
        self.view.pan(event.x - previous_x, event.y - previous_y)
        self._pan_last = (event.x, event.y)
        self._redraw()

    def _on_pan_end(self, _event: tk.Event) -> None:
        self._pan_last = None

    def _on_mode_change(self, _event: tk.Event) -> None:
        self.canvas.focus_set()
        if (
            self.curve_mode.get() == self.SKINNING_MODE
            and len(self.editor.circles) < 2
        ):
            self.status.set("A skinning mode-hoz legalább két kör szükséges.")
        else:
            self.status.set(f"Megjelenítési mód: {self.curve_mode.get()}.")
        self._redraw()

    def _redraw(self) -> bool:
        self.canvas.delete("all")
        rendered = True

        if len(self.editor.circles) >= 2:
            if self.curve_mode.get() == self.SKINNING_MODE:
                try:
                    contour = sample_skinning(self.editor.circles)
                    screen_points = [
                        self.view.to_screen(*point) for point in contour
                    ]
                    self.canvas.create_polygon(
                        *(
                            coordinate
                            for point in screen_points
                            for coordinate in point
                        ),
                        fill=self.TUBE_COLOR,
                        outline=self.TUBE_COLOR,
                    )
                except SkinningError as error:
                    self.status.set(f"A skinning mode nem alkalmazható: {error}")
                    rendered = False
            else:
                samples = sample_disk_bezier(self.editor.circles)
                for first, second in zip(samples, samples[1:]):
                    bridge = disk_bridge(first, second)
                    if bridge is not None:
                        screen_points = [
                            self.view.to_screen(*point) for point in bridge
                        ]
                        self.canvas.create_polygon(
                            *(
                                coordinate
                                for point in screen_points
                                for coordinate in point
                            ),
                            fill=self.TUBE_COLOR,
                            outline=self.TUBE_COLOR,
                        )

                for disk in samples:
                    center_x, center_y = self.view.to_screen(
                        disk.center_x, disk.center_y
                    )
                    radius = disk.radius * self.view.scale
                    self.canvas.create_oval(
                        center_x - radius,
                        center_y - radius,
                        center_x + radius,
                        center_y + radius,
                        fill=self.TUBE_COLOR,
                        outline=self.TUBE_COLOR,
                    )

        for circle in self.editor.circles:
            center_x, center_y = self.view.to_screen(
                circle.center_x, circle.center_y
            )
            radius = circle.radius * self.view.scale
            self.canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                outline=self.CIRCLE_COLOR,
                width=2,
            )

        if self.editor.pending_center is not None:
            center_x, center_y = self.view.to_screen(
                *self.editor.pending_center
            )
            marker_size = 4
            self.canvas.create_oval(
                center_x - marker_size,
                center_y - marker_size,
                center_x + marker_size,
                center_y + marker_size,
                fill=self.PENDING_COLOR,
                outline=self.PENDING_COLOR,
            )
        return rendered
