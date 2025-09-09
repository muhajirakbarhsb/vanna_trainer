# data_generator.py - Main orchestrator
import os
from sqlalchemy import create_engine
from generators.mahasiswa_generator import MahasiswaGenerator
from generators.dosen_generator import DosenGenerator
from generators.akademik_generator import AkademikGenerator
from generators.keuangan_generator import KeuanganGenerator
from generators.institusi_generator import InstitusiGenerator


class AcademicDataGenerator:
    """
    Main data generator that orchestrates all collection generators
    """

    def __init__(self):
        self.engine = self._connect_db()

        # Initialize all generators
        self.mahasiswa_gen = MahasiswaGenerator(self.engine)
        self.dosen_gen = DosenGenerator(self.engine)
        self.akademik_gen = AkademikGenerator(self.engine)
        self.keuangan_gen = KeuanganGenerator(self.engine)
        self.institusi_gen = InstitusiGenerator(self.engine)

    def _connect_db(self):
        """Connect to PostgreSQL"""
        host = os.getenv('POSTGRES_HOST', 'postgres')
        dbname = os.getenv('POSTGRES_DB', 'academic_datamart')
        user = os.getenv('POSTGRES_USER', 'postgres')
        password = os.getenv('POSTGRES_PASSWORD', 'academic123')
        port = os.getenv('POSTGRES_PORT', '5432')

        connection_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        return create_engine(connection_url)

    def generate_all_datamarts(self):
        """Generate ALL 15 datamart tables with complete data"""
        print("🎓 GENERATING ALL ACADEMIC DATAMARTS")
        print("=" * 50)

        # Collection 1: Student data (3 tables)
        print("\n📚 Collection 1: MAHASISWA (Student Data)")
        self.mahasiswa_gen.generate_all()

        # Collection 2: Lecturer data (3 tables)
        print("\n👨‍🏫 Collection 2: DOSEN (Lecturer Data)")
        self.dosen_gen.generate_all()

        # Collection 3: Academic data (3 tables)
        print("\n📖 Collection 3: AKADEMIK (Academic Data)")
        self.akademik_gen.generate_all()

        # Collection 4: Financial data (3 tables)
        print("\n💰 Collection 4: KEUANGAN (Financial Data)")
        self.keuangan_gen.generate_all()

        # Collection 5: Institutional data (3 tables)
        print("\n🏛️ Collection 5: INSTITUSI (Institutional Data)")
        self.institusi_gen.generate_all()

        print("\n🎉 ALL 15 DATAMART TABLES GENERATED SUCCESSFULLY!")

    def get_data_summary(self):
        """Get summary of ALL generated data"""
        import pandas as pd

        all_tables = [
            # Collection 1: Mahasiswa
            'student_performance', 'student_attendance', 'student_finance',
            # Collection 2: Dosen
            'lecturer_profile', 'lecturer_teaching', 'lecturer_activity',
            # Collection 3: Akademik
            'course_performance', 'grade_distribution', 'academic_trends',
            # Collection 4: Keuangan
            'revenue_summary', 'payment_analysis', 'financial_kpi',
            # Collection 5: Institusi
            'faculty_statistics', 'university_performance', 'accreditation_status'
        ]

        print("\n📊 COMPLETE DATA SUMMARY (ALL 15 TABLES)")
        print("=" * 60)

        total_records = 0
        collection_counts = {
            'MAHASISWA': 0, 'DOSEN': 0, 'AKADEMIK': 0,
            'KEUANGAN': 0, 'INSTITUSI': 0
        }

        for i, table in enumerate(all_tables):
            try:
                result = pd.read_sql(f"SELECT COUNT(*) as count FROM datamart.{table}", self.engine)
                count = result.iloc[0]['count']
                total_records += count

                # Determine collection
                if i < 3:
                    collection = 'MAHASISWA'
                elif i < 6:
                    collection = 'DOSEN'
                elif i < 9:
                    collection = 'AKADEMIK'
                elif i < 12:
                    collection = 'KEUANGAN'
                else:
                    collection = 'INSTITUSI'

                collection_counts[collection] += count

                print(f"{table:25}: {count:6} records")

            except Exception as e:
                print(f"{table:25}: {0:6} records (error)")

        print("=" * 60)
        print(f"{'TOTAL RECORDS':25}: {total_records:6}")
        print("=" * 60)

        print("\n📈 RECORDS PER COLLECTION:")
        for collection, count in collection_counts.items():
            print(f"{collection:12}: {count:6} records")


if __name__ == "__main__":
    generator = AcademicDataGenerator()
    generator.generate_all_datamarts()
    generator.get_data_summary()