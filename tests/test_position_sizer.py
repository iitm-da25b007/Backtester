from src.position_sizer import PercentageOfEquitySizer

def test_position_size():

    sizer = PercentageOfEquitySizer(1.0)

    quantity = sizer.get_target_position(
        signal=1,
        equity=20000,
        price=1400
    )

    assert quantity == 14

def test_zero_signal():

    sizer = PercentageOfEquitySizer(1.0)

    quantity = sizer.get_target_position(
        signal=0,
        equity=20000,
        price=1400
    )

    assert quantity == 0