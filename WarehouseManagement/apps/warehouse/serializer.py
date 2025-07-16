from apps.warehouse.documents import Warehouse, Inventory, Transaction
from utils.CustomSerializer.custom_serializer import CustomSerializer


class WarehouseSerializer(CustomSerializer):

    class Meta:
        model = Warehouse
        fields = '__all__'


class WarehouseSerializerPOST(CustomSerializer):

    class Meta:
        model = Warehouse
        fields = ['name', 'description', 'is_production_warehouse']


class InventorySerializer(CustomSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class InventorySerializerPOST(CustomSerializer):
    class Meta:
        model = Inventory
        fields = ['product', 'shelf_life', 'warehouse']


class TransactionSerializer(CustomSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionSerializerPOST(CustomSerializer):
    class Meta:
        model = Transaction
        fields = ['quantity', 'is_import', 'inventory', 'storage_location', 'description']