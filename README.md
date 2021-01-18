# PennyMac Code Test

## Problem Statement

Please complete the following in a dynamic language. 

1) In the attached file (w\_data.dat), you’ll find daily weather data.
Download this text file, then write a program to output the day number (column
one) with the smallest temperature spread (the maximum temperature is the
second column, the minimum the third column).

2) The attached soccer.dat file contains the results from the English Premier
League.  The columns labeled ‘F’ and ‘A’ contain the total number of goals
scored for and against each team in that season (so Arsenal scored 79 goals
against opponents, and had 36 goals scored against them). Write a program to
print the name of the team with the smallest difference in ‘for’ and ‘against’
goals.

Is the way you wrote the second program influenced by writing the first?

**Please put your response on github and send the link upon completion.

## Solution

### Requirements

Compatible with Python 3.9.

### Smallest Temperature Spread

Run with the provided weather file:

    python3 pnmac.py weather

Or run with a custom weather file:

    python3 pnmac.py weather my-weather-data.dat

### Smallest Soccer Score Difference

Run with the provided soccer file:

    python3 pnmac.py soccer

Or run with a custom soccer file:

    python3 pnmac.py soccer my-soccer-data.dat

### Discussion

Most of the code from part one was reused for part two (both data files were
reviewed ahead of time). For part two, the `parse_fixed_width_data` function
was enhanced a bit, e.g., to handle the horizontal "divider" line.

