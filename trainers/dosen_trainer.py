# trainers/dosen_trainer.py
import logging

logger = logging.getLogger(__name__)


class DosenTrainer:
    """Train dosen collection following repo style"""

    def __init__(self, trainer):
        self.trainer = trainer

    def train(self):
        """Train dosen collection"""
        logger.info("👨‍🏫 Training dosen_collection...")

        # Train DDL first
        self.train_ddl()

        # Train documentation
        self.train_documentation()

        # Train question-SQL pairs
        self.train_sample_questions()

        logger.info("✅ dosen_collection training completed")

    def train_ddl(self):
        """Train with database schema (DDL)"""
        logger.info("📚 Training with database schema...")

        ddl_statements = [
            """
            -- Lecturer Profile & Workload
            CREATE TABLE datamart.lecturer_profile
            (
                id                        SERIAL PRIMARY KEY,
                nip                       VARCHAR(20)  NOT NULL,
                nama_dosen                VARCHAR(100) NOT NULL,
                jenis_kelamin             VARCHAR(20),
                fakultas                  VARCHAR(100),
                program_studi             VARCHAR(100),
                pendidikan_terakhir       VARCHAR(50),
                jabatan_fungsional        VARCHAR(50),
                golongan                  VARCHAR(10),
                total_mata_kuliah         INTEGER,
                total_mahasiswa_bimbingan INTEGER,
                beban_sks                 INTEGER,
                status_aktif              BOOLEAN,
                tahun_akademik            VARCHAR(20)
            );
            -- Contains lecturer profiles with NIP, name, faculty, education, position, workload
            """,
            """
            -- Lecturer Teaching Performance
            CREATE TABLE datamart.lecturer_teaching
            (
                id                  SERIAL PRIMARY KEY,
                nip                 VARCHAR(20)  NOT NULL,
                nama_dosen          VARCHAR(100) NOT NULL,
                fakultas            VARCHAR(100),
                mata_kuliah         VARCHAR(100),
                kode_matkul         VARCHAR(20),
                kelas               VARCHAR(10),
                jumlah_mahasiswa    INTEGER,
                rata_rata_nilai     DECIMAL(5, 2),
                rata_rata_kehadiran DECIMAL(5, 2),
                tingkat_kelulusan   DECIMAL(5, 2),
                semester            VARCHAR(20),
                tahun_akademik      VARCHAR(20)
            );
            -- Contains lecturer teaching performance with courses, students, grades, attendance
            """,
            """
            -- Lecturer Research & Activity
            CREATE TABLE datamart.lecturer_activity
            (
                id                    SERIAL PRIMARY KEY,
                nip                   VARCHAR(20)  NOT NULL,
                nama_dosen            VARCHAR(100) NOT NULL,
                fakultas              VARCHAR(100),
                jumlah_penelitian     INTEGER        DEFAULT 0,
                jumlah_publikasi      INTEGER        DEFAULT 0,
                jumlah_pengabdian     INTEGER        DEFAULT 0,
                total_dana_penelitian DECIMAL(15, 2) DEFAULT 0,
                pelatihan_diikuti     INTEGER        DEFAULT 0,
                sertifikasi_dimiliki  INTEGER        DEFAULT 0,
                tahun_akademik        VARCHAR(20)
            );
            -- Contains lecturer research and academic activities including publications, research funding
            """
        ]

        for ddl in ddl_statements:
            self.trainer.add_schema_info("lecturer_schema", ddl.strip(), "ddl")

    def train_documentation(self):
        """Train with documentation about the lecturer system"""
        logger.info("📖 Training with documentation...")

        documentation_texts = [
            """
            Indonesian Lecturer Terms:
            - Dosen = Lecturer/Professor
            - NIP = Lecturer ID Number (Nomor Induk Pegawai)
            - Jabatan Fungsional = Functional Position
            - Beban SKS = Teaching Load in Credits
            - Penelitian = Research
            - Publikasi = Publication
            - Pengabdian = Community Service
            - Bimbingan = Student Supervision/Mentoring
            - Golongan = Civil Service Grade
            """,
            """
            Lecturer Business Rules:
            - Jabatan fungsional: 'Asisten Ahli', 'Lektor', 'Lektor Kepala', 'Guru Besar'
            - Pendidikan terakhir: 'S2' (Master), 'S3' (Doctorate)
            - Standard teaching load: 12-24 SKS per semester
            - Minimum research requirement: 1 research per year
            - Standard class size: 15-45 students
            - Golongan ranges from III/a to IV/e for academic staff
            - Community service (pengabdian) is mandatory for lecturers
            """,
            """
            Lecturer Datamart Structure:
            - lecturer_profile: Basic info and workload without joins
            - lecturer_teaching: Teaching performance with course details
            - lecturer_activity: Research and academic activities
            - All tables contain fakultas for easy filtering
            - Use simple aggregations like AVG, COUNT, SUM
            - Data is denormalized - no need for complex joins
            """
        ]

        for doc in documentation_texts:
            self.trainer.add_documentation(doc.strip())

    def train_sample_questions(self):
        """Train with sample question-SQL pairs"""
        logger.info("🤖 Training with sample questions...")

        training_pairs = [
            {
                "question": "Berapa jumlah dosen aktif per fakultas?",
                "sql": "SELECT fakultas, COUNT(*) as jumlah_dosen FROM datamart.lecturer_profile WHERE status_aktif = true GROUP BY fakultas ORDER BY jumlah_dosen DESC;"
            },
            {
                "question": "Dosen dengan beban mengajar tertinggi",
                "sql": "SELECT nip, nama_dosen, fakultas, beban_sks, total_mata_kuliah FROM datamart.lecturer_profile WHERE status_aktif = true ORDER BY beban_sks DESC LIMIT 10;"
            },
            {
                "question": "Rata-rata nilai mata kuliah per dosen",
                "sql": "SELECT nip, nama_dosen, fakultas, ROUND(AVG(rata_rata_nilai), 2) as rata_nilai_mengajar, COUNT(*) as jumlah_matkul FROM datamart.lecturer_teaching GROUP BY nip, nama_dosen, fakultas ORDER BY rata_nilai_mengajar DESC;"
            },
            {
                "question": "Dosen dengan publikasi terbanyak",
                "sql": "SELECT nip, nama_dosen, fakultas, jumlah_publikasi, jumlah_penelitian FROM datamart.lecturer_activity ORDER BY jumlah_publikasi DESC LIMIT 10;"
            },
            {
                "question": "Distribusi jabatan fungsional dosen",
                "sql": "SELECT jabatan_fungsional, COUNT(*) as jumlah, ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as persentase FROM datamart.lecturer_profile WHERE status_aktif = true GROUP BY jabatan_fungsional ORDER BY jumlah DESC;"
            },
            {
                "question": "Dosen dengan dana penelitian terbesar",
                "sql": "SELECT nip, nama_dosen, fakultas, total_dana_penelitian, jumlah_penelitian FROM datamart.lecturer_activity WHERE total_dana_penelitian > 0 ORDER BY total_dana_penelitian DESC LIMIT 10;"
            },
            {
                "question": "Tingkat kelulusan rata-rata per dosen",
                "sql": "SELECT nip, nama_dosen, fakultas, ROUND(AVG(tingkat_kelulusan), 2) as rata_kelulusan, COUNT(*) as jumlah_kelas FROM datamart.lecturer_teaching GROUP BY nip, nama_dosen, fakultas ORDER BY rata_kelulusan DESC;"
            },
            {
                "question": "Dosen dengan mahasiswa bimbingan terbanyak",
                "sql": "SELECT nip, nama_dosen, fakultas, total_mahasiswa_bimbingan, jabatan_fungsional FROM datamart.lecturer_profile WHERE status_aktif = true ORDER BY total_mahasiswa_bimbingan DESC LIMIT 10;"
            },
            {
                "question": "Perbandingan penelitian per jabatan fungsional",
                "sql": "SELECT lp.jabatan_fungsional, COUNT(*) as jumlah_dosen, ROUND(AVG(la.jumlah_penelitian), 2) as rata_penelitian, ROUND(AVG(la.jumlah_publikasi), 2) as rata_publikasi FROM datamart.lecturer_profile lp JOIN datamart.lecturer_activity la ON lp.nip = la.nip WHERE lp.status_aktif = true GROUP BY lp.jabatan_fungsional ORDER BY rata_penelitian DESC;"
            },
            {
                "question": "Dosen dengan pengabdian masyarakat terbanyak",
                "sql": "SELECT nip, nama_dosen, fakultas, jumlah_pengabdian, jumlah_penelitian FROM datamart.lecturer_activity ORDER BY jumlah_pengabdian DESC LIMIT 10;"
            }
        ]

        for pair in training_pairs:
            self.trainer.add_question_sql(pair["question"], pair["sql"])
            self.trainer.test_query(pair["question"], pair["sql"])