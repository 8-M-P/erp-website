from django.shortcuts import render

from core.models import Warehouse, WarehouseShelf
from front_end.forms import WarehouseForm, WarehouseShelfForm, WarehouseRackForm, WarehouseStockForm
from front_end.utils.crud import crud, crud_list, crud_delete


def warehouse(request, pk=None):
    return crud(request, 'front_end/pages/create_or_update/warehouse.html', Warehouse, WarehouseForm, pk)


def warehouse_dashboard(request):
    # TODO: Get all warehouses and their stock
    # TODO: Get most capacity used warehouse

    warehouse_pk = 1
    shelves = WarehouseShelf.objects.select_related('warehouse').filter(warehouse=warehouse_pk).order_by('shelf')
    # warehouse_name = table.first().warehouse.name
    for shelf in shelves:
        """
        shelf : 
            {
                'shelf': 'A',  # Shelf name
                'racks': [
                        { 
                            'name' : 'K1',
                            'order' : 1, 
                            'stock' : {'product' : 'product_name', 'quantity' : 12.00 },  # Stock object
                         },  # Rack object
                    ],
                'stock_count' : 1,  # Count of shelf stock
                'stock_percent' : 50.00,  # Percent of shelf stock
            }
        """
        shelf.racks = []
        racks = shelf.warehouserack_set.select_related('warehouse_shelf').filter(warehouse_shelf=shelf.id).order_by(
            'rack')
        shelf.stock_count = 0
        for rack in racks:
            rack.stock = None
            if rack.warehousestock_set.exists():
                rack.stock = rack.warehousestock_set.first()
                shelf.stock_count += 1
            shelf.racks.append(rack)

        def percent(part, whole):
            try:
                return round(100 * float(part) / float(whole), 2)
            except ZeroDivisionError:
                return 0

        shelf.stock_percent = percent(shelf.stock_count, len(shelf.racks))
        print(
            f"SHELF :{shelf.shelf} / Shelf Rack Count : {len(shelf.racks)}  / Shelf Stock Count : {shelf.stock_count} / Percent : {shelf.stock_percent}")
        # for x in shelf.racks:
        #     if x.stock:
        #         print(f"STOCK : {x.stock.product.name} / {x.stock.units}")
        # for rack in shelf.racks:
        #    print(rack)
        #    print(rack.stock)

    # print most capacity used shelf
    most_capacity_used_shelf = sorted(shelves, key=lambda x: x.stock_percent, reverse=True)[0]
    print(
        f"Most capacity used shelf : {most_capacity_used_shelf.shelf} / {len(most_capacity_used_shelf.racks)} / {most_capacity_used_shelf.stock_count} / {most_capacity_used_shelf.stock_percent}")
    return render(request, 'front_end/pages/list/warehouse.html')


def warehouse_delete(request, pk):
    return crud_delete(request, Warehouse, pk)
