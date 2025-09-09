# vanna_setup.py
import os
import hashlib
from typing import List, Dict, Optional
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import pandas as pd
from sqlalchemy import create_engine, text


class AcademicVannaTrainer:
    """
    Simplified Vanna-like implementation for academic datamart training
    """

    def __init__(self, collection_name: str):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.qdrant_url = os.getenv('QDRANT_URL', 'http://qdrant:6333')
        self.qdrant_api_key = os.getenv('QDRANT_API_KEY', 'qdrant123')
        self.collection_name = collection_name

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        # Initialize Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            timeout=60
        )

        # Create collection
        self._create_collection()

        # Connect to PostgreSQL
        self._connect_postgres()

        print(f"✅ AcademicVannaTrainer initialized for collection: {collection_name}")

    def _create_collection(self):
        """Create Qdrant collection for storing embeddings"""
        try:
            collections = self.qdrant_client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=768,  # Gemini embedding dimension
                        distance=Distance.COSINE
                    ),
                )
                print(f"✅ Created Qdrant collection: {self.collection_name}")
            else:
                print(f"✅ Using existing collection: {self.collection_name}")

        except Exception as e:
            print(f"❌ Error creating collection: {e}")
            raise

    def _connect_postgres(self):
        """Connect to PostgreSQL database"""
        try:
            host = os.getenv('POSTGRES_HOST', 'postgres')
            dbname = os.getenv('POSTGRES_DB', 'academic_datamart')
            user = os.getenv('POSTGRES_USER', 'postgres')
            password = os.getenv('POSTGRES_PASSWORD', 'academic123')
            port = os.getenv('POSTGRES_PORT', '5432')

            connection_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
            self.db_engine = create_engine(connection_url)

            # Test connection
            with self.db_engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            print(f"✅ Connected to PostgreSQL: {dbname}")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using Gemini"""
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"❌ Error generating embedding: {e}")
            return []

    def add_question_sql(self, question: str, sql: str) -> str:
        """Add a question-SQL pair to the vector database"""
        try:
            content = f"Question: {question}\nSQL: {sql}"
            doc_id = hashlib.md5(content.encode()).hexdigest()

            embedding = self.generate_embedding(content)
            if not embedding:
                return "Failed to generate embedding"

            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=doc_id,
                        vector=embedding,
                        payload={
                            "question": question,
                            "sql": sql,
                            "type": "question_sql",
                            "content": content
                        }
                    )
                ]
            )

            print(f"✅ Added Q-SQL: {question[:50]}...")
            return doc_id

        except Exception as e:
            print(f"❌ Error adding question-SQL: {e}")
            return "Error"

    def add_schema_info(self, schema_name: str, schema_description: str) -> str:
        """Add schema information to the vector database"""
        try:
            content = f"Schema: {schema_name}\n{schema_description}"
            doc_id = hashlib.md5(content.encode()).hexdigest()

            embedding = self.generate_embedding(content)
            if not embedding:
                return "Failed to generate embedding"

            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=doc_id,
                        vector=embedding,
                        payload={
                            "schema_name": schema_name,
                            "schema_description": schema_description,
                            "type": "schema",
                            "content": content
                        }
                    )
                ]
            )

            print(f"✅ Added schema: {schema_name}")
            return doc_id

        except Exception as e:
            print(f"❌ Error adding schema: {e}")
            return "Error"

    def run_sql(self, sql: str) -> pd.DataFrame:
        """Execute SQL query and return results"""
        try:
            df = pd.read_sql_query(sql, self.db_engine)
            return df
        except Exception as e:
            print(f"❌ Error executing SQL: {e}")
            return pd.DataFrame()

    def test_query(self, question: str, sql: str) -> bool:
        """Test if a SQL query works"""
        try:
            result = self.run_sql(sql)
            success = result is not None and len(result) >= 0
            if success:
                print(f"✅ Test passed: {question}")
                print(f"   📊 Result: {len(result)} rows")
            else:
                print(f"❌ Test failed: {question}")
            return success
        except Exception as e:
            print(f"❌ Test error for '{question}': {e}")
            return False

    def get_collection_stats(self) -> dict:
        """Get collection statistics"""
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return {
                'collection_name': self.collection_name,
                'total_points': collection_info.points_count,
                'vector_size': collection_info.config.params.vectors.size,
                'distance': collection_info.config.params.vectors.distance
            }
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}