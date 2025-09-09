# generators/akademik_generator.py
import random
import pandas as pd
from faker import Faker

fake = Faker('id_ID')


class AkademikGenerator:
    """Generate academic collection data (3 tables)"""

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
            'Teknik Informatika': ['Algoritma dan Pemrograman', 'Struktur Data', 'Basis Data', 'Jaringan Komputer',
                                   'Rekayasa Perangkat Lunak', 'Sistem Operasi', 'Pemrograman Web',
                                   'Kecerdasan Buatan'],
            'Teknik Elektro': ['Rangkaian Listrik', 'Elektronika Dasar', 'Sistem Kontrol', 'Mikroprosessor',
                               'Sistem Tenaga Listrik', 'Elektronika Daya', 'Komunikasi Data', 'Sistem Embedded'],
            'Manajemen': ['Manajemen Keuangan', 'Pemasaran', 'Manajemen SDM', 'Manajemen Operasi', 'Kewirausahaan',
                          'Manajemen Strategis', 'Perilaku Organisasi', 'Manajemen Risiko'],
            'Akuntansi': ['Akuntansi Dasar', 'Akuntansi Keuangan', 'Akuntansi Biaya', 'Auditing', 'Perpajakan',
                          'Sistem Informasi Akuntansi', 'Akuntansi Manajemen', 'Analisis Laporan Keuangan'],
            'Sistem Informasi': ['Analisis Sistem', 'Perancangan Sistem', 'Pemrograman Web', 'Mobile Programming',
                                 'Data Mining', 'E-Business', 'Manajemen Proyek TI', 'Keamanan Sistem Informasi'],
            'Default': ['Matematika Dasar', 'Bahasa Indonesia', 'Bahasa Inggris', 'Pancasila', 'Kewarganegaraan',
                        'Agama', 'Statistika', 'Fisika Dasar']
        }

    def generate_course_performance(self, count=200):
        """Generate course performance data"""
        print(f"📖 Generating {count} course performance records...")

        data = []
        for i in range(count):
            fakultas = random.choice(self.fakultas_list)
            prodi = random.choice(self.prodi_dict[fakultas])
            mata_kuliah = random.choice(self.mata_kuliah_list.get(prodi, self.mata_kuliah_list['Default']))

            data.append({
                'kode_matkul': f"MK{random.randint(1001, 9999)}",
                'nama_matkul': mata_kuliah,
                'fakultas': fakultas,
                'program_studi': prodi,
                'sks': random.choice([2, 3, 4]),
                'semester': random.randint(1, 8),
                'jenis_matkul': random.choice(['Wajib', 'Pilihan']),
                'dosen_pengampu': fake.name(),
                'jumlah_peserta': random.randint(15, 50),
                'rata_rata_nilai': round(random.uniform(65, 85), 2),
                'tingkat_kelulusan': round(random.uniform(80, 100), 2),
                'rata_rata_kehadiran': round(random.uniform(75, 95), 2),
                'tahun_akademik': '2024/2025'
            })

        df = pd.DataFrame(data)
        df.to_sql('course_performance', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {count} course performance records")

    def generate_grade_distribution(self, count=150):
        """Generate grade distribution data"""
        print(f"📊 Generating {count} grade distribution records...")

        try:
            courses_df = pd.read_sql(
                "SELECT kode_matkul, nama_matkul, fakultas, program_studi, jumlah_peserta FROM datamart.course_performance LIMIT 100",
                self.engine)
        except Exception as e:
            print(f"Warning: Could not load existing courses: {e}")
            # Create dummy course data
            courses_data = []
            for i in range(100):
                fakultas = random.choice(self.fakultas_list)
                prodi = random.choice(self.prodi_dict[fakultas])
                mata_kuliah = random.choice(self.mata_kuliah_list.get(prodi, self.mata_kuliah_list['Default']))
                courses_data.append({
                    'kode_matkul': f"MK{1000 + i}",
                    'nama_matkul': mata_kuliah,
                    'fakultas': fakultas,
                    'program_studi': prodi,
                    'jumlah_peserta': random.randint(15, 50)
                })
            courses_df = pd.DataFrame(courses_data)

        data = []
        for i in range(count):
            if len(courses_df) > 0:
                course = courses_df.iloc[i % len(courses_df)]
                total_students = course['jumlah_peserta']

                # Generate realistic grade distribution
                jumlah_a = random.randint(0, int(total_students * 0.15))
                jumlah_ab = random.randint(0, int(total_students * 0.20))
                jumlah_b = random.randint(0, int(total_students * 0.25))
                jumlah_bc = random.randint(0, int(total_students * 0.20))
                jumlah_c = random.randint(0, int(total_students * 0.15))
                jumlah_d = random.randint(0, int(total_students * 0.05))

                # Adjust to make total match
                assigned = jumlah_a + jumlah_ab + jumlah_b + jumlah_bc + jumlah_c + jumlah_d
                jumlah_e = max(0, total_students - assigned)

                data.append({
                    'kode_matkul': course['kode_matkul'],
                    'nama_matkul': course['nama_matkul'],
                    'fakultas': course['fakultas'],
                    'program_studi': course['program_studi'],
                    'dosen_pengampu': fake.name(),
                    'jumlah_a': jumlah_a,
                    'jumlah_ab': jumlah_ab,
                    'jumlah_b': jumlah_b,
                    'jumlah_bc': jumlah_bc,
                    'jumlah_c': jumlah_c,
                    'jumlah_d': jumlah_d,
                    'jumlah_e': jumlah_e,
                    'total_mahasiswa': total_students,
                    'semester': random.choice(['Ganjil', 'Genap']),
                    'tahun_akademik': '2024/2025'
                })

        df = pd.DataFrame(data)
        df.to_sql('grade_distribution', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {count} grade distribution records")

    def generate_academic_trends(self, count=100):
        """Generate academic trends data"""
        print(f"📈 Generating {count} academic trends records...")

        data = []
        periods = ['2023-1', '2023-2', '2024-1', '2024-2']
        metrics = ['IPK Rata-rata', 'Tingkat Kelulusan', 'Tingkat Kehadiran', 'Jumlah Mahasiswa Baru', 'Dropout Rate']

        for fakultas in self.fakultas_list:
            for prodi in self.prodi_dict[fakultas]:
                for periode in periods:
                    for metric in random.sample(metrics, 3):  # Random 3 metrics per period
                        if metric == 'IPK Rata-rata':
                            nilai = round(random.uniform(2.8, 3.8), 2)
                            satuan = 'Skala 4.0'
                        elif metric in ['Tingkat Kelulusan', 'Tingkat Kehadiran']:
                            nilai = round(random.uniform(75, 95), 2)
                            satuan = 'Persen'
                        elif metric == 'Jumlah Mahasiswa Baru':
                            nilai = random.randint(50, 200)
                            satuan = 'Orang'
                        else:  # Dropout Rate
                            nilai = round(random.uniform(2, 8), 2)
                            satuan = 'Persen'

                        data.append({
                            'periode': periode,
                            'fakultas': fakultas,
                            'program_studi': prodi,
                            'metrik': metric,
                            'nilai': nilai,
                            'satuan': satuan,
                            'persentase_perubahan': round(random.uniform(-10, 15), 2),
                            'kategori': random.choice(['Akademik', 'Operasional', 'Keuangan']),
                            'deskripsi': f"Trend {metric} untuk {prodi} periode {periode}",
                            'tahun_akademik': '2024/2025'
                        })

        df = pd.DataFrame(data)
        df.to_sql('academic_trends', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {len(data)} academic trends records")

    def generate_all(self):
        """Generate all academic collection tables"""
        self.generate_course_performance(200)
        self.generate_grade_distribution(150)
        self.generate_academic_trends(100)