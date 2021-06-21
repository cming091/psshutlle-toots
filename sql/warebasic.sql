use warebasic;
delete from `warehouse` where 1=1;
delete from `warehouse_ext` where 1=1;
delete from `region` where 1=1;
delete from `storage` where 1=1;
delete from `station` where 1=1;
delete from `station_group` where 1=1;
delete from `outline_routing` where 1=1;
delete from `original_routing` where 1=1;
delete from `detail_routing` where 1=1;
delete from `station_action_type` where 1=1;

insert into `warehouse` (`warehouse_id`, `warehouse_code`, `warehouse_name`, `create_time`, `update_time`) values
    ('${warehouseID}', '${warehouseCode}', '金隅测试仓', now(), now());
insert into `warehouse_ext` (`warehouse_code`, `country`, `province`, `city`, `address`, `desc`, `create_time`, `update_time`) values
    ('${warehouseCode}', '中国', '北京市', '北京市', '金隅智造工场N6一层', 'FR项目业务测试仓库', now(), now());

insert into `region` (`warehouse_code`, `region_id`, `region_code`, `region_name`, `region_type`, `entry_point`, `create_time`, `update_time`) values
    ('${warehouseCode}', '15856484353', 'PSRegion', 'PS子仓', 1, '15856484353', now(), now()),
    ('${warehouseCode}', '158816872223', 'CTURegion', 'CTU子仓', 2, '158816872223', now(), now()),
    ('${warehouseCode}', '15905511616', 'FARegion', 'FlipAGV子仓', 3, '15905511616', now(), now()),
    ('${warehouseCode}', '', 'ReceRegion', '收货子仓', 4, '', now(), now()),
    ('${warehouseCode}', '', 'PeakRegion', '人工Peak子仓', 5, '', now(), now()),
    ('${warehouseCode}', '', 'ExchangeRegion', '换箱区', 6, '', now(), now());


