SKU="""INSERT INTO warebasic.sku (rent_id, sku_code, sku_name, dept_no, item, band, length, width, height, volume, weight, price, pick_unit, sku_label, manage_flag, create_by, create_time, update_by, update_time, ip_address, del_flag, field1, field2, field3, field4, field5) VALUES

('', 'a', 'A', 'deptNo1', 'item11', 10, 10, 10, 20, 380, 200, 198.00, 20, 1, 3, '', '2020-08-31 11:58:52', '', '2020-08-31 11:58:52', 0, 0, '', '', '', '', ''),

('', 'b', 'B', 'deptNo1', 'item11', 10, 10, 10, 20, 270, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:00:28', '', '2020-08-31 12:00:28', 0, 0, '', '', '', '', ''),

('', 'c', 'C', 'deptNo1', 'item11', 10, 10, 10, 20, 420, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:01:29', '', '2020-08-31 12:01:29', 0, 0, '', '', '', '', ''),

('', 'd', 'D', 'deptNo1', 'item12', 10, 10, 10, 20, 260, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:02:11', '', '2020-08-31 12:02:11', 0, 0, '', '', '', '', ''),

('', 'e', 'E', 'deptNo1', 'item13', 10, 10, 10, 20, 330, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:03:22', '', '2020-08-31 12:03:22', 0, 0, '', '', '', '', ''),

('', 'f', 'F', 'deptNo2', 'item21', 10, 10, 10, 20, 220, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:05:06', '', '2020-08-31 12:05:06', 0, 0, '', '', '', '', ''),

('', 'g', 'G', 'deptNo2', 'item22', 10, 10, 10, 20, 510, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:05:22', '', '2020-08-31 12:08:29', 0, 0, '', '', '', '', ''),

('', 'h', 'H', 'deptNo3', 'item31', 10, 10, 10, 20, 190, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:07:17', '', '2020-08-31 12:07:17', 0, 0, '', '', '', '', ''),

('', 'i', 'I', 'deptNo3', 'item31', 10, 10, 10, 20, 290, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:07:40', '', '2020-08-31 13:39:41', 0, 0, '', '', '', '', ''),

('', 'j', 'J', 'deptNo3', 'item33', 10, 10, 10, 20, 360, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:07:59', '', '2020-08-31 12:09:10', 0, 0, '', '', '', '', '') ON DUPLICATE KEY UPDATE create_time=now();

INSERT INTO warebasic.sku (rent_id, sku_code, sku_name, dept_no, item, band, length, width, height, volume, weight, price, pick_unit, sku_label, manage_flag, create_by, create_time, update_by, update_time, ip_address, del_flag, field1, field2, field3, field4, field5) VALUES

('', '1001', '1001', 'deptNo1', 'item11', 10, 10, 10, 20, 380, 200, 198.00, 20, 1, 3, '', '2020-08-31 11:58:52', '', '2020-08-31 11:58:52', 0, 0, '', '', '', '', ''),

('', '1002', '1002', 'deptNo1', 'item11', 10, 10, 10, 20, 270, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:00:28', '', '2020-08-31 12:00:28', 0, 0, '', '', '', '', ''),

('', '1003', '1003', 'deptNo1', 'item11', 10, 10, 10, 20, 420, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:01:29', '', '2020-08-31 12:01:29', 0, 0, '', '', '', '', ''),

('', '1004', '1004', 'deptNo1', 'item12', 10, 10, 10, 20, 260, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:02:11', '', '2020-08-31 12:02:11', 0, 0, '', '', '', '', ''),

('', '1005', '1005', 'deptNo1', 'item13', 10, 10, 10, 20, 330, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:03:22', '', '2020-08-31 12:03:22', 0, 0, '', '', '', '', ''),

('', '1006', '1006', 'deptNo2', 'item21', 10, 10, 10, 20, 220, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:05:06', '', '2020-08-31 12:05:06', 0, 0, '', '', '', '', ''),

('', '1007', '1007', 'deptNo2', 'item22', 10, 10, 10, 20, 510, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:05:22', '', '2020-08-31 12:08:29', 0, 0, '', '', '', '', ''),

('', '1008', '1008', 'deptNo3', 'item31', 10, 10, 10, 20, 190, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:07:17', '', '2020-08-31 12:07:17', 0, 0, '', '', '', '', ''),

('', '1009', '1009', 'deptNo3', 'item31', 10, 10, 10, 20, 290, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:07:40', '', '2020-08-31 13:39:41', 0, 0, '', '', '', '', ''),

('', '1010', '1010', 'deptNo3', 'item33', 10, 10, 10, 20, 360, 200, 198.00, 20, 1, 3, '', '2020-08-31 12:07:59', '', '2020-08-31 12:09:10', 0, 0, '', '', '', '', '') ON DUPLICATE KEY UPDATE create_time=now();

INSERT INTO warebasic.sku_ext (rent_id, sku_code, sku_type, color, size, pattern, year_season, cost_seq, assort_code, sku_desc, min_stock, max_stock, create_by, create_time, update_by, update_time, ip_address, del_flag) VALUES

('', 'a', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 12, 20, '', '2020-08-31 11:58:52', '', '2020-08-31 11:58:52', 0, 0),

('', 'b', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 18, 30, '', '2020-08-31 12:00:28', '', '2020-08-31 12:00:28', 0, 0),

('', 'c', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 30, 50, '', '2020-08-31 12:01:29', '', '2020-08-31 12:01:29', 0, 0),

('', 'd', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 22, 37, '', '2020-08-31 12:02:11', '', '2020-08-31 12:02:11', 0, 0),

('', 'e', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 36, 60, '', '2020-08-31 12:03:22', '', '2020-08-31 12:03:22', 0, 0),

('', 'f', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 27, 45, '', '2020-08-31 12:05:06', '', '2020-08-31 12:05:06', 0, 0),

('', 'g', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 33, 55, '', '2020-08-31 12:05:22', '', '2020-08-31 12:05:22', 0, 0),

('', 'h', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 60, 100, '', '2020-08-31 12:07:17', '', '2020-08-31 12:07:17', 0, 0),

('', 'i', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 54, 90, '', '2020-08-31 12:07:40', '', '2020-08-31 12:07:40', 0, 0),

('', 'j', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 42, 70, '', '2020-08-31 12:07:59', '', '2020-08-31 12:07:59', 0, 0),

('', '1001', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 12, 20, '', '2020-08-31 11:58:52', '', '2020-08-31 11:58:52', 0, 0),

('', '1002', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 18, 30, '', '2020-08-31 12:00:28', '', '2020-08-31 12:00:28', 0, 0),

('', '1003', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 30, 50, '', '2020-08-31 12:01:29', '', '2020-08-31 12:01:29', 0, 0),

('', '1004', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 22, 37, '', '2020-08-31 12:02:11', '', '2020-08-31 12:02:11', 0, 0),

('', '1005', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 36, 60, '', '2020-08-31 12:03:22', '', '2020-08-31 12:03:22', 0, 0),

('', '1006', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 27, 45, '', '2020-08-31 12:05:06', '', '2020-08-31 12:05:06', 0, 0),

('', '1007', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 33, 55, '', '2020-08-31 12:05:22', '', '2020-08-31 12:05:22', 0, 0),

('', '1008', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 60, 100, '', '2020-08-31 12:07:17', '', '2020-08-31 12:07:17', 0, 0),

('', '1009', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 54, 90, '', '2020-08-31 12:07:40', '', '2020-08-31 12:07:40', 0, 0),

('', '1010', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 42, 70, '', '2020-08-31 12:07:59', '', '2020-08-31 12:07:59', 0, 0) ON DUPLICATE KEY UPDATE create_time=now();

INSERT INTO warebasic.sku_package (rent_id, sku_code, carton_type_id, package_amount, package_weight, create_by, create_time, update_by, update_time, ip_address, del_flag) VALUES ('', 'a', '317620771172122651', 8, 0, '', '2020-08-31 11:58:52', '', '2020-08-31 11:58:52', 0, 0),

('', 'b', '317620932417945627', 12, 0, '', '2020-08-31 12:00:28', '', '2020-08-31 12:00:28', 0, 0),

('', 'c', '317621033299345435', 20, 0, '', '2020-08-31 12:01:29', '', '2020-08-31 12:01:29', 0, 0),

('', 'd', '317621104770285595', 15, 0, '', '2020-08-31 12:02:11', '', '2020-08-31 12:02:11', 0, 0),

('', 'e', '317621223250984987', 24, 0, '', '2020-08-31 12:03:22', '', '2020-08-31 12:03:22', 0, 0),

('', 'f', '317621397230714907', 18, 0, '', '2020-08-31 12:05:06', '', '2020-08-31 12:05:06', 0, 0),

('', 'g', '317621424896344091', 22, 0, '', '2020-08-31 12:05:22', '', '2020-08-31 12:05:22', 0, 0),

('', 'h', '317621617465229339', 40, 0, '', '2020-08-31 12:07:17', '', '2020-08-31 12:07:17', 0, 0),

('', 'i', '317621656287707163', 36, 0, '', '2020-08-31 12:07:40', '', '2020-08-31 12:07:40', 0, 0),

('', 'j', '317621688902615067', 28, 0, '', '2020-08-31 12:07:59', '', '2020-08-31 12:07:59', 0, 0),

('', '1001', '317620771172122651', 8, 0, '', '2020-08-31 11:58:52', '', '2020-08-31 11:58:52', 0, 0),

('', '1002', '317620932417945627', 12, 0, '', '2020-08-31 12:00:28', '', '2020-08-31 12:00:28', 0, 0),

('', '1003', '317621033299345435', 20, 0, '', '2020-08-31 12:01:29', '', '2020-08-31 12:01:29', 0, 0),

('', '1004', '317621104770285595', 15, 0, '', '2020-08-31 12:02:11', '', '2020-08-31 12:02:11', 0, 0),

('', '1005', '317621223250984987', 24, 0, '', '2020-08-31 12:03:22', '', '2020-08-31 12:03:22', 0, 0),

('', '1006', '317621397230714907', 18, 0, '', '2020-08-31 12:05:06', '', '2020-08-31 12:05:06', 0, 0),

('', '1007', '317621424896344091', 22, 0, '', '2020-08-31 12:05:22', '', '2020-08-31 12:05:22', 0, 0),

('', '1008', '317621617465229339', 40, 0, '', '2020-08-31 12:07:17', '', '2020-08-31 12:07:17', 0, 0),

('', '1009', '317621656287707163', 36, 0, '', '2020-08-31 12:07:40', '', '2020-08-31 12:07:40', 0, 0),

('', '1010', '317621688902615067', 28, 0, '', '2020-08-31 12:07:59', '', '2020-08-31 12:07:59', 0, 0) ON DUPLICATE KEY UPDATE create_time=now();

INSERT INTO warebasic.carton_type (rent_id, carton_type_id, length, width, height, volume, specification, wrapping_flag, auto_stacking_flag, recycling_flag, create_by, create_time, update_by, update_time, ip_address, del_flag) VALUES

('', '319794813606035485', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317620771172122651', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317620932417945627', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317621033299345435', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317621104770285595', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317621223250984987', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317621397230714907', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317621424896344091', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317621617465229339', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317621656287707163', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '317621688902615067', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),

('', '319794813606035485', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0) ON DUPLICATE KEY UPDATE create_time=now();

"""

