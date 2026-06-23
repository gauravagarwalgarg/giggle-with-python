"""
unittest Examples the standard library testing framework.

Demonstrates unittest patterns: TestCase, setUp/tearDown, assertions,
mocking, and class-based test organization. Use when pytest isn't available
or when working with codebases that already use unittest.

Adapted from code_snippets/Python-Unit-Testing.
"""
import unittest
from unittest.mock import patch, MagicMock


# =============================================================================
# CODE UNDER TEST
# =============================================================================

class Calculator:
    """Simple calculator adapted from code_snippets/Python-Unit-Testing/calc.py."""

    def add(self, x: float, y: float) -> float:
        return x + y

    def subtract(self, x: float, y: float) -> float:
        return x - y

    def multiply(self, x: float, y: float) -> float:
        return x * y

    def divide(self, x: float, y: float) -> float:
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y


class Employee:
    """Employee class adapted from code_snippets/Python-Unit-Testing/employee.py.

    Demonstrates a class with external dependencies (HTTP call)
    that we'll mock in tests.
    """

    raise_amount = 1.05  # 5% raise

    def __init__(self, first: str, last: str, pay: int):
        self.first = first
        self.last = last
        self.pay = pay

    @property
    def email(self) -> str:
        return f"{self.first}.{self.last}@email.com"

    @property
    def fullname(self) -> str:
        return f"{self.first} {self.last}"

    def apply_raise(self) -> None:
        self.pay = int(self.pay * self.raise_amount)

    def monthly_schedule(self, month: str) -> str:
        """Calls an external API simulated for testing with mocks."""
        try:
            import requests
            response = requests.get(f"http://company.com/{self.last}/{month}")
            if response.ok:
                return response.text
            return "Bad Response!"
        except ImportError:
            return f"Schedule for {month}"


# =============================================================================
# BASIC TEST CASE
# =============================================================================

