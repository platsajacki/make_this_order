from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from apps.orders.api.serializers import ShiftRevenueSerializer
from apps.orders.data_types import WorkingTime
from apps.orders.models import Order, OrderStatus
from core.services import BaseService


class ShiftRevenueGetter(BaseService):
    """
    Сервис для получения общей выручки за смену.

    Этот класс позволяет:
    1. Рассчитать период рабочей смены (начало и конец),
       основываясь на конфигурации рабочего времени (WORKING_HOURS_START и WORKING_HOURS) в настройках.
    2. Получить общую выручку за период смены, фильтруя заказы со статусом 'paid' в заданном временном интервале.
    """

    def get_working_time_period(self) -> WorkingTime | None:
        """
        Определяет текущий рабочий интервал времени (начало и конец смены).

        Рассчитывает начало смены на основе текущего времени и времени начала рабочего дня,
        а также определяет, попадает ли текущее время в этот интервал.

        Возвращает:
            - WorkingTime: Объект с началом и концом смены, если текущее время находится в пределах смены.
            - None: Если текущее время не попадает в рабочий интервал.
        """
        current_time = timezone.now()
        working_hours_start = datetime.strptime(settings.WORKING_HOURS_START, '%H:%M').time()
        shift_start = current_time.replace(hour=working_hours_start.hour, minute=0, second=0, microsecond=0)
        shift_end = shift_start + timedelta(hours=settings.WORKING_HOURS)
        if shift_start <= current_time <= shift_end:
            return WorkingTime(start=shift_start, end=current_time)
        return None

    def get_data(self, total_revenue: Decimal) -> dict:
        """
        Форматирует данные общей выручки для ответа.

        Аргументы:
            total_revenue: Общая выручка за смену.

        Возвращает:
            dict: Отформатированные данные с общей выручкой.
        """
        return ShiftRevenueSerializer({'total_revenue': total_revenue}).data

    def get_total_revenue(self) -> Decimal:
        """
        Получает общую выручку за текущую смену.

        Фильтрует заказы по статусу "PAID" и суммирует выручку в пределах рабочего интервала времени.

        Возвращает:
            Decimal: Общая выручка за смену (или 0, если выручка не найдена).
        """
        working_time_period = self.get_working_time_period()
        if not working_time_period:
            return Decimal(0)
        total_revenue = (
            Order.objects.filter(status=OrderStatus.PAID)
            .filter(created__gte=working_time_period.start, created__lte=working_time_period.end)
            .aggregate(total_revenue=Sum('total_price'))['total_revenue']
        )
        return total_revenue or Decimal(0)

    def act(self) -> Response:
        total_revenue = self.get_total_revenue()
        return Response(self.get_data(total_revenue), status=status.HTTP_200_OK)