SKU_TEMP_FIELD = """rent_id, sku_code, sku_name, dept_no, item, band, length, width, height, volume, 
weight, price, pick_unit, sku_label, manage_flag, create_by, create_time, update_by, update_time, ip_address, 
del_flag, sku_type,color,size,pattern,year_season,cost_seq,assort_code,sku_desc,min_stock,max_stock,
carton_type_id,package_amount,package_weight,specification,wrapping_flag,auto_stacking_flag,recycling_flag
"""
SKU_TEMP = {'rent_id':'','sku_code':'','sku_name':'','dept_no':'',
            'item':'','band':'','length':'','width':'','height':'',
            'width':'','height':'','volume':'','weight':'','price':'',
            'pick_unit':'','sku_label':'','manage_flag':'','create_by':'',
            'create_time':'','update_by':'','update_time':'','ip_address':'',
            'del_flag':'','sku_type':'','color':'','size':'','pattern':'',
            'year_season':'','cost_seq':'','assort_code':'','sku_desc':'',
            'min_stock':'','max_stock':'','carton_type_id':'','package_amount':'',
            'package_weight':'','specification':'','wrapping_flag':'','auto_stacking_flag':'',
            'recycling_flag':'',
            }


def skuData(configData):#一种sku
    sql ="""INSERT INTO warebasic.sku 
                  (rent_id, sku_code, sku_name, dept_no, item, band, length, width, height, volume, weight, price, pick_unit, sku_label, manage_flag, create_by, create_time, update_by, update_time, ip_address, del_flag, field1, field2, field3, field4, field5) VALUES {}"""
    sqllines = """(\'{rent_id}\', \'{sku_code}\', \'{sku_name}\', 'deptNo1', 'item11', 10, 10, 10, 20, 380, 200, 198.00, 20, 1, 3, '', '2020-08-31 11:58:52', '', '2020-08-31 11:58:52', 0, 0, '', '', '', '', ''),""".format(rent_id='1',sku_code=configData['skuCode'],sku_name=configData['skuName'])
    return sql.format(sqllines)

