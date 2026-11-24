import backtrader as bt


class FinamCommission(bt.CommInfoBase):
    """ Брокерская коммисия в Финам
        минимальная 50 рублей или 0.05% от сделки
    """
    params = (
        ('commission', 0.0005),
        ('min_commission', 50.0),
        ('commtype', bt.CommInfoBase.COMM_PERC),
        ('stocklike', True),
        ('percabs', True),
    )

    def _getcommission(self, size, price, pseudoexec):
        commission = abs(size) * price * self.p.commission
        return max(commission, self.p.min_commission)
