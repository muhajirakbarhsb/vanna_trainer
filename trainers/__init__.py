# trainers/__init__.py
from .mahasiswa_trainer import MahasiswaTrainer
from .dosen_trainer import DosenTrainer
from .akademik_trainer import AkademikTrainer
from .keuangan_trainer import KeuanganTrainer
from .institusi_trainer import InstitusiTrainer

__all__ = [
    'MahasiswaTrainer',
    'DosenTrainer',
    'AkademikTrainer',
    'KeuanganTrainer',
    'InstitusiTrainer'
]