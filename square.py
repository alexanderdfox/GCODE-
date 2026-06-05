import os
import random

OUTPUT_DIR = "gcode_variants"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SQUARE_SIZE = 20
DEPTH = -1.0
FEED = 300

def header():
	return [
		"%",
		"G21",
		"G17",
	]

def footer():
	return [
		"G0 Z5",
		"M30",
		"%"
	]

def absolute_square(clockwise=True):
	pts = [
		(0, 0),
		(SQUARE_SIZE, 0),
		(SQUARE_SIZE, SQUARE_SIZE),
		(0, SQUARE_SIZE),
		(0, 0)
	]

	if not clockwise:
		pts = [
			(0, 0),
			(0, SQUARE_SIZE),
			(SQUARE_SIZE, SQUARE_SIZE),
			(SQUARE_SIZE, 0),
			(0, 0)
		]

	code = [
		"G90",
		"G0 X0 Y0",
		f"G1 Z{DEPTH} F100"
	]

	for x, y in pts[1:]:
		code.append(f"G1 X{x} Y{y} F{FEED}")

	return code

def incremental_square(clockwise=True):
	code = [
		"G91",
		"G0 X0 Y0",
		f"G1 Z{DEPTH} F100"
	]

	if clockwise:
		moves = [
			(20, 0),
			(0, 20),
			(-20, 0),
			(0, -20)
		]
	else:
		moves = [
			(0, 20),
			(20, 0),
			(0, -20),
			(-20, 0)
		]

	for dx, dy in moves:
		code.append(f"G1 X{dx} Y{dy} F{FEED}")

	return code

def segmented_square(segments):
	code = [
		"G90",
		"G0 X0 Y0",
		f"G1 Z{DEPTH} F100"
	]

	step = SQUARE_SIZE / segments

	for i in range(1, segments + 1):
		code.append(f"G1 X{i*step:.3f} Y0 F{FEED}")

	for i in range(1, segments + 1):
		code.append(f"G1 X20 Y{i*step:.3f}")

	for i in range(segments - 1, -1, -1):
		code.append(f"G1 X{i*step:.3f} Y20")

	for i in range(segments - 1, -1, -1):
		code.append(f"G1 X0 Y{i*step:.3f}")

	return code

def subroutine_square():
	return [
		"G90",
		"G0 X0 Y0",
		f"G1 Z{DEPTH} F100",
		"M98 P2000",
		"",
		"O2000",
		f"G1 X{SQUARE_SIZE} Y0 F{FEED}",
		f"G1 X{SQUARE_SIZE} Y{SQUARE_SIZE}",
		f"G1 X0 Y{SQUARE_SIZE}",
		"G1 X0 Y0",
		"M99"
	]

def variable_square():
	return [
		"#100=20",
		"G90",
		"G0 X0 Y0",
		f"G1 Z{DEPTH} F100",
		"G1 X#100 Y0 F300",
		"G1 X#100 Y#100",
		"G1 X0 Y#100",
		"G1 X0 Y0"
	]

generators = [
	lambda: absolute_square(True),
	lambda: absolute_square(False),
	lambda: incremental_square(True),
	lambda: incremental_square(False),
	lambda: segmented_square(2),
	lambda: segmented_square(4),
	lambda: segmented_square(5),
	lambda: segmented_square(10),
	subroutine_square,
	variable_square
]

for i in range(100):
	code = header()

	style = generators[i % len(generators)]
	code.extend(style())

	# Add harmless stylistic variations
	if i % 3 == 0:
		code.insert(1, f"(Variant {i+1})")

	if i % 5 == 0:
		code.insert(2, "G94")

	if i % 7 == 0:
		code.insert(2, "G40")

	code.extend(footer())

	filename = os.path.join(
		OUTPUT_DIR,
		f"square_variant_{i+1:03d}.nc"
	)

	with open(filename, "w") as f:
		f.write("\n".join(code))

print(f"Generated 100 G-code files in '{OUTPUT_DIR}'")