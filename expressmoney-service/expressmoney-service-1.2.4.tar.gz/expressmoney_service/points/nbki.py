__all__ = ('NbkiPoint',)

from expressmoney_service.api import *

_SERVICE = 'services'
_APP = 'nbki'


class _NbkiCreateContract(Contract):
    first_name = serializers.CharField(max_length=32)
    last_name = serializers.CharField(max_length=32)
    middle_name = serializers.CharField(max_length=32)
    birth_date = serializers.DateField()
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)
    passport_date = serializers.DateField()
    snils = serializers.CharField(max_length=11, allow_null=True)


class _NbkiResponseContract(Contract):
    total_accounts_mfo_new = serializers.IntegerField()
    total_accounts_mfo_old = serializers.IntegerField()
    total_accounts_bank_new = serializers.IntegerField()
    total_accounts_bank_old = serializers.IntegerField()
    total_accounts_other_new = serializers.IntegerField()
    total_accounts_other_old = serializers.IntegerField()
    total_accounts_active_balance_current_balance_more_0_mfo_new = serializers.IntegerField()
    total_accounts_active_balance_current_balance_more_0_mfo_old = serializers.IntegerField()
    total_accounts_active_balance_current_balance_more_0_bank_new = serializers.IntegerField()
    total_accounts_active_balance_current_balance_more_0_bank_old = serializers.IntegerField()
    total_accounts_active_balance_current_balance_more_0_other_new = serializers.IntegerField()
    total_accounts_active_balance_current_balance_more_0_other_old = serializers.IntegerField()
    total_accounts_active_balance_current_balance_0_mfo_new = serializers.IntegerField()
    total_accounts_active_balance_current_balance_0_mfo_old = serializers.IntegerField()
    total_accounts_active_balance_current_balance_0_bank_new = serializers.IntegerField()
    total_accounts_active_balance_current_balance_0_bank_old = serializers.IntegerField()
    total_accounts_active_balance_current_balance_0_other_new = serializers.IntegerField()
    total_accounts_active_balance_current_balance_0_other_old = serializers.IntegerField()
    total_accounts_negative_rating_mfo_new = serializers.IntegerField()
    total_accounts_negative_rating_mfo_old = serializers.IntegerField()
    total_accounts_negative_rating_bank_new = serializers.IntegerField()
    total_accounts_negative_rating_bank_old = serializers.IntegerField()
    total_accounts_negative_rating_other_new = serializers.IntegerField()
    total_accounts_negative_rating_other_old = serializers.IntegerField()
    total_accounts_positive_rating_mfo_new = serializers.IntegerField()
    total_accounts_positive_rating_mfo_old = serializers.IntegerField()
    total_accounts_positive_rating_bank_new = serializers.IntegerField()
    total_accounts_positive_rating_bank_old = serializers.IntegerField()
    total_accounts_positive_rating_other_new = serializers.IntegerField()
    total_accounts_positive_rating_other_old = serializers.IntegerField()
    total_accounts_past_due_current_balance_more_0_mfo_new = serializers.IntegerField()
    total_accounts_past_due_current_balance_more_0_mfo_old = serializers.IntegerField()
    total_accounts_past_due_current_balance_more_0_bank_new = serializers.IntegerField()
    total_accounts_past_due_current_balance_more_0_bank_old = serializers.IntegerField()
    total_accounts_past_due_current_balance_more_0_other_new = serializers.IntegerField()
    total_accounts_past_due_current_balance_more_0_other_old = serializers.IntegerField()
    total_accounts_past_due_current_balance_0_mfo_new = serializers.IntegerField()
    total_accounts_past_due_current_balance_0_mfo_old = serializers.IntegerField()
    total_accounts_past_due_current_balance_0_bank_new = serializers.IntegerField()
    total_accounts_past_due_current_balance_0_bank_old = serializers.IntegerField()
    total_accounts_past_due_current_balance_0_other_new = serializers.IntegerField()
    total_accounts_past_due_current_balance_0_other_old = serializers.IntegerField()
    total_accounts_closed_mfo_new = serializers.IntegerField()
    total_accounts_closed_mfo_old = serializers.IntegerField()
    total_accounts_closed_bank_new = serializers.IntegerField()
    total_accounts_closed_bank_old = serializers.IntegerField()
    total_accounts_closed_other_new = serializers.IntegerField()
    total_accounts_closed_other_old = serializers.IntegerField()
    date_last_account_mfo_new = serializers.IntegerField()
    date_last_account_mfo_old = serializers.IntegerField()
    date_last_account_bank_new = serializers.IntegerField()
    date_last_account_bank_old = serializers.IntegerField()
    date_last_account_other_new = serializers.IntegerField()
    date_last_account_other_old = serializers.IntegerField()
    date_first_account_mfo_new = serializers.IntegerField()
    date_first_account_mfo_old = serializers.IntegerField()
    date_first_account_bank_new = serializers.IntegerField()
    date_first_account_bank_old = serializers.IntegerField()
    date_first_account_other_new = serializers.IntegerField()
    date_first_account_other_old = serializers.IntegerField()
    total_amount_credit_limit_mfo_new = serializers.IntegerField()
    total_amount_credit_limit_mfo_old = serializers.IntegerField()
    total_amount_credit_limit_bank_new = serializers.IntegerField()
    total_amount_credit_limit_bank_old = serializers.IntegerField()
    total_amount_credit_limit_other_new = serializers.IntegerField()
    total_amount_credit_limit_other_old = serializers.IntegerField()
    total_amount_current_balance_mfo_new = serializers.IntegerField()
    total_amount_current_balance_mfo_old = serializers.IntegerField()
    total_amount_current_balance_bank_new = serializers.IntegerField()
    total_amount_current_balance_bank_old = serializers.IntegerField()
    total_amount_current_balance_other_new = serializers.IntegerField()
    total_amount_current_balance_other_old = serializers.IntegerField()
    total_amount_past_due_balance_mfo_new = serializers.IntegerField()
    total_amount_past_due_balance_mfo_old = serializers.IntegerField()
    total_amount_past_due_balance_bank_new = serializers.IntegerField()
    total_amount_past_due_balance_bank_old = serializers.IntegerField()
    total_amount_past_due_balance_other_new = serializers.IntegerField()
    total_amount_past_due_balance_other_old = serializers.IntegerField()
    total_amount_past_due_balance_active_mfo_new = serializers.IntegerField()
    total_amount_past_due_balance_active_mfo_old = serializers.IntegerField()
    total_amount_past_due_balance_active_bank_new = serializers.IntegerField()
    total_amount_past_due_balance_active_bank_old = serializers.IntegerField()
    total_amount_past_due_balance_active_other_new = serializers.IntegerField()
    total_amount_past_due_balance_active_other_old = serializers.IntegerField()
    total_amount_outstanding_balance_mfo_new = serializers.IntegerField()
    total_amount_outstanding_balance_mfo_old = serializers.IntegerField()
    total_amount_outstanding_balance_bank_new = serializers.IntegerField()
    total_amount_outstanding_balance_bank_old = serializers.IntegerField()
    total_amount_outstanding_balance_other_new = serializers.IntegerField()
    total_amount_outstanding_balance_other_old = serializers.IntegerField()
    total_amount_scheduled_monthly_pay_mfo_new = serializers.IntegerField()
    total_amount_scheduled_monthly_pay_mfo_old = serializers.IntegerField()
    total_amount_scheduled_monthly_pay_bank_new = serializers.IntegerField()
    total_amount_scheduled_monthly_pay_bank_old = serializers.IntegerField()
    total_amount_scheduled_monthly_pay_other_new = serializers.IntegerField()
    total_amount_scheduled_monthly_pay_other_old = serializers.IntegerField()
    total_num_days_30_mfo_new = serializers.IntegerField()
    total_num_days_30_mfo_old = serializers.IntegerField()
    total_num_days_30_bank_new = serializers.IntegerField()
    total_num_days_30_bank_old = serializers.IntegerField()
    total_num_days_30_other_new = serializers.IntegerField()
    total_num_days_30_other_old = serializers.IntegerField()
    total_num_days_60_mfo_new = serializers.IntegerField()
    total_num_days_60_mfo_old = serializers.IntegerField()
    total_num_days_60_bank_new = serializers.IntegerField()
    total_num_days_60_bank_old = serializers.IntegerField()
    total_num_days_60_other_new = serializers.IntegerField()
    total_num_days_60_other_old = serializers.IntegerField()
    total_num_days_90_mfo_new = serializers.IntegerField()
    total_num_days_90_mfo_old = serializers.IntegerField()
    total_num_days_90_bank_new = serializers.IntegerField()
    total_num_days_90_bank_old = serializers.IntegerField()
    total_num_days_90_other_new = serializers.IntegerField()
    total_num_days_90_other_old = serializers.IntegerField()
    total_pay_late_days_1_mfo_new = serializers.IntegerField()
    total_pay_late_days_1_mfo_old = serializers.IntegerField()
    total_pay_late_days_1_bank_new = serializers.IntegerField()
    total_pay_late_days_1_bank_old = serializers.IntegerField()
    total_pay_late_days_1_other_new = serializers.IntegerField()
    total_pay_late_days_1_other_old = serializers.IntegerField()
    total_pay_late_more_days_30_mfo_new = serializers.IntegerField()
    total_pay_late_more_days_30_mfo_old = serializers.IntegerField()
    total_pay_late_more_days_30_bank_new = serializers.IntegerField()
    total_pay_late_more_days_30_bank_old = serializers.IntegerField()
    total_pay_late_more_days_30_other_new = serializers.IntegerField()
    total_pay_late_more_days_30_other_old = serializers.IntegerField()
    total_pay_by_agreement_mfo_new = serializers.IntegerField()
    total_pay_by_agreement_mfo_old = serializers.IntegerField()
    total_pay_by_agreement_bank_new = serializers.IntegerField()
    total_pay_by_agreement_bank_old = serializers.IntegerField()
    total_pay_by_agreement_other_new = serializers.IntegerField()
    total_pay_by_agreement_other_old = serializers.IntegerField()
    average_time_obtaining_loan_mfo_new = serializers.IntegerField()
    average_time_obtaining_loan_mfo_old = serializers.IntegerField()
    average_time_obtaining_loan_bank_new = serializers.IntegerField()
    average_time_obtaining_loan_bank_old = serializers.IntegerField()
    average_time_obtaining_loan_other_new = serializers.IntegerField()
    average_time_obtaining_loan_other_old = serializers.IntegerField()
    total_inquiries_mfo = serializers.IntegerField()
    total_recent_inquiries_days_30_mfo = serializers.IntegerField()
    total_recent_inquiries_days_365_mfo = serializers.IntegerField()


class _NbkiID(ID):
    _service = _SERVICE
    _app = _APP
    _view_set = 'nbki'


class NbkiPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = _NbkiID()
    _create_contract = _NbkiCreateContract
    _response_contract = _NbkiResponseContract