class TestCalculator(unittest.TestCase):
    """Basic unittest.TestCase for Calculator.

    Adapted from code_snippets/Python-Unit-Testing/test_calc.py.
    """

    def setUp(self):
        """Run before EACH test method. Create fresh calculator."""
        self.calc = Calculator()

    def test_add(self):
        """Test addition with various inputs."""
        self.assertEqual(self.calc.add(10, 5), 15)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 5), 5)
        self.assertEqual(self.calc.subtract(-1, 1), -2)
        self.assertEqual(self.calc.subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(10, 5), 50)
        self.assertEqual(self.calc.multiply(-1, 1), -1)
        self.assertEqual(self.calc.multiply(-1, -1), 1)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 5), 2)
        self.assertEqual(self.calc.divide(-1, 1), -1)
        self.assertEqual(self.calc.divide(5, 2), 2.5)

    def test_divide_by_zero_raises(self):
        """Test that dividing by zero raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_divide_by_zero_message(self):
        """Test the specific error message."""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertIn("zero", str(context.exception))


# =============================================================================
# SETUP AND TEARDOWN PATTERNS
# =============================================================================

class TestEmployee(unittest.TestCase):
    """Demonstrates setUp/tearDown lifecycle methods.

    Adapted from code_snippets/Python-Unit-Testing/test_employee.py.
    """

    @classmethod
    def setUpClass(cls):
        """Run ONCE before all tests in this class.

        Use for expensive setup like database connections.
        """
        # print("setUpClass: one-time setup")
        pass

    @classmethod
    def tearDownClass(cls):
        """Run ONCE after all tests in this class."""
        # print("tearDownClass: one-time cleanup")
        pass

    def setUp(self):
        """Run before EACH test creates fresh test data."""
        self.emp_1 = Employee("Corey", "Schafer", 50000)
        self.emp_2 = Employee("Sue", "Smith", 60000)

    def tearDown(self):
        """Run after EACH test cleanup resources."""
        pass

    def test_email(self):
        """Test email property is constructed correctly."""
        self.assertEqual(self.emp_1.email, "Corey.Schafer@email.com")
        self.assertEqual(self.emp_2.email, "Sue.Smith@email.com")

    def test_email_updates_with_name(self):
        """Email should reflect name changes (it's a property)."""
        self.emp_1.first = "John"
        self.assertEqual(self.emp_1.email, "John.Schafer@email.com")

    def test_fullname(self):
        self.assertEqual(self.emp_1.fullname, "Corey Schafer")
        self.assertEqual(self.emp_2.fullname, "Sue Smith")

    def test_apply_raise(self):
        """Test that raise is applied correctly (5%)."""
        self.emp_1.apply_raise()
        self.assertEqual(self.emp_1.pay, 52500)

        self.emp_2.apply_raise()
        self.assertEqual(self.emp_2.pay, 63000)


# =============================================================================
# MOCKING EXTERNAL DEPENDENCIES
# =============================================================================

class TestEmployeeMocking(unittest.TestCase):
    """Demonstrate mocking HTTP requests in tests.

    Adapted from code_snippets/Python-Unit-Testing/test_employee.py.
    When code calls an external API, we mock it to:
    - Make tests fast (no network calls)
    - Make tests reliable (no dependency on external services)
    - Control the response for testing different scenarios
    """

    def setUp(self):
        self.emp = Employee("Corey", "Schafer", 50000)

    @patch("requests.get")
    def test_monthly_schedule_success(self, mock_get):
        """Mock a successful API response."""
        # Configure the mock
        mock_get.return_value.ok = True
        mock_get.return_value.text = "Meeting at 9am\nLunch at noon"

        # Call the method
        schedule = self.emp.monthly_schedule("May")

        # Verify the result
        self.assertEqual(schedule, "Meeting at 9am\nLunch at noon")

        # Verify the mock was called correctly
        mock_get.assert_called_once_with("http://company.com/Schafer/May")

    @patch("requests.get")
    def test_monthly_schedule_failure(self, mock_get):
        """Mock a failed API response."""
        mock_get.return_value.ok = False

        schedule = self.emp.monthly_schedule("June")

        self.assertEqual(schedule, "Bad Response!")
        mock_get.assert_called_once_with("http://company.com/Schafer/June")


# =============================================================================
# ASSERTION METHODS common assertions available in TestCase
# =============================================================================

class TestAssertionMethods(unittest.TestCase):
    """Reference for commonly used assertions."""

    def test_equality(self):
        self.assertEqual(1 + 1, 2)
        self.assertNotEqual(1 + 1, 3)

    def test_truthiness(self):
        self.assertTrue(True)
        self.assertFalse(False)
        self.assertIsNone(None)
        self.assertIsNotNone("something")

    def test_comparison(self):
        self.assertGreater(5, 3)
        self.assertGreaterEqual(5, 5)
        self.assertLess(3, 5)
        self.assertLessEqual(5, 5)

    def test_membership(self):
        self.assertIn("a", "abc")
        self.assertNotIn("d", "abc")
        self.assertIn(1, [1, 2, 3])

    def test_types(self):
        self.assertIsInstance([], list)
        self.assertIsInstance("hello", str)
        self.assertNotIsInstance([], dict)

    def test_identity(self):
        a = [1, 2, 3]
        b = a
        c = [1, 2, 3]
        self.assertIs(a, b)      # Same object
        self.assertIsNot(a, c)   # Different objects (same value)

    def test_approximate_equality(self):
        """For floating point comparisons."""
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=10)

    def test_regex_match(self):
        self.assertRegex("hello world", r"hello \w+")
        self.assertNotRegex("hello world", r"^world")

    def test_collections(self):
        """Compare collections regardless of order."""
        self.assertCountEqual([1, 2, 3], [3, 2, 1])  # Same elements, any order


# =============================================================================
# SKIPPING TESTS
# =============================================================================

class TestSkipping(unittest.TestCase):
    """Demonstrate test skipping patterns."""

    @unittest.skip("Feature not implemented yet")
    def test_future_feature(self):
        """This test is always skipped."""
        self.fail("Should not run")

    @unittest.skipIf(True, "Condition met, skipping")
    def test_conditional_skip(self):
        """Skipped based on a condition."""
        pass

    @unittest.expectedFailure
    def test_known_bug(self):
        """Expected to fail won't count as a test failure."""
        self.assertEqual(1 + 1, 3)


# =============================================================================
# SUBTESTS run multiple checks in one test method
# =============================================================================

class TestSubTests(unittest.TestCase):
    """Use subTest() to continue running after a failure."""

    def test_squares(self):
        """Test multiple inputs all failures are reported."""
        test_cases = [
            (2, 4),
            (3, 9),
            (4, 16),
            (5, 25),
            (-3, 9),
        ]
        for value, expected in test_cases:
            with self.subTest(value=value):
                self.assertEqual(value ** 2, expected)


if __name__ == "__main__":
    # Run all tests with verbose output
    unittest.main(verbosity=2)
