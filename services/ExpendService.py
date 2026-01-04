from models.Expend import ExpendInfoModel
from dao.ExpendDAO import ExpendDAO

class ExpendService:
    def __init__(self, expend_dao=None):
        self.expend_dao = expend_dao or ExpendDAO()

    def create_expend(self, money, account_id, user_id, remark, expend_time, expend_type_id, enable=True):
        if not all([money, account_id, user_id, expend_time, expend_type_id]):
            return False, "参数不能为空", None
        
        if money <= 0:
            return False, "金额必须大于0", None
        
        try:
            success, expend_id, error_msg = self.expend_dao.create_expend(money, account_id, user_id, remark, expend_time, expend_type_id, enable)
            if success:
                return True, "创建支出记录成功", {"id": expend_id}
            else:
                return False, f"创建支出记录失败: {error_msg}", None
        except Exception as e:
            return False, f"创建支出记录时发生错误: {str(e)}", None

    def update_expend(self, id, user_id, money=None, account_id=None, remark=None, expend_time=None, enable=None, expend_type_id=None):
        if not id or not user_id:
            return False, "参数不能为空", None
        
        if money is not None and money <= 0:
            return False, "金额必须大于0", None
        
        try:
            success, error_msg = self.expend_dao.update_expend(id, user_id, money, account_id, remark, expend_time, enable, expend_type_id)
            if success:
                return True, "更新支出记录成功", {"id": id}
            else:
                return False, f"更新支出记录失败: {error_msg}", None
        except Exception as e:
            return False, f"更新支出记录时发生错误: {str(e)}", None

    def delete_expend(self, id, user_id):
        if not all([id, user_id]):
            return False, "参数不能为空", None
        
        try:
            success, error_msg = self.expend_dao.delete_expend(id, user_id)
            if success:
                return True, "删除支出记录成功", {"id": id}
            else:
                return False, f"删除支出记录失败: {error_msg}", None
        except Exception as e:
            return False, f"删除支出记录时发生错误: {str(e)}", None

    def get_expend_by_id(self, id, user_id):
        if not all([id, user_id]):
            return False, "参数不能为空", None
        
        try:
            expend_data = self.expend_dao.get_expend_by_id(id, user_id)
            if expend_data:
                expend_model = ExpendInfoModel(expend_data)
                return True, "查询支出记录成功", expend_model.to_dict()
            else:
                return False, "支出记录不存在", None
        except Exception as e:
            return False, f"查询支出记录时发生错误: {str(e)}", None

    def get_expends_by_user_id(self, user_id):
        if not user_id:
            return False, "参数不能为空", None
        
        try:
            expends_data = self.expend_dao.get_expends_by_user_id(user_id)
            expends_list = [ExpendInfoModel(expend_data).to_dict() for expend_data in expends_data]
            return True, "查询支出记录列表成功", expends_list
        except Exception as e:
            return False, f"查询支出记录列表时发生错误: {str(e)}", None