insert into `storage` (`warehouse_code`, `region_code`, `storage_id`, `storage_code`, `storage_name`, `entry_point`, `create_time`, `update_time`) values
    ('${warehouseCode}', 'PSRegion', '158708880018003', 'PS-01-01', 'PS一层存储区一(3储位)', '158708880018003', now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880018000', 'PS-01-02', 'PS一层存储区二(2储位)', '158708880018000', now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880018020', 'PS-01-03', 'PS一层存储区三(6储位)', '158708880018020', now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880018023', 'PS-01-04', 'PS一层存储区四(9储位)', '158708880018023', now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880018065', 'PS-01-05', 'PS一层存储区五(1储位)', '158708880018065', now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880018103', 'PS-02-01', 'PS二层存储区一(3储位)', '158708880018103', now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880018100', 'PS-02-02', 'PS二层存储区二(2储位)', '158708880018100', now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880018120', 'PS-02-03', 'PS二层存储区三(6储位)', '158708880018120', now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880018123', 'PS-02-04', 'PS二层存储区三(9储位)', '158708880018123', now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880018164', 'PS-02-05', 'PS二层存储区五(2储位)', '158708880018164', now(), now()),
    ('${warehouseCode}', 'CTURegion', '158816872524', 'CTU-Storage', 'CTU存储区', '158816872524', now(), now());

insert into `station` (`warehouse_code`, `region_code`, `station_id`, `station_code`, `station_group_code`, `station_name`, `station_type`, `entry_point`, `node4device`, `trans_inv_flag`, `from_region`, `to_region`, `msg_flag`, `create_time`, `update_time`) values
    ('${warehouseCode}', 'PSRegion', '1', 'PS-Schedule', '', 'PS子仓起始站点', 99, '', '', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'CTURegion', '2', 'CTU-Schedule', '', 'CTU子仓起始站点', 99, '', '', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'FARegion', '3', 'FA-Schedule', '', 'FlipAGV子仓起始站点', 99, '', '', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'ReceRegion', '4', 'Rece-Schedule', '', '收货子仓起始站点', 99, '', '', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'PeakRegion', '5', 'Peak-Schedule', '', 'Peak区起始站点', 99, '', '', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'ExchangeRegion', '6', 'Exchange-Schedule', '', '换箱区起始站点', 99, '', '', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', '', 'sen_1', 'CTU-In-BCR', '', 'CTU收货BCR', 3, 'sen_1', 'sen_9', 1, '*', 'CTURegion', 1, now(), now()),
    ('${warehouseCode}', 'CTURegion', '15928133331', 'CTU-Couting-ST', '', '人工盘点工作站', 1, '15928133331', 'sen_5', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'CTURegion', '15911890841', 'CTU-Auto-Counting-ST', '', '自动盘点工作站', 3, '15911890841', 'sen_7', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'CTURegion', '15928133502', 'CTU-Out-ST', '', 'CTU出库工作站', 3, '15928133502', 'sen_3', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', '', 'sen_11', 'Exchange-In-BCR', 'Exchange-In-STG', '换箱区入库BCR', 3, 'sen_11', 'sen_11', 1, '*', 'ExchangeRegion', 1, now(), now()),
    ('${warehouseCode}', 'ExchangeRegion', 'sen_12', 'Exchange-OB-ST', 'Exchange-OB-STG', '换箱区原箱工作站', 3, 'sen_12', 'sen_12', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'ExchangeRegion', 'sen_13', 'Exchange-BB-ST', 'Exchange-BB-STG', '换箱区回箱工作站', 3, 'sen_13', 'sen_13', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'PSRegion', '309680989251336204', 'PS-PICK-001', 'PS-PICK-GROUP', '人工工作站', 1, '309680989251336204', '1,2', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'PSRegion', '309680989252057100', 'PS-PICK-002', '', 'BCR002', 3, '309680989252057100', 'sen_1', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'PSRegion', '309680989251926028', 'PS-PICK-003', '', 'BCR003', 3, '309680989251926028', 'sen_3', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'PSRegion', '158708880041025', 'PS-COLLECTOR', '', 'PS空托收集站点', 1, '158708880041025', '', 0, '', '', 1, now(), now()),
    ('${warehouseCode}', 'PSRegion', '309680989251401740', 'PS-IN-001', '', 'PS入库BCR1', 3, '309680989251401740', '', 1, '*', 'PSRegion', 1, now(), now()),
    ('${warehouseCode}', 'PSRegion', '309680989251401740', 'PS-IN-003', '', 'PS入库BCR3', 3, '309680989251401740', '', 1, '', '', 1, now(), now()),
    ('${warehouseCode}', 'PSRegion', '309680989251401740', 'PS-MOCK-BCR', '', 'PS出库BCR', 3, '309680989251401740', '', 0, '*', '', 1, now(), now()),
    ('${warehouseCode}', 'CTURegion', '309680989251860492', 'CTU-MOCK-BCR', '', 'CTU入库BCR', 3, '309680989251860492', '', 0, '', '', 1, now(), now());

insert into `station_group` (`warehouse_code`, `station_group_id`, `station_group_code`, `station_group_name`, `p_station_group_code`, `entry_point`, `trans_inv_flag`, `from_region`, `to_region`, `create_time`, `update_time`) values
    ('${warehouseCode}', '1001', 'Rece-STG-001', 'BoxCheck工作站组1', '', '', 0, '', '', now(), now()),
    ('${warehouseCode}', '1002', 'Rece-STG-002', 'BoxCheck工作站组2', '', '', 0, '', '', now(), now()),
    ('${warehouseCode}', '1003', 'Exchange-In-STG', '换箱区入库BCR组', '', '', 1, '*', 'ExchangeRegion', now(), now()),
    ('${warehouseCode}', '1004', 'Exchange-OB-STG', '换箱区原箱工作站组', '', '', 0, '', '', now(), now()),
    ('${warehouseCode}', '1005', 'Exchange-BB-STG', '换箱区回箱工作站组', '', '', 0, '', '', now(), now()),
    ('${warehouseCode}', '1006', 'PS-PICK-GROUP', 'PS子仓拣选工作站组', '', '', 0, '', '', now(), now());

insert into `outline_routing` (`warehouse_code`, `trans_type`, `from_region`, `to_region`, `create_time`, `update_time`) values
    ('${warehouseCode}', 1, 'PSRegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 2, 'PSRegion', 'ExchangeRegion', now(), now()),
    ('${warehouseCode}', 2, 'ExchangeRegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 4, 'CTURegion', 'FARegion', now(), now()),
    ('${warehouseCode}', 5, 'ReceRegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 8, 'CTURegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 9, 'CTURegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 10, 'CTURegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 11, 'CTURegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 12, 'CTURegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 101, 'PSRegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 102, 'PSRegion', 'CTURegion', now(), now()),
    ('${warehouseCode}', 22, 'PSRegion', 'PSRegion', now(), now()),
    ('${warehouseCode}', 13, 'ReceRegion', 'PSRegion', now(), now()),
    ('${warehouseCode}', 14, 'PSRegion', 'PSRegion', now(), now()),
    ('${warehouseCode}', 15, 'PSRegion', 'PSRegion', now(), now()),
    ('${warehouseCode}', 16, 'PSRegion', 'FARegion', now(), now()),
    ('${warehouseCode}', 17, 'ReceRegion', 'PSRegion', now(), now());

insert into `original_routing` (`warehouse_code`, `region_code`, `trans_type`, `original_station`, `create_time`, `update_time`) values
    ('${warehouseCode}', 'PSRegion', 1, 'PS-Schedule', now(), now()),
    ('${warehouseCode}', 'PSRegion', 2, 'PS-Schedule', now(), now()),
    ('${warehouseCode}', 'CTURegion', 4, 'CTU-Schedule', now(), now()),
    ('${warehouseCode}', 'ReceRegion', 5, 'CTU-In-BCR', now(), now()),
    ('${warehouseCode}', 'CTURegion', 8, 'CTU-Schedule', now(), now()),
    ('${warehouseCode}', 'CTURegion', 9, 'CTU-Schedule', now(), now()),
    ('${warehouseCode}', 'CTURegion', 10, 'CTU-Schedule', now(), now()),
    ('${warehouseCode}', 'CTURegion', 11, 'CTU-Couting-ST', now(), now()),
    ('${warehouseCode}', 'CTURegion', 12, 'CTU-Schedule', now(), now()),
    ('${warehouseCode}', 'PSRegion', 101, 'PS-Schedule', now(), now()),
    ('${warehouseCode}', 'PSRegion', 102, 'PS-Schedule', now(), now()),
    ('${warehouseCode}', 'PSRegion', 22, 'PS-Schedule', now(), now()),
    ('${warehouseCode}', 'PSRegion', 13, 'PS-IN-001', now(), now()),
    ('${warehouseCode}', 'PSRegion', 14, 'PS-PICK-GROUP', now(), now()),
    ('${warehouseCode}', 'PSRegion', 15, 'PS-PICK-GROUP', now(), now()),
    ('${warehouseCode}', 'PSRegion', 16, 'PS-Schedule', now(), now()),
    ('${warehouseCode}', 'ReceRegion', 17, 'PS-IN-001', now(), now());

insert into `detail_routing` (`warehouse_code`, `trans_type`, `from_station`, `from_station_type`, `to_station`, `to_station_type`, `condition`, `priority`, `create_time`, `update_time`) values
    ('${warehouseCode}', 1, 'PS-Schedule', 1, 'CTU-In-BCR', 1, '', 0, now(), now()),
    ('${warehouseCode}', 1, 'CTU-In-BCR', 1,  'CTU-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 2, 'PS-Schedule', 1, 'Exchange-In-STG', 2, '', 0, now(), now()),
    ('${warehouseCode}', 2, 'Exchange-In-STG', 2, 'Exchange-OB-STG', 2, '', 0, now(), now()),
    ('${warehouseCode}', 2, 'Exchange-OB-STG', 2, 'Exchange-BB-STG', 2, '', 0, now(), now()),
    ('${warehouseCode}', 2, 'Exchange-BB-STG', 2, 'CTU-In-BCR', 1, '', 0, now(), now()),
    ('${warehouseCode}', 2, 'CTU-In-BCR', 1,  'CTU-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 4, 'CTU-Schedule', 1, 'CTU-Out-ST', 1, '', 0, now(), now()),
    ('${warehouseCode}', 5, 'CTU-Couting-ST', 1, 'CTU-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 8, 'CTU-Schedule', 1, 'CTU-Auto-Counting-ST', 1, '', 0, now(), now()),
    ('${warehouseCode}', 8, 'CTU-Auto-Counting-ST', 1, 'CTU-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 9, 'CTU-Schedule', 1, 'CTU-Couting-ST', 1, '', 0, now(), now()),
    ('${warehouseCode}', 9, 'CTU-Couting-ST', 1, 'CTU-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 10, 'CTU-Schedule', 1, 'CTU-Couting-ST', 1, '', 0, now(), now()),
    ('${warehouseCode}', 10, 'CTU-Couting-ST', 1, 'CTU-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 11, 'CTU-Couting-ST', 1, 'CTU-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 12, 'CTU-Schedule', 1, 'CTU-Couting-ST', 1, '', 0, now(), now()),
    ('${warehouseCode}', 12, 'CTU-Couting-ST', 1, 'CTU-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 101, 'PS-Schedule', 1, 'PS-PICK-GROUP', 2, '', 0, now(), now()),
    ('${warehouseCode}', 101, 'PS-PICK-GROUP', 2, 'PS-PICK-003', 1, '', 0, now(), now()),
    ('${warehouseCode}', 101, 'PS-PICK-003', 1, 'CTU-MOCK-BCR', 1, '', 0, now(), now()),
    ('${warehouseCode}', 102, 'PS-Schedule', 1, 'PS-PICK-GROUP', 2, '', 0, now(), now()),
    ('${warehouseCode}', 102, 'PS-PICK-GROUP', 2, 'PS-PICK-002', 1, '', 0, now(), now()),
    ('${warehouseCode}', 102, 'PS-PICK-002', 1, 'CTU-MOCK-BCR', 1, '', 0, now(), now()),
    ('${warehouseCode}', 22, 'PS-Schedule', 1, 'PS-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 13, 'PS-IN-001', 1, 'PS-IN-003', 1, '', 0, now(), now()),
    ('${warehouseCode}', 13, 'PS-IN-003', 1, 'PS-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 14, 'PS-PICK-GROUP', 2, 'PS-COLLECTOR', 1, '', 0, now(), now()),
    ('${warehouseCode}', 15, 'PS-PICK-GROUP', 2, 'PS-Schedule', 1, '', 0, now(), now()),
    ('${warehouseCode}', 16, 'PS-Schedule', 1, 'PS-MOCK-BCR', 1, '', 0, now(), now()),
    ('${warehouseCode}', 17, 'PS-IN-001', 1, 'PS-IN-003', 1, '', 0, now(), now()),
    ('${warehouseCode}', 17, 'PS-IN-003', 1, 'PS-Schedule', 1, '', 0, now(), now());

insert into `station_action_type` (`warehouse_code`, `trans_type`, `station_code`, `action_type`, `create_time`, `update_time`) values
    ('${warehouseCode}', 1, 'PS-Schedule', '1', now(), now()),
    ('${warehouseCode}', 1, 'CTU-In-BCR', '3,1', now(), now()),
    ('${warehouseCode}', 1, 'CTU-Schedule', '1', now(), now()),
    ('${warehouseCode}', 2, 'PS-Schedule', '1', now(), now()),
    ('${warehouseCode}', 2, 'Exchange-In-STG', '5,1', now(), now()),
    ('${warehouseCode}', 2, 'Exchange-OB-STG', '10', now(), now()),
    ('${warehouseCode}', 2, 'Exchange-BB-STG', '6,7,113,1', now(), now()),
    ('${warehouseCode}', 2, 'CTU-In-BCR', '3,1', now(), now()),
    ('${warehouseCode}', 2, 'CTU-Schedule', '1', now(), now()),
    ('${warehouseCode}', 4, 'CTU-Schedule', '1', now(), now()),
    ('${warehouseCode}', 4, 'CTU-Out-ST', '3,1', now(), now()),
    ('${warehouseCode}', 5, 'CTU-Couting-ST', '3,1', now(), now()),
    ('${warehouseCode}', 5, 'CTU-Schedule', '1', now(), now()),
    ('${warehouseCode}', 8, 'CTU-Schedule', '1', now(), now()),
    ('${warehouseCode}', 8, 'CTU-Auto-Counting-ST', '4,1', now(), now()),
    ('${warehouseCode}', 9, 'CTU-Schedule', '1', now(), now()),
    ('${warehouseCode}', 9, 'CTU-Couting-ST', '4,1', now(), now()),
    ('${warehouseCode}', 10, 'CTU-Schedule', '1', now(), now()),
    ('${warehouseCode}', 10, 'CTU-Couting-ST', '6,7,111,1', now(), now()),
    ('${warehouseCode}', 11, 'CTU-Couting-ST', '3,1', now(), now()),
    ('${warehouseCode}', 11, 'CTU-Schedule', '1', now(), now()),
    ('${warehouseCode}', 12, 'CTU-Schedule', '1', now(), now()),
    ('${warehouseCode}', 101, 'PS-Schedule', '1', now(), now()),
    ('${warehouseCode}', 101, 'PS-PICK-GROUP', '3', now(), now()),
    ('${warehouseCode}', 101, 'PS-PICK-003', '6,7,113,1', now(), now()),
    ('${warehouseCode}', 101, 'CTU-MOCK-BCR', '3,1', now(), now()),
    ('${warehouseCode}', 102, 'PS-Schedule', '1', now(), now()),
    ('${warehouseCode}', 102, 'PS-PICK-GROUP', '3', now(), now()),
    ('${warehouseCode}', 102, 'PS-PICK-002', '6,7,113,1', now(), now()),
    ('${warehouseCode}', 102, 'CTU-MOCK-BCR', '3,1', now(), now()),
    ('${warehouseCode}', 22, 'PS-Schedule', '1', now(), now()),
    ('${warehouseCode}', 13, 'PS-IN-001', '3,1', now(), now()),
    ('${warehouseCode}', 13, 'PS-IN-003', '5,1', now(), now()),
    ('${warehouseCode}', 13, 'PS-Schedule', '1', now(), now()),
    ('${warehouseCode}', 14, 'PS-PICK-GROUP', '1', now(), now()),
    ('${warehouseCode}', 14, 'PS-COLLECTOR', '1', now(), now()),
    ('${warehouseCode}', 15, 'PS-PICK-GROUP', '1', now(), now()),
    ('${warehouseCode}', 15, 'PS-Schedule', '1', now(), now()),
    ('${warehouseCode}', 16, 'PS-Schedule', '1', now(), now()),
    ('${warehouseCode}', 17, 'PS-IN-001', '7,111,1', now(), now()),
    ('${warehouseCode}', 17, 'PS-IN-003', '6,1', now(), now()),
    ('${warehouseCode}', 17, 'PS-Schedule', '1', now(), now());