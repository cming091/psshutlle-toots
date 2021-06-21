stock;

INSERT INTO container_stock (warehouse_code, region_code, container_code, sku_code, container_type, pallet_model, lot, grade, qty, abnormal_qty, reserved_qty, create_by, create_at, update_at, version, delete_flag)
VALUES('${warehouseCode}','${regionCode}','${containercode}', '${skucode}', '${containertype}', '${palletmodal}', 0, 0, '${qty}', 0, 0, 'test', NOW(), NOW(), 1, 0);

INSERT INTO container_relation(warehouse_code,region_code,container_code,create_by,create_at,update_at,delete_flag)
VALUES('${warehouseCode}', '${regionCode}', '${containercode}','test', NOW(), NOW(), 0);

INSERT region_stock (warehouse_code,region_code,sku_code,qty,abnormal_qty,reserved_qty,create_by,create_at,update_at,version,delete_flag,lot)
VALUES('${warehouseCode}', '${regionCode}', '${skucode}' , '${qty}', 0, 0, 'test', NOW(), NOW(), 1, 0,'${lot}');

