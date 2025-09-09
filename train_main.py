# train_main.py
import os
import time
import logging
from datetime import datetime
from data_generator import AcademicDataGenerator
from vanna_setup import AcademicVannaTrainer
from trainers.mahasiswa_trainer import MahasiswaTrainer
from trainers.dosen_trainer import DosenTrainer
from trainers.akademik_trainer import AkademikTrainer
from trainers.keuangan_trainer import KeuanganTrainer
from trainers.institusi_trainer import InstitusiTrainer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AcademicCollectionTrainer:
    """
    Train 5 academic collections with different focus areas
    """

    def __init__(self):
        self.collections = [
            "mahasiswa_collection",    # Student-focused queries
            "dosen_collection",        # Lecturer-focused queries
            "akademik_collection",     # Academic performance queries
            "keuangan_collection",     # Financial queries
            "institusi_collection"     # Institutional queries
        ]

        self.trainers = {}
        self.data_generator = None

        # Initialize specific trainers
        self.mahasiswa_trainer = None
        self.dosen_trainer = None
        self.akademik_trainer = None
        self.keuangan_trainer = None
        self.institusi_trainer = None

    def initialize_trainers(self):
        """Initialize Vanna trainers for each collection"""
        logger.info("🤖 Initializing Vanna trainers for 5 collections...")

        for collection in self.collections:
            try:
                self.trainers[collection] = AcademicVannaTrainer(collection)
                logger.info(f"✅ Initialized trainer for {collection}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize {collection}: {e}")
                raise

        # Initialize specific trainers
        self.mahasiswa_trainer = MahasiswaTrainer(self.trainers["mahasiswa_collection"])
        self.dosen_trainer = DosenTrainer(self.trainers["dosen_collection"])
        self.akademik_trainer = AkademikTrainer(self.trainers["akademik_collection"])
        self.keuangan_trainer = KeuanganTrainer(self.trainers["keuangan_collection"])
        self.institusi_trainer = InstitusiTrainer(self.trainers["institusi_collection"])

    def generate_dummy_data(self):
        """Generate dummy data for all datamarts"""
        logger.info("📊 Generating dummy data for datamarts...")

        try:
            self.data_generator = AcademicDataGenerator()
            self.data_generator.generate_all_datamarts()
            logger.info("✅ Dummy data generation completed")
        except Exception as e:
            logger.error(f"❌ Failed to generate data: {e}")
            raise

    def run_all_training(self):
        """Run complete training process for all 5 collections"""
        start_time = time.time()

        logger.info("🎓 STARTING ACADEMIC COLLECTIONS TRAINING")
        logger.info("=" * 60)

        try:
            # Step 1: Generate dummy data
            self.generate_dummy_data()

            # Step 2: Initialize trainers
            self.initialize_trainers()

            # Step 3: Train each collection
            logger.info("👨‍🎓 Training mahasiswa_collection...")
            self.mahasiswa_trainer.train()

            logger.info("👨‍🏫 Training dosen_collection...")
            self.dosen_trainer.train()

            logger.info("📚 Training akademik_collection...")
            self.akademik_trainer.train()

            logger.info("💰 Training keuangan_collection...")
            self.keuangan_trainer.train()

            logger.info("🏛️ Training institusi_collection...")
            self.institusi_trainer.train()

            # Step 4: Show training summary
            self.show_training_summary()

            end_time = time.time()
            duration = end_time - start_time

            logger.info(f"\n🎉 ALL TRAINING COMPLETED SUCCESSFULLY!")
            logger.info(f"⏱️ Total training time: {duration:.2f} seconds")
            logger.info(f"📊 5 collections trained with dummy academic data")
            logger.info(f"🚀 Ready for academic query processing!")

        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            raise

    def show_training_summary(self):
        """Show summary of all trained collections"""
        logger.info("\n📊 TRAINING SUMMARY")
        logger.info("=" * 50)

        for collection in self.collections:
            try:
                trainer = self.trainers[collection]
                stats = trainer.get_collection_stats()

                logger.info(f"\n🎯 {collection}:")
                logger.info(f"   📈 Total points: {stats.get('total_points', 0)}")
                logger.info(f"   🔍 Vector size: {stats.get('vector_size', 0)}")
                logger.info(f"   📏 Distance metric: {stats.get('distance', 'cosine')}")

            except Exception as e:
                logger.error(f"❌ Error getting stats for {collection}: {e}")

        # Show data summary
        if self.data_generator:
            self.data_generator.get_data_summary()


def main():
    """Main training function"""
    logger.info("🚀 Academic Collections Trainer Starting...")

    # Check required environment variables
    required_vars = ['GEMINI_API_KEY', 'POSTGRES_HOST', 'QDRANT_HOST']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        return

    trainer = AcademicCollectionTrainer()
    trainer.run_all_training()


if __name__ == "__main__":
    main()