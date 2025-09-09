# generators/mahasiswa_generator.py
import random
import pandas as pd
from faker import Faker

fake = Faker('id_ID')


class MahasiswaGenerator:
    """Generate student collection data (3 tables)"""

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

    def generate_student_performance(self, count=500):
        """Generate student performance data"""
        print(f"👨‍🎓 Generating {count} student performance records...")

        data = []
        for i in range(count):
            fakultas = random.choice(self.fakultas_list)
            prodi = random.choice(self.prodi_dict[fakultas])
            angkatan = random.randint(2020, 2024)

            data.append({
                'nim': f"{angkatan}{random.randint(10, 99)}{i + 1:04d}",
                'nama_mahasiswa': fake.name(),
                'jenis_kelamin': random.choice(['Laki-laki', 'Perempuan']),
                'fakultas': fakultas,
                'program_studi': prodi,
                'angkatan': angkatan,
                'semester_aktif': random.randint(1, 8),
                'ipk': round(random.uniform(2.0, 4.0), 2),
                'total_sks': random.randint(120, 160),
                'sks_lulus': random.randint(80, 150),
                'status_mahasiswa': random.choice(['Aktif', 'Aktif', 'Aktif', 'Cuti', 'Lulus']),
                'tahun_akademik': '2024/2025'
            })

        df = pd.DataFrame(data)
        df.to_sql('student_performance', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {count} student performance records")

    def generate_student_attendance(self, count=800):
        """Generate student attendance data"""
        print(f"📅 Generating {count} attendance records...")

        # Get existing students or create dummy data
        try:
            students_df = pd.read_sql(
                "SELECT nim, nama_mahasiswa, fakultas, program_studi FROM datamart.student_performance LIMIT 200",
                self.engine)
        except Exception as e:
            print(f"Warning: Could not load existing students: {e}")
            students_df = pd.DataFrame({
                'nim': [f"202{i // 50}{(i % 50) + 1:02d}001" for i in range(200)],
                'nama_mahasiswa': [fake.name() for _ in range(200)],
                'fakultas': [random.choice(self.fakultas_list) for _ in range(200)],
                'program_studi': [random.choice(self.prodi_dict[random.choice(self.fakultas_list)]) for _ in range(200)]
            })

        data = []
        for i in range(count):
            if len(students_df) > 0:
                student = students_df.iloc[i % len(students_df)]
                prodi = student['program_studi']
                mata_kuliah = random.choice(self.mata_kuliah_list.get(prodi, self.mata_kuliah_list['Default']))

                hadir = random.randint(8, 14)
                izin = random.randint(0, 3)
                alpha = 14 - hadir - izin
                persentase = (hadir / 14) * 100

                data.append({
                    'nim': student['nim'],
                    'nama_mahasiswa': student['nama_mahasiswa'],
                    'fakultas': student['fakultas'],
                    'program_studi': student['program_studi'],
                    'mata_kuliah': mata_kuliah,
                    'kode_matkul': f"MK{random.randint(1001, 9999)}",
                    'semester': random.randint(1, 8),
                    'total_pertemuan': 14,
                    'hadir': hadir,
                    'izin': izin,
                    'alpha': alpha,
                    'persentase_kehadiran': round(persentase, 2),
                    'tahun_akademik': '2024/2025'
                })

        df = pd.DataFrame(data)
        df.to_sql('student_attendance', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {count} attendance records")

    def generate_student_finance(self, count=400):
        """Generate student finance data"""
        print(f"💰 Generating {count} finance records...")

        try:
            students_df = pd.read_sql(
                "SELECT nim, nama_mahasiswa, fakultas, program_studi FROM datamart.student_performance LIMIT 200",
                self.engine)
        except Exception as e:
            print(f"Warning: Could not load existing students: {e}")
            students_df = pd.DataFrame({
                'nim': [f"202{i // 50}{(i % 50) + 1:02d}001" for i in range(200)],
                'nama_mahasiswa': [fake.name() for _ in range(200)],
                'fakultas': [random.choice(self.fakultas_list) for _ in range(200)],
                'program_studi': [random.choice(self.prodi_dict[random.choice(self.fakultas_list)]) for _ in range(200)]
            })

        data = []
        for i in range(count):
            if len(students_df) > 0:
                student = students_df.iloc[i % len(students_df)]
                tagihan = random.choice([3500000, 4000000, 4500000, 5000000])
                status = random.choice(['Lunas', 'Lunas', 'Belum Lunas', 'Menunggak'])

                if status == 'Lunas':
                    dibayar = tagihan
                elif status == 'Belum Lunas':
                    dibayar = tagihan * random.uniform(0.3, 0.8)
                else:
                    dibayar = 0

                data.append({
                    'nim': student['nim'],
                    'nama_mahasiswa': student['nama_mahasiswa'],
                    'fakultas': student['fakultas'],
                    'program_studi': student['program_studi'],
                    'semester': random.choice(['Ganjil', 'Genap']),
                    'tahun_akademik': '2024/2025',
                    'jumlah_tagihan': tagihan,
                    'jumlah_dibayar': round(dibayar, 2),
                    'sisa_tagihan': round(tagihan - dibayar, 2),
                    'status_pembayaran': status,
                    'tanggal_bayar': fake.date_between(start_date='-6m',
                                                       end_date='today') if status == 'Lunas' else None,
                    'metode_pembayaran': random.choice(['Transfer Bank', 'Virtual Account', 'Kartu Kredit', 'E-wallet'])
                })

        df = pd.DataFrame(data)
        df.to_sql('student_finance', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {count} finance records")

    def generate_all(self):
        """Generate all student collection tables"""
        self.generate_student_performance(500)
        self.generate_student_attendance(800)
        self.generate_student_finance(400)