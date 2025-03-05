import random
import unittest

class RandomGen(object):
    # Values that may be returned by next_num()
    _random_nums = []

    # Probability of the occurence of random_nums
    _probabilities = []

    def __init__(self, nums, probabilities):
        if not all(isinstance(n, (int, float)) for n in nums):
            raise TypeError("All elements must be numbers.")
        
        if not all(isinstance(p, (int, float)) and p <= 1 and p >= 0 for p in probabilities):
            raise TypeError("All elements must be probabilities between 0 and 1 inclusive.")

        if len(nums) != len(probabilities):
            raise ValueError("Each number must have a probability.")
        
        if (round(sum(probabilities), 10) != 1):
            raise ValueError("Probabilities must sum to 1.")

        self._random_nums = nums
        self._probabilities = probabilities

    def next_num(self):
        """
        Returns one of the randomNums. When this method is called multiple
        times over a long period, it should return the numbers roughly with
        the initialized probabilities.
        """
        rand = random.random()

        probability_sum = 0

        # Iterate through summed probabilities.
        # If random number is less than sum, return the number at that index.
        for index, probability in enumerate(self._probabilities):
            probability_sum += probability
            if rand < probability_sum:
                return self._random_nums[index]
        
        # Should never happen.
        raise Exception("An unexpected error occured.")

# Unit tests.
class TestRandomGen(unittest.TestCase):
    def setUp(self):
        self.random_generator = RandomGen([-1, 0, 1, 2, 3], [0.01, 0.3, 0.58, 0.1, 0.01])

    def test_distribution(self):
        """
        Run next_num() 1,000,000 times and verify the approximate distribution.
        """
        num_runs = 1000000
        results = {num: 0 for num in self.random_generator._random_nums}

        for _ in range(num_runs):
            num = self.random_generator.next_num()
            results[num] += 1

        # Convert to approximate probabilities.
        actual_probabilities = {num: count / num_runs for num, count in results.items()}
        expected_probabilities = dict(zip(self.random_generator._random_nums, self.random_generator._probabilities))

        # Validate results within a reasonable margin (2%).
        for num in expected_probabilities:
            self.assertAlmostEqual(actual_probabilities[num], expected_probabilities[num], delta=0.02)

    def test_valid_numbers(self):
        """
        Ensure that next_num() always returns one of the expected numbers.
        """
        for _ in range(1000000):
            num = self.random_generator.next_num()
            self.assertIn(num, self.random_generator._random_nums)
    
    def test_init_with_invalid_numbers_fails(self):
        """
        Ensure that initialisation throws exception with invalid numbers.
        """
        with self.assertRaisesRegex(TypeError, "All elements must be numbers."):
            RandomGen(["test", 1, 2, 3, 4], [0.01, 0.3, 0.58, 0.1, 0.01])
    
    def test_init_with_invalid_probabilities_fails(self):
        """
        Ensure that initialisation throws exception with invalid probabilities.
        """
        with self.assertRaisesRegex(TypeError, "All elements must be probabilities between 0 and 1 inclusive."):
            RandomGen([0, 1, 2, 3, 4], [-0.01, 0.3, 0.58, 0.1, 0.01])

    def test_init_with_invalid_counts_fails(self):
        """
        Ensure that initialisation throws exception with invalid probabilities.
        """
        with self.assertRaisesRegex(ValueError, "Each number must have a probability."):
            RandomGen([0, 1, 2, 3], [0.01, 0.3, 0.58, 0.1, 0.01])
    
    def test_init_with_invalid_probabilities_sum_fails(self):
        """
        Ensure that initialisation throws exception with invalid probabilities.
        """
        with self.assertRaisesRegex(ValueError, "Probabilities must sum to 1."):
            RandomGen([0, 1, 2, 3, 4], [0.01, 0.6, 0.58, 0.1, 0.01])

if __name__ == "__main__":
    unittest.main()

