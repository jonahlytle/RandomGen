Please describe how you might implement this more "pythonically"

- Utilise existing packages to optimise!
  - Use decimal.Decimal for high precision on the provided Probabilities to ensure that they sum to exactly 1.
  - To optimise the selection of the random element (currently (O(n))) there are a few levels of optimisations:

  1: (O(log n)) solution -> Use itertools.accumulate() to create a cumulative probability on initialisation and use bisect.bisect() to use binary search to iterate through and select the element.

  2: (O(1)) solution -> Use random.choices() to directly select the element.

  3: Better (O(1)) solution -> Migrate to using NumPy's random package, storing the numbers and probabilities as numpy arrays and using numpy.random.choice() to get the next_num.

      - Faster and more memory efficient than the built in Python random as it supports vectorised operations, parallelism, and is optimised for handling larger arrays.
