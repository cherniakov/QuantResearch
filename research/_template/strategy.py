import backtrader as bt

from signals import Signal, SMACrossSignal


class ResearchStrategy(bt.Strategy):
    """
    Торговая стратегия на основе сигналов внешнего генератора.

    Отвечает за:
    - получение торговых сигналов;
    - открытие и закрытие позиций;
    - контроль активных заявок;
    - обработку результатов исполнения заявок.

    Генерация сигналов вынесена в SMACrossSignal.
    Размер позиции определяется Sizer, настроенным в Backtrader.
    """

    params = (
        ("fast_period", 10),
        ("slow_period", 30),
    )

    def __init__(self):
        self.order = None
        self.signal_generator = SMACrossSignal(
            self.data,
            fast_period=self.p.fast_period,
            slow_period=self.p.slow_period,
        )

    def next(self):
        """
        Обрабатывает очередной бар исторических данных.

        Получает сигнал от генератора и при отсутствии активной
        заявки выполняет торговое действие:

        - BUY: открывает длинную позицию, если её нет.
        - SELL: закрывает существующую длинную позицию.
        - None: не выполняет никаких действий.

        Размер покупки определяется настроенным Backtrader Sizer.
        """
            
        if self.order is not None:
            return

        signal = self.signal_generator.get_signal()

        if signal is None:
            return

        if signal == Signal.BUY and not self.position:
            self.order = self.buy()

        elif signal == Signal.SELL and self.position:
            self.order = self.close()

    def notify_order(self, order):
        """
        Обрабатывает изменения состояния торговой заявки.

        Args:
            order (bt.Order): Заявка Backtrader.

        Обработка включает:
        - Submitted / Accepted: ожидание исполнения;
        - Completed: вывод информации об исполненной заявке;
        - Canceled / Margin / Rejected / Expired: вывод ошибки
        или причины завершения заявки.

        После завершения заявки освобождает ссылку self.order,
        позволяя стратегии отправлять новые заявки.
        """
        
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status == order.Completed:
            action = "BUY" if order.isbuy() else "SELL"

            print(
                f"{self.data.datetime.date(0)}: "
                f"EXECUTED {action}, "
                f"price={order.executed.price:.2f}, "
                f"size={order.executed.size}"
            )

        elif order.status in [
            order.Canceled,
            order.Margin,
            order.Rejected,
            order.Expired,
        ]:
            print(
                f"{self.data.datetime.date(0)}: "
                f"ORDER FAILED, status={order.getstatusname()}"
            )
            
        if not order.alive():
            self.order = None
