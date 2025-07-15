import graphene
from apps.orders.documents import BankAccount
from apps.orders.graphQL_type import BankAccountType


class BankAccountQuery(graphene.ObjectType):
    all_bank_accounts = graphene.List(
        BankAccountType,
        owner_name=graphene.String(),
        account_number=graphene.String()
    )

    def resolve_all_bank_accounts(self, info, owner_name=None, account_number=None):
        query = {}

        if owner_name:
            query['owner_name__icontains'] = owner_name

        if account_number:
            query['account_number__icontains'] = account_number

        return list(BankAccount.objects(**query))
