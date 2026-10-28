# Tasks: Interaktív kör-tube szerkesztő

**Input**: Design documents from `/specs/001-circle-tube-editor/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md`

**Tests**: Dedicated automated test tasks are omitted because the feature specification does not
request a test suite. Validate the user flow with the manual scenarios in `quickstart.md`.

## Format

- Every task uses `- [ ] Txxx [P?] [Story?] Description with file path`.
- `[P]` marks tasks that can be done in parallel without editing the same files or depending on
  unfinished tasks.
- `[US1]` maps a task to User Story 1 in `spec.md`.

## Phase 1: Setup

**Purpose**: Establish the minimal dependency-free Python project layout.

- [X] T001 Create the root-level Python application files `main.py`, `app.py`, `editor.py`, and `geometry.py`; do not add third-party dependencies.

## Phase 2: Foundational

**Purpose**: Implement the ordered circle data and geometry used by the user-facing workflow.

- [X] T002 Implement the `Circle` model, Bernstein-weighted Disk-Bézier center/radius evaluation, and sampled disk generation in `geometry.py`; reject non-finite or non-positive radii.

**Checkpoint**: The application can represent valid control circles and evaluate the derived shape without requiring a GUI.

## Phase 3: User Story 1 - Csőszerű alakzat létrehozása körökből (Priority: P1) 🎯 MVP

**Goal**: Let the user define ordered circles with two clicks each and immediately see the derived tube.

**Independent Test**: Follow the full manual scenario in `quickstart.md`: place at least two circles, verify the tube appears and updates after another circle, and verify a zero-radius attempt can be retried.

### Implementation

- [X] T003 [US1] Implement the circle-entry state in `editor.py`: the first click stores a pending center, the second click creates a positive-radius circle in order, and a zero-radius click retains the pending center.
- [X] T004 [US1] Build the Tkinter window and canvas in `app.py`; bind mouse clicks, display control circles, draw the sampled Disk-Bézier disk union with a consistent fill, and redraw after every completed circle.
- [X] T005 [US1] Connect the editor and canvas in `main.py` and launch the Tkinter event loop when the application starts.

**Checkpoint**: The end-to-end P1 interaction works independently as the minimum viable application.

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Document setup and verify the completed application.

- [X] T006 Write `README.md` in Hungarian with Python/Tkinter prerequisites, dependency list, the Tkinter availability check, the application launch command, and the two-click interaction instructions.
- [X] T007 Validate the acceptance scenarios from `specs/001-circle-tube-editor/quickstart.md` with Python geometry, input-state, and Tkinter Canvas click-flow checks; fix defects in `geometry.py`, `editor.py`, `app.py`, or `main.py`.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; establishes the root-level source files.
- **Foundational (Phase 2)**: Depends on Setup; provides circle and Disk-Bézier calculations.
- **User Story 1 (Phase 3)**: Depends on the foundational geometry; completes the only user story.
- **Polish (Phase 4)**: Depends on the working P1 application.

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Phase 2; no dependencies on other stories.

### Parallel Opportunities

- No implementation tasks are marked `[P]`: each implementation step either shares the same
  source files or depends on the geometry/model interface from an earlier task.
- The project is small enough to implement sequentially without separate parallel workstreams.

## Parallel Example: User Story 1

The story implementation is intentionally sequential: `T003` defines the click-state behavior
used by `T004`, and `T004` is launched by `T005`.

## Implementation Strategy

### MVP First

1. Complete T001 and T002 to establish the project and geometry.
2. Complete T003 through T005 to implement the single P1 user journey.
3. Validate the complete journey using `quickstart.md`.
4. Complete T006 so the user can run the application and identify its dependencies.

### Incremental Delivery

- The feature contains one user story, so the independently demonstrable MVP is the completed
  P1 interaction: place circles, display them, and update the tube.
- Documentation and final smoke validation follow the working interaction.

## Phase 5: Convergence

- [X] T008 Ensure the sampled Disk-Bézier tube renders continuously for distant centers and small positive radii in `app.py` or `geometry.py` using common-tangent bridges between adjacent disks, per FR-005 and US1/AC2 (partial).