def skuextData(configData):
    sql = """INSERT INTO warebasic.sku_ext (rent_id, sku_code, sku_type, color, size, pattern, year_season, cost_seq, assort_code, sku_desc, min_stock, max_stock, create_by, create_time, update_by, update_time, ip_address, del_flag) VALUES {}"""
    sqllines = """(\'{rent_id}\', \'{sku_code}\', 0, '白色', '86A', '2020', 'spring', 'CostSeq66', 'Assort001', 'forTest', 12, 20, '', '2020-08-31 11:58:52',
     '', '2020-08-31 11:58:52', 0, 0),""".format(rent_id='1',sku_code=configData['skuCode'])
    return sql.format(sqllines)

def skupackageData(configData, packageAmount, cartonTypeId):
    sql = """INSERT INTO warebasic.sku_package (rent_id, sku_code, carton_type_id, package_amount, package_weight, create_by, create_time, update_by, update_time, ip_address, del_flag) VALUES"""
    sqllines = """(\'{rent_id}\', \'{sku_code}\', \'{carton_type_id}\',{package_amount}, 0, '', '2020-08-31 12:00:28', '', '2020-08-31 12:00:28', 0, 0),""".format(rent_id='1',sku_code=configData['skuCode'],carton_type_id=cartonTypeId,package_amount=packageAmount)
    return sql.format(sqllines)

def skucartontypeData(configData, cartonTypeId):
    sql = """INSERT INTO warebasic.carton_type (rent_id, carton_type_id, length, width, height, volume, specification, wrapping_flag, auto_stacking_flag, recycling_flag, create_by, create_time, update_by, update_time, ip_address, del_flag) VALUES {}"""
    sqllines = """(\'{rent_id}\', \'{carton_type_id}\', 200, 200, 200, 8000000, 'S', 0, 0, 0, '', '2020-09-15 11:56:03', '', '2020-09-15 11:56:03', 0, 0),
""".format(rent_id='1',carton_type_id=cartonTypeId,sku_code=configData['skuCode'])
    return sql.format(sqllines)




