from models.Income import IncomeInfoModel
from dao.IncomeDAO import IncomeDAO

class IncomeService:
    def __init__(self):
        self.income_dao = IncomeDAO()

    def create_income(self, money, account_id, user_id, remark, income_time, income_type_id, enable=True):
        if not all([money, account_id, user_id, income_time, income_type_id]):
            return False, "参数不能为空", None
        
        if money <= 0:
            return False, "金额必须大于0", None
        
        try:
            success, income_id = self.income_dao.create_income(money, account_id, user_id, remark, income_time, income_type_id, enable)
            if success:
                return True, "创建收入记录成功", {"id": income_id}
            else:
                return False, "创建收入记录失败", None
        except Exception as e:
            return False, f"创建收入记录时发生错误: {str(e)}", None

    def update_income(self, id, user_id, money=None, account_id=None, remark=None, income_time=None, enable=None, income_type_id=None):
        if not id or not user_id:
            return False, "参数不能为空", None
        
        if money is not None and money <= 0:
            return False, "金额必须大于0", None
        
        try:
            success = self.income_dao.update_income(id, user_id, money, account_id, remark, income_time, enable, income_type_id)
            if success:
                return True, "更新收入记录成功", {"id": id}
            else:
                return False, "更新收入记录失败或记录不存在", None
        except Exception as e:
            return False, f"更新收入记录时发生错误: {str(e)}", None

    def delete_income(self, id, user_id):
        if not all([id, user_id]):
            return False, "参数不能为空", None
        
        try:
            success = self.income_dao.delete_income(id, user_id)
            if success:
                return True, "删除收入记录成功", {"id": id}
            else:
                return False, "删除收入记录失败或记录不存在", None
        except Exception as e:
            return False, f"删除收入记录时发生错误: {str(e)}", None

    def get_income_by_id(self, id, user_id):
        if not all([id, user_id]):
            return False, "参数不能为空", None
        
        try:
            income_data = self.income_dao.get_income_by_id(id, user_id)
            if income_data:
                income_model = IncomeInfoModel(income_data)
                return True, "查询收入记录成功", income_model.to_dict()
            else:
                return False, "收入记录不存在", None
        except Exception as e:
            return False, f"查询收入记录时发生错误: {str(e)}", None

    def get_incomes_by_user_id(self, user_id):
        if not user_id:
            return False, "参数不能为空", None
        
        try:
            incomes_data = self.income_dao.get_incomes_by_user_id(user_id)
            incomes_list = [IncomeInfoModel(income_data).to_dict() for income_data in incomes_data]
            return True, "查询收入记录列表成功", incomes_list
        except Exception as e:
            return False, f"查询收入记录列表时发生错误: {str(e)}", None
