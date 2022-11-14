import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import (
    DEFAULT_INPUT_NAME,
    DEFAULT_OUTPUT_NAME,
    FunctionParams,
)


class QFT(FunctionParams):
    """
    Creates a quantum Fourier transform on a specified number of qubits.
    Use the inverse flag to create the inverse QFT circuit.
    """

    num_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits on which the QFT acts."
    )
    approximation_degree: pydantic.NonNegativeInt = pydantic.Field(
        default=0,
        description="The degree of approximation (0 for no approximation). The smallest "
        "'approximation_degree' rotation angles are dropped from the QFT.",
    )
    do_swaps: bool = pydantic.Field(
        default=True, description="Whether to include the final swaps in the QFT."
    )
    inverse: bool = pydantic.Field(
        default=False,
        description="If True, the inverse Fourier transform is constructed.",
    )

    def _create_ios(self) -> None:
        self._inputs = {
            DEFAULT_INPUT_NAME: RegisterUserInput(
                name=DEFAULT_INPUT_NAME, size=self.num_qubits
            )
        }
        self._outputs = {
            DEFAULT_OUTPUT_NAME: RegisterUserInput(
                name=DEFAULT_OUTPUT_NAME, size=self.num_qubits
            )
        }

    def get_power_order(self) -> int:
        return 4
