import graphene
from apps.orders.documents import Payment
from apps.orders.graphQL_type import PaymentType


class PaymentQuery(graphene.ObjectType):
    all_payments = graphene.List(
        PaymentType,
        payment_type=graphene.String(),
        amount_min=graphene.Int(),
        amount_max=graphene.Int()
    )

    def resolve_all_payments(self, info, payment_type=None, amount_min=None, amount_max=None):
        query = {}

        if payment_type:
            query['payment_type'] = payment_type

        if amount_min is not None:
            query['amount__gte'] = amount_min

        if amount_max is not None:
            query['amount__lte'] = amount_max

        return list(Payment.objects(**query))
