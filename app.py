from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Species, Sample, PipelineRun
from pipeline import run_full_pipeline
import os

app = FastAPI(title="Microbiome Backend")

# Pydantic models
class SampleInput(BaseModel):
    species_name: str
    fastq_path: str

class PipelineResult(BaseModel):
    run_id: int
    metrics: dict

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/species", response_model=dict)
def create_species(species_name: str, db: Session = next(get_db())):
    species = Species(name=species_name, iucn_status="VU")  # Mock ground truth
    db.add(species)
    db.commit()
    db.refresh(species)
    return {"species_id": species.id}

@app.post("/samples")
def create_sample(sample: SampleInput, db: Session = next(get_db())):
    species = db.query(Species).filter(Species.name == sample.species_name).first()
    if not species:
        raise HTTPException(404, "Species not found")
    
    sample_obj = Sample(species_id=species.id, fastq_path=sample.fastq_path)
    db.add(sample_obj)
    db.commit()
    db.refresh(sample_obj)
    return {"sample_id": sample_obj.id}

@app.post("/analyze/{sample_id}")
async def trigger_analysis(sample_id: int, background_tasks: BackgroundTasks, db: Session = next(get_db())):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(404, "Sample not found")
    
    run = PipelineRun(sample_id=sample_id, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)
    
    background_tasks.add_task(process_sample, db, run.id, sample.fastq_path)
    return {"run_id": run.id, "status": "queued"}

async def process_sample(db: Session, run_id: int, fastq_path: str):
    """Background pipeline execution"""
    try:
        metrics = run_full_pipeline(fastq_path)
        run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
        run.status = "completed"
        run.metrics = metrics
        db.commit()
    except Exception as e:
        run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
        run.status = "failed"
        db.commit()

@app.get("/results/{run_id}")
def get_results(run_id: int, db: Session = next(get_db())):
    run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
    if not run:
        raise HTTPException(404, "Run not found")
    return {"run_id": run.id, "status": run.status, "metrics": run.metrics}
