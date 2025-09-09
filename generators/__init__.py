# generators/__init__.py
from .mahasiswa_generator import MahasiswaGenerator
from .dosen_generator import DosenGenerator
from .akademik_generator import AkademikGenerator
from .keuangan_generator import KeuanganGenerator
from .institusi_generator import InstitusiGenerator

__all__ = [
    'MahasiswaGenerator',
    'DosenGenerator',
    'AkademikGenerator',
    'KeuanganGenerator',
    'InstitusiGenerator'
]