import pytest
from aiqa.models import validate

def test_validate():
    assert validate({"scenario":"x","expected":"y"}).scenario=="x"

def test_invalid():
    with pytest.raises(ValueError): validate({"scenario":"x"})
