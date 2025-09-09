# trainers/akademik_trainer.py
import logging

logger = logging.getLogger(__name__)


class AkademikTrainer:
    """Train akademik collection following repo style"""

    def __init__(self, trainer):
        self.trainer = trainer

    def train(self):
        """Train akademik collection"""
        logger.info("📚 Training akademik_collection...")

        # Train DDL first
        self.train_ddl()

        # Train documentation
        self.train_documentation()

        # Train question-SQL pairs
        self.train_sample_questions()

        logger.info("✅ akademik_collection training completed")

    def train_ddl(self):
        """Train with database schema (DDL)"""
        logger.info("📚 Training with database schema...")

        ddl_statements = [
            """
            -- Course Performance Summary
            CREATE TABLE datamart.course_performance
            (
                id                  SERIAL PRIMARY KEY,
                kode_matkul         VARCHAR(20)  NOT NULL,
                nama_matkul         VARCHAR(100) NOT NULL,
                fakultas            VARCHAR(100),
                program_studi       VARCHAR(100),
                sks                 INTEGER,
                semester            INTEGER,
                jenis_matkul        VARCHAR(20),
                dosen_pengampu      VARCHAR(100),
                jumlah_peserta      INTEGER,
                rata_rata_nilai     DECIMAL(5, 2),
                tingkat_kelulusan   DECIMAL(5, 2),
                rata_rata_kehadiran DECIMAL(5, 2),
                tahun_akademik      VARCHAR(20)
            );
            -- Contains course performance metrics including enrollment, grades, pass rates
            """,
            """
            -- Grade Distribution Analysis
            CREATE TABLE datamart.grade_distribution
            (
                id              SERIAL PRIMARY KEY,
                kode_matkul     VARCHAR(20)  NOT NULL,
                nama_matkul     VARCHAR(100) NOT NULL,
                fakultas        VARCHAR(100),
                program_studi   VARCHAR(100),
                dosen_pengampu  VARCHAR(100),
                jumlah_a        INTEGER DEFAULT 0,
                jumlah_ab       INTEGER DEFAULT 0,
                jumlah_b        INTEGER DEFAULT 0,
                jumlah_bc       INTEGER DEFAULT 0,
                jumlah_c        INTEGER DEFAULT 0,
                jumlah_d        INTEGER DEFAULT 0,
                jumlah_e        INTEGER DEFAULT 0,
                total_mahasiswa INTEGER,
                semester        VARCHAR(20),
                tahun_akademik  VARCHAR(20)
            );
            -- Contains grade distribution analysis across courses and programs
            """,
            """
            -- Academic Trends
            CREATE TABLE datamart.academic_trends
            (
                id                   SERIAL PRIMARY KEY,
                periode              VARCHAR(20) NOT NULL,
                fakultas             VARCHAR(100),
                program_studi        VARCHAR(100),
                metrik               VARCHAR(50),
                nilai                DECIMAL(10, 2),
                satuan               VARCHAR(20),
                persentase_perubahan DECIMAL(5, 2),
                kategori             VARCHAR(30),
                deskripsi            TEXT,
                tahun_akademik       VARCHAR(20)
            );
            -- Contains academic trends and performance indicators over time
            """
        ]

        for ddl in ddl_statements:
            self.trainer.add_schema_info("academic_schema", ddl.strip(), "ddl")

    def train_documentation(self):
        """Train with documentation about the academic system"""
        logger.info("📖 Training with documentation...")

        documentation_texts = [
            """
            Indonesian Academic Terms:
            - Mata Kuliah = Course/Subject
            - SKS = Credit Units (Sistem Kredit Semester)
            - Tingkat Kelulusan = Pass Rate
            - Nilai = Grade/Score
            - Kehadiran = Attendance
            - Semester = Academic Period
            - Jenis Matkul = Course Type
            - Dosen Pengampu = Course Lecturer
            - Peserta = Participants/Students
            """,
            """
            Academic Business Rules:
            - SKS ranges from 1 to 6 credits per course
            - Semester ranges from 1 to 8
            - Jenis matkul: 'Wajib' (Required), 'Pilihan' (Elective)
            - Nilai ranges from 0 to 100
            - Tingkat kelulusan percentage (0-100%)
            - Standard class size: 15-50 students
            - Grade distribution: A (85-100), A- (80-84), B+ (75-79), B (70-74), B- (65-69), C+ (60-64), C (55-59), C- (50-54), D+ (45-49), D (40-44), E (0-39)
            """,
            """
            Academic Datamart Structure:
            - course_performance: Complete course metrics without joins
            - grade_distribution: Grade analysis by course and lecturer
            - academic_trends: Performance trends over time
            - All tables contain fakultas and program_studi for filtering
            - Use aggregations like AVG, COUNT, SUM for analysis
            - Data is denormalized for optimal query performance
            """
        ]

        for doc in documentation_texts:
            self.trainer.add_documentation(doc.strip())

    def train_sample_questions(self):
        """Train with sample question-SQL pairs"""
        logger.info("🤖 Training with sample questions...")

        training_pairs = [
            {
                "question": "Mata kuliah dengan nilai rata-rata tertinggi",
                "sql": "SELECT nama_matkul, fakultas, program_studi, rata_rata_nilai, jumlah_peserta FROM datamart.course_performance ORDER BY rata_rata_nilai DESC LIMIT 10;"
            },
            {
                "question": "Tingkat kelulusan per program studi",
                "sql": "SELECT program_studi, fakultas, ROUND(AVG(tingkat_kelulusan), 2) as rata_kelulusan, COUNT(*) as jumlah_matkul FROM datamart.course_performance GROUP BY program_studi, fakultas ORDER BY rata_kelulusan DESC;"
            },
            {
                "question": "Mata kuliah dengan peserta terbanyak",
                "sql": "SELECT nama_matkul, kode_matkul, fakultas, program_studi, jumlah_peserta FROM datamart.course_performance ORDER BY jumlah_peserta DESC LIMIT 10;"
            },
            {
                "question": "Perbandingan kehadiran per fakultas",
                "sql": "SELECT fakultas, ROUND(AVG(rata_rata_kehadiran), 2) as rata_kehadiran, COUNT(*) as jumlah_matkul FROM datamart.course_performance GROUP BY fakultas ORDER BY rata_kehadiran DESC;"
            },
            {
                "question": "Mata kuliah dengan tingkat kelulusan rendah",
                "sql": "SELECT nama_matkul, fakultas, program_studi, tingkat_kelulusan, jumlah_peserta FROM datamart.course_performance WHERE tingkat_kelulusan < 80 ORDER BY tingkat_kelulusan ASC;"
            },
            {
                "question": "Distribusi SKS per fakultas",
                "sql": "SELECT fakultas, SUM(sks * jumlah_peserta) as total_sks_diambil, COUNT(*) as jumlah_matkul, ROUND(AVG(sks), 2) as rata_sks FROM datamart.course_performance GROUP BY fakultas ORDER BY total_sks_diambil DESC;"
            },
            {
                "question": "Mata kuliah wajib vs pilihan per fakultas",
                "sql": "SELECT fakultas, jenis_matkul, COUNT(*) as jumlah_matkul, ROUND(AVG(rata_rata_nilai), 2) as rata_nilai FROM datamart.course_performance GROUP BY fakultas, jenis_matkul ORDER BY fakultas, jenis_matkul;"
            },
            {
                "question": "Dosen dengan mata kuliah terbaik",
                "sql": "SELECT dosen_pengampu, fakultas, COUNT(*) as jumlah_matkul, ROUND(AVG(rata_rata_nilai), 2) as rata_nilai, ROUND(AVG(tingkat_kelulusan), 2) as rata_kelulusan FROM datamart.course_performance GROUP BY dosen_pengampu, fakultas ORDER BY rata_nilai DESC LIMIT 10;"
            },
            {
                "question": "Performa akademik per semester",
                "sql": "SELECT semester, COUNT(*) as jumlah_matkul, ROUND(AVG(rata_rata_nilai), 2) as rata_nilai, ROUND(AVG(tingkat_kelulusan), 2) as rata_kelulusan, ROUND(AVG(rata_rata_kehadiran), 2) as rata_kehadiran FROM datamart.course_performance GROUP BY semester ORDER BY semester;"
            },
            {
                "question": "Mata kuliah dengan kehadiran terendah",
                "sql": "SELECT nama_matkul, fakultas, program_studi, dosen_pengampu, rata_rata_kehadiran, jumlah_peserta FROM datamart.course_performance ORDER BY rata_rata_kehadiran ASC LIMIT 10;"
            }
        ]

        for pair in training_pairs:
            self.trainer.add_question_sql(pair["question"], pair["sql"])
            self.trainer.test_query(pair["question"], pair["sql"])