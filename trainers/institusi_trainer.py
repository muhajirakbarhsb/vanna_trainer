# trainers/institusi_trainer.py
import logging
import random
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class InstitusiTrainer:
    """Train institusi collection following repo style"""

    def __init__(self, trainer):
        self.trainer = trainer

    def train(self):
        """Train institusi collection"""
        logger.info("🏛️ Training institusi_collection...")

        # Generate additional institutional data first
        self._generate_institutional_data()

        # Train DDL first
        self.train_ddl()

        # Train documentation
        self.train_documentation()

        # Train question-SQL pairs
        self.train_sample_questions()

        logger.info("✅ institusi_collection training completed")

    def _generate_institutional_data(self):
        """Generate additional institutional datamart data"""
        logger.info("🏛️ Generating additional institutional data...")

        try:
            engine = self.trainer.db_engine

            fakultas_list = [
                'Fakultas Teknik',
                'Fakultas Ekonomi dan Bisnis',
                'Fakultas Ilmu Komputer',
                'Fakultas Kedokteran',
                'Fakultas Hukum'
            ]

            prodi_dict = {
                'Fakultas Teknik': ['Teknik Informatika', 'Teknik Elektro', 'Teknik Sipil', 'Teknik Mesin',
                                    'Teknik Industri'],
                'Fakultas Ekonomi dan Bisnis': ['Manajemen', 'Akuntansi', 'Ekonomi Pembangunan', 'Bisnis Digital'],
                'Fakultas Ilmu Komputer': ['Sistem Informasi', 'Ilmu Komputer', 'Teknologi Informasi'],
                'Fakultas Kedokteran': ['Pendidikan Dokter', 'Keperawatan'],
                'Fakultas Hukum': ['Ilmu Hukum', 'Hukum Bisnis']
            }

            # Generate university performance data
            perf_data = []
            for periode in ['2023/2024', '2024/2025']:
                perf_data.append({
                    'periode': periode,
                    'total_mahasiswa': random.randint(3000, 5000),
                    'total_dosen': random.randint(200, 400),
                    'total_program_studi': random.randint(15, 25),
                    'total_fakultas': 5,
                    'rata_rata_ipk_universitas': round(random.uniform(3.0, 3.8), 2),
                    'tingkat_kelulusan': round(random.uniform(85, 95), 2),
                    'tingkat_drop_out': round(random.uniform(3, 8), 2),
                    'student_lecturer_ratio': round(random.uniform(15, 25), 2),
                    'tingkat_kepuasan_mahasiswa': round(random.uniform(75, 90), 2),
                    'akreditasi_institusi': 'B',
                    'tahun_akademik': periode
                })

            df = pd.DataFrame(perf_data)
            df.to_sql('university_performance', engine, schema='datamart', if_exists='append', index=False)

            # Generate accreditation status data
            accred_data = []

            # Program studi accreditations
            for fakultas in fakultas_list:
                for prodi in prodi_dict[fakultas]:
                    accred_data.append({
                        'unit_name': prodi,
                        'unit_type': 'Program Studi',
                        'fakultas': fakultas,
                        'akreditasi_current': random.choice(['A', 'B', 'C', 'Unggul', 'Baik Sekali']),
                        'tanggal_akreditasi': datetime.now() - timedelta(days=random.randint(365, 1095)),
                        'masa_berlaku': datetime.now() + timedelta(days=random.randint(365, 1825)),
                        'akreditasi_previous': random.choice(['B', 'C', 'Baik']),
                        'status_renewal': random.choice(['On Track', 'Needs Attention', 'In Progress']),
                        'target_akreditasi': random.choice(['A', 'Unggul']),
                        'progress_percentage': round(random.uniform(60, 95), 2),
                        'tahun_akademik': '2024/2025'
                    })

            # Faculty accreditations
            for fakultas in fakultas_list:
                accred_data.append({
                    'unit_name': fakultas,
                    'unit_type': 'Fakultas',
                    'fakultas': fakultas,
                    'akreditasi_current': random.choice(['A', 'B', 'Unggul', 'Baik Sekali']),
                    'tanggal_akreditasi': datetime.now() - timedelta(days=random.randint(365, 1095)),
                    'masa_berlaku': datetime.now() + timedelta(days=random.randint(365, 1825)),
                    'akreditasi_previous': 'B',
                    'status_renewal': random.choice(['On Track', 'In Progress']),
                    'target_akreditasi': 'A',
                    'progress_percentage': round(random.uniform(70, 90), 2),
                    'tahun_akademik': '2024/2025'
                })

            # Institution accreditation
            accred_data.append({
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

            df = pd.DataFrame(accred_data)
            df.to_sql('accreditation_status', engine, schema='datamart', if_exists='append', index=False)

            logger.info("✅ Institutional data generated successfully")

        except Exception as e:
            logger.error(f"❌ Error generating institutional data: {e}")

    def train_ddl(self):
        """Train with database schema (DDL)"""
        logger.info("📚 Training with database schema...")

        ddl_statements = [
            """
            -- Faculty Statistics
            CREATE TABLE datamart.faculty_statistics
            (
                id                       SERIAL PRIMARY KEY,
                fakultas                 VARCHAR(100) NOT NULL,
                dekan                    VARCHAR(100),
                tahun_berdiri            INTEGER,
                jumlah_program_studi     INTEGER,
                jumlah_dosen             INTEGER,
                jumlah_mahasiswa_aktif   INTEGER,
                jumlah_lulusan_tahun_ini INTEGER,
                rata_rata_ipk_fakultas   DECIMAL(3, 2),
                tingkat_kehadiran_rata   DECIMAL(5, 2),
                akreditasi_fakultas      VARCHAR(20),
                ranking_nasional         INTEGER,
                tahun_akademik           VARCHAR(20)
            );
            -- Contains faculty-level statistics including student counts, lecturer counts, GPA averages
            """,
            """
            -- University Performance
            CREATE TABLE datamart.university_performance
            (
                id                         SERIAL PRIMARY KEY,
                periode                    VARCHAR(20) NOT NULL,
                total_mahasiswa            INTEGER,
                total_dosen                INTEGER,
                total_program_studi        INTEGER,
                total_fakultas             INTEGER,
                rata_rata_ipk_universitas  DECIMAL(3, 2),
                tingkat_kelulusan          DECIMAL(5, 2),
                tingkat_drop_out           DECIMAL(5, 2),
                student_lecturer_ratio     DECIMAL(5, 2),
                tingkat_kepuasan_mahasiswa DECIMAL(5, 2),
                akreditasi_institusi       VARCHAR(20),
                tahun_akademik             VARCHAR(20)
            );
            -- Contains university-wide performance metrics and KPIs
            """,
            """
            -- Accreditation Status
            CREATE TABLE datamart.accreditation_status
            (
                id                  SERIAL PRIMARY KEY,
                unit_name           VARCHAR(100) NOT NULL,
                unit_type           VARCHAR(20),
                fakultas            VARCHAR(100),
                akreditasi_current  VARCHAR(20),
                tanggal_akreditasi  DATE,
                masa_berlaku        DATE,
                akreditasi_previous VARCHAR(20),
                status_renewal      VARCHAR(30),
                target_akreditasi   VARCHAR(20),
                progress_percentage DECIMAL(5, 2),
                tahun_akademik      VARCHAR(20)
            );
            -- Contains accreditation status and progress for programs, faculties, and institution
            """
        ]

        for ddl in ddl_statements:
            self.trainer.add_schema_info("institutional_schema", ddl.strip())

    def train_documentation(self):
        """Train with documentation about the institutional system"""
        logger.info("📖 Training with documentation...")

        documentation_texts = [
            """
            Indonesian Institutional Terms:
            - Fakultas = Faculty
            - Dekan = Dean
            - Akreditasi = Accreditation
            - Institusi = Institution
            - Ranking = Ranking/Rating
            - Tingkat Kelulusan = Graduation Rate
            - Tingkat Drop Out = Dropout Rate
            - Kepuasan Mahasiswa = Student Satisfaction
            - Program Studi = Study Program
            - Performa = Performance
            """,
            """
            Institutional Business Rules:
            - Akreditasi levels: 'A', 'B', 'C', 'Unggul', 'Baik Sekali', 'Baik'
            - Unit types: 'Program Studi', 'Fakultas', 'Institusi'
            - Status renewal: 'On Track', 'Needs Attention', 'In Progress'
            - Student-lecturer ratio: ideal range 15-25 students per lecturer
            - Accreditation validity: typically 5 years
            - Progress percentage: 0-100% completion towards renewal
            """,
            """
            Institutional Datamart Structure:
            - faculty_statistics: Complete faculty metrics without joins
            - university_performance: University-wide KPIs and trends
            - accreditation_status: Accreditation tracking and progress
            - All tables designed for direct queries without complex joins
            - Use aggregations and date calculations for analysis
            - Data is denormalized for optimal performance
            """
        ]

        for doc in documentation_texts:
            self.trainer.add_schema_info("institutional_documentation", doc.strip())

    def train_sample_questions(self):
        """Train with sample question-SQL pairs"""
        logger.info("🤖 Training with sample questions...")

        training_pairs = [
            {
                "question": "Statistik per fakultas",
                "sql": "SELECT fakultas, jumlah_program_studi, jumlah_dosen, jumlah_mahasiswa_aktif, rata_rata_ipk_fakultas, akreditasi_fakultas FROM datamart.faculty_statistics ORDER BY jumlah_mahasiswa_aktif DESC;"
            },
            {
                "question": "Fakultas dengan IPK tertinggi",
                "sql": "SELECT fakultas, rata_rata_ipk_fakultas, jumlah_mahasiswa_aktif FROM datamart.faculty_statistics ORDER BY rata_rata_ipk_fakultas DESC LIMIT 5;"
            },
            {
                "question": "Rasio dosen mahasiswa per fakultas",
                "sql": "SELECT fakultas, jumlah_dosen, jumlah_mahasiswa_aktif, ROUND(jumlah_mahasiswa_aktif::decimal / jumlah_dosen, 2) as rasio_mahasiswa_dosen FROM datamart.faculty_statistics ORDER BY rasio_mahasiswa_dosen DESC;"
            },
            {
                "question": "Performa universitas secara keseluruhan",
                "sql": "SELECT periode, total_mahasiswa, total_dosen, rata_rata_ipk_universitas, tingkat_kelulusan, tingkat_drop_out, student_lecturer_ratio FROM datamart.university_performance ORDER BY periode DESC LIMIT 1;"
            },
            {
                "question": "Status akreditasi program studi",
                "sql": "SELECT unit_name, fakultas, akreditasi_current, tanggal_akreditasi, masa_berlaku, status_renewal FROM datamart.accreditation_status WHERE unit_type = 'Program Studi' ORDER BY masa_berlaku ASC;"
            },
            {
                "question": "Program studi yang perlu renewal akreditasi",
                "sql": "SELECT unit_name, fakultas, akreditasi_current, masa_berlaku, EXTRACT(DAYS FROM masa_berlaku - CURRENT_DATE) as hari_tersisa FROM datamart.accreditation_status WHERE unit_type = 'Program Studi' AND masa_berlaku <= CURRENT_DATE + INTERVAL '1 year' ORDER BY masa_berlaku ASC;"
            },
            {
                "question": "Progress akreditasi institusi",
                "sql": "SELECT unit_name, akreditasi_current, target_akreditasi, progress_percentage, status_renewal FROM datamart.accreditation_status WHERE unit_type = 'Institusi';"
            },
            {
                "question": "Fakultas dengan akreditasi terbaik",
                "sql": "SELECT fakultas, akreditasi_fakultas, jumlah_program_studi, rata_rata_ipk_fakultas FROM datamart.faculty_statistics WHERE akreditasi_fakultas IN ('A', 'Unggul') ORDER BY akreditasi_fakultas, rata_rata_ipk_fakultas DESC;"
            },
            {
                "question": "Trend performa universitas",
                "sql": "SELECT periode, total_mahasiswa, total_dosen, rata_rata_ipk_universitas, tingkat_kelulusan, tingkat_kepuasan_mahasiswa FROM datamart.university_performance ORDER BY periode;"
            },
            {
                "question": "Distribusi akreditasi program studi",
                "sql": "SELECT akreditasi_current, COUNT(*) as jumlah_prodi, ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as persentase FROM datamart.accreditation_status WHERE unit_type = 'Program Studi' GROUP BY akreditasi_current ORDER BY jumlah_prodi DESC;"
            },
            {
                "question": "Fakultas dengan lulusan terbanyak",
                "sql": "SELECT fakultas, jumlah_lulusan_tahun_ini, jumlah_mahasiswa_aktif, ROUND(jumlah_lulusan_tahun_ini * 100.0 / jumlah_mahasiswa_aktif, 2) as tingkat_kelulusan_fakultas FROM datamart.faculty_statistics ORDER BY jumlah_lulusan_tahun_ini DESC;"
            },
            {
                "question": "Status renewal akreditasi per fakultas",
                "sql": "SELECT a.fakultas, COUNT(*) as total_unit, SUM(CASE WHEN a.status_renewal = 'On Track' THEN 1 ELSE 0 END) as on_track, SUM(CASE WHEN a.status_renewal = 'Needs Attention' THEN 1 ELSE 0 END) as needs_attention, ROUND(AVG(a.progress_percentage), 2) as rata_progress FROM datamart.accreditation_status a WHERE a.unit_type = 'Program Studi' GROUP BY a.fakultas ORDER BY rata_progress DESC;"
            }
        ]

        for pair in training_pairs:
            self.trainer.add_question_sql(pair["question"], pair["sql"])
            self.trainer.test_query(pair["question"], pair["sql"])