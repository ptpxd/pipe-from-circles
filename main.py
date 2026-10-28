"""Application entry point."""

import tkinter as tk

from app import CircleTubeApp


def main() -> None:
    root = tk.Tk()
    CircleTubeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
