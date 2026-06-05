# Proof of Concept: Infinite Ways to Do the Same Thing in G-code

## Abstract

G-code appears deterministic: a machine receives commands and executes them. However, the same physical result can be achieved through countless alternative command sequences. This property creates a combinatorial explosion of valid programs that produce identical outputs, making G-code an interesting example of non-unique machine instructions.

This document demonstrates how a single manufacturing objective can be represented in infinitely many equivalent forms.

---

## Core Observation

Consider the goal:

> Move a tool from X0 Y0 to X10 Y10.

A straightforward implementation is:

```gcode
G0 X10 Y10
```

However, the exact same result can be expressed as:

```gcode
G0 X5 Y5
G0 X10 Y10
```

Or:

```gcode
G0 X1 Y1
G0 X2 Y2
G0 X3 Y3
G0 X4 Y4
G0 X5 Y5
G0 X6 Y6
G0 X7 Y7
G0 X8 Y8
G0 X9 Y9
G0 X10 Y10
```

Or:

```gcode
G0 X0.1 Y0.1
G0 X0.2 Y0.2
...
G0 X10 Y10
```

As the number of intermediate points approaches infinity, the number of valid programs also approaches infinity.

---

## Feed Rate Equivalence

These two programs produce identical final positions:

```gcode
G1 X10 F1000
```

```gcode
F1000
G1 X10
```

Likewise:

```gcode
F500
F750
F1000
G1 X10
```

Only the final active feed rate affects the move.

An arbitrary number of redundant state changes can be inserted without altering the final outcome.

---

## Coordinate System Equivalence

The following programs result in the same tool location:

### Absolute

```gcode
G90
G0 X10 Y10
```

### Relative

```gcode
G91
G0 X5 Y5
G0 X5 Y5
```

### Mixed

```gcode
G91
G0 X20 Y20
G0 X-10 Y-10
```

Different coordinate interpretations can describe the same physical endpoint.

---

## State Redundancy

Machine state can be repeatedly asserted:

```gcode
G90
G90
G90
G90
G0 X10
```

The extra commands contribute no behavioral difference.

The same applies to:

* Units (`G20` / `G21`)
* Motion modes (`G0`, `G1`)
* Plane selection (`G17`, `G18`, `G19`)
* Tool selection
* Work offsets

Any state can be redundantly re-declared.

---

## Geometric Decomposition

A line can be represented as:

```gcode
G1 X100
```

Or:

```gcode
G1 X50
G1 X100
```

Or:

```gcode
G1 X25
G1 X50
G1 X75
G1 X100
```

Or through arbitrarily many segments.

The geometric result remains identical.

---

## Arc Approximation

A circular path may be expressed as:

```gcode
G2 X10 Y0 I5 J0
```

Or:

```gcode
G1 X9.99 Y0.31
G1 X9.96 Y0.62
...
```

The approximation can be refined indefinitely.

A single command can therefore correspond to infinitely many equivalent linearized representations.

---

## Formal Argument

Let:

* P be a target machine state.
* G be a G-code program.
* E(G) be the execution result of G.

If:

```text
E(G1) = P
```

and arbitrary redundant operations R can be inserted such that:

```text
E(G1 + R) = P
```

then for every integer n:

```text
E(G1 + R₁ + R₂ + ... + Rₙ) = P
```

Since n is unbounded, the number of valid programs producing P is also unbounded.

---

## Implications

### Program Obfuscation

Two G-code files may appear completely different while producing identical toolpaths.

### Compression

Many commands can be removed without changing output.

### Verification Challenges

Comparing source files is insufficient to determine equivalence.

The actual machine state trajectory must be analyzed.

### AI Generation

An AI model can generate countless valid solutions for the same machining objective because the mapping from intent to G-code is one-to-many rather than one-to-one.

---

## Conclusion

G-code demonstrates a fundamental property of machine instruction languages:

> A physical outcome does not uniquely determine the program that produced it.

Because redundant state changes, alternative coordinate systems, path decomposition, interpolation methods, and geometric approximations can all represent the same operation, the number of valid G-code programs for a given result is effectively infinite.

The machine executes one path; the programmer has infinitely many ways to describe it.
