use tes;
delete from zone where zone_id in('158708880021073','158708880021074','158708880021075','158708880021076');
INSERT INTO `zone` (`zone_id`, `zone_type`, `warehouse_id`, `map_id`, `map_ids`, `property`, `status`, `create_time`, `update_time`)
VALUES
('158708880021073', 22, '${warehouseID}', 11, '[1,11]', '{\"name\":\"传送位-1\",\"relatedConfs\":null,\"points\":[{\"nodeID\":\"309680989251074060\"},{\"nodeID\":\"1577944800046\"}],\"isNeedBindDevice\":0,\"transferPointType\":2}', 1, '2020-07-03 07:05:07', '2020-07-03 07:05:10'),
('158708880021074', 22, '${warehouseID}', 11, '[11]', '{\"name\":\"传送位-1\",\"relatedConfs\":null,\"points\":[{\"nodeID\":\"309680989251139596\"}],\"isNeedBindDevice\":0,\"transferPointType\":1}', 1, '2020-07-03 07:11:45', '2020-07-03 07:11:56'),
('158708880021075', 22, '${warehouseID}', 11, '[11,3]', '{\"name\":\"传送位-1\",\"relatedConfs\":null,\"points\":[{\"nodeID\":\"309680989251205132\"},{\"nodeID\":\"1587114000120\"}],\"isNeedBindDevice\":0,\"transferPointType\":2}', 1, '2020-07-03 07:11:51', '2020-07-03 07:11:57'),
('158708880021076', 22, '${warehouseID}', 11, '[11]', '{\"name\":\"传送位-1\",\"relatedConfs\":null,\"points\":[{\"nodeID\":\"309680989251270668\"}],\"isNeedBindDevice\":0,\"transferPointType\":1}', 1, '2020-07-03 07:11:53', '2020-07-03 07:11:59');

update map_info set map_type = 141 where map_id = 11;
update tes.map_info set  property ='{"offsetX":0,"offsetY":0,"offsetZ":0,"deviceTypes":["13"],"originMapID":"","width":0,"height":0}' where  map_id=12 and map_type=8 and warehouse_id='${warehouseID}';
update tes.conveyor_station set conveyor_station_id='sta_5' , conveyor_id='con_1' , buffer_cnt=8 where warehouse_id='${warehouseID}' and map_id=12 and node_id='309680989251467276' ;
INSERT INTO tes.conveyor_biz_register (warehouse_id, client_code, map_id, node_id, conveyor_id, reporter, conveyor_station_id, conveyor_zone_id, need_report, fake_map_id, create_time, update_time)
VALUES ('${warehouseID}', 'SUPER', 12, '309680989251729420', 'con_1', 'sen_1', '', '309680989252057100', '1', '0', '2020-08-09 10:19:26', '2020-08-09 10:19:29'),('${warehouseID}', 'SUPER', 12, '309680989251598348', 'con_1', 'sen_3', '', '309680989251926028', '1', '0', '2020-08-09 10:19:26', '2020-08-09 10:19:29');