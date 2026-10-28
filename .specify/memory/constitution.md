<!--
Sync Impact Report
Version change: not established → 1.0.0 (initial constitution)
Modified principles: none
Added sections: Core Principles, Additional Constraints, Development Workflow, Governance
Removed sections: none
Follow-up TODOs: Establish the original ratification date.
-->

# Task Two Constitution

## Core Principles

### I. Clarity and Understandability
Code and technical documentation MUST make their purpose, behavior, and important assumptions
clear to the people maintaining them. Names and structure MUST reflect the concepts they represent.
Prefer straightforward solutions over clever constructs that make behavior harder to follow.

### II. Simplicity
Changes MUST use the simplest design that fully meets the stated requirements. Avoid speculative
features, unnecessary abstractions, duplicate logic, and configurability without a demonstrated
need. Complexity that cannot be avoided MUST be explained and justified.

### III. Efficiency
Implementations MUST use resources proportionately to the task and MUST meet any stated performance
requirements. Do not trade away clarity or correctness for unmeasured optimization; when performance
is a concern, validate it with relevant measurements.

### IV. Correctness and Validation
Changes MUST preserve existing behavior unless a behavior change is explicitly required. Validate
the requested outcome with the most relevant available tests, checks, or reproducible evidence.
Report validation that could not be completed and why.

### V. Focused, Maintainable Changes
Changes MUST stay within the requested scope and follow established project conventions. Update
directly related documentation and tests when behavior changes. Do not include unrelated cleanup.

## Additional Constraints

- Use the repository's existing tools, dependencies, and conventions where practical.
- Add dependencies only when required to satisfy the task and document their purpose.
- Do not introduce complexity or performance claims without a concrete requirement or evidence.

## Development Workflow

- Before implementation, inspect the relevant code and existing patterns.
- After implementation, run the smallest relevant test or validation command available.
- Review the final change for scope, clarity, correctness, and consistency with these principles.
- Communicate material assumptions, behavior changes, and validation results.

## Governance

This constitution governs project development practices. Amendments MUST be made through an
explicit review of the proposed change and its effect on existing principles and project guidance.
Every amendment MUST update the version and last-amended date.

Versioning follows semantic versioning: MAJOR for backward-incompatible changes to principles or
governance, MINOR for added principles or materially expanded requirements, and PATCH for
clarifications and non-semantic refinements.

Contributors and reviewers MUST assess relevant changes for compliance with this constitution.
Any exception MUST be explicit, limited to the specific change, and accompanied by its rationale.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date not available | **Last Amended**: 2026-10-28
