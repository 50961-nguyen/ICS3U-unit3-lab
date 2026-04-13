# Unit 2 Lab

## Instructions
This lab is broken up into three sections:

| Category | Max Grade |
|----------|-----------|
| Bronze   | 70%       |
| Silver   | 85%       |
| Gold     | 100%      |


### Reminders

* Do not forget header comments (author, date, description)
* Make sure your code has IPO comments in main().
* Make sure all of your functions have type annotations
* Make sure all of your functions have proper docstrings
    * A plain-English description of what the function does
    * An `Args:` section listing each parameter with its type and description
    * A `Returns:` section with the return type and description
    * An `Example:` section showing a sample function call and result
* Read through all of the tasks before you start. You'll note that they are not really that long.
* Submit your .py file as unit1_lab_tier.py (e.g., unit1_lab_gold.py) via GitHub
* Starter code at the bottom of this document. Copy it to complete your work. 
---

## Bronze Tier - Max Grade of 70%

You are the coach of a competitive speedcubing team (people who solve Rubik's Cubes really fast). After the latest tournament, you recorded the solve times (in seconds) for each member of your team:

```plaintext
solve_times = [12, 45, 8, 23, 31, 17, 52, 9]
```

As a data-driven coach, you want to analyze this data to figure out some key stats. Specifically, you want to know:

1. The total of all solve times combined (`total_time`)
2. The slowest solve time — the highest number (`slowest_solve`)
3. The fastest solve time — the lowest number (`fastest_solve`)


### Requirement
For Bronze, **you must write the complete docstrings yourself** for each of the three functions. Each docstring must include:
* A plain-English description
* An `Args:` section
* A `Returns:` section
* An `Example:` section

The test file *will* check that your docstrings are complete.

### Expected Output
```
Total of all solve times: 197 seconds
Slowest solve: 52 seconds
Fastest solve: 8 seconds
```

---

## Silver Tier - Max Grade of 85%

After the tournament, you discover something interesting about the scoring system. The judges have a "bonus round" rule:

If a competitor solved the cube in **less than 15 seconds**, their time stays the same because they were already fast enough. But if they took **15 seconds or more**, the judges apply a penalty: the score becomes the solve time **multiplied by 2** (because slow solves count double against the team).

You want to write a Python function to apply this penalty rule, then see how it changes the team's total.

### Requirements
Create a function called `apply_penalty(time: int) -> int` that takes in **one** solve time and transforms it based on the following rule:
- If the time is **less than 15**, return it as-is
- If the time is **15 or more**, return the time multiplied by 2

For example: if the time is `8`, the result is still `8`. If the time is `23`, the result is `46`.

Then, inside the main method:
1. Print the `sum` of the original list of solve times
2. Transform the list of solve times using the `apply_penalty` function and a for loop
3. Print the `sum` of the new, transformed, list of penalized times
4. Don't print anything but those two numbers!

### Expected Output
```
Total Original Time: 197 seconds
Total Time with Penality: 365 seconds
```
---

## Gold Tier - Max Grade of 100%
You and your friend Aria decide to create a "Cubing Name Power" ranking system. The idea is that a cuber's name contains hidden power based on specific letters:

A **power letter** is any of the following (case-sensitive!):

* `c` — because of "cube"
* `R` — because of "Rubik's" (capital R only!)
* `s` — because of "solve"
* `T` — because of "Timer" (capital T only!)

To calculate a cuber's **name power**, count how many power letters appear in their name. For example:
- `"Rascal"` has a name power of 3 (`R` + `s` + `c`)
- `"rascal"` has a name power of 2 (`s` + `c`) — lowercase `r` doesn't count!
- `"Tim"` has a name power of 1 (capital `T` counts!)
- `"John"` has a name power of 0: no power letters at all.

### Requirements
To complete this challenge:
* In the `main` function, allow the user to input exactly **6** names. Store each name in a list.
* In `calculate_power` function, it takes in a name (string) and returns the power level (int), calculate this value by counting all of the power letters in the name.
* Back in the main function, transform each element of the original list to its power count.
* The only thing I want you to print is the **sum** of all of the power counts in the list.

---

### Starter Code
```python
"""
HEADER COMMENTS
"""

# Bronze Functions to implement
def total_time(times: list[int]) -> int:
    """
    TODO: complete docstring
    """
    pass  # Replace with your code

def slowest_solve(times: list[int]) -> int:
    """
    TODO: complete docstring
    """
    pass  # Replace with your code

def fastest_solve(times: list[int]) -> int:
    """
    TODO: complete docstring
    """
    pass  # Replace with your code

# Silver Function to implement
def apply_penalty(time: int) -> int:
    """Applies the bonus-round penalty to a single solve time and returns that time.

    If the time is less than 15, it stays the same.
    If the time is 15 or more, it is doubled as a penalty.

    Args:
        time (int): The original solve time in seconds.

    Returns:
        int: The penalized solve time.

    Example:
    >>> apply_penalty(8)
    8
    >>> apply_penalty(23) 
    46
    """
    pass  # Replace with your code

# Gold Function to implement
def calculate_power(name: str) -> int:
    """Calculates the 'Cubing Name Power' of a given name.

    Counts the number of power letters in the name.
    Power letters (case-sensitive): 'c', 'R', 's', 'T'

    Args:
        name (str): The cuber's name to analyze.

    Returns:
        int: The total power level based on power letters found.

    Example:
    >>> calculate_power("Rascal")
    3
    >>> calculate_power("Tim")
    1
    """
    pass  # Replace with your code

def main():
    """Main program to run the entire lab. """
    # TODO: add IPO comments 
    solve_times = []  # Copy / paste the solve times from the instructions

    # TODO for Bronze: call the three functions by using solve_times as the argument and display the outputs. 
    # TODO for Silver: call apply_penalty function by using solve_times as the argument and display the original total time and the total time with penality
    # TODO for Gold: Collects cuber names, calculates power, and prints the total.
    
if __name__ == "__main__":
    main()
```