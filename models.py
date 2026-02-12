from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
Base = declarative_base()

class Species(Base):
    __tablename__ = "species"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    iucn_status = Column(String(20))

class Sample(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True)
    species_id = Column(Integer, ForeignKey("species.id"))
    fastq_path = Column(String(500))
    status = Column(String(20), default="raw")

class PipelineRun(Base):
    __tablename__ = "pipeline_runs"
    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey("samples.id"))
    status = Column(String(20), default="pending")
    metrics = Column(JSON)  # {"shannon": 4.2, "predicted_risk": "VU"}
    created_at = Column(DateTime, default=func.now())
