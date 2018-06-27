import numpy as np
import pytest

from hrv.rri import RRi, _validate_rri, _create_time_array, _validate_time
from tests.test_utils import FAKE_RRI


class TestRRiClassArguments:
    def test_transform_rri_to_numpy_array(self):
        validated_rri = _validate_rri(FAKE_RRI)
        np.testing.assert_array_equal(validated_rri, np.array(FAKE_RRI))

    def test_transform_rri_in_seconds_to_miliseconds(self):
        rri_in_seconds = [0.8, 0.9, 1.2]

        validated_rri = _validate_rri(rri_in_seconds)

        assert isinstance(validated_rri, np.ndarray)
        np.testing.assert_array_equal(
                _validate_rri(rri_in_seconds),
                [800, 900, 1200]
        )

    def test_rri_values(self):
        rri = RRi(FAKE_RRI).values

        assert isinstance(rri, np.ndarray)
        np.testing.assert_array_equal(rri, np.array(FAKE_RRI))

    def test_create_time_array(self):
        rri_time = _create_time_array(FAKE_RRI)

        assert isinstance(rri_time, np.ndarray)
        expected = np.cumsum(FAKE_RRI) / 1000
        expected -= expected[0]
        np.testing.assert_array_equal(rri_time, expected)

    def test_rri_time_auto_creation(self):
        rri = RRi(FAKE_RRI)
        expected = np.cumsum(FAKE_RRI) / 1000
        expected -= expected[0]

        np.testing.assert_array_equal(
            rri.time,
            expected
        )

    def test_rri_time_passed_as_argument(self):
        rri_time = [1, 2, 3, 4]
        rri = RRi(FAKE_RRI, rri_time)

        assert isinstance(rri.time, np.ndarray)
        np.testing.assert_array_equal(rri.time, np.array([1, 2, 3, 4]))

    def test_raises_exception_if_rri_and_time_havent_same_length(self):
        with pytest.raises(ValueError) as e:
            _validate_time(FAKE_RRI, [1, 2, 3])

        with pytest.raises(ValueError):
            RRi(FAKE_RRI, [1, 2, 3])

        assert e.value.args[0] == (
                'rri and time series must have the same length')

    def test_rri_and_time_have_same_length_in_class_construction(self):
        rri = RRi(FAKE_RRI, [1, 2, 3, 4])

        np.testing.assert_array_equal(rri.time, np.array([1, 2, 3, 4]))

    def test_time_has_no_zero_value_besides_in_first_position(self):
        with pytest.raises(ValueError) as e:
            _validate_time(FAKE_RRI, [1, 2, 0, 3])

        assert e.value.args[0] == (
                'time series cannot have 0 values after first position')

    def test_time_is_monotonically_increasing(self):
        with pytest.raises(ValueError) as e:
            _validate_time(FAKE_RRI, [0, 1, 4, 3])

        assert e.value.args[0] == (
                'time series must be monotonically increasing'
        )

    def test_time_series_have_no_negative_values(self):
        with pytest.raises(ValueError) as e:
            _validate_time(FAKE_RRI, [-1, 1, 2, 3])

        assert e.value.args[0] == ('time series cannot have negative values')

    def test_rri_series_have_no_negative_values(self):
        with pytest.raises(ValueError) as e:
            _validate_rri([0.0, 1.0, 2.0, 3.0])

        with pytest.raises(ValueError):
            _validate_rri([1.0, 2.0, -3.0, 4.0])

        assert e.value.args[0] == ('rri series can only have positive values')

    def test_rri_class_encapsulation(self):
        rri = RRi(FAKE_RRI)

        with pytest.raises(AttributeError):
            rri.rri = [1, 2, 3, 4]

        with pytest.raises(AttributeError):
            rri.time = [1, 2, 3, 4]

    def test_class_repr_short_array(self):
        rri = RRi([1, 2, 3, 4])

        assert rri.__repr__() == 'RRi array([1000., 2000., 3000., 4000.])'

    def test_class_repr_long_array(self):
        rri = RRi(range(1, 100000))

        assert rri.__repr__() == (
                'RRi array([1.0000e+00, 2.0000e+00, 3.0000e+00, ..., '
                '9.9997e+04, 9.9998e+04,\n       9.9999e+04])'
        )

    def test__mul__method(self):
        rri = RRi(FAKE_RRI)

        result = rri * 10

        assert isinstance(result, RRi)
        np.testing.assert_equal(result, rri.values * 10)

    def test__add__method(self):
        rri = RRi(FAKE_RRI)

        result = rri + 10

        assert isinstance(result, RRi)
        np.testing.assert_equal(result, rri.values + 10)

    def test__sub__method(self):
        rri = RRi(FAKE_RRI)

        result = rri - 10

        assert isinstance(result, RRi)
        np.testing.assert_equal(result, rri.values - 10)

    def test__truediv__method(self):
        rri = RRi(FAKE_RRI)

        result = rri / 10

        assert isinstance(result, RRi)
        np.testing.assert_equal(result, rri.values / 10)

    def test__abs__method(self):
        rri = RRi(FAKE_RRI)

        result = abs(rri)

        assert isinstance(result, RRi)
        np.testing.assert_equal(result, abs(rri.values))

    def test__eq__method(self):
        rri = RRi(FAKE_RRI)

        result = rri == 810

        np.testing.assert_equal(result, rri.values == 810)

    def test__ne__method(self):
        rri = RRi(FAKE_RRI)

        result = rri != 810

        np.testing.assert_equal(result, rri.values != 810)

    def test__gt__method(self):
        rri = RRi(FAKE_RRI)

        result = rri > 810

        np.testing.assert_equal(result, rri.values > 810)

    def test__ge__method(self):
        rri = RRi(FAKE_RRI)

        result = rri >= 810

        np.testing.assert_equal(result, rri.values >= 810)

    def test__lt__method(self):
        rri = RRi(FAKE_RRI)

        result = rri < 810

        np.testing.assert_equal(result, rri.values < 810)

    def test__le__method(self):
        rri = RRi(FAKE_RRI)

        result = rri <= 810

        np.testing.assert_equal(result, rri.values <= 810)

    def test__pow__method(self):
        rri = RRi(FAKE_RRI)

        result = rri ** 2

        np.testing.assert_equal(result, rri.values ** 2)


