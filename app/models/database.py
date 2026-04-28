"""
Database models and configuration for NotebookUM.

This module defines SQLAlchemy ORM models for:
- Usuario: User accounts
- HistorialDocumento: Document upload history
- HistorialPregunta: Question history
- Resumen: Generated summaries

Follows clean code principles with clear naming and single responsibility.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/notebookum'
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============ ORM MODELS ============

class Usuario(Base):
    """
    Usuario model represents a system user.
    
    Attributes:
        id: Primary key
        nombre: User's full name (required)
        email: User's email (unique, required)
        contraseña: Hashed password (required)
        fecha_creacion: Account creation timestamp (auto-set)
    """
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    historiales_documentos = relationship(
        "HistorialDocumento",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    historiales_preguntas = relationship(
        "HistorialPregunta",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )


class HistorialDocumento(Base):
    """
    HistorialDocumento tracks documents uploaded by users.
    
    Attributes:
        id: Primary key
        usuario_id: Foreign key to Usuario (required)
        nombre_archivo: Original filename
        ruta_archivo: Storage path
        fecha_carga: Upload timestamp (auto-set)
        tamaño_bytes: File size in bytes
        texto_extraido: Full text extracted from the uploaded PDF
    """
    __tablename__ = "historiales_documentos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(500), nullable=False)
    fecha_carga = Column(DateTime, default=datetime.utcnow)
    tamaño_bytes = Column(Integer)
    texto_extraido = Column(Text, nullable=True)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="historiales_documentos")
    resumenes = relationship(
        "Resumen",
        back_populates="historial_documento",
        cascade="all, delete-orphan"
    )


class HistorialPregunta(Base):
    """
    HistorialPregunta tracks questions asked about documents.
    
    Attributes:
        id: Primary key
        usuario_id: Foreign key to Usuario (required)
        pregunta: Question text (required)
        respuesta: Answer text (nullable)
        fecha_pregunta: Question timestamp (auto-set)
    """
    __tablename__ = "historiales_preguntas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    pregunta = Column(Text, nullable=False)
    respuesta = Column(Text)
    fecha_pregunta = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    usuario = relationship("Usuario", back_populates="historiales_preguntas")


class Resumen(Base):
    """
    Resumen model stores AI-generated document summaries.
    
    Attributes:
        id: Primary key
        historial_documento_id: Foreign key to HistorialDocumento (required)
        titulo: Summary title
        contenido: Summary content (required)
        fecha_generacion: Generation timestamp (auto-set)
    """
    __tablename__ = "resumenes"
    
    id = Column(Integer, primary_key=True, index=True)
    historial_documento_id = Column(
        Integer,
        ForeignKey("historiales_documentos.id"),
        nullable=False
    )
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_generacion = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    historial_documento = relationship(
        "HistorialDocumento",
        back_populates="resumenes"
    )


# ============ DATABASE UTILITIES ============

def crear_tablas() -> None:
    """
    Create all database tables defined in the models.
    
    Raises:
        SQLAlchemy exceptions for database connection issues
    """
    Base.metadata.create_all(bind=engine)
    _asegurar_columna_texto_extraido()


def _asegurar_columna_texto_extraido() -> None:
    """Backfill `texto_extraido` column when running over an existing database."""
    columnas = {
        columna["name"]
        for columna in inspect(engine).get_columns("historiales_documentos")
    }
    if "texto_extraido" in columnas:
        return

    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE historiales_documentos ADD COLUMN texto_extraido TEXT")
        )


def obtener_sesion_db():
    """
    Dependency injection generator for FastAPI database sessions.
    
    Yields:
        SessionLocal: Database session
        
    Usage:
        @app.get("/usuarios")
        def get_usuarios(db: Session = Depends(obtener_sesion_db)):
            return db.query(Usuario).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def limpiar_sesion() -> None:
    """Close all active database sessions (cleanup utility)."""
    SessionLocal.remove()
