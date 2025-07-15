import graphene
from apps.orders.documents import Invoice
from apps.orders.graphQL_type import InvoiceType


class InvoiceQuery(graphene.ObjectType):
    all_invoices = graphene.List(
        InvoiceType,
        invoice_number=graphene.String(),
        title=graphene.String(),
        is_paid=graphene.Boolean()
    )

    def resolve_all_invoices(self, info, invoice_number=None, title=None, is_paid=None):
        query = {}

        if invoice_number:
            query['invoice_number__icontains'] = invoice_number

        if title:
            query['title__icontains'] = title

        if is_paid is not None:
            query['is_paid'] = is_paid

        return list(Invoice.objects(**query))
