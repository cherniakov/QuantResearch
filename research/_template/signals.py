from enum import IntEnum

import backtrader as bt


class Signal(IntEnum):
    BUY = 1
    SELL = -1


class SMACrossSignal:
    """
    Генератор торговых сигналов на основе пересечения двух SMA.

    BUY — быстрая SMA пересекает медленную снизу вверх.
    SELL — быстрая SMA пересекает медленную сверху вниз.
    None — пересечения нет.

    Генератор не управляет позициями и не отправляет заявки.
    """

    def __init__(self, data, fast_period=10, slow_period=30):
        self.fast_sma = bt.indicators.SMA(
            data.close, period=fast_period
        )
        self.slow_sma = bt.indicators.SMA(
            data.close, period=slow_period
        )
        self.cross = bt.indicators.CrossOver(
            self.fast_sma, self.slow_sma
        )

    def get_signal(self):
        if self.cross[0] > 0:
            return Signal.BUY

        if self.cross[0] < 0:
            return Signal.SELL

        return None
