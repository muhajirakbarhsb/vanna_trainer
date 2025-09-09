# trainers/keuangan_trainer.py
import logging
import random
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


class KeuanganTrainer:
    """Train keuangan collection following repo style"""

    def __init__(self, trainer):
        self.trainer = trainer

    def train(self):
        """Train keuangan collection"""
        logger.info("💰 Training keuangan_collection...")

        # Generate additional financial data first
        self._generate_financial_data()

        # Train DDL first
        self.train_ddl()

        # Train documentation
        self.train_documentation()

        # Train question-SQL pairs
        self.train_sample_questions()

        logger.info("✅ keuangan_collection training completed")

    def _generate_financial_data(self):
        """Generate additional financial datamart data"""
        logger.info("💰 Generating additional financial data...")

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

            # Generate revenue summary data
            revenue_data = []
            for fakultas in fakultas_list:
                for prodi in prodi_dict[fakultas]:
                    for periode in ['2024-1', '2024-2']:
                        total_tagihan = random.randint(500000000, 2000000000)
                        collection_rate = random.uniform(75, 95)
                        total_terbayar = total_tagihan * (collection_rate / 100)

                        revenue_data.append({
                            'periode': periode,
                            'fakultas': fakultas,
                            'program_studi': prodi,
                            'jenis_pendapatan': 'SPP',
                            'total_tagihan': total_tagihan,
                            'total_terbayar': total_terbayar,
                            'total_outstanding': total_tagihan - total_terbayar,
                            'jumlah_mahasiswa': random.randint(50, 200),
                            'tingkat_kolektibilitas': round(collection_rate, 2),
                            'tahun_akademik': '2024/2025'
                        })

            df = pd.DataFrame(revenue_data)
            df.to_sql('revenue_summary', engine, schema='datamart', if_exists='append', index=False)

            # Generate payment analysis data
            payment_data = []
            payment_methods = ['Transfer Bank', 'Virtual Account', 'Kartu Kredit', 'E-wallet', 'Cash']

            for fakultas in fakultas_list:
                for method in payment_methods:
                    for periode in ['2024-1', '2024-2']:
                        payment_data.append({
                            'periode': periode,
                            'fakultas': fakultas,
                            'metode_pembayaran': method,
                            'jumlah_transaksi': random.randint(50, 500),
                            'total_nominal': random.randint(100000000, 1000000000),
                            'rata_rata_waktu_bayar': random.randint(1, 30),
                            'tingkat_keterlambatan': round(random.uniform(5, 25), 2),
                            'jumlah_cicilan': random.randint(0, 10),
                            'tahun_akademik': '2024/2025'
                        })

            df = pd.DataFrame(payment_data)
            df.to_sql('payment_analysis', engine, schema='datamart', if_exists='append', index=False)

            # Generate financial KPI data
            kpi_data = []
            for periode in ['2024-1', '2024-2']:
                for fakultas in fakultas_list:
                    kpi_data.append({
                        'periode': periode,
                        'fakultas': fakultas,
                        'total_revenue': random.randint(1000000000, 5000000000),
                        'collection_rate': round(random.uniform(80, 95), 2),
                        'bad_debt_ratio': round(random.uniform(2, 8), 2),
                        'average_payment_time': random.randint(15, 45),
                        'scholarship_disbursed': random.randint(50000000, 300000000),
                        'operational_cost': random.randint(800000000, 2000000000),
                        'net_income': random.randint(200000000, 1000000000),
                        'tahun_akademik': '2024/2025'
                    })

            df = pd.DataFrame(kpi_data)
            df.to_sql('financial_kpi', engine, schema='datamart', if_exists='append', index=False)

            logger.info("✅ Financial data generated successfully")

        except Exception as e:
            logger.error(f"❌ Error generating financial data: {e}")

    def train_ddl(self):
        """Train with database schema (DDL)"""
        logger.info("📚 Training with database schema...")

        ddl_statements = [
            """
            -- Revenue Summary
            CREATE TABLE datamart.revenue_summary
            (
                id                     SERIAL PRIMARY KEY,
                periode                VARCHAR(20) NOT NULL,
                fakultas               VARCHAR(100),
                program_studi          VARCHAR(100),
                jenis_pendapatan       VARCHAR(50),
                total_tagihan          DECIMAL(15, 2),
                total_terbayar         DECIMAL(15, 2),
                total_outstanding      DECIMAL(15, 2),
                jumlah_mahasiswa       INTEGER,
                tingkat_kolektibilitas DECIMAL(5, 2),
                tahun_akademik         VARCHAR(20)
            );
            -- Contains revenue summary by faculty and program including collection rates
            """,
            """
            -- Payment Analysis
            CREATE TABLE datamart.payment_analysis
            (
                id                    SERIAL PRIMARY KEY,
                periode               VARCHAR(20) NOT NULL,
                fakultas              VARCHAR(100),
                metode_pembayaran     VARCHAR(50),
                jumlah_transaksi      INTEGER,
                total_nominal         DECIMAL(15, 2),
                rata_rata_waktu_bayar INTEGER,
                tingkat_keterlambatan DECIMAL(5, 2),
                jumlah_cicilan        INTEGER DEFAULT 0,
                tahun_akademik        VARCHAR(20)
            );
            -- Contains payment method analysis and collection patterns
            """,
            """
            -- Financial KPI
            CREATE TABLE datamart.financial_kpi
            (
                id                    SERIAL PRIMARY KEY,
                periode               VARCHAR(20) NOT NULL,
                fakultas              VARCHAR(100),
                total_revenue         DECIMAL(15, 2),
                collection_rate       DECIMAL(5, 2),
                bad_debt_ratio        DECIMAL(5, 2),
                average_payment_time  INTEGER,
                scholarship_disbursed DECIMAL(15, 2),
                operational_cost      DECIMAL(15, 2),
                net_income            DECIMAL(15, 2),
                tahun_akademik        VARCHAR(20)
            );
            -- Contains financial key performance indicators and metrics
            """
        ]

        for ddl in ddl_statements:
            self.trainer.add_schema_info("financial_schema", ddl.strip(), "ddl")

    def train_documentation(self):
        """Train with documentation about the financial system"""
        logger.info("📖 Training with documentation...")

        documentation_texts = [
            """
            Indonesian Financial Terms:
            - Pendapatan = Revenue
            - Tagihan = Billing/Invoice
            - Terbayar = Paid Amount
            - Outstanding = Outstanding Balance
            - Kolektibilitas = Collection Rate
            - SPP = Tuition Fee (Sumbangan Pembinaan Pendidikan)
            - Cicilan = Installment
            - Beasiswa = Scholarship
            - Biaya Operasional = Operational Cost
            """,
            """
            Financial Business Rules:
            - Collection rate: percentage of billed amount collected
            - Bad debt ratio: percentage of uncollectable debt
            - Payment methods: Transfer Bank, Virtual Account, Kartu Kredit, E-wallet
            - Average payment time: days from billing to payment
            - Outstanding: total_tagihan - total_terbayar
            - Tingkat keterlambatan: percentage of late payments
            - All amounts in Indonesian Rupiah (IDR)
            """,
            """
            Financial Datamart Structure:
            - revenue_summary: Revenue data by faculty and program
            - payment_analysis: Payment method and timing analysis
            - financial_kpi: Key financial performance indicators
            - All amounts in Indonesian Rupiah (IDR)
            - Use SUM for totals, AVG for rates and percentages
            - Data is denormalized for fast query performance
            """
        ]

        for doc in documentation_texts:
            self.trainer.add_documentation(doc.strip())

    def train_sample_questions(self):
        """Train with sample question-SQL pairs"""
        logger.info("🤖 Training with sample questions...")

        training_pairs = [
            {
                "question": "Total pendapatan per fakultas",
                "sql": "SELECT fakultas, SUM(total_terbayar) as total_pendapatan, SUM(total_tagihan) as total_tagihan, ROUND(SUM(total_terbayar) * 100.0 / SUM(total_tagihan), 2) as tingkat_koleksi FROM datamart.revenue_summary GROUP BY fakultas ORDER BY total_pendapatan DESC;"
            },
            {
                "question": "Metode pembayaran paling populer",
                "sql": "SELECT metode_pembayaran, SUM(jumlah_transaksi) as total_transaksi, SUM(total_nominal) as total_nominal FROM datamart.payment_analysis GROUP BY metode_pembayaran ORDER BY total_transaksi DESC;"
            },
            {
                "question": "Tingkat kolektibilitas per program studi",
                "sql": "SELECT program_studi, fakultas, ROUND(AVG(tingkat_kolektibilitas), 2) as rata_kolektibilitas FROM datamart.revenue_summary GROUP BY program_studi, fakultas ORDER BY rata_kolektibilitas DESC;"
            },
            {
                "question": "Outstanding pembayaran terbesar",
                "sql": "SELECT fakultas, program_studi, SUM(total_outstanding) as total_piutang FROM datamart.revenue_summary GROUP BY fakultas, program_studi ORDER BY total_piutang DESC;"
            },
            {
                "question": "KPI keuangan universitas",
                "sql": "SELECT periode, SUM(total_revenue) as total_revenue, ROUND(AVG(collection_rate), 2) as avg_collection_rate, ROUND(AVG(bad_debt_ratio), 2) as avg_bad_debt FROM datamart.financial_kpi GROUP BY periode ORDER BY periode DESC;"
            },
            {
                "question": "Perbandingan pendapatan per periode",
                "sql": "SELECT rs.periode, SUM(rs.total_terbayar) as pendapatan, SUM(rs.total_outstanding) as piutang, COUNT(DISTINCT rs.fakultas) as jumlah_fakultas FROM datamart.revenue_summary rs GROUP BY rs.periode ORDER BY rs.periode;"
            },
            {
                "question": "Fakultas dengan tingkat keterlambatan pembayaran tertinggi",
                "sql": "SELECT fakultas, ROUND(AVG(tingkat_keterlambatan), 2) as rata_keterlambatan, SUM(jumlah_transaksi) as total_transaksi FROM datamart.payment_analysis GROUP BY fakultas ORDER BY rata_keterlambatan DESC;"
            },
            {
                "question": "Rata-rata waktu pembayaran per metode",
                "sql": "SELECT metode_pembayaran, ROUND(AVG(rata_rata_waktu_bayar), 2) as rata_waktu_bayar, SUM(jumlah_transaksi) as total_transaksi FROM datamart.payment_analysis GROUP BY metode_pembayaran ORDER BY rata_waktu_bayar ASC;"
            },
            {
                "question": "Profitabilitas per fakultas",
                "sql": "SELECT fakultas, SUM(total_revenue) as revenue, SUM(operational_cost) as cost, SUM(net_income) as profit, ROUND(SUM(net_income) * 100.0 / SUM(total_revenue), 2) as profit_margin FROM datamart.financial_kpi GROUP BY fakultas ORDER BY profit DESC;"
            },
            {
                "question": "Total beasiswa yang disalurkan",
                "sql": "SELECT periode, fakultas, SUM(scholarship_disbursed) as total_beasiswa, COUNT(*) as jumlah_record FROM datamart.financial_kpi GROUP BY periode, fakultas ORDER BY total_beasiswa DESC;"
            }
        ]

        for pair in training_pairs:
            self.trainer.add_question_sql(pair["question"], pair["sql"])
            self.trainer.test_query(pair["question"], pair["sql"])