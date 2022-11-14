from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _



class StateChoices(TextChoices):
    STATUS_DRAFT = 'DRAFT', _('DRAFT')
    STATUS_AW_APPROVAL = 'AWAITING_APPROVAL', _('AWAITING_APPROVAL')
    STATUS_AW_ACCEPT = 'AWAITING_ACCEPTANCE', _('AWAITING_ACCEPTANCE')
    STATUS_ACCEPTED = 'ACCEPTED', _('ACCEPTED')
    STATUS_APPROVED = 'APPROVED', _('APPROVED')
    STATUS_REJECTED = 'REJECTED', _('REJECTED')
    STATUS_FINANCE_REQUESTED = 'FINANCE_REQUESTED', _('FINANCE_REQUESTED')
    STATUS_COMPLETED = 'COMPLETED', _('COMPLETED')
    STATUS_AWAITING_BUYER_APPROVAL = 'AWAITING_BUYER_APPROVAL' , _('AWAITING_BUYER_APPROVAL')
    STATUS_APPROVED_BY_BUYER = 'APPROVED_BY_BUYER' , _('APPROVED_BY_BUYER')
    STATUS_REJECTED_BY_BUYER = 'REJECTED_BY_BUYER' , _('REJECTED_BY_BUYER')
    STATUS_ARCHIVED = 'STATUS_ARCHIVED' , _('STATUS_ARCHIVED')
    STATUS_FINANCED = 'FINANCED', _('FINANCED')
    STATUS_FINANCE_REJECTED = 'FINANCE_REJECTED', _('FINANCE_REJECTED')
    STATUS_SETTLED = 'SETTLED', _('SETTLED')
    STATUS_OVERDUE = 'OVERDUE', _('OVERDUE')
    STATUS_NO_AWAITING_SIGN = 'NO_AWAITING_SIGN', _('NO_AWAITING_SIGN')
    STATUS_AWAITING_SIGN_A = 'AWAITING_SIGN_A', _('AWAITING_SIGN_A')
    STATUS_AWAITING_SIGN_B = 'AWAITING_SIGN_B', _('AWAITING_SIGN_B')
    STATUS_AWAITING_SIGN_C = 'AWAITING_SIGN_C', _('AWAITING_SIGN_C')
    STATUS_AWAITING_SIGN_D = 'AWAITING_SIGN_D', _('AWAITING_SIGN_C')
    STATUS_AWAITING_SIGN_E = 'AWAITING_SIGN_E', _('AWAITING_SIGN_E')
    STATUS_AWAITING_SIGN_F = 'AWAITING_SIGN_F', _('AWAITING_SIGN_F')
    STATUS_AWAITING_SIGN_G = 'AWAITING_SIGN_G', _('AWAITING_SIGN_G')
    STATUS_AWAITING_SIGN_H = 'AWAITING_SIGN_H', _('AWAITING_SIGN_H')
    STATUS_AWAITING_SIGN_I = 'AWAITING_SIGN_I', _('AWAITING_SIGN_I')
    STATUS_AWAITING_SIGN_J = 'AWAITING_SIGN_J', _('AWAITING_SIGN_J')
    STATUS_AWAITING_SIGN_K = 'AWAITING_SIGN_K', _('AWAITING_SIGN_K')
    STATUS_AWAITING_SIGN_L = 'AWAITING_SIGN_L', _('AWAITING_SIGN_L')
    STATUS_AWAITING_SIGN_M = 'AWAITING_SIGN_M', _('AWAITING_SIGN_M')
    STATUS_AWAITING_SIGN_N = 'AWAITING_SIGN_N', _('AWAITING_SIGN_N')
    STATUS_AWAITING_SIGN_O = 'AWAITING_SIGN_O', _('AWAITING_SIGN_O')
    STATUS_AWAITING_SIGN_P = 'AWAITING_SIGN_P', _('AWAITING_SIGN_P')
    STATUS_AWAITING_SIGN_Q = 'AWAITING_SIGN_Q', _('AWAITING_SIGN_Q')
    STATUS_AWAITING_SIGN_R = 'AWAITING_SIGN_R', _('AWAITING_SIGN_R')
    STATUS_AWAITING_SIGN_S = 'AWAITING_SIGN_S', _('AWAITING_SIGN_S')
    STATUS_AWAITING_SIGN_T = 'AWAITING_SIGN_T', _('AWAITING_SIGN_T')
    STATUS_DELETED = 'DELETED', _('DELETED')
    # action and subaction
    SIGN_A = 'SIGN_A',_('SIGN_A')
    APPROVE = 'APPROVE',_('APPROVE')
    ACCEPT = 'ACCEPT',_('ACCEPT')
    ARCHIVE = 'ARCHIVE',_('ARCHIVE')
    SETTLE = 'SETTLE',_('SETTLE')
    REJECT = 'REJECT',_('REJECT')
    RETURN = 'RETURN',_('RETURN')
    SIGN_B = 'SIGN_B',_('SIGN_B')
    SIGN_C = 'SIGN_C',_('SIGN_C')
    REQUEST_FINANCE = 'REQUEST_FINANCE',_('REQUEST_FINANCE')
    SUBMIT = 'SUBMIT',_('SUBMIT')
    MAKER = 'MAKER',_('MAKER')
    INITIAL_STATE = 'INITIAL_STATE',_('INITIAL_STATE')
    # end of action
    NONE = 'NONE',_('NONE')
    