import logging
import subprocess
import tempfile
from os import path, unlink
from pathlib import Path
from ...exceptions import EvaluationNotRelevant
from ...transport import TLSTransport
from ...certificate import BaseCertificate, IntermediateCertificate
from .. import BaseEvaluationTask

logger = logging.getLogger(__name__)
STATUS = [
    "Expired",
    "Good",
    "NotCovered",
    "NotEnrolled",
    "Revoked",
]


class EvaluationTask(BaseEvaluationTask):
    def __init__(
        self, transport: TLSTransport, metadata: dict, config: dict
    ) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(transport, metadata, config)

    def evaluate(self, certificate: BaseCertificate):
        if not isinstance(certificate, IntermediateCertificate):
            raise EvaluationNotRelevant
        tmp_path_prefix = self._configuration.get("tmp_path_prefix", "/tmp")
        db_path = path.join(tmp_path_prefix, ".crlite_db")
        tmp = tempfile.NamedTemporaryFile(delete=False, dir=tmp_path_prefix)
        try:
            tmp.write(certificate.pem.encode())
        finally:
            tmp.close()
        status = query_crlite(tmp.name, db_path)
        unlink(tmp.name)
        if status not in STATUS:
            logger.error(f"Unknown CRLite response {status}")
        return status


def query_crlite(pem_path: str, db_path: str) -> str:
    try:
        stdout_string = subprocess.check_output(
            [
                "./rust-query-crlite",
                "-vvv",
                "--db",
                db_path,
                "--update",
                "prod",
                "x509",
            ],
            stderr=subprocess.STDOUT,
            cwd=str(Path(__file__).parent.parent.with_name("vendor")),
        )
        logger.debug(stdout_string)
        result = subprocess.check_output(
            ["./rust-query-crlite", "-vv", "--db", db_path, "x509", pem_path],
            stderr=subprocess.STDOUT,
            cwd=str(Path(__file__).parent.parent.with_name("vendor")),
        )
        if result:
            return result.decode().split(pem_path)[1].strip()
    except subprocess.CalledProcessError as cpe:
        print(cpe.returncode)
        print(cpe.output)
    except OSError as err:
        print(err)
    return None