class TestRRiClassMethods:
    def test_rri_statistical_values(self):
        rri = RRi(FAKE_RRI)

        np.testing.assert_array_equal(rri.mean(),  np.mean(FAKE_RRI))
        np.testing.assert_array_equal(rri.var(),  np.var(FAKE_RRI))
        np.testing.assert_array_equal(rri.std(),  np.std(FAKE_RRI))
        np.testing.assert_array_equal(rri.median(),  np.median(FAKE_RRI))
        np.testing.assert_array_equal(rri.max(),  np.max(FAKE_RRI))
        np.testing.assert_array_equal(rri.min(),  np.min(FAKE_RRI))
        np.testing.assert_array_equal(
                rri.amplitude(),
                np.max(FAKE_RRI) - np.min(FAKE_RRI),
        )
        np.testing.assert_array_equal(
                rri.rms(),
                np.sqrt(np.mean(np.square(FAKE_RRI))),
        )

    def test_rri_describe(self):
        rri = RRi(FAKE_RRI)
        description = rri.describe()

        assert isinstance(description, dict)
        assert description.__repr__() == 'description'
        keys = ['min', 'max', 'amplitude', 'mean', 'median', 'var', 'std']

        for key in description.keys():
            assert key in keys

    def test_rri_to_hear_rate(self):
        rri = RRi(FAKE_RRI)
        heart_rate = rri.to_hr()
        expected = np.array([75., 74.07407407, 73.6196319, 80.])

        np.testing.assert_array_almost_equal(heart_rate, expected)
