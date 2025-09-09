# generators/dosen_generator.py
import random
import pandas as pd
from faker import Faker

fake = Faker('id_ID')


class DosenGenerator:
    """Generate lecturer collection data (3 tables)"""

    def __init__(self, engine):
        self.engine = engine
        self.fakultas_list = [
            'Fakultas Teknik',
            'Fakultas Ekonomi dan Bisnis',
            'Fakultas Ilmu Komputer',
            'Fakultas Kedokteran',
            'Fakultas Hukum'
        ]

        self.prodi_dict = {
            'Fakultas Teknik': ['Teknik Informatika', 'Teknik Elektro', 'Teknik Sipil', 'Teknik Mesin',
                                'Teknik Industri'],
            'Fakultas Ekonomi dan Bisnis': ['Manajemen', 'Akuntansi', 'Ekonomi Pembangunan', 'Bisnis Digital'],
            'Fakultas Ilmu Komputer': ['Sistem Informasi', 'Ilmu Komputer', 'Teknologi Informasi'],
            'Fakultas Kedokteran': ['Pendidikan Dokter', 'Keperawatan'],
            'Fakultas Hukum': ['Ilmu Hukum', 'Hukum Bisnis']
        }

        self.mata_kuliah_list = {
            'Teknik Informatika': ['Algoritma dan Pemrograman', 'Struktur Data', 'Basis Data', 'Jaringan Komputer'],
            'Teknik Elektro': ['Rangkaian Listrik', 'Elektronika Dasar', 'Sistem Kontrol', 'Mikroprosessor'],
            'Manajemen': ['Manajemen Keuangan', 'Pemasaran', 'Manajemen SDM', 'Manajemen Operasi'],
            'Akuntansi': ['Akuntansi Dasar', 'Akuntansi Keuangan', 'Akuntansi Biaya', 'Auditing'],
            'Sistem Informasi': ['Analisis Sistem', 'Perancangan Sistem', 'Pemrograman Web', 'Mobile Programming'],
            'Default': ['Matematika Dasar', 'Bahasa Indonesia', 'Bahasa Inggris', 'Pancasila']
        }

    def generate_lecturer_profile(self, count=150):
        """Generate lecturer profile data"""
        print(f"👨‍🏫 Generating {count} lecturer profiles...")

        data = []
        for i in range(count):
            fakultas = random.choice(self.fakultas_list)
            prodi = random.choice(self.prodi_dict[fakultas])

            data.append({
                'nip': f"NIP{random.randint(1970, 1999)}{random.randint(10, 12)}{random.randint(10, 28)}{i + 1:03d}",
                'nama_dosen': fake.name(),
                'jenis_kelamin': random.choice(['Laki-laki', 'Perempuan']),
                'fakultas': fakultas,
                'program_studi': prodi,
                'pendidikan_terakhir': random.choice(['S2', 'S3']),
                'jabatan_fungsional': random.choice(['Asisten Ahli', 'Lektor', 'Lektor Kepala', 'Guru Besar']),
                'golongan': random.choice(['III/a', 'III/b', 'III/c', 'III/d', 'IV/a', 'IV/b']),
                'total_mata_kuliah': random.randint(2, 6),
                'total_mahasiswa_bimbingan': random.randint(5, 20),
                'beban_sks': random.randint(12, 24),
                'status_aktif': True,
                'tahun_akademik': '2024/2025'
            })

        df = pd.DataFrame(data)
        df.to_sql('lecturer_profile', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {count} lecturer profiles")

    def generate_lecturer_teaching(self, count=300):
        """Generate lecturer teaching data"""
        print(f"📚 Generating {count} teaching records...")

        try:
            lecturers_df = pd.read_sql(
                "SELECT nip, nama_dosen, fakultas, program_studi FROM datamart.lecturer_profile LIMIT 50", self.engine)
        except Exception as e:
            print(f"Warning: Could not load existing lecturers: {e}")
            lecturers_df = pd.DataFrame({
                'nip': [f"NIP{1970 + i // 10}{(i % 12) + 1:02d}{(i % 28) + 1:02d}{i + 1:03d}" for i in range(50)],
                'nama_dosen': [fake.name() for _ in range(50)],
                'fakultas': [random.choice(self.fakultas_list) for _ in range(50)],
                'program_studi': [random.choice(self.prodi_dict[random.choice(self.fakultas_list)]) for _ in range(50)]
            })

        data = []
        for i in range(count):
            if len(lecturers_df) > 0:
                lecturer = lecturers_df.iloc[i % len(lecturers_df)]
                prodi = lecturer['program_studi']
                mata_kuliah = random.choice(self.mata_kuliah_list.get(prodi, self.mata_kuliah_list['Default']))

                data.append({
                    'nip': lecturer['nip'],
                    'nama_dosen': lecturer['nama_dosen'],
                    'fakultas': lecturer['fakultas'],
                    'mata_kuliah': mata_kuliah,
                    'kode_matkul': f"MK{random.randint(1001, 9999)}",
                    'kelas': random.choice(['A', 'B', 'C']),
                    'jumlah_mahasiswa': random.randint(15, 45),
                    'rata_rata_nilai': round(random.uniform(65, 85), 2),
                    'rata_rata_kehadiran': round(random.uniform(75, 95), 2),
                    'tingkat_kelulusan': round(random.uniform(80, 100), 2),
                    'semester': random.choice(['Ganjil', 'Genap']),
                    'tahun_akademik': '2024/2025'
                })

        df = pd.DataFrame(data)
        df.to_sql('lecturer_teaching', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {count} teaching records")

    def generate_lecturer_activity(self, count=150):
        """Generate lecturer activity data"""
        print(f"🔬 Generating {count} activity records...")

        try:
            lecturers_df = pd.read_sql("SELECT nip, nama_dosen, fakultas FROM datamart.lecturer_profile", self.engine)
        except Exception as e:
            print(f"Warning: Could not load existing lecturers: {e}")
            lecturers_df = pd.DataFrame({
                'nip': [f"NIP{1970 + i // 10}{(i % 12) + 1:02d}{(i % 28) + 1:02d}{i + 1:03d}" for i in range(150)],
                'nama_dosen': [fake.name() for _ in range(150)],
                'fakultas': [random.choice(self.fakultas_list) for _ in range(150)]
            })

        data = []
        for _, lecturer in lecturers_df.iterrows():
            data.append({
                'nip': lecturer['nip'],
                'nama_dosen': lecturer['nama_dosen'],
                'fakultas': lecturer['fakultas'],
                'jumlah_penelitian': random.randint(0, 5),
                'jumlah_publikasi': random.randint(0, 8),
                'jumlah_pengabdian': random.randint(1, 4),
                'total_dana_penelitian': random.randint(0, 500000000),
                'pelatihan_diikuti': random.randint(1, 6),
                'sertifikasi_dimiliki': random.randint(0, 3),
                'tahun_akademik': '2024/2025'
            })

        df = pd.DataFrame(data)
        df.to_sql('lecturer_activity', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {len(data)} activity records")

    def generate_all(self):
        """Generate all lecturer collection tables"""
        self.generate_lecturer_profile(150)
        self.generate_lecturer_teaching(300)
        self.generate_lecturer_activity(150)