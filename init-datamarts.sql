-- init-datamarts.sql
-- Academic Datamart Tables (Denormalized for easy querying)

-- Create schema
CREATE SCHEMA IF NOT EXISTS datamart;
SET search_path TO datamart, public;

-- =====================================================
-- COLLECTION 1: MAHASISWA DATAMART (3 tables)
-- =====================================================

-- 1.1 Student Academic Performance
CREATE TABLE datamart.student_performance (
    id SERIAL PRIMARY KEY,
    nim VARCHAR(20) NOT NULL,
    nama_mahasiswa VARCHAR(100) NOT NULL,
    jenis_kelamin VARCHAR(20),
    fakultas VARCHAR(100),
    program_studi VARCHAR(100),
    angkatan INTEGER,
    semester_aktif INTEGER,
    ipk DECIMAL(3,2),
    total_sks INTEGER,
    sks_lulus INTEGER,
    status_mahasiswa VARCHAR(20),
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 1.2 Student Attendance Summary
CREATE TABLE datamart.student_attendance (
    id SERIAL PRIMARY KEY,
    nim VARCHAR(20) NOT NULL,
    nama_mahasiswa VARCHAR(100) NOT NULL,
    fakultas VARCHAR(100),
    program_studi VARCHAR(100),
    mata_kuliah VARCHAR(100),
    kode_matkul VARCHAR(20),
    semester INTEGER,
    total_pertemuan INTEGER DEFAULT 14,
    hadir INTEGER,
    izin INTEGER,
    alpha INTEGER,
    persentase_kehadiran DECIMAL(5,2),
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 1.3 Student Financial Status
CREATE TABLE datamart.student_finance (
    id SERIAL PRIMARY KEY,
    nim VARCHAR(20) NOT NULL,
    nama_mahasiswa VARCHAR(100) NOT NULL,
    fakultas VARCHAR(100),
    program_studi VARCHAR(100),
    semester VARCHAR(20),
    tahun_akademik VARCHAR(20),
    jumlah_tagihan DECIMAL(12,2),
    jumlah_dibayar DECIMAL(12,2),
    sisa_tagihan DECIMAL(12,2),
    status_pembayaran VARCHAR(30),
    tanggal_bayar DATE,
    metode_pembayaran VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- COLLECTION 2: DOSEN DATAMART (3 tables)
-- =====================================================

-- 2.1 Lecturer Profile & Workload
CREATE TABLE datamart.lecturer_profile (
    id SERIAL PRIMARY KEY,
    nip VARCHAR(20) NOT NULL,
    nama_dosen VARCHAR(100) NOT NULL,
    jenis_kelamin VARCHAR(20),
    fakultas VARCHAR(100),
    program_studi VARCHAR(100),
    pendidikan_terakhir VARCHAR(50),
    jabatan_fungsional VARCHAR(50),
    golongan VARCHAR(10),
    total_mata_kuliah INTEGER,
    total_mahasiswa_bimbingan INTEGER,
    beban_sks INTEGER,
    status_aktif BOOLEAN,
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2.2 Lecturer Teaching Performance
CREATE TABLE datamart.lecturer_teaching (
    id SERIAL PRIMARY KEY,
    nip VARCHAR(20) NOT NULL,
    nama_dosen VARCHAR(100) NOT NULL,
    fakultas VARCHAR(100),
    mata_kuliah VARCHAR(100),
    kode_matkul VARCHAR(20),
    kelas VARCHAR(10),
    jumlah_mahasiswa INTEGER,
    rata_rata_nilai DECIMAL(5,2),
    rata_rata_kehadiran DECIMAL(5,2),
    tingkat_kelulusan DECIMAL(5,2),
    semester VARCHAR(20),
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2.3 Lecturer Research & Activity
CREATE TABLE datamart.lecturer_activity (
    id SERIAL PRIMARY KEY,
    nip VARCHAR(20) NOT NULL,
    nama_dosen VARCHAR(100) NOT NULL,
    fakultas VARCHAR(100),
    jumlah_penelitian INTEGER DEFAULT 0,
    jumlah_publikasi INTEGER DEFAULT 0,
    jumlah_pengabdian INTEGER DEFAULT 0,
    total_dana_penelitian DECIMAL(15,2) DEFAULT 0,
    pelatihan_diikuti INTEGER DEFAULT 0,
    sertifikasi_dimiliki INTEGER DEFAULT 0,
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- COLLECTION 3: AKADEMIK DATAMART (3 tables)
-- =====================================================

-- 3.1 Course Performance Summary
CREATE TABLE datamart.course_performance (
    id SERIAL PRIMARY KEY,
    kode_matkul VARCHAR(20) NOT NULL,
    nama_matkul VARCHAR(100) NOT NULL,
    fakultas VARCHAR(100),
    program_studi VARCHAR(100),
    sks INTEGER,
    semester INTEGER,
    jenis_matkul VARCHAR(20),
    dosen_pengampu VARCHAR(100),
    jumlah_peserta INTEGER,
    rata_rata_nilai DECIMAL(5,2),
    tingkat_kelulusan DECIMAL(5,2),
    rata_rata_kehadiran DECIMAL(5,2),
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3.2 Grade Distribution Analysis
CREATE TABLE datamart.grade_distribution (
    id SERIAL PRIMARY KEY,
    kode_matkul VARCHAR(20) NOT NULL,
    nama_matkul VARCHAR(100) NOT NULL,
    fakultas VARCHAR(100),
    program_studi VARCHAR(100),
    dosen_pengampu VARCHAR(100),
    jumlah_a INTEGER DEFAULT 0,
    jumlah_ab INTEGER DEFAULT 0,
    jumlah_b INTEGER DEFAULT 0,
    jumlah_bc INTEGER DEFAULT 0,
    jumlah_c INTEGER DEFAULT 0,
    jumlah_d INTEGER DEFAULT 0,
    jumlah_e INTEGER DEFAULT 0,
    total_mahasiswa INTEGER,
    semester VARCHAR(20),
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3.3 Academic Trends
CREATE TABLE datamart.academic_trends (
    id SERIAL PRIMARY KEY,
    periode VARCHAR(20) NOT NULL,
    fakultas VARCHAR(100),
    program_studi VARCHAR(100),
    metrik VARCHAR(50),
    nilai DECIMAL(10,2),
    satuan VARCHAR(20),
    persentase_perubahan DECIMAL(5,2),
    kategori VARCHAR(30),
    deskripsi TEXT,
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- COLLECTION 4: KEUANGAN DATAMART (3 tables)
-- =====================================================

-- 4.1 Revenue Summary
CREATE TABLE datamart.revenue_summary (
    id SERIAL PRIMARY KEY,
    periode VARCHAR(20) NOT NULL,
    fakultas VARCHAR(100),
    program_studi VARCHAR(100),
    jenis_pendapatan VARCHAR(50),
    total_tagihan DECIMAL(15,2),
    total_terbayar DECIMAL(15,2),
    total_outstanding DECIMAL(15,2),
    jumlah_mahasiswa INTEGER,
    tingkat_kolektibilitas DECIMAL(5,2),
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4.2 Payment Analysis
CREATE TABLE datamart.payment_analysis (
    id SERIAL PRIMARY KEY,
    periode VARCHAR(20) NOT NULL,
    fakultas VARCHAR(100),
    metode_pembayaran VARCHAR(50),
    jumlah_transaksi INTEGER,
    total_nominal DECIMAL(15,2),
    rata_rata_waktu_bayar INTEGER, -- days
    tingkat_keterlambatan DECIMAL(5,2),
    jumlah_cicilan INTEGER DEFAULT 0,
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4.3 Financial KPI
CREATE TABLE datamart.financial_kpi (
    id SERIAL PRIMARY KEY,
    periode VARCHAR(20) NOT NULL,
    fakultas VARCHAR(100),
    total_revenue DECIMAL(15,2),
    collection_rate DECIMAL(5,2),
    bad_debt_ratio DECIMAL(5,2),
    average_payment_time INTEGER, -- days
    scholarship_disbursed DECIMAL(15,2),
    operational_cost DECIMAL(15,2),
    net_income DECIMAL(15,2),
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- COLLECTION 5: INSTITUSI DATAMART (3 tables)
-- =====================================================

-- 5.1 Faculty Statistics
CREATE TABLE datamart.faculty_statistics (
    id SERIAL PRIMARY KEY,
    fakultas VARCHAR(100) NOT NULL,
    dekan VARCHAR(100),
    tahun_berdiri INTEGER,
    jumlah_program_studi INTEGER,
    jumlah_dosen INTEGER,
    jumlah_mahasiswa_aktif INTEGER,
    jumlah_lulusan_tahun_ini INTEGER,
    rata_rata_ipk_fakultas DECIMAL(3,2),
    tingkat_kehadiran_rata DECIMAL(5,2),
    akreditasi_fakultas VARCHAR(20),
    ranking_nasional INTEGER,
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5.2 University Performance
CREATE TABLE datamart.university_performance (
    id SERIAL PRIMARY KEY,
    periode VARCHAR(20) NOT NULL,
    total_mahasiswa INTEGER,
    total_dosen INTEGER,
    total_program_studi INTEGER,
    total_fakultas INTEGER,
    rata_rata_ipk_universitas DECIMAL(3,2),
    tingkat_kelulusan DECIMAL(5,2),
    tingkat_drop_out DECIMAL(5,2),
    student_lecturer_ratio DECIMAL(5,2),
    tingkat_kepuasan_mahasiswa DECIMAL(5,2),
    akreditasi_institusi VARCHAR(20),
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5.3 Accreditation Status
CREATE TABLE datamart.accreditation_status (
    id SERIAL PRIMARY KEY,
    unit_name VARCHAR(100) NOT NULL,
    unit_type VARCHAR(20), -- 'Program Studi', 'Fakultas', 'Institusi'
    fakultas VARCHAR(100),
    akreditasi_current VARCHAR(20),
    tanggal_akreditasi DATE,
    masa_berlaku DATE,
    akreditasi_previous VARCHAR(20),
    status_renewal VARCHAR(30),
    target_akreditasi VARCHAR(20),
    progress_percentage DECIMAL(5,2),
    tahun_akademik VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_student_perf_nim ON datamart.student_performance(nim);
CREATE INDEX idx_student_perf_prodi ON datamart.student_performance(program_studi);
CREATE INDEX idx_student_att_nim ON datamart.student_attendance(nim);
CREATE INDEX idx_student_fin_nim ON datamart.student_finance(nim);
CREATE INDEX idx_lecturer_prof_nip ON datamart.lecturer_profile(nip);
CREATE INDEX idx_lecturer_teach_nip ON datamart.lecturer_teaching(nip);
CREATE INDEX idx_course_perf_kode ON datamart.course_performance(kode_matkul);
CREATE INDEX idx_revenue_fakultas ON datamart.revenue_summary(fakultas);
CREATE INDEX idx_faculty_stats_fakultas ON datamart.faculty_statistics(fakultas);

-- Insert sample seed data for testing
INSERT INTO datamart.faculty_statistics (fakultas, dekan, tahun_berdiri, jumlah_program_studi, jumlah_dosen, jumlah_mahasiswa_aktif, akreditasi_fakultas, tahun_akademik) VALUES
('Fakultas Teknik', 'Prof. Dr. Ir. Ahmad Budi, M.T.', 1985, 5, 45, 850, 'A', '2024/2025'),
('Fakultas Ekonomi dan Bisnis', 'Dr. Siti Rahayu, M.M.', 1987, 4, 35, 720, 'A', '2024/2025'),
('Fakultas Ilmu Komputer', 'Prof. Dr. Wijaya Kusuma, M.Sc.', 1995, 3, 28, 650, 'B', '2024/2025'),
('Fakultas Kedokteran', 'Prof. Dr. dr. Maria Susanti, Sp.PD.', 2000, 2, 52, 380, 'A', '2024/2025'),
('Fakultas Hukum', 'Dr. Bambang Priono, S.H., M.H.', 1990, 2, 25, 420, 'B', '2024/2025');

\echo 'Academic datamart schema created successfully!'