from typing import Any, Dict, Optional, Union

import pydantic
from typing_extensions import Literal

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.standard_gates.standard_gates import (
    DEFAULT_STANDARD_GATE_ARG_NAME,
    _StandardGate,
)

CONTROLLED_GATE_CONTROL: str = "CTRL"
CONTROLLED_GATE_TARGET: str = DEFAULT_STANDARD_GATE_ARG_NAME
DEFAULT_NUM_CTRL_QUBITS: int = 1

CtrlState = Optional[Union[pydantic.StrictStr, pydantic.NonNegativeInt]]


class ControlledGate(_StandardGate):
    """
    Base model for controlled Gates
    """

    num_ctrl_qubits: pydantic.PositiveInt = pydantic.Field(
        default=DEFAULT_NUM_CTRL_QUBITS
    )

    def _create_ios(self) -> None:
        _StandardGate._create_ios(self)
        control = RegisterUserInput(
            name=CONTROLLED_GATE_CONTROL, size=self.num_ctrl_qubits
        )
        self._inputs[CONTROLLED_GATE_CONTROL] = control
        self._outputs[CONTROLLED_GATE_CONTROL] = control


class ControlledGateWithState(ControlledGate):
    """
    Base model for controlled Gates with control over the controlled_state
    """

    ctrl_state: CtrlState = pydantic.Field(
        description="The control state in decimal or as a bit string (e.g. '1011'). If not specified, the control "
        "state is 2**num_ctrl_qubits - 1.\n"
        "The gate will be performed if the state of the control qubits matches the control state"
    )

    @pydantic.validator("ctrl_state", always=True)
    def _validate_ctrl_state(
        cls, ctrl_state: CtrlState, values: Dict[str, Any]
    ) -> CtrlState:
        num_ctrl_qubits: int = values.get("num_ctrl_qubits", DEFAULT_NUM_CTRL_QUBITS)
        ctrl_state = ctrl_state or "1" * num_ctrl_qubits

        ctrl_state_int: pydantic.NonNegativeInt = (
            int(ctrl_state, 2) if isinstance(ctrl_state, str) else ctrl_state
        )
        if ctrl_state_int < 0 or ctrl_state_int >= 2**num_ctrl_qubits:
            raise ValueError(
                "Control state value should be zero or positive and smaller than 2**num_ctrl_qubits"
            )
        return ctrl_state


class CXGate(ControlledGateWithState):
    """
    The Controlled-X Gate
    """

    num_ctrl_qubits: Literal[1] = pydantic.Field(default=1)

    def get_power_order(self) -> int:
        return 2


class CCXGate(ControlledGateWithState):
    """
    The Double Controlled-X Gate
    """

    num_ctrl_qubits: Literal[2] = pydantic.Field(default=2)

    def get_power_order(self) -> int:
        return 2


class C3XGate(ControlledGateWithState):
    """
    The X Gate controlled on 3 qubits
    """

    _name: str = "mcx"
    num_ctrl_qubits: Literal[3] = pydantic.Field(default=3)

    def get_power_order(self) -> int:
        return 2


class C4XGate(ControlledGateWithState):
    """
    The X Gate controlled on 4 qubits
    """

    _name: str = "mcx"
    num_ctrl_qubits: Literal[4] = pydantic.Field(default=4)

    def get_power_order(self) -> int:
        return 2


class CYGate(ControlledGateWithState):
    """
    The Controlled-Y Gate
    """

    def get_power_order(self) -> int:
        return 2


class CZGate(ControlledGateWithState):
    """
    The Controlled-Z Gate
    """

    def get_power_order(self) -> int:
        return 2


class CHGate(ControlledGateWithState):
    """
    The Controlled-H Gate
    """

    def get_power_order(self) -> int:
        return 2


class CSXGate(ControlledGateWithState):
    """
    The Controlled-SX Gate
    """

    def get_power_order(self) -> int:
        return 4


class CRXGate(ControlledGateWithState, angles=["theta"]):
    """
    The Controlled-RX Gate
    """


class CRYGate(ControlledGateWithState, angles=["theta"]):
    """
    The Controlled-RY Gate
    """


class CRZGate(ControlledGateWithState, angles=["theta"]):
    """
    The Controlled-RZ Gate
    """


class CPhaseGate(ControlledGateWithState, angles=["theta"]):
    """
    The Controlled-Phase Gate
    """

    _name: str = "cp"


class MCPhaseGate(ControlledGate, angles=["lam"]):
    """
    The Controlled-Phase Gate
    """

    _name: str = "mcphase"
