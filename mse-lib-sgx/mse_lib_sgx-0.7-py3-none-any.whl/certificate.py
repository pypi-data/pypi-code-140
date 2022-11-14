"""mse_lib_sgx.certificate module."""

import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, cast

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import (Encoding,
                                                          NoEncryption,
                                                          PrivateFormat,
                                                          PublicFormat,
                                                          load_pem_private_key)
from intel_sgx_ra.quote import Quote
from intel_sgx_ra.ratls import get_quote_from_cert, SGX_QUOTE_EXTENSION_OID
from mse_lib_crypto.conversion import ed25519_to_x25519_sk
from mse_lib_crypto.seal_box import unseal

from mse_lib_sgx.sgx_quote import get_quote


class SelfSignedCertificate:
    """SelfSignedCertificate class."""

    def __init__(self, dns_name: str, subject: x509.Name, root_path: Path,
                 expires_in: int):
        """Init constructor of SGXCertificate."""
        self.cert_path: Path = root_path / "cert.pem"
        self.key_path: Path = root_path / "key.pem"
        self.sk: Ed25519PrivateKey = (Ed25519PrivateKey.generate()
                                      if not self.key_path.exists() else cast(
                                          Ed25519PrivateKey,
                                          load_pem_private_key(
                                              data=self.key_path.read_bytes(),
                                              password=None)))
        self.x25519_sk: X25519PrivateKey = ed25519_to_x25519_sk(self.sk)
        self.expires_in: int = expires_in
        self.cert: x509.Certificate
        if self.key_path.exists() and self.cert_path.exists():
            self.cert = x509.load_pem_x509_certificate(
                data=self.cert_path.read_bytes())
        else:
            self.cert = generate_x509(dns_name=dns_name,
                                      subject=subject,
                                      private_key=self.sk,
                                      expires_in=expires_in)
            self.write(self.cert_path, self.key_path)

    def write(self,
              cert_path: Path,
              sk_path: Path,
              encoding: Encoding = Encoding.PEM) -> None:
        """Write X509 certificate and private key to `cert_path` and `sk_path`."""
        cert_path.write_bytes(self.cert.public_bytes(encoding))
        sk_path.write_bytes(
            self.sk.private_bytes(encoding=Encoding.PEM,
                                  format=PrivateFormat.PKCS8,
                                  encryption_algorithm=NoEncryption()))

    def unseal(self, data: bytes) -> bytes:
        """Unseal data sent for certificate public key."""
        return unseal(
            data,
            self.x25519_sk.private_bytes(encoding=Encoding.Raw,
                                         format=PrivateFormat.Raw,
                                         encryption_algorithm=NoEncryption()))


class SGXCertificate:
    """SGXCertificate class."""

    def __init__(self, dns_name: str, subject: x509.Name, root_path: Path,
                 expires_in: int):
        """Init constructor of SGXCertificate."""
        self.cert_path: Path = root_path / "cert.pem"
        self.key_path: Path = root_path / "key.pem"
        self.sk: Ed25519PrivateKey = (Ed25519PrivateKey.generate()
                                      if not self.key_path.exists() else cast(
                                          Ed25519PrivateKey,
                                          load_pem_private_key(
                                              data=self.key_path.read_bytes(),
                                              password=None)))
        self.x25519_sk: X25519PrivateKey = ed25519_to_x25519_sk(self.sk)
        self.expires_in: int = expires_in
        self.cert: x509.Certificate
        self.quote: Quote
        if self.key_path.exists() and self.cert_path.exists():
            self.cert = x509.load_pem_x509_certificate(
                data=self.cert_path.read_bytes())
            self.quote = get_quote_from_cert(self.cert)
        else:
            self.quote = Quote.from_bytes(
                get_quote(user_report_data=hashlib.sha256(self.sk.public_key(
                ).public_bytes(encoding=Encoding.Raw,
                               format=PublicFormat.Raw)).digest()))
            self.cert = generate_x509(
                dns_name=dns_name,
                subject=subject,
                private_key=self.sk,
                expires_in=self.expires_in,
                custom_extension=x509.UnrecognizedExtension(
                    oid=SGX_QUOTE_EXTENSION_OID, value=bytes(self.quote)))
            self.write(self.cert_path, self.key_path)

    def write(self,
              cert_path: Path,
              sk_path: Path,
              encoding: Encoding = Encoding.PEM) -> None:
        """Write X509 certificate and private key to `cert_path` and `sk_path`."""
        cert_path.write_bytes(self.cert.public_bytes(encoding))
        sk_path.write_bytes(
            self.sk.private_bytes(encoding=Encoding.PEM,
                                  format=PrivateFormat.PKCS8,
                                  encryption_algorithm=NoEncryption()))

    def unseal(self, data: bytes) -> bytes:
        """Unseal data sent for certificate public key."""
        return unseal(
            data,
            self.x25519_sk.private_bytes(encoding=Encoding.Raw,
                                         format=PrivateFormat.Raw,
                                         encryption_algorithm=NoEncryption()))


def generate_x509(
    dns_name: str,
    subject: x509.Name,
    private_key: Ed25519PrivateKey,
    expires_in: int,
    custom_extension: Optional[x509.UnrecognizedExtension] = None
) -> x509.Certificate:
    """X509 certificate generation."""
    issuer: x509.Name = subject  # issuer=subject for self-signed certificate

    builder: x509.CertificateBuilder = x509.CertificateBuilder()

    builder = builder.subject_name(subject).issuer_name(issuer).public_key(
        private_key.public_key()).serial_number(
            x509.random_serial_number()).not_valid_before(
                datetime.utcnow()).not_valid_after(
                    datetime.utcnow() +
                    timedelta(days=expires_in)).add_extension(
                        x509.SubjectAlternativeName([x509.DNSName(dns_name)]),
                        critical=False,
                    )

    if custom_extension is not None:
        builder = builder.add_extension(custom_extension, critical=False)

    return builder.sign(private_key=private_key, algorithm=None)
