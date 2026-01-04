-- 修改expend表中的consumption_id字段名为expend_type_id
ALTER TABLE expend CHANGE consumption_id expend_type_id BIGINT COMMENT '消费类型id';