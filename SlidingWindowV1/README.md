## Quickly what the program does:
The code uses the hex data from the Shremple towers to create a bitmap and searches for the hard-coded coordinates. \
Once found, it colors the fragments according to the legend to show where they are, and this may help find a rule about where and how the potential coordinates are placed in the towers' code.

## More about how the program searches for coordinates:
The program takes a window of a specific size (hardcoded) and then shifts the window in 1-bit increments. It shifts the window so that each bit is checked. After checking them, the closest fragment (translated to decimal) to the desired decimal is found and then displayed.

## Why such coordinates and why in this form?:
The coordinates searched for in the code are those from the end temple, as they are known coordinates, and the structure itself may correlate with the black glass "port" in Shremple. 

In the code, I assumed the coordinates in the towers' code were in XYZ format, with an X and Z precision of 3 decimal places and a Y precision of 5 decimal places, as it is the case in Minecraft. \
Because I'm assuming floating point, instead of 1607 it's 1607000 (1607.000 without the decimal point) \
I could be wrong; they could only be X and Z. They might be integers, not floating-point values.

## What about unknown coordinates?
This is where the problem arises: it's like looking for a pin in a hard haystack blindfolded. \
You don't know what's a pin and what's hard, unbreakable hay. So the program in its current form is more for reverse engineering based on known coordinates, but who knows what you could get out of it.

Play around with the code, maybe you'll find something.
