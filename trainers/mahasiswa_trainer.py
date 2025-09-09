# trainers/mahasiswa_trainer.py
import logging

logger = logging.getLogger(__name__)


class MahasiswaTrainer:
    """Train mahasiswa collection following repo style"""

    def __init__(self, trainer):
        self.trainer = trainer

    def train(self):
        """Train mahasiswa collection"""
        logger.info("👨‍🎓 Training mahasiswa_collection...")

        # Train DDL first
        self.train_ddl()

        # Train documentation
        self.train_documentation()

        # Train question-SQL pairs
        self.train_sample_questions()

        logger.info("✅ mahasiswa_collection training completed")

    def train_ddl(self):
        """Train with database schema (DDL)"""
        logger.info("📚 Training with database schema...")

        ddl_statements = [
            """
            -- Student Academic Performance
            CREATE TABLE datamart.student_performance
            (
                id               SERIAL PRIMARY KEY,
                nim              VARCHAR(20)  NOT NULL,
                nama_mahasiswa   VARCHAR(100) NOT NULL,
                jenis_kelamin    VARCHAR(20),
                fakultas         VARCHAR(100),
                program_studi    VARCHAR(100),
                angkatan         INTEGER,
                semester_aktif   INTEGER,
                ipk              DECIMAL(3, 2),
                total_sks        INTEGER,
                sks_lulus        INTEGER,
                status_mahasiswa VARCHAR(20),
                tahun_akademik   VARCHAR(20)
            );
            -- Contains student academic performance with NIM, name, faculty, program, GPA, credits, status
            """,
            """
            -- Student Attendance Summary
            CREATE TABLE datamart.student_attendance
            (
                id                   SERIAL PRIMARY KEY,
                nim                  VARCHAR(20)  NOT NULL,
                nama_mahasiswa       VARCHAR(100) NOT NULL,
                fakultas             VARCHAR(100),
                program_studi        VARCHAR(100),
                mata_kuliah          VARCHAR(100),
                kode_matkul          VARCHAR(20),
                semester             INTEGER,
                total_pertemuan      INTEGER DEFAULT 14,
                hadir                INTEGER,
                izin                 INTEGER,
                alpha                INTEGER,
                persentase_kehadiran DECIMAL(5, 2),
                tahun_akademik       VARCHAR(20)
            );
            -- Contains student attendance records with course attendance percentages
            """,
            """
            -- Student Financial Status
            CREATE TABLE datamart.student_finance
            (
                id                SERIAL PRIMARY KEY,
                nim               VARCHAR(20)  NOT NULL,
                nama_mahasiswa    VARCHAR(100) NOT NULL,
                fakultas          VARCHAR(100),
                program_studi     VARCHAR(100),
                semester          VARCHAR(20),
                tahun_akademik    VARCHAR(20),
                jumlah_tagihan    DECIMAL(12, 2),
                jumlah_dibayar    DECIMAL(12, 2),
                sisa_tagihan      DECIMAL(12, 2),
                status_pembayaran VARCHAR(30),
                tanggal_bayar     DATE,
                metode_pembayaran VARCHAR(50)
            );
            -- Contains student financial records including tuition payments and outstanding balances
            """
        ]

        for ddl in ddl_statements:
            self.trainer.add_schema_info("student_schema", ddl.strip())

    def train_documentation(self):
        """Train with documentation about the student system"""
        logger.info("📖 Training with documentation...")

        documentation_texts = [
            """
            Indonesian Student Terms:
            - Mahasiswa = Student
            - NIM = Student ID Number (Nomor Induk Mahasiswa) 
            - IPK = GPA (Indeks Prestasi Kumulatif)
            - SKS = Credit Units (Sistem Kredit Semester)
            - Angkatan = Academic Year/Batch
            - Status Mahasiswa = Student Status
            - Fakultas = Faculty
            - Program Studi = Study Program/Major
            - Kehadiran = Attendance
            - Tagihan = Billing/Invoice
            - Lunas = Paid in Full
            """,
            """
            Student Business Rules:
            - IPK (GPA) ranges from 0.00 to 4.00
            - Status mahasiswa: 'Aktif' (Active), 'Cuti' (Leave), 'Lulus' (Graduated), 'DO' (Dropped Out)
            - Minimum attendance requirement: 75% to be eligible for exams
            - Standard semester duration: 14 meetings per course
            - Status pembayaran: 'Lunas' (Paid), 'Belum Lunas' (Partially Paid), 'Menunggak' (Outstanding)
            - Angkatan represents the year student enrolled (e.g., 2020, 2021)
            """,
            """
            Student Datamart Structure:
            - student_performance: Academic data without joins - contains all student academic info
            - student_attendance: Attendance data with course details - no need to join with courses table
            - student_finance: Financial data with payment status - contains all billing info
            - All tables contain fakultas and program_studi for easy filtering
            - Use simple WHERE clauses instead of complex JOINs
            - Data is denormalized for fast query performance
            """
        ]

        for doc in documentation_texts:
            self.trainer.add_schema_info("student_documentation", doc.strip())

    def train_sample_questions(self):
        """Train with sample question-SQL pairs"""
        logger.info("🤖 Training with sample questions...")

        training_pairs = [
            {
                "question": "Berapa jumlah mahasiswa aktif?",
                "sql": "SELECT COUNT(*) as total_mahasiswa_aktif FROM datamart.student_performance WHERE status_mahasiswa = 'Aktif';"
            },
            {
                "question": "Berapa total mahasiswa aktif?",
                "sql": "SELECT COUNT(nim) as total_mahasiswa FROM datamart.student_performance WHERE status_mahasiswa = 'Aktif';"
            },
            {
                "question": "Siapa mahasiswa dengan IPK tertinggi?",
                "sql": "SELECT nim, nama_mahasiswa, ipk, fakultas, program_studi FROM datamart.student_performance WHERE status_mahasiswa = 'Aktif' ORDER BY ipk DESC LIMIT 1;"
            },
            {
                "question": "Berapa rata-rata IPK per fakultas?",
                "sql": "SELECT fakultas, ROUND(AVG(ipk), 2) as rata_rata_ipk, COUNT(*) as jumlah_mahasiswa FROM datamart.student_performance WHERE status_mahasiswa = 'Aktif' GROUP BY fakultas ORDER BY rata_rata_ipk DESC;"
            },
            {
                "question": "Daftar mahasiswa dengan IPK di atas 3.5",
                "sql": "SELECT nim, nama_mahasiswa, ipk, fakultas, program_studi FROM datamart.student_performance WHERE ipk > 3.5 AND status_mahasiswa = 'Aktif' ORDER BY ipk DESC;"
            },
            {
                "question": "Mahasiswa dengan kehadiran di bawah 75%",
                "sql": "SELECT DISTINCT nim, nama_mahasiswa, fakultas, program_studi, AVG(persentase_kehadiran) as rata_kehadiran FROM datamart.student_attendance GROUP BY nim, nama_mahasiswa, fakultas, program_studi HAVING AVG(persentase_kehadiran) < 75 ORDER BY rata_kehadiran ASC;"
            },
            {
                "question": "Status pembayaran mahasiswa per fakultas",
                "sql": "SELECT fakultas, status_pembayaran, COUNT(*) as jumlah, ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY fakultas), 2) as persentase FROM datamart.student_finance GROUP BY fakultas, status_pembayaran ORDER BY fakultas, jumlah DESC;"
            },
            {
                "question": "Mahasiswa dengan tunggakan terbesar",
                "sql": "SELECT nim, nama_mahasiswa, fakultas, program_studi, sisa_tagihan FROM datamart.student_finance WHERE status_pembayaran = 'Menunggak' ORDER BY sisa_tagihan DESC LIMIT 10;"
            },
            {
                "question": "Distribusi mahasiswa per angkatan",
                "sql": "SELECT angkatan, COUNT(*) as jumlah_mahasiswa, ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as persentase FROM datamart.student_performance WHERE status_mahasiswa = 'Aktif' GROUP BY angkatan ORDER BY angkatan DESC;"
            },
            {
                "question": "Mahasiswa dengan IPK tertinggi per program studi",
                "sql": "SELECT program_studi, fakultas, nim, nama_mahasiswa, ipk FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY program_studi ORDER BY ipk DESC) as rn FROM datamart.student_performance WHERE status_mahasiswa = 'Aktif') t WHERE rn = 1 ORDER BY ipk DESC;"
            }
        ]

        for pair in training_pairs:
            self.trainer.add_question_sql(pair["question"], pair["sql"])
            self.trainer.test_query(pair["question"], pair["sql"])