# generators/institusi_generator.py
import random
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import text
from faker import Faker

fake = Faker('id_ID')


class InstitusiGenerator:
    """Generate institutional collection data (3 tables)"""

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

    def generate_faculty_statistics(self):
        """Generate/update faculty statistics with real data"""
        print(f"🏛️ Updating faculty statistics with real data...")

        # Update existing faculty statistics with more realistic data
        for fakultas in self.fakultas_list:
            try:
                # Count actual students
                student_count_result = pd.read_sql(
                    f"SELECT COUNT(*) as count FROM datamart.student_performance WHERE fakultas = '{fakultas}' AND status_mahasiswa = 'Aktif'",
                    self.engine
                )
                student_count = student_count_result.iloc[0]['count'] if len(
                    student_count_result) > 0 else random.randint(100, 300)

                # Count actual lecturers
                lecturer_count_result = pd.read_sql(
                    f"SELECT COUNT(*) as count FROM datamart.lecturer_profile WHERE fakultas = '{fakultas}' AND status_aktif = true",
                    self.engine
                )
                lecturer_count = lecturer_count_result.iloc[0]['count'] if len(
                    lecturer_count_result) > 0 else random.randint(20, 60)

                # Get average IPK
                avg_ipk_result = pd.read_sql(
                    f"SELECT AVG(ipk) as avg_ipk FROM datamart.student_performance WHERE fakultas = '{fakultas}' AND status_mahasiswa = 'Aktif'",
                    self.engine
                )
                avg_ipk = avg_ipk_result.iloc[0]['avg_ipk'] if len(avg_ipk_result) > 0 and avg_ipk_result.iloc[0][
                    'avg_ipk'] is not None else random.uniform(3.0, 3.6)

                # Count program studi
                prodi_count = len(self.prodi_dict[fakultas])

                # Update faculty statistics
                update_query = f"""
                UPDATE datamart.faculty_statistics 
                SET jumlah_mahasiswa_aktif = {student_count},
                    jumlah_dosen = {lecturer_count},
                    jumlah_program_studi = {prodi_count},
                    rata_rata_ipk_fakultas = {round(avg_ipk, 2)},
                    jumlah_lulusan_tahun_ini = {random.randint(int(student_count * 0.1), int(student_count * 0.3))},
                    tingkat_kehadiran_rata = {round(random.uniform(80, 95), 2)}
                WHERE fakultas = '{fakultas}'
                """

                with self.engine.connect() as conn:
                    result = conn.execute(text(update_query))
                    conn.commit()
                    print(f"✅ Updated {fakultas}: {student_count} students, {lecturer_count} lecturers")

            except Exception as e:
                print(f"Warning: Could not update {fakultas} statistics: {e}")

        print(f"✅ Updated faculty statistics with real calculated data")

    def generate_university_performance(self):
        """Generate university performance data"""
        print(f"🎓 Generating university performance data...")

        data = []
        for periode in ['2023/2024', '2024/2025']:
            # Calculate totals from actual data
            try:
                total_mahasiswa_result = pd.read_sql(
                    "SELECT COUNT(*) as count FROM datamart.student_performance WHERE status_mahasiswa = 'Aktif'",
                    self.engine
                )
                total_mahasiswa = total_mahasiswa_result.iloc[0]['count'] if len(
                    total_mahasiswa_result) > 0 else random.randint(3000, 5000)

                total_dosen_result = pd.read_sql(
                    "SELECT COUNT(*) as count FROM datamart.lecturer_profile WHERE status_aktif = true",
                    self.engine
                )
                total_dosen = total_dosen_result.iloc[0]['count'] if len(total_dosen_result) > 0 else random.randint(
                    200, 400)

                avg_ipk_result = pd.read_sql(
                    "SELECT AVG(ipk) as avg_ipk FROM datamart.student_performance WHERE status_mahasiswa = 'Aktif'",
                    self.engine
                )
                avg_ipk = avg_ipk_result.iloc[0]['avg_ipk'] if len(avg_ipk_result) > 0 and avg_ipk_result.iloc[0][
                    'avg_ipk'] is not None else random.uniform(3.0, 3.8)

            except Exception as e:
                print(f"Warning: Could not get actual data: {e}")
                total_mahasiswa = random.randint(3000, 5000)
                total_dosen = random.randint(200, 400)
                avg_ipk = random.uniform(3.0, 3.8)

            # Calculate total program studi
            total_prodi = sum(len(prodi_list) for prodi_list in self.prodi_dict.values())

            data.append({
                'periode': periode,
                'total_mahasiswa': total_mahasiswa,
                'total_dosen': total_dosen,
                'total_program_studi': total_prodi,
                'total_fakultas': len(self.fakultas_list),
                'rata_rata_ipk_universitas': round(avg_ipk, 2),
                'tingkat_kelulusan': round(random.uniform(85, 95), 2),
                'tingkat_drop_out': round(random.uniform(3, 8), 2),
                'student_lecturer_ratio': round(total_mahasiswa / max(total_dosen, 1), 2),
                'tingkat_kepuasan_mahasiswa': round(random.uniform(75, 90), 2),
                'akreditasi_institusi': 'B',
                'tahun_akademik': periode
            })

        df = pd.DataFrame(data)
        df.to_sql('university_performance', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {len(data)} university performance records")

    def generate_accreditation_status(self):
        """Generate accreditation status data"""
        print(f"🏆 Generating accreditation status data...")

        data = []

        # Program studi accreditations
        for fakultas in self.fakultas_list:
            for prodi in self.prodi_dict[fakultas]:
                akreditasi_current = random.choice(['A', 'B', 'C', 'Unggul', 'Baik Sekali'])
                tanggal_akreditasi = datetime.now() - timedelta(days=random.randint(365, 1095))
                masa_berlaku = datetime.now() + timedelta(days=random.randint(365, 1825))

                data.append({
                    'unit_name': prodi,
                    'unit_type': 'Program Studi',
                    'fakultas': fakultas,
                    'akreditasi_current': akreditasi_current,
                    'tanggal_akreditasi': tanggal_akreditasi,
                    'masa_berlaku': masa_berlaku,
                    'akreditasi_previous': random.choice(['B', 'C', 'Baik']),
                    'status_renewal': random.choice(['On Track', 'Needs Attention', 'In Progress']),
                    'target_akreditasi': random.choice(['A', 'Unggul']),
                    'progress_percentage': round(random.uniform(60, 95), 2),
                    'tahun_akademik': '2024/2025'
                })

        # Faculty accreditations
        for fakultas in self.fakultas_list:
            akreditasi_current = random.choice(['A', 'B', 'Unggul', 'Baik Sekali'])
            tanggal_akreditasi = datetime.now() - timedelta(days=random.randint(365, 1095))
            masa_berlaku = datetime.now() + timedelta(days=random.randint(365, 1825))

            data.append({
                'unit_name': fakultas,
                'unit_type': 'Fakultas',
                'fakultas': fakultas,
                'akreditasi_current': akreditasi_current,
                'tanggal_akreditasi': tanggal_akreditasi,
                'masa_berlaku': masa_berlaku,
                'akreditasi_previous': 'B',
                'status_renewal': random.choice(['On Track', 'In Progress']),
                'target_akreditasi': 'A',
                'progress_percentage': round(random.uniform(70, 90), 2),
                'tahun_akademik': '2024/2025'
            })

        # Institution accreditation
        data.append({
            'unit_name': 'Universitas Indonesia Raya',
            'unit_type': 'Institusi',
            'fakultas': 'All',
            'akreditasi_current': 'B',
            'tanggal_akreditasi': datetime.now() - timedelta(days=730),
            'masa_berlaku': datetime.now() + timedelta(days=1095),
            'akreditasi_previous': 'C',
            'status_renewal': 'In Progress',
            'target_akreditasi': 'A',
            'progress_percentage': 75.5,
            'tahun_akademik': '2024/2025'
        })

        df = pd.DataFrame(data)
        df.to_sql('accreditation_status', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {len(data)} accreditation status records")

    def generate_all(self):
        """Generate all institutional collection tables"""
        self.generate_faculty_statistics()  # Update existing with real data
        self.generate_university_performance()
        self.generate_accreditation_status()