from Create import validateLevels
from example1 import exampleLevel


def testValidateLevels():
    result = validateLevels(exampleLevel)
    assert result is True
