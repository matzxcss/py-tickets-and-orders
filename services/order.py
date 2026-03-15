from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)

    order_data = {"user": user}
    if date:
        order_data["created_at"] = date

    order = Order.objects.create(**order_data)

    for ticket_item in tickets:
        ticket = Ticket(
            order=order,
            movie_session_id=ticket_item["movie_session"],
            row=ticket_item["row"],
            seat=ticket_item["seat"],
        )

        ticket.full_clean()
        ticket.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
