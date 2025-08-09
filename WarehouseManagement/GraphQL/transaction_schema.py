import graphene
from apps.warehouse.documents import Transaction
from apps.warehouse.graphql_type import TransactionType


class TransactionQuery(graphene.ObjectType):
    all_transactions = graphene.List(
        TransactionType,
        is_import=graphene.Boolean(),
        inventory_id=graphene.String()
    )

    def resolve_all_transactions(self, info, is_import=None, inventory_id=None):
        query = {}

        if is_import is not None:
            query['is_import'] = is_import

        if inventory_id:
            query['inventory'] = inventory_id

        return list(Transaction.objects(**query))
