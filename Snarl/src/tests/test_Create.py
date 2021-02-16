from Create import validateLevels
from examples import exampleLevel


def testValidateLevels():
    result = validateLevels(exampleLevel)
    assert result is True
