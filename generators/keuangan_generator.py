# generators/keuangan_generator.py
import random
import pandas as pd
from faker import Faker

fake = Faker('id_ID')


class KeuanganGenerator:
    """Generate financial collection data (3 tables)"""

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

    def generate_revenue_summary(self, count=50):
        """Generate revenue summary data"""
        print(f"💰 Generating {count} revenue summary records...")

        data = []
        for fakultas in self.fakultas_list:
            for prodi in self.prodi_dict[fakultas]:
                for periode in ['2024-1', '2024-2']:
                    total_tagihan = random.randint(500000000, 2000000000)
                    collection_rate = random.uniform(75, 95)
                    total_terbayar = total_tagihan * (collection_rate / 100)

                    data.append({
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

        df = pd.DataFrame(data)
        df.to_sql('revenue_summary', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {len(data)} revenue summary records")

    def generate_payment_analysis(self, count=50):
        """Generate payment analysis data"""
        print(f"💳 Generating {count} payment analysis records...")

        data = []
        payment_methods = ['Transfer Bank', 'Virtual Account', 'Kartu Kredit', 'E-wallet', 'Cash']

        for fakultas in self.fakultas_list:
            for method in payment_methods:
                for periode in ['2024-1', '2024-2']:
                    data.append({
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

        df = pd.DataFrame(data)
        df.to_sql('payment_analysis', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {len(data)} payment analysis records")

    def generate_financial_kpi(self, count=20):
        """Generate financial KPI data"""
        print(f"📊 Generating {count} financial KPI records...")

        data = []
        for periode in ['2024-1', '2024-2']:
            for fakultas in self.fakultas_list:
                total_revenue = random.randint(1000000000, 5000000000)
                operational_cost = random.randint(800000000, int(total_revenue * 0.8))
                net_income = total_revenue - operational_cost

                data.append({
                    'periode': periode,
                    'fakultas': fakultas,
                    'total_revenue': total_revenue,
                    'collection_rate': round(random.uniform(80, 95), 2),
                    'bad_debt_ratio': round(random.uniform(2, 8), 2),
                    'average_payment_time': random.randint(15, 45),
                    'scholarship_disbursed': random.randint(50000000, 300000000),
                    'operational_cost': operational_cost,
                    'net_income': net_income,
                    'tahun_akademik': '2024/2025'
                })

        df = pd.DataFrame(data)
        df.to_sql('financial_kpi', self.engine, schema='datamart',
                  if_exists='append', index=False)
        print(f"✅ Added {len(data)} financial KPI records")

    def generate_all(self):
        """Generate all financial collection tables"""
        self.generate_revenue_summary(50)
        self.generate_payment_analysis(50)
        self.generate_financial_kpi(20)