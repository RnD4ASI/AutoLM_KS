import os
import datetime
import pickle
import os
import sys
import re
import json
import glob
import time
import uuid
import base64
import hashlib
import logging
import warnings
import traceback
import random
import subprocess
import numpy as np
import pandas as pd
import networkx as nx
import spacy
import matplotlib.pyplot as plt
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from spacy.cli import download
from markitdown import MarkItDown
from pdf2image import convert_from_path
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple, Union, Optional, Any, Set, Callable, Iterator, Generator
from src.pipeline.shared.logging import get_logger
from src.pipeline.processing.generator import Generator, MetaGenerator
from src.pipeline.shared.utility import DataUtility

logger = get_logger(__name__)


@dataclass
class DocumentInfo:
    """Dataclass for storing document information."""
    file_path: Path
    file_type: str          # 'pdf' or 'markdown'
    file_name: str
    region: str             # 'au', 'bs', 'eu', 'unknown'
    doc_type: str           # 'standard', 'guidance', 'opinion', 'unknown'
    base_name: str          # filename without extension
    is_processed: bool = False


class DocumentDiscoverer:
    """Handles document discovery and organization."""
    
    @staticmethod
    def discover_documents(raw_dir: Path, process_subdirs: bool = True) -> List[DocumentInfo]:
        """Discover documents in the specified directory.
        
        Args:
            raw_dir: Directory to search for documents
            process_subdirs: Whether to search in subdirectories
            
        Returns:
            List of DocumentInfo objects representing discovered documents
        """
        documents = []
        raw_path = Path(raw_dir)
        
        if not raw_path.exists():
            logger.warning(f"Raw directory {raw_path} does not exist")
            return documents
        
        if process_subdirs:
            # Get files from all subdirectories
            logger.info(f"Discovering documents in {raw_path} and all subdirectories")
            
            # First, collect all files
            all_files = []
            for ext in ['pdf', 'md', 'PDF', 'MD']:
                pattern = f'**/*.{ext}'
                logger.debug(f"Searching for {pattern} in {raw_path}")
                
                # Use Path.rglob() which is equivalent to os.walk() for recursive directory traversal
                for file_path in raw_path.rglob(f'*.{ext}'):
                    path_str = str(file_path)
                    # Skip files in hierarchy directory
                    if 'hierarchy' not in path_str:
                        # Extract metadata from file path
                        metadata = DocumentDiscoverer._extract_metadata(file_path)
                        
                        all_files.append({
                            'file_path': file_path,
                            'file_type': 'pdf' if ext.lower() == 'pdf' else 'md',
                            'file_name': file_path.name,
                            'is_processed': False,
                            'region': metadata['region'],
                            'doc_type': metadata['doc_type'],
                            'base_name': file_path.stem  # Store the stem (filename without extension)
                        })
            
            # Group files by their base name and location
            file_groups = DocumentDiscoverer._group_files_by_basename(all_files)
            
            # Apply file priority rules for each group
            documents = DocumentDiscoverer._apply_file_priority_rules(file_groups)
            
            # Log which directories we're processing files from
            file_dirs = set(str(doc.file_path.parent) for doc in documents)
            logger.info(f"Found documents in {len(file_dirs)} directories: {file_dirs}")
            
        else:
            # Just get files from the immediate directory
            logger.info(f"Discovering documents in {raw_path} (not recursive)")
            # Iterate through PDF and markdown files
            for ext in ['pdf', 'md', 'PDF', 'MD']:
                for file_path in raw_path.glob(f'*.{ext}'):
                    # Skip files in hierarchy directory
                    if 'hierarchy' not in str(file_path):
                        # Extract metadata from file path
                        metadata = DocumentDiscoverer._extract_metadata(file_path)
                        
                        doc_info = DocumentInfo(
                            file_path=file_path,
                            file_type='pdf' if ext.lower() == 'pdf' else 'md',
                            file_name=file_path.name,
                            region=metadata['region'],
                            doc_type=metadata['doc_type'],
                            base_name=file_path.stem,
                            is_processed=False
                        )
                        documents.append(doc_info)
        
        logger.info(f"Discovered {len(documents)} documents")
        return documents
    
    @staticmethod
    def _extract_metadata(file_path: Path) -> Dict[str, str]:
        """Extract region and document type from file path.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Dictionary with region and doc_type keys
        """
        path_str = str(file_path)
        region = "unknown"
        doc_type = "unknown"
        
        # Determine region from path
        if '/au/' in path_str or '\\au\\' in path_str:
            region = 'au'
        elif '/bs/' in path_str or '\\bs\\' in path_str:
            region = 'bs'
        elif '/eu/' in path_str or '\\eu\\' in path_str:
            region = 'eu'
            
        # Determine document type from path
        if '/standard/' in path_str or '\\standard\\' in path_str:
            doc_type = 'standard'
        elif '/guidance/' in path_str or '\\guidance\\' in path_str:
            doc_type = 'guidance'
        elif '/opinion/' in path_str or '\\opinion\\' in path_str:
            doc_type = 'opinion'
        
        return {'region': region, 'doc_type': doc_type}
    
    @staticmethod
    def _group_files_by_basename(files: List[Dict]) -> Dict[str, List[Dict]]:
        """Group files by their base name and location.
        
        Args:
            files: List of file dictionaries
            
        Returns:
            Dictionary mapping location|basename to list of file dictionaries
        """
        file_groups = {}
        for file_info in files:
            # Create a key based on directory and base name
            parent_dir = file_info['file_path'].parent
            base_name = file_info['base_name']
            key = f"{parent_dir}|{base_name}"
            
            if key not in file_groups:
                file_groups[key] = []
            file_groups[key].append(file_info)
        
        return file_groups
    
    @staticmethod
    def _apply_file_priority_rules(file_groups: Dict[str, List[Dict]]) -> List[DocumentInfo]:
        """Apply file priority rules to grouped files.
        
        Priority rules:
        1. When both .md and .pdf files exist with the same name, prefer .md
        2. When only one file exists, use it
        
        Args:
            file_groups: Dictionary mapping location|basename to list of file dictionaries
            
        Returns:
            List of DocumentInfo objects representing selected documents
        """
        documents = []
        
        for group_key, files in file_groups.items():
            selected_file = None
            
            if len(files) > 1:
                # Check if we have both .md and .pdf files
                md_files = [f for f in files if f['file_type'] == 'md']
                pdf_files = [f for f in files if f['file_type'] == 'pdf']
                
                if md_files:  # Scenario 1 & 2: If .md exists, use it
                    logger.info(f"Found both .md and .pdf for {group_key}, prioritizing .md file")
                    selected_file = md_files[0]
                else:  # Only PDF files exist
                    selected_file = pdf_files[0]
            else:  # Only one file exists (either .md or .pdf)
                selected_file = files[0]
            
            if selected_file:
                doc_info = DocumentInfo(
                    file_path=selected_file['file_path'],
                    file_type=selected_file['file_type'],
                    file_name=selected_file['file_name'],
                    region=selected_file['region'],
                    doc_type=selected_file['doc_type'],
                    base_name=selected_file['base_name'],
                    is_processed=selected_file['is_processed']
                )
                documents.append(doc_info)
        
        return documents


class TextParser:
    """
    Provides methods for cleansing data including PDF to Markdown conversion and text chunking.
    """
    def __init__(self) -> None:
        """Initialize a TextParser instance.
        No parameters required.
        Returns:
            None
        """
        # Initialize any resources, e.g., spaCy model if needed
        logger.debug("TextParser initialization started")
        try:
            start_time = time.time()
            try:
                # Attempt to load the small English model
                self.nlp = spacy.load("en_core_web_sm")
            except Exception:
                # Model not found, download then load
                download("en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
            logger.debug(f"Loaded spaCy model in {time.time() - start_time:.2f} seconds")

            # Initialize the Generator
            self.generator = Generator()
            logger.debug("TextParser initialized successfully")
        except Exception as e:
            logger.error(f"TextParser initialization failed: {str(e)}")
            logger.debug(f"Initialization error details: {traceback.format_exc()}")
            raise

    def pdf2md_markitdown(self, pdf_path: str) -> None:
        """Convert a PDF to Markdown using the MarkItDown package.

        Parameters:
            pdf_path (str): The file path to the PDF.

        Returns:
            None.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            ImportError: If MarkItDown package is not installed.
            RuntimeError: If conversion fails.
        """
        logger.info(f"Converting PDF to Markdown using pdf2md_markitdown (MarkItDown) for {pdf_path}")
        logger.debug(f"PDF path details: {os.path.abspath(pdf_path)}, size: {os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 'N/A'} bytes")
        
        # Verify PDF file exists
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create output path for markdown file
        md_path = os.path.splitext(pdf_path)[0] + '.md'
        
        try:
            # Initialize converter and convert PDF to Markdown
            start_time = time.time()
            logger.debug(f"Initializing MarkItDown converter")
            converter = MarkItDown()
            logger.debug(f"Starting PDF conversion: {pdf_path} -> {md_path}")
            converter.convert_file(pdf_path, md_path)
            
            conversion_time = time.time() - start_time
            logger.info(f"Successfully converted PDF to Markdown: {md_path} in {conversion_time:.2f} seconds")
            if os.path.exists(md_path):
                logger.debug(f"Generated markdown file size: {os.path.getsize(md_path)} bytes")
            return None
            
        except Exception as e:
            logger.error(f"Failed to convert PDF to Markdown: {str(e)}")
            logger.debug(f"PDF conversion error details: {traceback.format_exc()}")
            raise RuntimeError(f"PDF conversion failed: {str(e)}")

    def pdf2md_openleaf(self, pdf_path: str) -> None:
        """Convert a PDF to Markdown using the openleaf-markdown-pdf shell command.

        Parameters:
            pdf_path (str): The file path to the PDF.

        Returns:
            None.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            RuntimeError: If the openleaf-markdown-pdf command fails or isn't installed.
        """
        logger.info(f"Converting PDF to Markdown using pdf2md_openleaf (OpenLeaf) for {pdf_path}")

        # Verify PDF file exists
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create output path for markdown file
        md_path = os.path.splitext(pdf_path)[0] + '.md'

        try:
            # Run the openleaf-markdown-pdf command
            cmd = ['openleaf-markdown-pdf', '--input', pdf_path, '--output', md_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully converted PDF to Markdown: {md_path}")
                return None
            else:
                error_msg = result.stderr or "Unknown error occurred"
                logger.error(f"Command failed: {error_msg}")
                raise RuntimeError(f"PDF conversion failed: {error_msg}")
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute openleaf-markdown-pdf: {str(e)}")
            raise RuntimeError(f"openleaf-markdown-pdf command failed: {str(e)}")
        except FileNotFoundError:
            logger.error("openleaf-markdown-pdf command not found. Please install it first.")
            raise RuntimeError("openleaf-markdown-pdf is not installed")

    # def pdf2md_ocr(self, pdf_path: str, md_path: str, model: str = "GOT-OCR2") -> None:
    #     """Convert a PDF to Markdown using an open sourced model from HuggingFace.
    #     tmp/ocr folder is used to store the temporary images.

    #     Parameters:
    #         pdf_path (str): The file path to the PDF.
    #         md_path (str): The file path to save the generated Markdown.
    #         model (str): The model to use for conversion (default is "GOT-OCR2").

    #     Returns:
    #         None

    #     Raises:
    #         FileNotFoundError: If the PDF file doesn't exist.
    #         ImportError: If required packages are not installed.
    #         RuntimeError: If conversion fails.
    #     """
    #     # Convert PDF pages to images
    #     logger.info(f"Converting PDF to Markdown using pdf2md_ocr (OCR Model) for {pdf_path}")
    #     if pdf_path is None or not os.path.exists(pdf_path):
    #         raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
    #     pages = convert_from_path(pdf_path)
    #     if not pages:
    #         raise ValueError("No pages found in the PDF.")
        
    #     tmp_dir = Path.cwd() / "tmp/ocr"
    #     tmp_dir.mkdir(exist_ok=True)
        
    #     # Save each image temporarily and collect their file paths
    #     try:
    #         image_paths = []
    #         for idx, page in enumerate(pages):
    #             image_path = tmp_dir / f"temp_page_{idx}.jpg"
    #             page.save(image_path, "JPEG")
    #             image_paths.append(image_path)
            
    #         # Execute OCR on all temporary image files
    #         ocr_text = self.generator.get_ocr(image_paths=image_paths, model=model)
    #         with open(md_path, "w", encoding="utf-8") as f:
    #             f.write(ocr_text)
            
    #         # Clean up temporary files
    #         for image_path in image_paths:
    #             os.remove(image_path)
    #         logger.info(f"PDF to Markdown conversion completed.")

    #     except Exception as e:
    #         logger.error(f"PDF to Markdown conversion failed: {str(e)}")
    #         raise e

    def pdf2md_llamaindex(self, pdf_path: str) -> None:
        """Convert a PDF to Markdown using LlamaIndex and PyMuPDF.

        Parameters:
            pdf_path (str): The file path to the PDF.

        Returns:
            None

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            ImportError: If required packages are not installed.
            RuntimeError: If conversion fails.
        """
        logger.info(f"Converting PDF to Markdown using pdf2md_llamaindex for {pdf_path}")
        logger.debug(f"PDF path details: {os.path.abspath(pdf_path)}, size: {os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 'N/A'} bytes")
        
        try:
            # Import required packages
            import pymupdf4llm
            from llama_index.core import Document
        except ImportError:
            logger.error("Required packages not installed. Please install using: pip install pymupdf4llm llama-index")
            raise ImportError("Required packages not installed: pymupdf4llm, llama-index")

        # Verify PDF file exists
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create output path for markdown file
        md_path = os.path.splitext(pdf_path)[0] + '.md'
        
        try:
            # Initialize LlamaIndex processor options
            llamaindex_options = {
                'chunk_size': 1000,
                'chunk_overlap': 200,
                'use_chunks': False
            }
            
            # Extract text using LlamaIndex and PyMuPDF
            start_time = time.time()
            logger.debug(f"Initializing LlamaIndexPDFProcessor with options: {llamaindex_options}")
            
            # Create a LlamaMarkdownReader with appropriate options
            import inspect
            reader_params = inspect.signature(pymupdf4llm.LlamaMarkdownReader.__init__).parameters
            
            # Prepare kwargs based on available parameters
            kwargs = {}
            
            # Add options if they are supported by the current version
            if 'chunk_size' in reader_params:
                kwargs['chunk_size'] = llamaindex_options['chunk_size']
                
            if 'chunk_overlap' in reader_params:
                kwargs['chunk_overlap'] = llamaindex_options['chunk_overlap']
            
            # Create reader with configured options
            logger.debug(f"Creating LlamaMarkdownReader with parameters: {kwargs}")
            llama_reader = pymupdf4llm.LlamaMarkdownReader(**kwargs)
            
            # Load and convert the PDF to LlamaIndex documents
            load_data_params = inspect.signature(llama_reader.load_data).parameters
            load_kwargs = {}
            
            # Add any additional load_data parameters if supported
            if 'use_chunks' in load_data_params:
                load_kwargs['use_chunks'] = llamaindex_options['use_chunks']
                
            logger.debug(f"Loading PDF with parameters: {load_kwargs}")
            documents = llama_reader.load_data(str(pdf_path), **load_kwargs)
            
            # Combine all documents into a single markdown text
            if llamaindex_options['use_chunks']:
                # Return documents as they are (already chunked by LlamaIndex)
                markdown_text = "\n\n---\n\n".join([doc.text for doc in documents])
            else:
                # Combine all text into a single document
                markdown_text = "\n\n".join([doc.text for doc in documents])
            
            # Write the markdown output to file
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
            
            conversion_time = time.time() - start_time
            logger.info(f"Successfully converted PDF to Markdown: {md_path} in {conversion_time:.2f} seconds")
            if os.path.exists(md_path):
                logger.debug(f"Generated markdown file size: {os.path.getsize(md_path)} bytes")
            return None
            
        except Exception as e:
            logger.error(f"Failed to convert PDF to Markdown using LlamaIndex: {str(e)}")
            logger.debug(f"PDF conversion error details: {traceback.format_exc()}")
            raise RuntimeError(f"PDF conversion failed: {str(e)}")
    
    def pdf2md_pymupdf(self, pdf_path: str) -> None:
        """Convert a PDF to Markdown using PyMuPDF directly.

        Parameters:
            pdf_path (str): The file path to the PDF.

        Returns:
            None

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            ImportError: If pymupdf4llm package is not installed.
            RuntimeError: If conversion fails.
        """
        logger.info(f"Converting PDF to Markdown using pdf2md_pymupdf for {pdf_path}")
        logger.debug(f"PDF path details: {os.path.abspath(pdf_path)}, size: {os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 'N/A'} bytes")
        
        try:
            # Import required packages
            import pymupdf4llm
            import inspect
        except ImportError:
            logger.error("pymupdf4llm package not installed. Please install using: pip install pymupdf4llm")
            raise ImportError("pymupdf4llm package not installed")

        # Verify PDF file exists
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create output path for markdown file
        md_path = os.path.splitext(pdf_path)[0] + '.md'
        
        try:
            # Initialize PyMuPDF processor options
            pymupdf_options = {
                'preserve_images': False,
                'preserve_tables': True
            }
            
            start_time = time.time()
            logger.debug(f"Using PyMuPDF with options: {pymupdf_options}")
            
            # Use pymupdf4llm to convert directly to markdown
            # Check pymupdf4llm version to see if it supports the options
            to_markdown_params = inspect.signature(pymupdf4llm.to_markdown).parameters
            
            # Prepare kwargs based on available parameters
            kwargs = {}
            
            # Add options if they are supported by the current version
            if 'preserve_images' in to_markdown_params:
                kwargs['preserve_images'] = pymupdf_options['preserve_images']
                
            if 'preserve_tables' in to_markdown_params:
                kwargs['preserve_tables'] = pymupdf_options['preserve_tables']
                
            # Call to_markdown with appropriate options
            logger.debug(f"Converting PDF to Markdown with parameters: {kwargs}")
            markdown_text = pymupdf4llm.to_markdown(str(pdf_path), **kwargs)
            
            # Write the markdown output to file
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
            
            conversion_time = time.time() - start_time
            logger.info(f"Successfully converted PDF to Markdown: {md_path} in {conversion_time:.2f} seconds")
            if os.path.exists(md_path):
                logger.debug(f"Generated markdown file size: {os.path.getsize(md_path)} bytes")
            return None
            
        except Exception as e:
            logger.error(f"Failed to convert PDF to Markdown using PyMuPDF: {str(e)}")
            logger.debug(f"PDF conversion error details: {traceback.format_exc()}")
            raise RuntimeError(f"PDF conversion failed: {str(e)}")
    
    def pdf2md_textract(self, pdf_path: str) -> None:
        """Convert a PDF to Markdown using the textract library.

        Parameters:
            pdf_path (str): The file path to the PDF.

        Returns:
            None

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            ImportError: If textract package is not installed.
            RuntimeError: If conversion fails.
        """
        logger.info(f"Converting PDF to Markdown using pdf2md_textract for {pdf_path}")
        logger.debug(f"PDF path details: {os.path.abspath(pdf_path)}, size: {os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 'N/A'} bytes")
        
        try:
            import textract
        except ImportError:
            logger.error("textract package not installed. Please install using: pip install textract")
            raise ImportError("textract package not installed")

        # Verify PDF file exists
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Create output path for markdown file
        md_path = os.path.splitext(pdf_path)[0] + '.md'
        
        try:
            # Initialize textract options
            textract_options = {
                'method': 'pdftotext',
                'encoding': 'utf-8',
                'layout': True
            }
            
            start_time = time.time()
            logger.debug(f"Using textract with options: {textract_options}")
            
            # Build the extraction options
            extract_kwargs = {
                'method': textract_options['method'],
                'encoding': textract_options['encoding'],
                'layout': textract_options['layout']
            }
            
            # Remove None values
            extract_kwargs = {k: v for k, v in extract_kwargs.items() if v is not None}
            
            # Extract text from PDF
            logger.debug(f"Extracting text with parameters: {extract_kwargs}")
            text = textract.process(str(pdf_path), **extract_kwargs).decode(textract_options['encoding'])
            
            # Convert plain text to basic markdown
            # This is a simple conversion since textract doesn't preserve formatting well
            lines = text.split('\n')
            markdown_lines = []
            in_paragraph = False
            
            for line in lines:
                line = line.strip()
                if not line:  # Empty line
                    if in_paragraph:
                        markdown_lines.append('')  # End paragraph
                        in_paragraph = False
                else:
                    # Very basic heuristic for headings: all caps, not too long
                    if line.isupper() and len(line) < 100:
                        markdown_lines.append(f"## {line}")
                        in_paragraph = False
                    else:
                        if not in_paragraph:
                            in_paragraph = True
                        markdown_lines.append(line)
            
            markdown_text = '\n'.join(markdown_lines)
            
            # Write the markdown output to file
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
            
            conversion_time = time.time() - start_time
            logger.info(f"Successfully converted PDF to Markdown: {md_path} in {conversion_time:.2f} seconds")
            if os.path.exists(md_path):
                logger.debug(f"Generated markdown file size: {os.path.getsize(md_path)} bytes")
            return None
            
        except Exception as e:
            logger.error(f"Failed to convert PDF to Markdown using textract: {str(e)}")
            logger.debug(f"PDF conversion error details: {traceback.format_exc()}")
            raise RuntimeError(f"PDF conversion failed: {str(e)}")


class TextChunker:
    """Handles text chunking and markdown processing operations.
    
    This class provides methods for splitting markdown documents into chunks using different strategies:
    1. Length-based chunking: Divides text into fixed-size chunks with configurable overlap
    2. Hierarchy-based chunking: Divides text based on heading structure and document hierarchy
    
    The chunking parameters (chunk size and overlap) can be configured through the main_config.json file
    or passed directly to the chunking methods. Default values are used as fallbacks.
    
    Attributes:
        nlp: spaCy language model for text processing
        default_chunk_size: Default size of chunks in characters (from config or 1000)
        default_chunk_overlap: Default overlap between chunks in characters (from config or 100)
    """
    
    def __init__(self, config_file_path: Optional[Union[str, Path]] = None) -> None:
        """Initialize TextChunker with default configuration from main_config.json.
        
        Parameters:
            config_file_path (Optional[Union[str, Path]]): Path to the configuration file.
                If None, defaults to Path.cwd() / "config" / "main_config.json".
                
        Returns:
            None
        """
        logger.debug("TextChunker initialization started")
        try:
            start_time = time.time()
            # Load spaCy model
            
            self.datautility = DataUtility()
            
            # Load defaults from config file
            chunker_config_path = Path(config_file_path) if config_file_path else Path.cwd() / "config" / "main_config.json"
            try:
                if os.path.exists(chunker_config_path):
                    with open(chunker_config_path, 'r') as f:
                        config = json.load(f)
                    # Get chunking configuration from main_config.json
                    chunker_config = config.get('knowledge_base', {}).get('chunking', {}).get('other_config', {})
                    self.default_chunk_size = chunker_config.get('chunk_size', 500)
                    self.default_chunk_overlap = chunker_config.get('chunk_overlap', 50)
                    logger.debug(f"Loaded chunking configuration from {chunker_config_path}: chunk_size={self.default_chunk_size}, chunk_overlap={self.default_chunk_overlap}")
                else:
                    logger.warning(f"Config file not found at {chunker_config_path}, using default values")
                    self.default_chunk_size = 500
                    self.default_chunk_overlap = 50
                    
            except Exception as config_error:
                logger.error(f"Error loading config: {str(config_error)}, using default values")
                self.default_chunk_size = 500
                self.default_chunk_overlap = 50
                
            build_time = time.time() - start_time
            logger.debug(f"Loaded spaCy model in {build_time:.2f} seconds")
            logger.debug("TextChunker initialized successfully")
        except Exception as e:
            logger.error(f"TextChunker initialization failed: {str(e)}")
            logger.debug(f"Initialization error details: {traceback.format_exc()}")
            raise

    def length_based_chunking(self, markdown_file: str, chunk_size: Optional[int] = None, overlap: Optional[int] = None) -> pd.DataFrame:
        """Chunks text from a markdown file into overlapping segments and returns as DataFrame.
        This is a pure length-based chunking method that doesn't consider headings.

        Parameters:
            markdown_file (str): Path to the markdown file.
            chunk_size (int, optional): Size of each chunk in characters. If None, uses the default_chunk_size.
            overlap (int, optional): Number of characters to overlap between chunks. If None, uses the default_chunk_overlap.

        Returns:
            pd.DataFrame: DataFrame containing:
                - source: Source of the document
                - document_id: Unique identifier for source document
                - chunk_id: Unique identifier for text chunk
                - document_name: Name of the source document
                - reference: Unique identifier for each chunk
                - hierarchy: Document name (no heading hierarchy)
                - corpus: The chunk text content
                - embedding_model: Model used to generate embeddings (None at this stage)

        Raises:
            FileNotFoundError: If markdown file doesn't exist
            ValueError: If chunk_size <= overlap
        """
        # Use default values if not provided
        if chunk_size is None:
            chunk_size = self.default_chunk_size
        if overlap is None:
            overlap = self.default_chunk_overlap
        if chunk_size <= overlap:
            raise ValueError("chunk_size must be greater than overlap")
            
        # Get filename for reference generation
        filename = Path(markdown_file).stem.upper()
        logger.debug(f"Processing {filename} with chunk_size={chunk_size}, overlap={overlap}")
            
        # Read markdown file
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            logger.error(f"Markdown file not found: {markdown_file}")
            raise
            
        # Initialize chunks list
        chunks = []
        start = 0
        chunk_id = 0
        text_length = len(text)
        
        while start < text_length:
            # Calculate chunk boundaries
            end = min(start + chunk_size, text_length)
            
            # Get chunk text
            chunk_text = text[start:end].strip()
            
            # Only add chunk if it contains content
            if chunk_text:                
                # Generate a document_id for the first chunk, then reuse for all chunks
                if chunk_id == 0:
                    document_uuid = self.datautility.generate_uuid()
                
                # Ensure heading and content_type are added for schema compliance, even if basic for length-based
                # Ensure heading and content_type are added for schema compliance, even if basic for length-based
                chunk = {
                    'source': markdown_file,
                    'document_id': document_uuid,
                    'chunk_id': self.datautility.generate_uuid(),
                    'document_name': filename,
                    'reference': f"{filename} Chunk {chunk_id + 1}.",
                    'hierarchy': filename,  # Just use filename, no heading hierarchy
                    'corpus': chunk_text,
                    'embedding_model': None,
                    'heading': None,  # Optional field, None for length-based
                    'content_type': 'paragraph'  # Default for length-based
                }
                chunks.append(chunk)
                chunk_id += 1
            
            # Move to next chunk
            start = end - overlap
            
        # Convert to DataFrame
        df = pd.DataFrame(chunks)
        logger.info(f"Created {len(chunks)} chunks from {markdown_file}")
        return df

    def hierarchy_based_chunking(self, markdown_file: str, df_headings: pd.DataFrame) -> pd.DataFrame:
        """Extract hierarchical content chunks from a markdown file based on headings.
        
        Args:
            markdown_file: Path to the markdown file to process
            df_headings: DataFrame containing heading metadata with columns:
                - Level: Heading hierarchy level (e.g. 1, 2, 3)
                - Heading: Heading text
                - Page: Page number
                - File: File identifier (e.g. APS113)
                - Index: Index number
        
        Returns:
            DataFrame containing:
                - source: Source of the document
                - document_id: Unique identifier for source document
                - chunk_id: Unique identifier for text chunk
                - document_name: Name of the source document
                - hierarchy: Full heading path (e.g. "APS 113 > Main Body > Application")
                - heading: Current heading text
                - reference: Document reference
                - corpus: Text content under the heading
                - content_type: Type of content ('paragraph', 'table', etc.)
                - embedding_model: Model used to generate embeddings (None at this stage)
        """
        try:
            # Extract filename and read content
            filename = Path(markdown_file).stem.upper()
            logger.debug(f"Processing {filename}")
            
            # Clean heading metadata
            df_clean = df_headings.copy()
            df_clean['Level'] = pd.to_numeric(df_clean['Level'], errors='coerce', downcast='integer')
            df_clean['Heading'] = df_clean['Heading'].str.strip()
            df_clean = df_clean.dropna(subset=['Level', 'Heading'])
            
            # Filter headings for current document
            doc_headings = df_clean[df_clean['File'].str.contains(filename, case=False, na=False)]
            doc_headings = doc_headings.sort_values(by='Index')
            if doc_headings.empty:
                logger.warning(f"No matching headings found for document {filename} in the hierarchy file. Returning empty DataFrame.")
                return pd.DataFrame(columns=['source', 'document_id', 'chunk_id', 'document_name',
                                           'reference', 'hierarchy', 'corpus', 'embedding_model',
                                           'heading', 'content_type'])

            # Load markdown file
            with open(markdown_file, 'r', encoding='utf-8') as f:
                md_content = f.read().strip()
            
            # Extract content after the first heading
            first_heading = "## " + doc_headings.iloc[0]['Heading']
            first_heading_index = md_content.find(first_heading)
            if first_heading_index != -1:
                # Extract date from content before first heading if exists
                # header_content = md_content[:first_heading_index]
                md_content = md_content[first_heading_index:]
                logger.debug(f"First heading {first_heading} found at index {first_heading_index}")
            else:
                md_content = ""
                logger.error(f"First heading {first_heading} not found in {filename}")
            
            # Split content into lines
            lines = md_content.split('\n')

            # Initialize variables
            extracted_sections = []
            current_heading = None
            current_content = []
            current_level = 0
            hierarchy = [] 
            
            # Process content line by line
            for i, line in enumerate(lines):                
                # Check if line is a heading
                if line.startswith('## '):
                    if current_heading:
                        self._append_section(filename = filename,
                                        hierarchy = hierarchy,
                                        current_heading = current_heading,
                                        current_content = current_content,
                                        extracted_sections = extracted_sections)
                    
                    current_heading = re.sub(r'\$.*\$', '', line[3:]).strip()
                    current_level = doc_headings[doc_headings['Heading'] == current_heading]['Level'].iloc[0]
                    doc_headings = doc_headings.drop(doc_headings.index[0])
                    
                    if current_level == 1:
                        if "Attachment" not in current_heading:
                            current_heading = filename + " - " + current_heading
                        hierarchy = [current_heading]
                    elif current_level >= 1:
                        if len(hierarchy) >= current_level:
                            hierarchy = hierarchy[:current_level-1]
                            hierarchy.append(current_heading)
                        else:
                            hierarchy.append(current_heading)  
                    current_content = []
                else:
                    if line.strip():
                        current_content.append(line.strip())
            
            # Append last section
            if current_heading:
                self._append_section(filename = filename,
                                hierarchy = hierarchy,
                                current_heading = current_heading,
                                current_content = current_content,
                                extracted_sections = extracted_sections)
            
            # Convert to DataFrame with proper column names
            if extracted_sections:
                # Columns: 'hierarchy', 'reference', 'heading', 'corpus', 'content_type'
                df_sections = pd.DataFrame(extracted_sections, columns=['hierarchy', 'reference', 'heading', 'corpus', 'content_type'])
                
                # Generate a single document_id for all chunks from this file
                document_uuid = self.datautility.generate_uuid() # Generate once for the document
                
                # Add required fields from schema
                df_sections['source'] = markdown_file
                df_sections['document_id'] = document_uuid # Apply same document_id to all
                df_sections['chunk_id'] = df_sections.apply(lambda _: self.datautility.generate_uuid(), axis=1)
                df_sections['document_name'] = filename
                df_sections['embedding_model'] = None # Placeholder, filled by VectorBuilder
                # 'heading' and 'content_type' are already columns from extracted_sections
                # 'level' is optional and not explicitly added here, can be derived if needed.
                
                logger.info(f"Extracted {len(df_sections)} sections from {markdown_file}")
                return df_sections
            else:
                # Return empty DataFrame with required columns for schema consistency
                logger.warning(f"No sections extracted from {markdown_file}")
                return pd.DataFrame(columns=['source', 'document_id', 'chunk_id', 'document_name', 
                                           'reference', 'hierarchy', 'corpus', 'embedding_model', 
                                           'heading', 'content_type'])
            
        except FileNotFoundError:
            logger.error(f"Markdown file not found: {markdown_file}")
            raise
        except Exception as e:
            logger.error(f"Error processing markdown file {markdown_file}: {str(e)}")
            raise

    def _append_section(
        self, 
        filename: str, 
        hierarchy: List[str], 
        current_heading: str,
        current_content: List[str],
        extracted_sections: List[Tuple[str, str, str, str, str]], # Tuple: hierarchy_path, reference, heading, corpus, content_type
        content_type: str = 'paragraph'): # Default content_type passed from caller
        """ Append a section to the extracted sections.
        
        Args:
            filename: Document identifier
            hierarchy: Current heading hierarchy (list of strings)
            current_heading: Heading text of the current section
            current_content: List of text lines for the current section's content
            extracted_sections: List to append the new section tuple to
            content_type: The initial type of content being appended (e.g., 'paragraph', 'table')
        """
        # Construct full hierarchy path string
        hierarchy_path_str = filename + " > " + ' > '.join(hierarchy) if hierarchy else filename
        
        text_contents = '\n'.join(current_content).strip()
        if not text_contents: # Do not append if there is no actual content
            return

        # Determine prefix for reference based on hierarchy (e.g., Attachment, Chapter)
        attachment_info = None
        chapter_info = None
        
        # For any documents, we need to extract attachment information from the full hierarchy path
        if hierarchy and len(hierarchy) > 1:
            # Look through the entire hierarchy for attachment information
            for heading in hierarchy:
                attachment_match = re.search(r'Attachment ([A-Z])', heading, re.IGNORECASE)
                if attachment_match:
                    attachment_info = attachment_match.group(0)
                    break
        
        if hierarchy and len(hierarchy) > 1:
            for heading in hierarchy:
                chapter_match = re.search(r'Chapter ([A-Z])', heading, re.IGNORECASE)
                if chapter_match:
                    chapter_info = chapter_match.group(0)
                    break
        
        # For other documents, check just the last heading
        # SC
        # elif hierarchy: 
        #     last_heading_part = hierarchy[-1]
        #     attachment_match = re.search(r'Attachment ([A-Z])', last_heading_part, re.IGNORECASE) or \
        #                        re.search(r'Chapter (\d+)', last_heading_part, re.IGNORECASE)
        #     if attachment_match:
        #         attachment_info = attachment_match.group(0)
                
        # Format reference with proper APS number and attachment information
        # Example: "APS 113, Attachment D" without trailing periods
        if 'APS' in filename and attachment_info:
            prefix_para = f"{filename.replace('APS', 'APS ').strip()}, {attachment_info}"
        else:
            prefix_para = filename.replace('APS', 'APS ').strip()

        if 'CRE' in filename and chapter_info:
            prefix_para = f"{filename.replace('CRE', 'CRE ').strip()}, {chapter_info}"
        else:
            prefix_para = filename.replace('CRE', 'CRE ').strip()


        # Specific to Basel Framework (CRE documents)
        # if "CRE" in filename:
        #     # Split by numbering system like NNN.N or N.N, possibly prefixed by CRE.
        #     paragraphs = re.split(r'\n(?=(?:[A-Z]+\.)?\d+\.\d+)', text_contents) 
        #     for para_idx, paragraph_text in enumerate(paragraphs):
        #         paragraph_text_stripped = paragraph_text.strip()
        #         if not paragraph_text_stripped: continue

        #         match = re.match(r'(?:([A-Z]+)\.)?(\d+\.\d+)', paragraph_text_stripped) 
        #         para_num_text = match.group(2) if match else f"auto{para_idx+1}"
        #         # Use the captured prefix (e.g., "CRE") if present, otherwise default to no specific prefix in ref.
        #         ref_prefix_text = f", {match.group(1)}" if match and match.group(1) else ""
                
        #         # Format: "APS 113, Attachment A, Para 1" without trailing period
        #         final_reference = f"{prefix_para}, Para {para_num_text.rstrip('.')}" + (ref_prefix_text if ref_prefix_text else "")
                
        #         # Determine content type using regex for better table detection
        #         content_type = 'paragraph'
        #         if re.search(r'\|[-:\| ]+\|', paragraph_text_stripped) or re.search(r'^Table \d+', paragraph_text_stripped, re.IGNORECASE):
        #             content_type = 'table'
                
        #         extracted_sections.append((hierarchy_path_str,
        #                                    final_reference,
        #                                    current_heading, 
        #                                    paragraph_text_stripped,
        #                                    content_type))
        #         logger.debug(f"Paragraph found: {filename} - {current_heading} - Ref: {final_reference}")

        # Specific to APS, APG and Risk Opinions
        # else:

            # Determine initial block content type based on content analysis
        block_content_type = content_type
        
        # Improved content type detection
        if re.search(r'^Table \d+', text_contents, re.IGNORECASE) or \
            re.search(r'\|[-:\| ]+\|', text_contents) or \
            re.search(r'^\+[-+]+\+$', text_contents, re.MULTILINE):
            block_content_type = 'table'
        elif re.search(r'^\d+\.\s', text_contents) or re.search(r'^[a-z]\)\s', text_contents):
            block_content_type = 'list'
        elif re.search(r'^NOTE:', text_contents, re.IGNORECASE) or re.search(r'^Example:', text_contents, re.IGNORECASE):
            block_content_type = 'note'
        
        # If it's a table, treat as a single unit. Otherwise, split by paragraph markers.
        if block_content_type == 'table':
            paragraphs = [text_contents]
        elif re.search(r'^\d+\.', text_contents, re.MULTILINE): 
                paragraphs = re.split(r'\n(?=\d+\.)', text_contents) 
        elif len(text_contents) > 8000: 
                paragraphs = re.split(r'\n', text_contents)
        else:
                paragraphs = [text_contents]

        for para_idx, paragraph_text in enumerate(paragraphs):
            paragraph_text_stripped = paragraph_text.strip()
            if not paragraph_text_stripped: 
                continue

            # Default content type for this specific segment
            current_segment_content_type = 'paragraph' 
            final_reference = f"{prefix_para} Orphan {para_idx+1}" 

            match_table = re.match(r'^Table (\d+)', paragraph_text_stripped, re.IGNORECASE)
            match_para = re.match(r'^(\d+\.)', paragraph_text_stripped)

            if match_table: 
                table_num_text = match_table.group(1)
                final_reference = f"{prefix_para}, Table {table_num_text}"
                current_segment_content_type = 'table'
                logger.debug(f"Table found: {filename} - {current_heading} - Ref: {final_reference}")
            elif match_para: 
                para_num_text = match_para.group(1)
                final_reference = f"{prefix_para}, Para {para_num_text}"
                current_segment_content_type = 'paragraph' # Explicitly paragraph
                # logger.debug(f"Paragraph found: {filename} - {current_heading} - Ref: {final_reference}")
            else: # Orphan or unnumbered content
                # If the broader block was identified as a table, this segment is part of it.
                final_reference = f"{prefix_para}"
                # if block_content_type == 'table': 
                #     current_segment_content_type = 'table' 
                #     final_reference = f"{prefix_para} Table Content {para_idx+1}" 
                # else: # Otherwise, it's a paragraph.
                #     current_segment_content_type = 'paragraph'
                logger.debug(f"Orphan/unnumbered content: {filename} - {current_heading} - Default Ref: {final_reference}")
            
            extracted_sections.append((hierarchy_path_str,
                                        final_reference,
                                        current_heading,
                                        paragraph_text_stripped,
                                        current_segment_content_type))


class VectorBuilder:
    """
    Creates and manages a vector database for knowledge representation.
    Depends on TextParser and TextChunker for text parsing and chunking.
    
    Methods:
        create_vectordb: Creates a vector database from markdown files
        load_vectordb: Loads a vector database from a file
        merge_vectordbs: Merges multiple vector databases into one
    """
    def __init__(self, parser: TextParser, chunker: TextChunker, generator=None, config_file_path: Optional[Union[str, Path]] = None) -> None:
        """Initialize VectorBuilder with a DataCleanser instance.
        
        Parameters:
            parser (TextParser): Instance of TextParser.
            chunker (TextChunker): Instance of TextChunker.
            generator (Generator, optional): Instance of Generator. If None, a new one will be created.
            config_file_path (Optional[Union[str, Path]]): Path to the configuration file.
                If None, defaults to Path.cwd() / "config" / "main_config.json".
        
        Returns:
            None
        """
        # Store parser, chunker, and generator instances
        self.parser = parser
        self.chunker = chunker
        self.generator = generator if generator is not None else Generator()
        self.default_buffer_ratio = 0.9
        self.db_dir = Path.cwd() / "db"
        self.vector_dir = self.db_dir / "vector"
        self.vector_dir.mkdir(exist_ok=True, parents=True)
        
    def process_input_file(self, file_path: str, output_md_path: Optional[str] = None, conversion_method: str = 'pymupdf') -> str:
        """Process input file (PDF or Markdown) and return path to markdown file.
        
        Args:
            file_path: Path to input file (PDF or Markdown)
            output_md_path: Optional path for output markdown file (for PDF conversion)
            conversion_method: Method to use for PDF conversion ('pymupdf', 'openleaf', 'markitdown', 'ocr', 'llamaindex')
            
        Returns:
            str: Path to markdown file for further processing
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # If file is already markdown, return its path
        if file_ext == '.md':
            return file_path
        
        # If file is PDF, convert to markdown
        elif file_ext == '.pdf':
            if output_md_path is None:
                output_md_path = os.path.splitext(file_path)[0] + '.md'
                
            # Select conversion method
            if conversion_method == 'pymupdf':
                self.parser.pdf2md_pymupdf(file_path)
            elif conversion_method == 'openleaf':
                self.parser.pdf2md_openleaf(file_path)
            elif conversion_method == 'markitdown':
                self.parser.pdf2md_markitdown(file_path)
            elif conversion_method == 'ocr':
                self.parser.pdf2md_ocr(file_path, output_md_path)
            elif conversion_method == 'llamaindex':
                self.parser.pdf2md_llamaindex(file_path)
            else:
                raise ValueError(f"Unsupported conversion method: {conversion_method}")
                
            return output_md_path
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Only .md and .pdf are supported.")
        

    def apply_chunking(self, 
                      input_file: str,
                      df_headings: Optional[pd.DataFrame] = None,
                      chunking_method: str = 'hierarchy',
            **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Apply text chunking to input file and collect document metadata.
        
        Args:
            input_file: Path to the input file (PDF or markdown)
            df_headings: DataFrame containing heading metadata (for hierarchy chunking)
            chunking_method: Method to use for chunking ('hierarchy' or 'length')
            **kwargs: Additional arguments for chunking method (e.g., conversion_method for process_input_file)
            
        Returns:
            Tuple[pd.DataFrame, Dict[str, Any]]: 
                - DataFrame with chunked text
                - Dictionary with document-level metadata
        """
        # Process input file (convert PDF to markdown if needed)
        # kwargs here might include 'conversion_method'
        markdown_file = self.process_input_file(input_file, conversion_method=kwargs.get('conversion_method', 'pymupdf'))
        
        # Validate chunking method
        if chunking_method not in ['hierarchy', 'length']:
            raise ValueError(f"Invalid chunking method: {chunking_method}")
        
        chunks_df = pd.DataFrame()
        # Set defaults and validate parameters based on chunking method
        if chunking_method == 'length':
            chunk_size = kwargs.get('chunk_size', self.chunker.default_chunk_size) # Use chunker's default
            chunk_overlap = kwargs.get('chunk_overlap', self.chunker.default_chunk_overlap) # Use chunker's default
            chunks_df = self.chunker.length_based_chunking(
                markdown_file,
                chunk_size=chunk_size,
                overlap=chunk_overlap
            )
        elif chunking_method == 'hierarchy':
            if df_headings is None or df_headings.empty: # Ensure df_headings is provided for hierarchy
                 raise ValueError(f"Hierarchy data (df_headings) not provided for hierarchy-based chunking of {input_file}")
            # chunk_size and chunk_overlap are not used for hierarchy, but pass other kwargs if any
            chunks_df = self.chunker.hierarchy_based_chunking(
                markdown_file,
                df_headings
            )
        
        # Determine the partition based on the document name or file path
        partition = None
        file_path = Path(input_file)
        file_path_str = str(file_path)
        
        if 'standard' in file_path_str:
            partition = 'standard'
        elif 'guidance' in file_path_str:
            partition = 'guidance'
        elif 'opinion' in file_path_str:
            partition = 'opinion'
        else:
            partition = 'general'

        if 'au' in file_path_str:
            partition = 'au-' + partition    
        elif 'eu' in file_path_str:
            partition = 'eu-' + partition
        elif 'bs' in file_path_str:
            partition = 'bs-' + partition
        else:
            partition = 'ge-' + partition

        # Add partition field to the chunks DataFrame
        if not chunks_df.empty:
            chunks_df['partition'] = partition
            
        # Collect document-level metadata
        doc_meta = {
            'document_id': None, 
            'document_author': "Unknown", 
            'document_format': Path(input_file).suffix.replace('.', ''), 
            'partition': partition,
            'n_sections': 0, # Placeholder, could be enhanced by analyzing unique hierarchy paths in chunks_df
            'n_chunks': len(chunks_df)
        }

        if not chunks_df.empty and 'document_id' in chunks_df.columns:
            # All chunks from the same document should have the same document_id
            doc_meta['document_id'] = chunks_df['document_id'].iloc[0] 
            # Estimate n_sections by counting unique top-level hierarchy entries if available
            if 'hierarchy' in chunks_df.columns:
                 try: # Handle potential errors if hierarchy is not as expected (e.g. None)
                    doc_meta['n_sections'] = chunks_df['hierarchy'].astype(str).apply(lambda x: x.split(' > ')[0]).nunique()
                 except Exception:
                    logger.debug("Could not derive n_sections from hierarchy for metadata.")

        elif not chunks_df.empty: 
            logger.warning(f"document_id column missing in chunks_df for {input_file}. Generating a new one for metadata.")
            # This case should ideally not occur if chunkers correctly add document_id
            doc_meta['document_id'] = self.chunker.datautility.generate_uuid() # Generate a new one for the metadata
        else: 
            logger.warning(f"No chunks produced for {input_file}. Generating a document_id for metadata record.")
            doc_meta['document_id'] = self.chunker.datautility.generate_uuid()


        return chunks_df, doc_meta

    def create_embeddings(self, 
                          chunks_df: pd.DataFrame,
                          model: Optional[str] = None,
                          **kwargs) -> pd.DataFrame:
        """Generate embeddings for text chunks.
        
        Args:
            chunks_df: DataFrame with chunked text
            model: Model to use for embedding generation
            **kwargs: Additional arguments for embedding generation
            
        Returns:
            pd.DataFrame: DataFrame with embeddings added
        """
        # Generate embeddings for corpus and hierarchy
        logger.info("Generating embeddings for corpus texts")
        buffer_ratio = kwargs.get('buffer_ratio', self.default_buffer_ratio)
        
        corpus_vectors = self.generator.get_embeddings(
            text=chunks_df['corpus'].tolist(),
            model=model,
            buffer_ratio=buffer_ratio
        )
        
        logger.info("Generating embeddings for hierarchy texts")
        hierarchy_vectors = self.generator.get_embeddings(
            text=chunks_df['hierarchy'].tolist(),
            model=model,
            buffer_ratio=buffer_ratio
        )
        
        # Convert 2D arrays to list of 1D arrays if needed
        import numpy as np
        if isinstance(corpus_vectors, np.ndarray) and corpus_vectors.ndim == 2:
            logger.info(f"Converting 2D corpus vectors array with shape {corpus_vectors.shape} to list of 1D arrays")
            corpus_vectors = [row.tolist() for row in corpus_vectors]
        
        if isinstance(hierarchy_vectors, np.ndarray) and hierarchy_vectors.ndim == 2:
            logger.info(f"Converting 2D hierarchy vectors array with shape {hierarchy_vectors.shape} to list of 1D arrays")
            hierarchy_vectors = [row.tolist() for row in hierarchy_vectors]
        
        # Add vector columns
        chunks_df['corpus_vector'] = corpus_vectors
        chunks_df['hierarchy_vector'] = hierarchy_vectors
        
        # Update embedding_model field if not already set
        if 'embedding_model' in chunks_df.columns and chunks_df['embedding_model'].isnull().all():
            chunks_df['embedding_model'] = model
        
        return chunks_df


    def save_db(self, 
                chunks_df: pd.DataFrame,
                input_file: str,
                **kwargs) -> str:
        """Save DataFrame to parquet file.
        
        Args:
            chunks_df: DataFrame to save
            input_file: Original input file path (used for naming)
            **kwargs: Additional arguments for parquet saving
            
        Returns:
            str: Path to saved parquet file
        """
        # Save to parquet file
        input_name_no_ext = os.path.splitext(os.path.basename(input_file))[0].lower()
        
        # Add source_file column to help with debugging and tracking
        chunks_df['source_file'] = str(input_file)
        
        # Extract region and document type from the file path
        file_path_str = str(input_file)
        region = "general"
        doc_type = "standard"
        
        # Extract region (au, bs, eu) from the file path
        logger.critical(file_path_str)
        if '/au/' in file_path_str or '\\au\\' in file_path_str:
            region = 'au'
        elif '/bs/' in file_path_str or '\\bs\\' in file_path_str:
            region = 'bs'
        elif '/eu/' in file_path_str or '\\eu\\' in file_path_str:
            region = 'eu'
        
        # Extract document type (standard, guidance, opinion) from the file path
        if '/standard/' in file_path_str or '\\standard\\' in file_path_str:
            doc_type = 'standard'
        elif '/guidance/' in file_path_str or '\\guidance\\' in file_path_str:
            doc_type = 'guidance'
        elif '/opinion/' in file_path_str or '\\opinion\\' in file_path_str:
            doc_type = 'opinion'
            
        # Add region and doc_type columns
        chunks_df['region'] = region
        chunks_df['doc_type'] = doc_type
        
        # Ensure using proper db directory path
        output_file = self.vector_dir / f'v_{input_name_no_ext}.parquet'
        chunks_df.to_parquet(output_file)
        
        logger.info(f"Vector database created with {len(chunks_df)} chunks and saved to {output_file}")
        return str(output_file)


    def create_db(self, 
                  input_file: str,
                  df_headings: pd.DataFrame,
                  chunking_method: str = 'hierarchy',
                  model: Optional[str] = None,
                  **kwargs) -> Tuple[Optional[str], Dict[str, Any]]:
        """Create a vector database from input files and return its path and metadata.
        
        Args:
            input_file: Path to the input file (PDF or markdown)
            df_headings: DataFrame containing heading metadata
            chunking_method: Method to use for chunking ('hierarchy' or 'length')
            model: Model to use for embedding generation
            **kwargs: Additional arguments (e.g., conversion_method for PDF, chunk_size, chunk_overlap for length chunking)
            
        Returns:
            Tuple[Optional[str], Dict[str, Any]]: 
                - Path to the saved vector database file (None if no chunks)
                - Dictionary with document-level metadata
        """
        try:
            # Step 1: Apply chunking and get document metadata
            # Pass relevant kwargs to apply_chunking, which then passes to process_input_file or chunkers
            chunks_df, doc_meta = self.apply_chunking(
                input_file=input_file,
                df_headings=df_headings, 
                chunking_method=chunking_method,
                conversion_method=kwargs.get('conversion_method'), 
                chunk_size=kwargs.get('chunk_size'), # For length_based_chunking
                chunk_overlap=kwargs.get('chunk_overlap') # For length_based_chunking
            )

            if chunks_df.empty:
                logger.warning(f"No chunks generated for {input_file}. Vector DB will not be created.")
                return None, doc_meta

            # Step 2: Create embeddings
            chunks_df = self.create_embeddings(  # This modifies chunks_df or returns a new one
                chunks_df=chunks_df,
                model=model,
                **kwargs
            )
            
            # Step 3: Save to parquet
            output_file_path = self.save_db( 
                chunks_df=chunks_df,
                input_file=input_file 
            )
            
            return output_file_path, doc_meta
            
        except Exception as e:
            logger.error(f"Error creating vector database for {input_file}: {str(e)}")
            logger.debug(f"Vector database creation error details: {traceback.format_exc()}")
            raise

    def load_db(self, parquet_file: str = None) -> pd.DataFrame:
        """Load the vector database from disk.
        
        Args:
            parquet_file: Path to the parquet file containing the vector database.
                          If None, will look for a file in the db directory.
            
        Returns:
            DataFrame containing the knowledge base with vector columns
            
        Raises:
            FileNotFoundError: If the vector database file doesn't exist
            ValueError: If the file format is not supported or the file is corrupted
        """
        logger.debug(f"Starting to load vector database from {parquet_file}")
        start_time = time.time()
        
        try:
            # If no filepath is provided, try to find a vector database in the db/vector directory
            if parquet_file is None:
                vector_files = list(self.vector_dir.glob('v_*.parquet'))
                if not vector_files:
                    raise FileNotFoundError("No vector database files found in the db directory")
                # Use the most recently modified file
                parquet_file = str(sorted(vector_files, key=lambda f: f.stat().st_mtime, reverse=True)[0])
                logger.debug(f"Using most recent vector database file: {parquet_file}")
            
            # Check if file exists
            if not os.path.exists(parquet_file):
                raise FileNotFoundError(f"Vector database not found: {parquet_file}")
            
            # Load parquet file
            df = pd.read_parquet(parquet_file)
            
            # Validate required columns
            required_columns = ['reference', 'hierarchy', 'corpus']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Required column '{col}' not found in vector database")
            
            # Check for vector columns
            vector_columns = [col for col in df.columns if 'vector' in col or 'embedding' in col]
            if not vector_columns:
                logger.warning(f"No vector columns found in {parquet_file}")
            
            # Convert vector columns from string to numpy arrays if needed
            for col in vector_columns:
                if df[col].dtype == object:
                    try:
                        df[col] = df[col].apply(np.array)
                    except Exception as e:
                        logger.warning(f"Could not convert column {col} to numpy arrays: {e}")
            
            logger.info(f"Loaded vector database from {parquet_file} with {len(df)} chunks in {time.time() - start_time:.2f} seconds")
            return df
            
        except Exception as e:
            logger.error(f"Error loading vector database: {str(e)}")
            logger.debug(f"Load error details: {traceback.format_exc()}")
            raise
    
    def _format_reference(self, hierarchy: str, reference: str) -> str:
        """
        Format the reference string correctly by combining hierarchy and reference information.
        
        Args:
            hierarchy: The hierarchy information (e.g., "APS113 > Attachment B - Risk components for...") 
            reference: The reference information (e.g., "APS113, Para 35.")
            
        Returns:
            Properly formatted reference (e.g., "APS 113, Attachment B, Para 35")
        """
        # Default to original reference if we can't improve it
        if not hierarchy or not reference:
            return reference
        
        # Extract components
        try:
            # Extract document ID
            doc_id = None
            if hierarchy and '>' in hierarchy:
                doc_id_part = hierarchy.split('>')[0].strip()
                if doc_id_part:
                    # Format as 'APS 113' instead of 'APS113'
                    doc_id = re.sub(r'([A-Za-z]+)([0-9]+)', r'\1 \2', doc_id_part)
            
            # Extract section from hierarchy (Attachment, Chapter, etc.)
            section = None
            if hierarchy and '>' in hierarchy:
                parts = hierarchy.split('>')
                if len(parts) > 1 and '-' in parts[1]:
                    section_part = parts[1].split('-')[0].strip()
                    # Remove any redundancy with the document ID
                    if section_part != doc_id_part:
                        section = section_part
            
            # Extract paragraph number from reference
            para = None
            if reference and 'Para' in reference:
                para_match = re.search(r'Para\s+([0-9.]+)', reference)
                if para_match:
                    # Remove any trailing period from the paragraph number
                    para_num = para_match.group(1)
                    if para_num.endswith('.'):
                        para_num = para_num[:-1]  # Remove trailing period
                    para = f"Para {para_num}"
            
            # Remove redundancy in reference (e.g., don't repeat document ID)
            ref_parts = []
            if doc_id:
                ref_parts.append(doc_id)
            if section and section not in str(doc_id):
                ref_parts.append(section)
            if para:
                ref_parts.append(para)
                
            # Combine components into proper format
            if ref_parts:
                formatted_ref = ", ".join(ref_parts)
                # Ensure no trailing period
                if formatted_ref.endswith('.'):
                    formatted_ref = formatted_ref[:-1]
                return formatted_ref
        except Exception as e:
            logger.warning(f"Error formatting reference: {str(e)} - using original")
        
        # Return original if formatting fails
        return reference
        
    def merge_db(self, parquet_files: List[str], output_name: str = None) -> pd.DataFrame:
        """Merge multiple vector databases into one.
        
        Args:
            parquet_files: List of paths to vector database files to merge
            output_name: Name for the merged vector database file (without extension)
            
        Returns:
            pd.DataFrame: The merged vector database
            
        Raises:
            ValueError: If no parquet_files are provided or they are incompatible
            FileNotFoundError: If any of the specified files don't exist
        """
        logger.debug(f"Starting to merge {len(parquet_files)} vector databases")
        start_time = time.time()
        
        if not parquet_files:
            raise ValueError("No parquet files provided for merging")
            
        try:
            # Load and validate each dataframe
            dataframes = []
            for i, filepath in enumerate(parquet_files):
                logger.debug(f"Loading vector database {i+1}/{len(parquet_files)}: {filepath}")
                
                # Check if file exists
                if not os.path.exists(filepath):
                    raise FileNotFoundError(f"Vector database file not found: {filepath}")
                
                # Load dataframe
                df = pd.read_parquet(filepath)
                
                # Validate required columns
                required_columns = ['reference', 'hierarchy', 'corpus']
                for col in required_columns:
                    if col not in df.columns:
                        logger.warning(f"Required column '{col}' not found in {filepath}, skipping")
                        continue
                
                # Check for vector columns
                vector_columns = [col for col in df.columns if 'vector' in col or 'embedding' in col]
                if not vector_columns:
                    logger.warning(f"No vector columns found in {filepath}, skipping")
                    continue
                
                # Add source file information with full path to identify the directory
                df['source_file'] = str(filepath)
                
                # Extract region and type from file path
                file_path_str = str(filepath)
                region = "general"
                doc_type = "standard"
                
                # Extract region (au, bs, eu) from the file path
                if '/au/' in file_path_str or '\\au\\' in file_path_str:
                    region = 'au'
                elif '/bs/' in file_path_str or '\\bs\\' in file_path_str:
                    region = 'bs'
                elif '/eu/' in file_path_str or '\\eu\\' in file_path_str:
                    region = 'eu'
                
                # Extract document type (standard, guidance, opinion) from the file path
                if '/standard/' in file_path_str or '\\standard\\' in file_path_str:
                    doc_type = 'standard'
                elif '/guidance/' in file_path_str or '\\guidance\\' in file_path_str:
                    doc_type = 'guidance'
                elif '/opinion/' in file_path_str or '\\opinion\\' in file_path_str:
                    doc_type = 'opinion'
                
                # Add region and doc_type columns to the dataframe
                df['region'] = region
                df['doc_type'] = doc_type
                
                # Format references properly
                if 'reference' in df.columns and 'hierarchy' in df.columns:
                    df['reference'] = df.apply(
                        lambda row: self._format_reference(row['hierarchy'], row['reference']),
                        axis=1
                    )
                
                dataframes.append(df)
                logger.debug(f"Added {len(df)} chunks from {filepath}")
            
            if not dataframes:
                raise ValueError("No valid vector databases found to merge")
                
            # Merge dataframes
            merged_df = pd.concat(dataframes, ignore_index=True)
            
            # Determine region and doc_type for the merged database
            # If all dataframes have the same region and doc_type, use those
            # Otherwise, use the output_name if provided or generate a default name
            regions = set()
            doc_types = set()
            
            for df in dataframes:
                if 'region' in df.columns:
                    regions.update(df['region'].unique())
                if 'doc_type' in df.columns:
                    doc_types.update(df['doc_type'].unique())
            
            # Generate output name based on region and doc_type if they are consistent
            if len(regions) == 1 and len(doc_types) == 1:
                region = list(regions)[0]
                doc_type = list(doc_types)[0]
                output_name = f"{region}_{doc_type}"
            elif not output_name:
                # Use a timestamp if no consistent region/type and no output_name provided
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_name = f"merged_vectordb_{timestamp}"
                
            # Remove any prefix from the output_name to avoid double prefixes
            if output_name.startswith("v_"):
                output_name = output_name[2:]
            
            # Remove .parquet extension if included
            if output_name.endswith('.parquet'):
                output_name = output_name[:-8]
            
            # Save the merged vector database
            output_path = self.vector_dir / f"v_{output_name}.parquet"
            merged_df.to_parquet(output_path)
                
            logger.info(f"Merged {len(dataframes)} vector databases into {output_path} with {len(merged_df)} total chunks in {time.time() - start_time:.2f} seconds")
            return merged_df
            
        except Exception as e:
            logger.error(f"Failed to merge vector databases: {str(e)}")
            logger.debug(f"Merge error details: {traceback.format_exc()}")
            raise
    

class MemoryBuilder:
    """
    Builds memory databases by extracting entries from the vector database.
    Handles separate memory databases for episodic and personality data.
    
    Memory databases are kept completely separate with distinct schemas:
    
    1. Episodic Memory Schema:
       - memory_id: UUID for the memory entry
       - query: The query that would retrieve this memory
       - entity: Unique identifier for the entity (document_name + reference)
       - context: JSON object containing:
         - document_name: Name of the source document
         - content: The actual text content
         - reference: Reference identifier for the chunk
         - source: Source of the document
         - chunk_id: Unique identifier for the chunk
         - hierarchy: Document structure path
         - timestamp: When this memory was created
    
    2. Personality Memory Schema:
       - mode_id: UUID for the personality mode
       - mode_name: Name of the personality mode
       - personality_type: List of personality types (e.g., ["openness", "conscientiousness"])
       - personality_score: Object with scores (0-100) for each Big Five trait
       - cognitive_style: String describing cognitive approach
       - mbti_type: MBTI personality type (e.g., "INTJ")
       - sentiment_score: Float (-1.0 to 1.0) representing emotional tone
       - mode_description: Text description of the mode
       - activation_contexts: List of contexts where this mode is appropriate
       - activation_triggers: List of trigger objects that activate this mode
    
    Methods:
        create_episodic_db: Creates an episodic memory database from vector database entries
        create_personality_db: Creates a personality memory database (placeholder for future implementation)
        load_db: Loads a memory database from a file
    """
    
    def __init__(self) -> None:
        """
        Initialize a MemoryBuilder instance.
        """
        try:
            self.datautility = DataUtility()
            # Set up database directory paths
            self.db_dir = Path.cwd() / "db"
            self.memory_dir = self.db_dir / "memory"
            self.vector_dir = self.db_dir / "vector"
            
            # Create directories if they don't exist
            self.memory_dir.mkdir(exist_ok=True, parents=True)
            logger.debug(f"MemoryBuilder initialized with memory_dir: {self.memory_dir}")
        except Exception as e:
            logger.error(f"MemoryBuilder initialization failed: {str(e)}")
            logger.debug(f"Initialization error details: {traceback.format_exc()}")
            raise
    
    def create_episodic_db(self, vector_db_file: Optional[str] = None, num_entries: int = 5) -> str:
        """
        Create an episodic memory database from vector database entries.
        Extracts the first N entries from a vector database and stores them as
        episodic memory entries in the memory database. This method specifically
        creates episodic memory databases, which have a different schema than
        personality memory databases.
        
        Episodic Memory Schema:
        - memory_id: UUID for the memory entry
        - query: The query that would retrieve this memory
        - entity: Unique identifier for the entity (document_name + reference)
        - context: JSON object containing:
          - document_name: Name of the source document
          - content: The actual text content
          - reference: Reference identifier for the chunk
          - source: Source of the document
          - chunk_id: Unique identifier for the chunk
          - hierarchy: Document structure path
          - timestamp: When this memory was created
        
        Args:
            vector_db_file: Path to the vector database parquet file.
                           If None, will look for a file in the db/vector directory.
            num_entries: Number of entries to extract from the vector database (default: 5)
            
        Returns:
            str: Path to the saved episodic memory database file
            
        Raises:
            FileNotFoundError: If the vector database file doesn't exist
            ValueError: If the vector database format is not supported or the file is corrupted
        """
        logger.debug(f"Starting to create memory database from {vector_db_file}")
        start_time = time.time()
        
        try:
            # If no filepath is provided, try to find a vector database in the db/vector directory
            if vector_db_file is None:
                vector_files = list(self.vector_dir.glob('v_*.parquet'))
                if not vector_files:
                    raise FileNotFoundError("No vector database files found in the db/vector directory")
                # Use the most recently modified file
                vector_db_file = str(sorted(vector_files, key=lambda f: f.stat().st_mtime, reverse=True)[0])
                logger.debug(f"Using most recent vector database file: {vector_db_file}")
            
            # Check if file exists
            if not os.path.exists(vector_db_file):
                raise FileNotFoundError(f"Vector database not found: {vector_db_file}")
            
            # Load vector database
            df_vector = pd.read_parquet(vector_db_file)
            
            # Validate required columns
            required_columns = ['corpus', 'document_name', 'hierarchy']
            for col in required_columns:
                if col not in df_vector.columns:
                    raise ValueError(f"Required column '{col}' not found in vector database")
            
            # Extract the first N entries
            sample_df = df_vector.head(num_entries).copy()
            
            
            episodic_memory_parquet_path = self.memory_dir / 'episodic_memory.parquet'
            memory_entries = []
            existing_entities = set()
            existing_context_chunk_ids = set()

            if episodic_memory_parquet_path.exists():
                logger.info(f"Loading existing episodic memory from {episodic_memory_parquet_path}")
                try:
                    existing_memory_df = pd.read_parquet(episodic_memory_parquet_path)
                    memory_entries = existing_memory_df.to_dict('records')
                    existing_entities = set(existing_memory_df['entity'].tolist())
                    # Correctly extract chunk_ids from the context dictionary
                    for entry in memory_entries:
                        if isinstance(entry.get('context'), dict) and entry['context'].get('chunk_id'):
                            existing_context_chunk_ids.add(entry['context']['chunk_id'])
                    logger.info(f"Loaded {len(memory_entries)} existing entries.")
                except Exception as e:
                    logger.warning(f"Could not load existing episodic memory database: {e}. It might be recreated or appended to if possible.")
                    memory_entries = [] # Start fresh if loading fails catastrophically
            else:
                logger.info(f"{episodic_memory_parquet_path} not found. Creating with dummy entries.")
                for i in range(1, 4): # Create 3 dummy entries
                    dummy_entry = {
                        'memory_id': self.datautility.generate_uuid(),
                        'query': "Dummy query",
                        'entity': f"Dummy entity {i}",
                        'context': {
                            'document_name': "Dummy document",
                            'content': "Dummy content",
                            'reference': f"Dummy reference {i}",
                            'source': "Dummy source",
                            'chunk_id': f"dummy_chunk_id_{i}",
                            'hierarchy': "Dummy hierarchy",
                            'timestamp': datetime.datetime.now().isoformat()
                        }
                    }
                    memory_entries.append(dummy_entry)
                    existing_entities.add(dummy_entry['entity'])
                    existing_context_chunk_ids.add(dummy_entry['context']['chunk_id'])
                logger.info(f"Created {len(memory_entries)} dummy entries.")

            # If vector_db_file is provided, process it and append new, non-duplicate entries
            if vector_db_file:
                if not os.path.exists(vector_db_file):
                    logger.error(f"Vector database not found: {vector_db_file}. Cannot append entries.")
                else:
                    df_vector = pd.read_parquet(vector_db_file)
                    required_columns = ['corpus', 'document_name', 'hierarchy', 'chunk_id', 'reference']
                    if not all(col in df_vector.columns for col in required_columns):
                        raise ValueError(f"Vector database {vector_db_file} is missing one or more required columns: {required_columns}")

                    sample_df = df_vector.head(num_entries).copy()
                    logger.info(f"Processing {len(sample_df)} entries from {vector_db_file} for episodic memory.")

                    for _, row in sample_df.iterrows():
                        prospective_entity = f"{row['document_name']}_{row.get('reference', self.datautility.generate_uuid()[:8])}"
                        prospective_context_chunk_id = row.get('chunk_id')

                        if prospective_entity in existing_entities:
                            logger.warning(f"Skipping entry for entity '{prospective_entity}' as it already exists.")
                            continue

                        if prospective_context_chunk_id in existing_context_chunk_ids:
                            logger.warning(f"Skipping entry for context.chunk_id '{prospective_context_chunk_id}' as it already exists in memory.")
                            continue

                        context = {
                            'document_name': row['document_name'],
                            'content': row['corpus'],
                            'reference': row.get('reference', f"Ref-{self.datautility.generate_uuid()[:8]}"),
                            'source': row.get('source', Path(vector_db_file).stem),
                            'chunk_id': prospective_context_chunk_id, # Use original chunk_id from vector_db
                            'hierarchy': row['hierarchy'],
                            'timestamp': datetime.datetime.now().isoformat()
                        }

                        memory_entry = {
                            'memory_id': self.datautility.generate_uuid(),
                            'query': f"Tell me about {row['document_name']}", # Generic query
                            'entity': prospective_entity,
                            'context': context
                        }
                        memory_entries.append(memory_entry)
                        existing_entities.add(prospective_entity)
                        existing_context_chunk_ids.add(prospective_context_chunk_id)

            if not memory_entries:
                 logger.warning("No entries (dummy or new) to save for episodic memory. Parquet file will not be created/updated.")
                 return str(episodic_memory_parquet_path) # Return path, even if not written, to avoid downstream errors expecting path

            memory_df = pd.DataFrame(memory_entries)
            memory_df.to_parquet(episodic_memory_parquet_path)
            
            logger.info(f"Episodic memory database saved to {episodic_memory_parquet_path} with {len(memory_df)} entries.")
            logger.debug(f"Episodic memory database creation/update completed in {time.time() - start_time:.2f} seconds.")
            
            return str(episodic_memory_parquet_path)
            
        except Exception as e:
            logger.error(f"Error creating/updating episodic memory database: {str(e)}")
            logger.debug(f"Memory database creation error details: {traceback.format_exc()}")
            raise
    
    def create_personality_db(self) -> str:
        """
        Create a personality memory database by loading from 'db/memory/personality_memory_full.json'
        and saving to 'db/memory/personality_memory.parquet'.
        This method specifically handles personality memory, which has a different schema
        than episodic memory and should remain separate.
        
        Personality Memory Schema:
        - mode_id: UUID for the personality mode
        - mode_name: Name of the personality mode
        - personality_type: List of personality types (e.g., ["openness", "conscientiousness"])
        - personality_score: Object with scores (0-100) for each Big Five trait
        - cognitive_style: String describing cognitive approach
        - mbti_type: MBTI personality type (e.g., "INTJ")
        - sentiment_score: Float (-1.0 to 1.0) representing emotional tone
        - mode_description: Text description of the mode
        - activation_contexts: List of contexts where this mode is appropriate
        - activation_triggers: List of trigger objects that activate this mode
            
        Returns:
            str: Path to the saved personality memory database file (personality_memory.parquet)
            
        Raises:
            FileNotFoundError: If personality_memory_full.json is not found.
            ValueError: If the loaded personality traits are invalid or missing required fields.
            RuntimeError: If file operations fail.
        """
        logger.debug("Starting to create personality memory database from JSON file.")
        start_time = time.time()

        input_json_path = self.memory_dir / 'personality_memory_full.json'
        output_parquet_path = self.memory_dir / 'personality_memory.parquet'

        try:
            # Load personality traits from JSON file
            if not input_json_path.exists():
                logger.error(f"Input JSON file not found: {input_json_path}")
                raise FileNotFoundError(f"Input JSON file not found: {input_json_path}")

            with open(input_json_path, 'r', encoding='utf-8') as f:
                personality_traits = json.load(f)
            
            if not isinstance(personality_traits, list):
                logger.error(f"Invalid format in {input_json_path}: Expected a list of traits.")
                raise ValueError(f"Invalid format in {input_json_path}: Expected a list of traits.")

            if not personality_traits:
                logger.warning(f"No personality traits found in {input_json_path}. Output Parquet file will be empty or reflect existing data if append logic is used.")
                # Depending on desired behavior, could raise ValueError or just create an empty/unchanged parquet.
                # For now, proceed to allow handling of existing parquet.
            
            # Check if existing personality DB exists (the output parquet file)
            existing_modes = {}
            if output_parquet_path.exists():
                try:
                    existing_df = pd.read_parquet(output_parquet_path)
                    # Convert existing data to dict for easier handling
                    for _, row in existing_df.iterrows():
                        if 'mode_id' in row and row['mode_id']: # Ensure mode_id is valid before using as key
                            existing_modes[row['mode_id']] = row.to_dict()
                    logger.info(f"Loaded existing personality database from {output_parquet_path} with {len(existing_modes)} entries")
                except Exception as e:
                    logger.warning(f"Could not load existing personality database from {output_parquet_path}: {e}. Treating as new.")
            
            # Standardize and validate personality traits
            validated_traits = []
            required_fields = ['mode_id', 'mode_name', 'personality_type']
            
            # Create lookup dictionaries for existing traits
            existing_mode_ids = set(existing_modes.keys())
            existing_mode_names = {mode['mode_name']: mode_id for mode_id, mode in existing_modes.items() if 'mode_name' in mode}
            
            # Track MBTI types to ensure uniqueness - we want exactly one personality per MBTI type
            existing_mbti_types = {}
            duplicate_mbti_mode_ids = set()
            
            # First pass: identify duplicate MBTI types
            for mode_id, mode in existing_modes.items():
                if 'mbti_type' in mode and mode['mbti_type']:
                    mbti = mode['mbti_type']
                    if mbti not in existing_mbti_types:
                        existing_mbti_types[mbti] = mode_id
                    else:
                        # Mark this as a duplicate MBTI
                        logger.debug(f"Found duplicate MBTI type {mbti} with mode_id {mode_id}")
                        duplicate_mbti_mode_ids.add(mode_id)
            
            # Remove all identified duplicates
            for mode_id in duplicate_mbti_mode_ids:
                if mode_id in existing_modes:
                    logger.debug(f"Removing duplicate mode_id {mode_id} with MBTI {existing_modes[mode_id].get('mbti_type')}")
                    del existing_modes[mode_id]
            
            # Rebuild lookups after cleanup
            existing_mode_ids = set(existing_modes.keys())
            existing_mode_names = {mode['mode_name']: mode_id for mode_id, mode in existing_modes.items() if 'mode_name' in mode}
            
            for trait in personality_traits:
                # Ensure mode_id exists
                if 'mode_id' not in trait or not trait['mode_id']:
                    trait['mode_id'] = self.datautility.generate_uuid()
                
                # Check for duplicates by mode_id
                if trait['mode_id'] in existing_mode_ids:
                    logger.debug(f"Skipping trait with duplicate mode_id: {trait['mode_id']}")
                    continue
                    
                # Check for duplicates by mode_name
                if trait.get('mode_name') and trait['mode_name'] in existing_mode_names:
                    logger.debug(f"Skipping trait with duplicate mode_name: {trait['mode_name']}")
                    continue
                    
                # Check for duplicates by mbti_type
                if trait.get('mbti_type') and trait['mbti_type'] in existing_mbti_types:
                    logger.debug(f"Skipping trait with duplicate mbti_type: {trait['mbti_type']}")
                    continue
                
                # Validate required fields
                missing_fields = [field for field in required_fields if field not in trait]
                if missing_fields:
                    logger.warning(f"Skipping trait due to missing fields: {missing_fields}")
                    continue
                
                # Standardize personality_type to list if not already
                if 'personality_type' in trait and not isinstance(trait['personality_type'], list):
                    trait['personality_type'] = [trait['personality_type']]
                
                # Add default personality_score if missing
                if 'personality_score' not in trait:
                    trait['personality_score'] = {
                        "openness": 50,
                        "conscientiousness": 50,
                        "extraversion": 50,
                        "agreeableness": 50,
                        "neuroticism": 50
                    }
                
                # Add default sentiment_score if missing
                if 'sentiment_score' not in trait:
                    trait['sentiment_score'] = 0.0  # Neutral sentiment
                
                validated_traits.append(trait)
            
            # Combine existing and new entries
            # The `validated_traits` will be populated based on `personality_traits` read from JSON
            all_entries = list(existing_modes.values()) + validated_traits # validated_traits is populated below

            if not all_entries and not personality_traits: # If no existing and no new traits from JSON
                logger.warning(f"No valid personality traits from {input_json_path} and no existing data in {output_parquet_path}. Output will be empty.")
                # Create an empty DataFrame with schema if necessary, or handle as per requirements
                # For now, let it proceed; an empty df.to_parquet() might be fine or error.
                # Let's ensure an empty DataFrame is created if all_entries is empty.
                if not all_entries:
                    df = pd.DataFrame(columns=['mode_id', 'mode_name', 'personality_type', 'personality_score',
                                               'cognitive_style', 'mbti_type', 'sentiment_score',
                                               'mode_description', 'activation_contexts', 'activation_triggers'])
                else:
                    df = pd.DataFrame(all_entries)

            else: # If there are entries to process
                df = pd.DataFrame(all_entries)
            
            # Handle complex data types for Parquet compatibility
            list_columns = ['personality_type', 'activation_contexts', 'activation_triggers']
            dict_columns = ['personality_score']
            
            for col in df.columns:
                # Force standardization of known list columns
                if col in list_columns:
                    logger.debug(f"Standardizing list column {col} for Parquet compatibility")
                    # Convert None to empty list, then all lists to JSON strings
                    df[col] = df[col].apply(lambda x: [] if x is None else x)
                    df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, list) else json.dumps([]) if x is None else json.dumps([str(x)]) if not isinstance(x, list) else x)
                
                # Force standardization of known dict columns
                elif col in dict_columns:
                    logger.debug(f"Standardizing dictionary column {col} for Parquet compatibility")
                    # Convert None to empty dict, then all dicts to JSON strings
                    df[col] = df[col].apply(lambda x: {} if x is None else x)
                    df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else json.dumps({}))
                
                # Detect and handle any other complex types
                elif df[col].dtype == 'object':
                    # Check for lists
                    if df[col].apply(lambda x: isinstance(x, list)).any():
                        logger.debug(f"Converting list column {col} to JSON strings for Parquet compatibility")
                        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
                    # Check for dictionaries
                    elif df[col].apply(lambda x: isinstance(x, dict)).any():
                        logger.debug(f"Converting dictionary column {col} to JSON strings for Parquet compatibility")
                        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)
            
            # Save the personality database
            df.to_parquet(output_parquet_path)
            
            logger.info(f"Personality memory database created/updated with {len(df)} entries and saved to {output_parquet_path}")
            logger.debug(f"Personality memory database creation completed in {time.time() - start_time:.2f} seconds")
            
            return str(output_parquet_path)

        except FileNotFoundError:
            # Already logged, re-raise for calling code to handle
            raise
        except json.JSONDecodeError as je:
            logger.error(f"Error decoding JSON from {input_json_path}: {je}")
            raise RuntimeError(f"Failed to decode JSON from {input_json_path}") from je
        except Exception as e:
            logger.error(f"Error creating personality memory database: {e}")
            logger.debug(f"Personality memory database creation error details: {traceback.format_exc()}")
            raise
    
    def load_db(self, memory_db_file: Optional[str] = None, memory_type: str = 'episodic') -> pd.DataFrame:
        """
        Load a memory database from disk.
        
        Args:
            memory_db_file: Path to the parquet file containing the memory database.
                           If None, will look for the standard file based on memory_type.
            memory_type: Type of memory database to load ('episodic' or 'personality').
                         This determines the default file to load if memory_db_file is None.
            
        Returns:
            DataFrame containing the memory database
            
        Raises:
            FileNotFoundError: If the memory database file doesn't exist
            ValueError: If the file format is not supported or the file is corrupted
        """
        logger.debug(f"Loading {memory_type} memory database from {memory_db_file}")
        start_time = time.time()
        
        try:
            # If no path is provided, use the appropriate default file based on memory_type
            if memory_db_file is None:
                if memory_type.lower() == 'episodic':
                    memory_db_file = self.memory_dir / 'episodic_memory.parquet'
                elif memory_type.lower() == 'personality':
                    memory_db_file = self.memory_dir / 'personality_memory.parquet'
                else:
                    raise ValueError(f"Unsupported memory type: {memory_type}. Must be 'episodic' or 'personality'.")
                    
                logger.debug(f"No file specified, using default {memory_type} memory file: {memory_db_file}")
            else:
                memory_db_file = Path(memory_db_file)
            
            # Check if file exists
            if not os.path.exists(memory_db_file):
                raise FileNotFoundError(f"Memory database not found: {memory_db_file}")
            
            # Load parquet file
            df = pd.read_parquet(memory_db_file)
            
            # If this is a personality memory database, convert JSON strings back to Python objects
            if memory_type.lower() == 'personality':
                # Check if any columns might contain JSON strings
                for col in df.columns:
                    if df[col].dtype == 'object':
                        try:
                            # Try to parse the first non-null value to see if it's a JSON string
                            sample = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
                            if isinstance(sample, str):
                                # Check for list format
                                if sample.startswith('[') and sample.endswith(']'):
                                    logger.debug(f"Converting JSON strings in column {col} back to lists")
                                    df[col] = df[col].apply(lambda x: json.loads(x) if isinstance(x, str) and x.startswith('[') else x)
                                # Check for dictionary format
                                elif sample.startswith('{') and sample.endswith('}'):
                                    logger.debug(f"Converting JSON strings in column {col} back to dictionaries")
                                    df[col] = df[col].apply(lambda x: json.loads(x) if isinstance(x, str) and x.startswith('{') else x)
                        except (ValueError, IndexError, AttributeError, TypeError):
                            # Skip if conversion fails or no data exists
                            pass
            
            # Validate required columns
            required_columns = ['memory_id', 'query', 'entity', 'context']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Required column '{col}' not found in memory database")
            
            logger.info(f"Loaded memory database from {memory_db_file} with {len(df)} entries in {time.time() - start_time:.2f} seconds")
            return df
            
        except Exception as e:
            logger.error(f"Error loading memory database: {str(e)}")
            logger.debug(f"Load error details: {traceback.format_exc()}")
            raise
    

class GraphBuilder:
    """
    Builds graph representations of the knowledge base using NetworkX.
    Creates graph databases that conform to the schema defined in schema_graph_db.json.
    
    The graph database stores structural relationships between text chunks, documents,
    and sections, with references to content stored in the vector database.
    
    Methods:
        create_db: Creates a graph database from a vector database
        save_db: Saves the graph to a file in the db/graph directory
        load_db: Loads a graph from a file in the db/graph directory
        merge_dbs: Merges multiple graph databases into one
        view_db: Generates visual representations of the graphs
    """

    def __init__(self, vectordb_file: Optional[str] = None) -> None:
        """Initialize a GraphBuilder instance.
        
        Args:
            vectordb_file (Optional[str]): Path to the vector database file to use.
                If provided, relative paths are resolved relative to the db/vector directory.
                If None, no database is loaded initially.
        """
        try:
            # Initialize NetworkX for graph operations
            self.nx = nx
            self.datautility = DataUtility()
            
            # Initialize generator and meta-generator for LLM operations
            self.generator = Generator()
            self.metagenerator = MetaGenerator(generator=self.generator)
            self.datautility = DataUtility()  # Use DataUtility instead of AIUtility
            
            # Set up directory structure
            self.db_dir = Path.cwd() / "db"
            self.graph_dir = self.db_dir / "graph"
            self.vector_dir = self.db_dir / "vector"
            
            # Create directories if they don't exist
            self.graph_dir.mkdir(exist_ok=True, parents=True)
            
            # Store the base vectordb file path
            if vectordb_file:
                # Handle both relative and absolute paths
                if os.path.isabs(vectordb_file):
                    self.vectordb_path = Path(vectordb_file)
                else:
                    self.vectordb_path = self.vector_dir / vectordb_file
                
                self.db_name = Path(vectordb_file).stem
                if self.db_name.startswith('v_'):
                    self.db_name = self.db_name[2:]  # Remove 'v_' prefix
                logger.debug(f"GraphBuilder using vector database file: {self.vectordb_path}")
            else:
                self.vectordb_path = None
                self.db_name = None
                logger.debug("GraphBuilder initialized without a base vector database file")
            
            # Initialize graph containers
            self.graph = None  # Standard graph conforming to schema
            self.hypergraph = None  # Hypergraph for advanced queries
            
            # Track creation timestamp for metadata
            self.created_at = datetime.datetime.now().isoformat()
            
            logger.debug("GraphBuilder initialized successfully")
        except ImportError:
            logger.error("NetworkX not found. Please install with: pip install networkx")
            raise

    def create_db(self, vector_db_file: Optional[str] = None, graph_type: str = 'standard') -> nx.Graph:
        """
        Create a graph database from a vector database file.
        
        This method builds a graph representation of the knowledge base that conforms to
        the schema defined in schema_graph_db.json. The process involves the following steps:
        
        1. Determine the source vector database file to use, with fallback mechanisms
        2. Load and validate the vector database content
        3. Create the appropriate graph structure based on the specified type:
           - 'standard': Creates a directed graph with hierarchical relationships
           - 'hypergraph': Creates a hypergraph with additional semantic relationships
        4. Store the graph in the instance and return it
        
        The resulting graph will contain the following node types:
        - Document: Root nodes representing source documents
        - Section: Intermediate nodes representing document sections
        - Chunk: Leaf nodes representing text chunks with embedded content
        
        Relationships between nodes include:
        - CONTAINS: Document → Section → Chunk hierarchy
        - REFERENCES: Cross-references between related nodes
        - SIMILAR: Similarity relationships between chunks
        
        Args:
            vector_db_file: Path to the vector database parquet file. If None, uses the file
                           specified during initialization or finds the most recent one.
            graph_type: Type of graph to create ('standard' or 'hypergraph')
            
        Returns:
            nx.Graph: The created graph database with nodes and relationships
            
        Raises:
            FileNotFoundError: If the vector database file doesn't exist
            ValueError: If the vector database format is not supported or the file is corrupted
            
        Example:
            >>> builder = GraphBuilder()
            >>> graph = builder.create_db('my_vectors.parquet', graph_type='standard')
            >>> print(f"Created graph with {graph.number_of_nodes()} nodes")
        """
        logger.debug(f"Starting to create {graph_type} graph database")
        start_time = time.time()
        
        try:
            # Step 1: Determine the vector database file to use
            # Priority: 1. Explicitly provided file 2. Instance's vectordb_path 3. Most recent file in vector_dir
            if vector_db_file is not None:
                # Handle both relative and absolute paths
                if os.path.isabs(vector_db_file):
                    vector_path = Path(vector_db_file)
                else:
                    vector_path = self.vector_dir / vector_db_file
            elif self.vectordb_path is not None:
                vector_path = self.vectordb_path
            else:
                # Try to find a vector database file
                vector_files = list(self.vector_dir.glob('v_*.parquet'))
                if not vector_files:
                    raise FileNotFoundError("No vector database files found in the db/vector directory")
                # Use the most recently modified file
                vector_path = sorted(vector_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]
                logger.debug(f"Using most recent vector database file: {vector_path}")
            
            # Check if file exists
            if not os.path.exists(vector_path):
                raise FileNotFoundError(f"Vector database not found: {vector_path}")
            
            # Step 2: Load and validate the vector database
            logger.debug(f"Loading vector database from {vector_path}")
            df_vector = pd.read_parquet(vector_path)
            
            # Step 3: Validate the vector database structure
            # Ensure all required columns are present for graph construction
            required_columns = ['document_id', 'chunk_id', 'document_name', 'hierarchy', 'corpus']
            for col in required_columns:
                if col not in df_vector.columns:
                    raise ValueError(f"Required column '{col}' not found in vector database")
            
            # Step 4: Create the appropriate graph based on type
            logger.debug(f"Creating {graph_type} graph structure")
            if graph_type == 'standard':
                # Standard graph with hierarchical relationships
                graph = self._create_standard_graph(df_vector)
                self.graph = graph  # Store reference to the standard graph
            elif graph_type == 'hypergraph':
                # Hypergraph with additional semantic relationships
                graph = self._create_hypergraph(df_vector)
                self.hypergraph = graph  # Store reference to the hypergraph
            else:
                raise ValueError(f"Unknown graph type: {graph_type}")
                
            # Step 5: Store metadata about the graph
            self._store_graph_metadata(graph, graph_type)
            
            # Save the database name for future reference
            self.db_name = Path(vector_path).stem
            if self.db_name.startswith('v_'):
                self.db_name = self.db_name[2:]  # Remove 'v_' prefix
            
            logger.info(f"Created {graph_type} graph database with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges in {time.time() - start_time:.2f} seconds")
            return graph
            
        except Exception as e:
            logger.error(f"Failed to create graph database: {str(e)}")
            logger.debug(f"Graph creation error details: {traceback.format_exc()}")
            raise
    
    def _find_cross_references(self, chunk_content: str, all_chunks: pd.DataFrame) -> list:
        """
        Extract cross-references from chunk content using an open-source language model.
        
        This method analyzes the content of a text chunk to identify references to other chunks
        in the corpus. It uses a language model with a specialized meta prompt to extract
        these references.
        
        Args:
            chunk_content: The text content of the chunk to analyze
            all_chunks: DataFrame containing all chunks in the corpus for reference matching
            
        Returns:
            list: List of chunk_ids that are referenced by this chunk
        """
        try:
            logger.debug("Extracting cross-references using MetaGenerator")
            # Use the metagenerator to apply the meta prompt and call the language model
            try:                
                # Call metagenerator with the custom meta prompt
                # This follows the pattern seen in topologist.py examples
                response = self.metagenerator.get_meta_generation(
                    application="metaworkflow",  # Custom application since we're not using a library prompt
                    category="dbbuilder",  # Category for extraction tasks
                    action="crossreference",  # Specific action
                    prompt_id=100,  # Default prompt ID
                    model="Qwen2.5-1.5B",  # Use a smaller, efficient model
                    temperature=0.7,  # Balanced temperature for creative yet focused extraction
                    max_tokens=500,  # Reasonable length for responses
                    chunk_content=chunk_content,  # Pass the chunk content as a parameter with the key 'chunk_content'
                    return_full_response=False  # We just want the text output
                )
                
                # Parse the response to extract references
                try:
                    if response:
                        references_data = self.aiutility.format_json_response(response)
                        references = references_data.get("references", [])
                    else:
                        references = []
                except (ValueError, TypeError) as je:
                    logger.warning(f"Could not parse JSON from LLM response: {str(je)}")
                    references = []
            except Exception as e:
                logger.warning(f"Error using MetaGenerator: {str(e)}. Using fallback method.")
                references = []
            
            # Match references to actual chunks in the corpus - this part remains mostly unchanged
            referenced_chunk_ids = []
            if references and len(references) > 0:
                # Create a function to score how well a reference matches a chunk
                def match_score(reference, row):
                    # Check various fields for matches
                    score = 0
                    reference = reference.lower()
                    
                    # Check content (most important)
                    if 'content' in row and isinstance(row['content'], str):
                        content = row['content'].lower()
                        if reference in content:
                            score += 10  # Strong match in content
                        
                    # Check document name and section headers
                    if 'document_name' in row and isinstance(row['document_name'], str):
                        doc_name = row['document_name'].lower()
                        if reference in doc_name:
                            score += 5  # Good match in document name
                    
                    # Check section hierarchy
                    if 'hierarchy' in row and isinstance(row['hierarchy'], str):
                        hierarchy = row['hierarchy'].lower()
                        if reference in hierarchy:
                            score += 3  # Match in section hierarchy
                    
                    return score
                
                # For each reference, find the best matching chunks
                for ref in references:
                    if not ref or len(ref.strip()) < 3:  # Skip very short references
                        continue
                        
                    # Calculate match scores for all chunks
                    all_chunks['match_score'] = all_chunks.apply(lambda row: match_score(ref, row), axis=1)
                    
                    # Get the top matches (score > 0 and max 3 per reference)
                    matches = all_chunks[all_chunks['match_score'] > 0].nlargest(3, 'match_score')
                    
                    # Add the chunk IDs to our result list
                    for _, match in matches.iterrows():
                        if match['chunk_id'] not in referenced_chunk_ids:  # Avoid duplicates
                            referenced_chunk_ids.append(match['chunk_id'])
                
                # Remove the temporary column we added
                if 'match_score' in all_chunks.columns:
                    all_chunks.drop('match_score', axis=1, inplace=True)
            
            logger.debug(f"Found {len(referenced_chunk_ids)} cross-references for chunk")
            return referenced_chunk_ids
            
        except Exception as e:
            logger.warning(f"Failed to extract cross-references: {str(e)}")
            logger.debug(f"Cross-reference extraction error details: {traceback.format_exc()}")
            return []
    
    # _find_similar_chunks is implemented above (consolidation of methods)

    def _create_standard_graph(self, df_vector: pd.DataFrame) -> nx.MultiDiGraph:
        """
        Create a standard graph database conforming to schema_graph_db.json.
        
        This internal method builds a directed multigraph with nodes for documents,
        sections, and text chunks, with relationships between them as defined in the schema.
        Implements all required edge types: "CONTAINS", "REFERENCES", and "SIMILAR".
        
        Args:
            df_vector: DataFrame containing vector database entries
            
        Returns:
            nx.MultiDiGraph: The created standard graph
        """
        logger.debug("Creating standard graph database with all required edge types")
        
        # Create a new directed multigraph
        G = self.nx.MultiDiGraph()
        
        # Track created nodes to avoid duplicates
        created_documents = set()
        created_sections = set()
        created_chunks = set()
        chunk_document_map = {}  # Maps chunk_id to document_id for cross-document edges
        
        # First pass: Create all nodes and store mappings
        for _, row in df_vector.iterrows():
            # Create Chunk node with full content
            chunk_id = row['chunk_id']
            document_id = row['document_id']
            chunk_document_map[chunk_id] = document_id
            
            if chunk_id not in created_chunks:
                G.add_node(chunk_id, 
                          node_type='Chunk',
                          chunk_id=chunk_id,
                          document_id=document_id,
                          text=row['corpus'],  # Store actual content
                          reference=row.get('reference', ''),
                          hierarchy=row.get('hierarchy', ''),
                          created_at=self.created_at)
                created_chunks.add(chunk_id)
            
            # Create Document node if it doesn't exist
            if document_id not in created_documents:
                G.add_node(document_id, 
                          node_type='Document',
                          document_id=document_id,
                          document_name=row.get('document_name', ''),
                          created_at=self.created_at)
                created_documents.add(document_id)
            
            # Process hierarchy to create Section nodes
            hierarchy_parts = row['hierarchy'].split(' > ')
            current_level = 1
            parent_section = None
            
            for i, part in enumerate(hierarchy_parts):
                # Generate a consistent section ID based on document and hierarchy path
                section_path = ' > '.join(hierarchy_parts[:i+1])
                section_id = f"section_{document_id}_{hash(section_path) % 10000000}"
                
                if section_id not in created_sections:
                    G.add_node(section_id,
                              node_type='Section',
                              section_id=section_id,
                              section_name=part,
                              level=current_level,
                              parent_document_id=document_id,
                              section_path=section_path,
                              section_order=i,
                              created_at=self.created_at)
                    created_sections.add(section_id)
                    
                    # Connect to document (CONTAINS relationship)
                    if i == 0:  # Top-level section
                        G.add_edge(document_id, section_id, 
                                  edge_type='CONTAINS', 
                                  order=i,
                                  created_at=self.created_at)
                    # Connect to parent section (CONTAINS relationship)
                    elif parent_section:
                        G.add_edge(parent_section, section_id, 
                                  edge_type='CONTAINS', 
                                  order=i,
                                  created_at=self.created_at)
                
                parent_section = section_id
                current_level += 1
            
            # Connect the deepest section to the text chunk (CONTAINS relationship)
            if parent_section:
                G.add_edge(parent_section, chunk_id, 
                          edge_type='CONTAINS', 
                          order=0,  # Only one chunk per section-chunk relationship
                          created_at=self.created_at)
            else:  # Fallback: connect document directly to chunk
                G.add_edge(document_id, chunk_id, 
                          edge_type='CONTAINS', 
                          order=0,
                          created_at=self.created_at)
        
        # Second pass: Create REFERENCES and SIMILAR edges
        for _, row in df_vector.iterrows():
            chunk_id = row['chunk_id']
            document_id = row['document_id']
            
            # 1. Create REFERENCES edges from chunk content
            # Check for 'corpus' field which contains the actual content
            if 'corpus' in row and row['corpus']:
                # Extract cross-references using LLM-based analysis
                referenced_chunks = self._find_cross_references(row['corpus'], df_vector)
                
                # Create REFERENCES edges for each extracted cross-reference
                for ref_chunk_id in referenced_chunks:
                    if ref_chunk_id in created_chunks and ref_chunk_id != chunk_id:
                        ref_document_id = chunk_document_map.get(ref_chunk_id)
                        # Determine if this is a cross-document reference
                        is_cross_document = ref_document_id != document_id
                        
                        G.add_edge(chunk_id, ref_chunk_id, 
                                  edge_type='REFERENCES',
                                  reference_type='cross_reference',
                                  cross_document=is_cross_document,
                                  from_document=document_id,
                                  to_document=ref_document_id,
                                  created_at=self.created_at,
                                  created_by='llm')
            
            # 2. Create SIMILAR edges based on vector similarity
            if 'corpus_vector' in row and isinstance(row['corpus_vector'], (list, np.ndarray)):
                similar_chunks = self._find_similar_chunks(row, df_vector)
                for similar_id, similarity in similar_chunks:
                    if similar_id in created_chunks and similar_id != chunk_id:
                        similar_document_id = chunk_document_map.get(similar_id)
                        # Determine if this is a cross-document similarity
                        is_cross_document = similar_document_id != document_id
                        
                        G.add_edge(chunk_id, similar_id, 
                                  edge_type='SIMILAR',
                                  similarity_score=float(similarity),
                                  similarity_type='semantic',
                                  cross_document=is_cross_document,
                                  from_document=document_id,
                                  to_document=similar_document_id,
                                  embedding_model=row.get('embedding_model', 'unknown'),
                                  threshold=0.7,
                                  created_at=self.created_at)
        
        # Add metadata to the graph
        self._store_graph_metadata(G, 'standard')
        
        # Log statistics about edge types
        edge_type_counts = {}
        cross_doc_counts = {}
        for _, _, data in G.edges(data=True):
            edge_type = data.get('edge_type')
            if edge_type:
                edge_type_counts[edge_type] = edge_type_counts.get(edge_type, 0) + 1
                if data.get('cross_document', False):
                    cross_doc_counts[edge_type] = cross_doc_counts.get(edge_type, 0) + 1
        
        logger.info(f"Edge type statistics: {edge_type_counts}")
        logger.info(f"Cross-document edge statistics: {cross_doc_counts}")
        
        return G

    def _create_hypergraph(self, df_vector: pd.DataFrame) -> nx.Graph:
        """
        Create a hypergraph representation for advanced queries.
        
        This internal method builds a bipartite graph to represent hyperedges connecting
        multiple nodes based on document groups, topic clusters, and hierarchical levels.
        It also creates direct edges for cross-references and similarities between chunks,
        with special handling for cross-document relationships.
        
        Args:
            df_vector: DataFrame containing vector database entries
            
        Returns:
            nx.Graph: Bipartite graph representing the hypergraph with all required relationships
        """
        logger.debug("Creating enhanced hypergraph database with cross-document edges")
        
        # Create a bipartite graph to represent the hypergraph
        H = self.nx.Graph()
        
        # Track hyperedge IDs and created nodes
        next_edge_id = 0
        created_chunks = set()
        chunk_document_map = {}  # Maps chunk_id to document_id for cross-document edges
        
        # First, create all chunk nodes with full content
        for _, row in df_vector.iterrows():
            chunk_id = row['chunk_id']
            document_id = row['document_id']
            chunk_document_map[chunk_id] = document_id
            
            if chunk_id not in created_chunks:
                # Store actual content in the node
                H.add_node(chunk_id, 
                           node_type='Chunk',
                           chunk_id=chunk_id,
                           document_id=document_id,
                           document_name=row.get('document_name', ''),
                           text=row.get('corpus', ''),  # Store actual content
                           reference=row.get('reference', ''),
                           hierarchy=row.get('hierarchy', ''),
                           created_at=self.created_at)
                created_chunks.add(chunk_id)
        
        # Create document nodes and hyperedges
        doc_groups = df_vector.groupby('document_id')
        documents = {}
        
        for doc_id, group in doc_groups:
            # Create document node
            doc_name = group['document_name'].iloc[0] if 'document_name' in group.columns else f"Document {doc_id}"
            documents[doc_id] = {
                'name': doc_name,
                'chunks': list(group['chunk_id'])
            }
            
            # Create document group hyperedge
            edge_id = f"he_doc_{next_edge_id}"
            next_edge_id += 1
            H.add_node(edge_id, 
                       type='hyperedge', 
                       edge_type='document_group',
                       document_id=doc_id,
                       document_name=doc_name,
                       created_at=self.created_at)
            
            # Connect all chunks in this document to the hyperedge
            for chunk_id in documents[doc_id]['chunks']:
                H.add_edge(edge_id, chunk_id, type='CONTAINS')
        
        # Create partition-based hyperedges if partition field exists
        if 'partition' in df_vector.columns:
            partition_groups = df_vector.groupby('partition')
            
            for partition_name, group in partition_groups:
                if len(group) > 1:  # Only create partition groups with multiple chunks
                    edge_id = f"he_partition_{next_edge_id}"
                    next_edge_id += 1
                    
                    H.add_node(edge_id,
                              type='hyperedge',
                              edge_type='partition_group',
                              partition_name=partition_name,
                              created_at=self.created_at)
                    
                    # Connect chunks to partition hyperedge
                    for _, row in group.iterrows():
                        H.add_edge(edge_id, row['chunk_id'], type='BELONGS_TO')
        
        # Create topic cluster hyperedges using corpus_vector
        if 'corpus_vector' in df_vector.columns:
            import uuid
            # Generate clusters using improved clustering with corpus_vector
            clusters = self._cluster_by_embedding(df_vector, vector_field='corpus_vector')
            
            for cluster_idx, cluster_chunks in enumerate(clusters):
                if len(cluster_chunks) > 1:  # Only create groups for actual clusters
                    # Create a hyperedge node for the topic cluster
                    edge_id = f"he_topic_{next_edge_id}"
                    next_edge_id += 1
                    
                    # Generate required properties for TOPIC_GROUP
                    topic_id = str(uuid.uuid4())
                    topic_name = f"Topic Cluster {cluster_idx + 1}"
                    
                    # Extract keywords from chunks in this cluster
                    topic_keywords = self._extract_topic_keywords(cluster_chunks, df_vector)
                    
                    # Calculate coherence score for the cluster
                    coherence_score = self._calculate_cluster_coherence(cluster_chunks, df_vector)
                    
                    # Check if this is a cross-document cluster
                    doc_ids = set(chunk_document_map.get(chunk_id) for chunk_id in cluster_chunks)
                    is_cross_document = len(doc_ids) > 1
                    
                    # Add hyperedge node with topic metadata
                    H.add_node(edge_id, 
                               type='hyperedge', 
                               edge_type='topic_group',
                               topic_id=topic_id,
                               topic_name=topic_name,
                               topic_keywords=topic_keywords,
                               coherence_score=coherence_score,
                               is_cross_document=is_cross_document,
                               document_count=len(doc_ids),
                               algorithm='hdbscan',
                               created_at=self.created_at)
                    
                    # Connect chunks to the topic hyperedge with membership scores
                    for chunk_id in cluster_chunks:
                        if chunk_id in created_chunks:  # Ensure chunk exists
                            # Calculate membership score for this chunk in the cluster
                            membership_score = self._calculate_membership_score(chunk_id, cluster_idx, clusters, df_vector)
                            
                            # Add edge with required TOPIC_GROUP properties
                            H.add_edge(edge_id, chunk_id,
                                       type='TOPIC_GROUP',
                                       topic_id=topic_id,
                                       membership_score=membership_score)
        
        # Create hierarchy level hyperedges
        df_vector['level'] = df_vector['hierarchy'].apply(lambda h: len(h.split(' > ')))
        level_groups = df_vector.groupby('level')
        
        for level, group in level_groups:
            edge_id = f"he_level_{next_edge_id}"
            next_edge_id += 1
            H.add_node(edge_id, 
                       type='hyperedge', 
                       edge_type='hierarchy_level', 
                       level=level,
                       created_at=self.created_at)
            
            for _, row in group.iterrows():
                H.add_edge(edge_id, row['chunk_id'], type='AT_LEVEL')
        
        # Add direct cross-reference relationships between chunks (REFERENCES edge type)
        for _, row in df_vector.iterrows():
            chunk_id = row['chunk_id']
            document_id = row['document_id']
            
            # Extract cross-references from chunk content
            if 'corpus' in row and row['corpus']:
                # Extract cross-references using content analysis
                referenced_chunks = self._find_cross_references(row['corpus'], df_vector)
                
                # Create REFERENCES edges for each extracted cross-reference
                for ref_chunk_id in referenced_chunks:
                    if ref_chunk_id in created_chunks and ref_chunk_id != chunk_id:
                        ref_document_id = chunk_document_map.get(ref_chunk_id)
                        # Determine if this is a cross-document reference
                        is_cross_document = ref_document_id != document_id
                        
                        # Add a direct edge with REFERENCES type
                        H.add_edge(chunk_id, ref_chunk_id, 
                                  edge_type='REFERENCES',
                                  reference_type='cross_reference',
                                  cross_document=is_cross_document,
                                  from_document=document_id,
                                  to_document=ref_document_id,
                                  created_at=self.created_at,
                                  created_by='llm')
        
        # Add direct similarity relationships (SIMILAR edge type)
        for _, row in df_vector.iterrows():
            chunk_id = row['chunk_id']
            document_id = row['document_id']
            
            # Use corpus_vector for similarity if available
            if 'corpus_vector' in row and isinstance(row['corpus_vector'], (list, np.ndarray)):
                similar_chunks = self._find_similar_chunks(row, df_vector)
                for similar_id, similarity in similar_chunks:
                    if similar_id in created_chunks and similar_id != chunk_id:
                        similar_document_id = chunk_document_map.get(similar_id)
                        # Determine if this is a cross-document similarity
                        is_cross_document = similar_document_id != document_id
                        
                        # Add a direct edge with SIMILAR type
                        H.add_edge(chunk_id, similar_id, 
                                  edge_type='SIMILAR',
                                  similarity_score=float(similarity),
                                  similarity_type='semantic',
                                  cross_document=is_cross_document,
                                  from_document=document_id,
                                  to_document=similar_document_id,
                                  embedding_model=row.get('embedding_model', 'unknown'),
                                  created_at=self.created_at)
        
        # Store metadata about the hypergraph
        self._store_graph_metadata(H, 'hypergraph')
        
        # Log statistics about the hypergraph
        edge_type_counts = {}
        cross_doc_counts = {}
        hyperedge_counts = {}
        
        for node, data in H.nodes(data=True):
            if data.get('type') == 'hyperedge':
                edge_type = data.get('edge_type')
                if edge_type:
                    hyperedge_counts[edge_type] = hyperedge_counts.get(edge_type, 0) + 1
        
        for u, v, data in H.edges(data=True):
            edge_type = data.get('edge_type')
            if edge_type:
                edge_type_counts[edge_type] = edge_type_counts.get(edge_type, 0) + 1
                if data.get('cross_document', False):
                    cross_doc_counts[edge_type] = cross_doc_counts.get(edge_type, 0) + 1
        
        logger.info(f"Hypergraph hyperedge counts: {hyperedge_counts}")
        logger.info(f"Hypergraph edge type counts: {edge_type_counts}")
        logger.info(f"Hypergraph cross-document edge counts: {cross_doc_counts}")
        
        return H
        
    def _store_graph_metadata(self, graph: nx.Graph, graph_type: str) -> None:
        """
        Store metadata about the graph database.
        
        This method adds graph-level attributes to store important metadata such as:
        - Creation timestamp
        - Graph type
        - Node and edge counts
        - Database name (if available)
        
        Args:
            graph: The graph database to store metadata for
            graph_type: Type of graph ('standard' or 'hypergraph')
        """
        logger.debug(f"Storing metadata for {graph_type} graph")
        
        # Add metadata as graph attributes
        graph.graph['created_at'] = self.created_at
        graph.graph['graph_type'] = graph_type
        graph.graph['node_count'] = graph.number_of_nodes()
        graph.graph['edge_count'] = graph.number_of_edges()
        
        # Add database name if available
        if hasattr(self, 'db_name') and self.db_name:
            graph.graph['db_name'] = self.db_name
            
        logger.debug(f"Stored metadata for {graph_type} graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
    

    def _find_similar_chunks(self, row: pd.Series, df: pd.DataFrame, threshold: float = 0.7, top_k: int = 10) -> list:
        """
        Find chunks with similar embeddings, prioritizing corpus_vector field.
        
        This unified method handles both corpus_vector and embedding fields,
        with a preference for corpus_vector when available.
        
        Args:
            row: DataFrame row containing the source chunk and its vector
            df: DataFrame containing all chunks
            threshold: Minimum similarity score to consider (default: 0.7)
            top_k: Maximum number of similar chunks to return (default: 10)
            
        Returns:
            List of tuples containing (chunk_id, similarity_score)
        """
        try:
            # Check if corpus_vector is available, otherwise fall back to embedding
            vector_field = 'corpus_vector' if 'corpus_vector' in row and isinstance(row['corpus_vector'], (list, np.ndarray)) else 'embedding'
            
            if vector_field not in row or not isinstance(row[vector_field], (list, np.ndarray)):
                logger.warning(f"No valid {vector_field} found for similarity comparison")
                return []
            
            # Convert to numpy array
            query_vector = np.array(row[vector_field])
            query_vector_norm = np.linalg.norm(query_vector)

            if query_vector_norm == 0:
                logger.warning(f"Query vector for chunk_id '{row['chunk_id']}' has zero norm. Skipping similarity calculation for this chunk.")
                return []
            query_vector = query_vector / query_vector_norm
            
            # Calculate similarities for all chunks with appropriate vectors
            similarities = []
            for _, other_row in df.iterrows():
                if other_row['chunk_id'] == row['chunk_id']:
                    continue  # Skip self
                
                # Use the same vector field as the query
                if vector_field not in other_row or not isinstance(other_row[vector_field], (list, np.ndarray)):
                    continue  # Skip if no matching vector
                
                # Convert to numpy array
                other_vector = np.array(other_row[vector_field])
                other_vector_norm = np.linalg.norm(other_vector)

                if other_vector_norm == 0:
                    logger.warning(f"Comparison vector for chunk_id '{other_row['chunk_id']}' has zero norm. Skipping this comparison.")
                    continue
                other_vector = other_vector / other_vector_norm
                
                # Calculate cosine similarity
                try:
                    similarity = np.dot(query_vector, other_vector)
                    if similarity >= threshold:
                        similarities.append((other_row['chunk_id'], similarity))
                except Exception as e:
                    logger.debug(f"Error calculating similarity: {str(e)}")
                    continue
            
            # Sort by similarity (highest first) and limit to top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
        
        except Exception as e:
            logger.warning(f"Failed to find similar chunks: {str(e)}")
            logger.debug(f"Similarity calculation error details: {traceback.format_exc()}")
            return []

    def _cluster_by_embedding(self, df: pd.DataFrame, n_clusters: int = 10) -> List[List[str]]:
        """Cluster sections by their embeddings using KMeans."""
        from sklearn.cluster import KMeans
        
        if 'embedding' not in df.columns:
            return []
            
        # Stack embeddings into a matrix
        embeddings = np.vstack(df['embedding'].values)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=min(n_clusters, len(df)))
        clusters = kmeans.fit_predict(embeddings)
        
        # Group sections by cluster
        cluster_groups = [[] for _ in range(max(clusters) + 1)]
        for idx, cluster_id in enumerate(clusters):
            cluster_groups[cluster_id].append(df.iloc[idx]['reference'])
            
        return cluster_groups

    def _find_reference_chains(self, df: pd.DataFrame) -> List[List[str]]:
        """Find chains of connected references."""
        chains = []
        visited = set()
        
        def dfs(node: str, current_chain: List[str]):
            visited.add(node)
            current_chain.append(node)
            
            # Get references from this node
            row = df[df['reference'] == node].iloc[0]
            if row.get('reference_additional'):
                refs = row['reference_additional'].split(',')
                for ref in refs:
                    ref = ref.strip()
                    if ref and ref not in visited:
                        dfs(ref, current_chain)
        
        # Start DFS from each unvisited node
        for _, row in df.iterrows():
            if row['reference'] not in visited:
                current_chain = []
                dfs(row['reference'], current_chain)
                if len(current_chain) > 1:  # Only keep chains with multiple nodes
                    chains.append(current_chain)
        
        return chains

    def save_db(self, db_type: str = 'standard', custom_name: str = None) -> str:
        """Save the graph database to a file in the db/graph directory.
        
        Args:
            db_type: Type of graph to save ('standard' or 'hypergraph')
            custom_name: Optional custom name for the graph file
            
        Returns:
            str: Path to the saved graph file
            
        Raises:
            ValueError: If the specified graph type is not built yet
        """
        logger.debug(f"Starting to save {db_type} graph database")
        start_time = time.time()
        
        try:
            # Determine which graph to save
            if db_type == 'standard':
                graph = self.graph
            elif db_type == 'hypergraph':
                graph = self.hypergraph
            else:
                raise ValueError(f"Unknown graph type: {db_type}")
                
            # Check if graph exists
            if graph is None:
                raise ValueError(f"{db_type.capitalize()} graph not built yet")
            
            # Determine filename
            if custom_name:
                filename = f"g_{custom_name}.pkl"
            elif self.db_name:
                filename = f"g_{self.db_name}_{db_type}.pkl"
            else:
                # Generate a timestamp-based name if no db name is available
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"g_{db_type}_{timestamp}.pkl"
            
            # Create full path
            filepath = self.graph_dir / filename
            
            # Save graph using NetworkX's pickle functionality
            with open(filepath, 'wb') as f:
                pickle.dump(graph, f)
                
            logger.info(f"Saved {db_type} graph to {filepath} in {time.time() - start_time:.2f} seconds")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to save {db_type} graph: {str(e)}")
            logger.debug(f"Save error details: {traceback.format_exc()}")
            raise
    
    def load_db(self, graph_file: str = None, db_type: str = 'standard') -> nx.Graph:
        """Load a graph database from a file in the db/graph directory.
        
        Args:
            graph_file: Path to the graph file (.pkl)
            db_type: Type of graph to load ('standard' or 'hypergraph')
            
        Returns:
            nx.Graph: The loaded graph
            
        Raises:
            FileNotFoundError: If the graph file doesn't exist
            ValueError: If the file format is not supported
        """
        logger.debug(f"Starting to load {db_type} graph database")
        start_time = time.time()
        
        try:
            # If no filepath is provided, try to find a graph database file
            if graph_file is None:
                # Look for files matching the pattern g_*_{db_type}.pkl
                graph_files = list(self.graph_dir.glob(f'g_*_{db_type}.pkl'))
                if not graph_files:
                    raise FileNotFoundError(f"No {db_type} graph database files found in the db/graph directory")
                # Use the most recently modified file
                graph_path = sorted(graph_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]
                logger.debug(f"Using most recent {db_type} graph database file: {graph_path}")
            else:
                # Handle both relative and absolute paths
                if os.path.isabs(graph_file):
                    graph_path = Path(graph_file)
                else:
                    graph_path = self.graph_dir / graph_file
            
            # Check if file exists
            if not os.path.exists(graph_path):
                raise FileNotFoundError(f"Graph database not found: {graph_path}")
            
            # Load graph based on file extension
            if graph_path.suffix.lower() == '.pkl':
                with open(graph_path, 'rb') as f:
                    loaded_graph = pickle.load(f)
            else:
                raise ValueError(f"Unsupported file format: {graph_path.suffix}. Only .pkl files are supported.")
            
            # Store the loaded graph in the appropriate attribute
            if db_type == 'standard':
                self.graph = loaded_graph
                # Extract db_name from filename if possible
                filename = graph_path.stem
                if filename.startswith('g_') and '_standard' in filename:
                    self.db_name = filename[2:].replace('_standard', '')
            elif db_type == 'hypergraph':
                self.hypergraph = loaded_graph
                # Extract db_name from filename if possible
                filename = graph_path.stem
                if filename.startswith('g_') and '_hypergraph' in filename:
                    self.db_name = filename[2:].replace('_hypergraph', '')
            else:
                raise ValueError(f"Unknown graph type: {db_type}")
            
            logger.info(f"Loaded {db_type} graph from {graph_path} with {loaded_graph.number_of_nodes()} nodes and {loaded_graph.number_of_edges()} edges in {time.time() - start_time:.2f} seconds")
            return loaded_graph
            
        except Exception as e:
            logger.error(f"Failed to load graph database: {str(e)}")
            logger.debug(f"Load error details: {traceback.format_exc()}")
            raise
    
    def merge_dbs(self, graph_files: List[str], output_name: str = None, db_type: str = 'standard') -> nx.Graph:
        """Merge multiple graph databases into one.
        
        This method combines multiple graph databases, preserving all nodes, edges, 
        and their attributes. It properly handles cross-document edges and ensures 
        all required edge types ("CONTAINS", "REFERENCES", "SIMILAR") are maintained.
        Node content is preserved during the merge process.
        
        Args:
            graph_files: List of paths to graph files to merge
            output_name: Name for the merged graph file (without extension)
            db_type: Type of graphs to merge ('standard' or 'hypergraph')
            
        Returns:
            nx.Graph: The merged graph with all nodes, edges, and relationships
            
        Raises:
            ValueError: If no graph files are provided or graph types are incompatible
            FileNotFoundError: If any of the specified files don't exist
        """
        logger.debug(f"Starting to merge {len(graph_files)} graph databases of type {db_type}")
        start_time = time.time()
        
        if not graph_files:
            raise ValueError("No graph files provided for merging")
            
        try:
            # Initialize merged graph based on type
            if db_type == 'standard':
                merged_graph = self.nx.MultiDiGraph()
            elif db_type == 'hypergraph':
                merged_graph = self.nx.Graph()
            else:
                raise ValueError(f"Unsupported graph type for merging: {db_type}")
            
            # Track document mappings across graphs to handle cross-document edges properly
            document_id_mappings = {}
            chunk_id_mappings = {}
            edge_type_counts = {"CONTAINS": 0, "REFERENCES": 0, "SIMILAR": 0}
            cross_doc_edge_counts = {"REFERENCES": 0, "SIMILAR": 0}
            
            # Process each graph file
            processed_files = 0
            for i, graph_file in enumerate(graph_files):
                logger.debug(f"Processing graph file {i+1}/{len(graph_files)}: {graph_file}")
                
                # Handle both relative and absolute paths
                if os.path.isabs(graph_file):
                    graph_path = Path(graph_file)
                else:
                    graph_path = self.graph_dir / graph_file
                
                # Check if file exists
                if not os.path.exists(graph_path):
                    logger.warning(f"Graph file not found, skipping: {graph_path}")
                    continue
                
                # Load graph from file
                if graph_path.suffix.lower() == '.pkl':
                    with open(graph_path, 'rb') as f:
                        graph = pickle.load(f)
                else:
                    logger.warning(f"Unsupported file format, skipping: {graph_path.suffix}")
                    continue
                
                # Verify graph type
                if (db_type == 'standard' and not isinstance(graph, self.nx.MultiDiGraph)) or \
                   (db_type == 'hypergraph' and not isinstance(graph, self.nx.Graph)):
                    logger.warning(f"Graph type mismatch, skipping: {graph_path}")
                    continue
                
                # Process nodes first to establish mappings
                node_mapping = {}
                graph_doc_mappings = {}
                graph_chunk_mappings = {}
                
                for node, attrs in graph.nodes(data=True):
                    new_attrs = attrs.copy()  # Create a copy to avoid modifying the original
                    
                    if 'node_type' in attrs:
                        if attrs['node_type'] == 'Chunk':
                            # Track original and new chunk IDs
                            original_chunk_id = attrs.get('chunk_id', node)
                            new_chunk_id = f"g{i}_{original_chunk_id}"
                            new_attrs['chunk_id'] = new_chunk_id
                            
                            # Preserve document reference for cross-document edge handling
                            document_id = attrs.get('document_id')
                            if document_id:
                                graph_chunk_mappings[node] = {'doc_id': document_id, 'new_chunk_id': new_chunk_id}
                                chunk_id_mappings[node] = new_chunk_id
                            
                            # Ensure content is preserved
                            if 'text' not in new_attrs and 'corpus' in new_attrs:
                                new_attrs['text'] = new_attrs['corpus']
                            
                            node_mapping[node] = node  # Keep original node ID
                            
                        elif attrs['node_type'] == 'Document':
                            # Track document ID mappings
                            original_doc_id = attrs.get('document_id', node)
                            new_doc_id = f"g{i}_{original_doc_id}"
                            new_attrs['document_id'] = new_doc_id
                            
                            # Store document mapping for cross-document edge handling
                            graph_doc_mappings[original_doc_id] = new_doc_id
                            document_id_mappings[original_doc_id] = new_doc_id
                            
                            node_mapping[node] = node  # Keep original node ID
                            
                        elif attrs['node_type'] == 'Section':
                            # Update section attributes
                            new_attrs['section_id'] = f"g{i}_{attrs.get('section_id', node)}"
                            
                            # Update parent document reference
                            if 'parent_document_id' in new_attrs:
                                original_parent = new_attrs['parent_document_id']
                                new_attrs['parent_document_id'] = f"g{i}_{original_parent}"
                                
                            # Update section path if present
                            if 'section_path' in new_attrs:
                                new_attrs['section_path'] = f"g{i}_{new_attrs['section_path']}"
                                
                            node_mapping[node] = node  # Keep original node ID
                        else:
                            # For other node types, add prefix to node ID
                            node_mapping[node] = f"g{i}_{node}"
                    else:
                        # For nodes without node_type (like hyperedges), add prefix
                        node_mapping[node] = f"g{i}_{node}"
                        
                        # For hyperedges, update topic_id if present
                        if attrs.get('type') == 'hyperedge':
                            if 'topic_id' in new_attrs:
                                new_attrs['topic_id'] = f"g{i}_{new_attrs['topic_id']}"
                            if 'document_id' in new_attrs:
                                new_attrs['document_id'] = f"g{i}_{new_attrs['document_id']}"
                    
                    # Add node to merged graph with updated attributes
                    merged_graph.add_node(node_mapping[node], **new_attrs)
                
                # Process edges with proper handling of cross-document relationships
                for u, v, key, attrs in graph.edges(data=True, keys=True):
                    new_attrs = attrs.copy()  # Create a copy to avoid modifying the original
                    
                    # Handle edge type-specific processing
                    edge_type = attrs.get('edge_type')
                    if edge_type:
                        # Track edge type statistics
                        if edge_type in edge_type_counts:
                            edge_type_counts[edge_type] += 1
                        
                        # Update document references for cross-document edges
                        if edge_type in ['REFERENCES', 'SIMILAR']:
                            # Update from_document and to_document attributes
                            if 'from_document' in new_attrs:
                                original_from = new_attrs['from_document']
                                new_attrs['from_document'] = graph_doc_mappings.get(original_from, f"g{i}_{original_from}")
                            
                            if 'to_document' in new_attrs:
                                original_to = new_attrs['to_document']
                                new_attrs['to_document'] = graph_doc_mappings.get(original_to, f"g{i}_{original_to}")
                            
                            # Update cross_document flag
                            if new_attrs.get('cross_document', False):
                                cross_doc_edge_counts[edge_type] = cross_doc_edge_counts.get(edge_type, 0) + 1
                    
                    # Add edge to merged graph with mapped nodes and updated attributes
                    if db_type == 'standard':
                        merged_graph.add_edge(node_mapping[u], node_mapping[v], key, **new_attrs)
                    else:
                        merged_graph.add_edge(node_mapping[u], node_mapping[v], **new_attrs)
                
                processed_files += 1
                logger.debug(f"Merged graph {i+1}: added {len(node_mapping)} nodes and {graph.number_of_edges()} edges")
            
            if processed_files == 0:
                raise ValueError("No valid graph files were processed")
            
            # Create cross-database edges connecting related content across original databases
            self._create_cross_database_edges(merged_graph, db_type, document_id_mappings, chunk_id_mappings)
            
            # Generate output name if not provided
            if not output_name:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_name = f"merged_{db_type}_{timestamp}"
            
            # Remove .pkl extension if included
            if output_name.endswith('.pkl'):
                output_name = output_name[:-4]
            
            # Save the merged graph
            output_file = self.graph_dir / f"g_{output_name}.pkl"
            with open(output_file, 'wb') as f:
                pickle.dump(merged_graph, f)
            
            # Store the merged graph in the appropriate attribute
            if db_type == 'standard':
                self.graph = merged_graph
            elif db_type == 'hypergraph':
                self.hypergraph = merged_graph
            
            # Update db_name to reflect merged status
            self.db_name = output_name
            
            # Log edge type statistics
            logger.info(f"Edge type statistics: {edge_type_counts}")
            logger.info(f"Cross-document edge statistics: {cross_doc_edge_counts}")
            logger.info(f"Merged {processed_files} graphs into {output_file} with {merged_graph.number_of_nodes()} nodes and {merged_graph.number_of_edges()} edges in {time.time() - start_time:.2f} seconds")
            
            return merged_graph
            
        except Exception as e:
            logger.error(f"Failed to merge graph databases: {str(e)}")
            logger.debug(f"Merge error details: {traceback.format_exc()}")
            raise
    
    def _create_cross_database_edges(self, merged_graph, db_type, document_id_mappings, chunk_id_mappings):
        """Create edges between related content across the original databases.
        
        This method analyzes node content and creates new edges for cross-database
        relationships that weren't captured in the individual graphs.
        
        Args:
            merged_graph: The merged graph being constructed
            db_type: Type of graph ('standard' or 'hypergraph')
            document_id_mappings: Mapping of original to new document IDs
            chunk_id_mappings: Mapping of original to new chunk IDs
            
        Returns:
            None (modifies merged_graph in place)
        """
        logger.debug("Creating cross-database edges between related content")
        cross_db_similar_edges = 0
        cross_db_reference_edges = 0
        
        # Only process if we have sufficient nodes
        if merged_graph.number_of_nodes() < 5:
            logger.debug("Not enough nodes for meaningful cross-database edge creation")
            return
        
        try:
            # Find all chunk nodes to analyze for cross-database relationships
            chunk_nodes = []
            chunk_texts = {}
            
            for node, attrs in merged_graph.nodes(data=True):
                if attrs.get('node_type') == 'Chunk':
                    chunk_nodes.append(node)
                    # Collect text content for similarity analysis
                    text = attrs.get('text', '')
                    if text:
                        chunk_texts[node] = text
            
            # Skip if we don't have enough chunks with text
            if len(chunk_texts) < 2:
                logger.debug("Not enough chunks with text content for cross-database edge creation")
                return
            
            # Create a document prefix set to identify cross-database edges
            # Example: {'g0_', 'g1_', 'g2_'}
            doc_prefixes = set()
            for doc_id in document_id_mappings.values():
                if '_' in doc_id:
                    prefix = doc_id.split('_')[0] + '_'
                    doc_prefixes.add(prefix)
            
            # For graphs with many nodes, limit the number of comparisons
            max_comparisons = 1000  # Limit to prevent excessive processing
            if len(chunk_nodes) > 100:
                chunk_nodes = random.sample(chunk_nodes, 100)
            
            # Create similarity edges between chunks from different original databases
            comparisons = 0
            for i, node1 in enumerate(chunk_nodes):
                if comparisons >= max_comparisons:
                    break
                    
                attrs1 = merged_graph.nodes[node1]
                text1 = chunk_texts.get(node1, '')
                if not text1 or len(text1) < 20:  # Skip chunks with minimal content
                    continue
                    
                doc_id1 = attrs1.get('document_id', '')
                prefix1 = doc_id1.split('_')[0] + '_' if '_' in doc_id1 else ''
                
                for j in range(i+1, len(chunk_nodes)):
                    node2 = chunk_nodes[j]
                    attrs2 = merged_graph.nodes[node2]
                    text2 = chunk_texts.get(node2, '')
                    
                    if not text2 or len(text2) < 20:  # Skip chunks with minimal content
                        continue
                        
                    doc_id2 = attrs2.get('document_id', '')
                    prefix2 = doc_id2.split('_')[0] + '_' if '_' in doc_id2 else ''
                    
                    # Only create edges between chunks from different original databases
                    if prefix1 and prefix2 and prefix1 != prefix2:
                        comparisons += 1
                        
                        # Check for content similarity
                        # Simple approach: check for shared significant words or phrases
                        # In a real implementation, would use vector similarity or LLM analysis
                        if self._check_content_similarity(text1, text2):
                            # Create SIMILAR edge
                            edge_attrs = {
                                'edge_type': 'SIMILAR',
                                'similarity_type': 'cross_database',
                                'similarity_score': 0.75,  # Default score
                                'cross_document': True,
                                'from_document': doc_id1,
                                'to_document': doc_id2,
                                'created_at': self.created_at
                            }
                            
                            if db_type == 'standard':
                                merged_graph.add_edge(node1, node2, **edge_attrs)
                            else:
                                merged_graph.add_edge(node1, node2, **edge_attrs)
                                
                            cross_db_similar_edges += 1
                        
                        # Check for cross-references
                        if self._check_cross_reference(text1, text2):
                            # Create REFERENCES edge
                            edge_attrs = {
                                'edge_type': 'REFERENCES',
                                'reference_type': 'cross_database',
                                'cross_document': True,
                                'from_document': doc_id1,
                                'to_document': doc_id2,
                                'created_at': self.created_at,
                                'created_by': 'merge_process'
                            }
                            
                            if db_type == 'standard':
                                merged_graph.add_edge(node1, node2, **edge_attrs)
                            else:
                                merged_graph.add_edge(node1, node2, **edge_attrs)
                                
                            cross_db_reference_edges += 1
            
            logger.info(f"Created {cross_db_similar_edges} cross-database SIMILAR edges")
            logger.info(f"Created {cross_db_reference_edges} cross-database REFERENCES edges")
            
        except Exception as e:
            logger.warning(f"Error during cross-database edge creation: {str(e)}")
            logger.debug(traceback.format_exc())
    
    def _check_content_similarity(self, text1, text2):
        """Check if two text chunks are semantically similar.
        
        This is a simplified implementation. In a real-world scenario, this would use
        vector similarity calculations or more sophisticated text analysis.
        
        Args:
            text1: First text chunk
            text2: Second text chunk
            
        Returns:
            bool: True if the texts are similar, False otherwise
        """
        # Extract words (removing common stop words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
                      'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'that', 'this'}
        
        # Extract significant words (longer than 4 chars and not in stop words)
        words1 = {word.lower() for word in re.findall(r'\b\w+\b', text1) 
                 if len(word) > 4 and word.lower() not in stop_words}
        words2 = {word.lower() for word in re.findall(r'\b\w+\b', text2) 
                 if len(word) > 4 and word.lower() not in stop_words}
        
        # Calculate Jaccard similarity
        if not words1 or not words2:
            return False
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union)
        return similarity > 0.3  # Arbitrary threshold
    
    def _check_cross_reference(self, text1, text2):
        """Check if one text likely references the other.
        
        This is a simplified implementation. In a real-world scenario, would use
        more sophisticated methods like named entity recognition.
        
        Args:
            text1: First text chunk
            text2: Second text chunk
            
        Returns:
            bool: True if a reference is detected, False otherwise
        """
        # Extract potential reference patterns (simplified approach)
        doc_patterns = [r'(?i)\b(see|refer to|according to|as stated in|as mentioned in)\b']
        
        # Check if one text contains a reference-like pattern
        for pattern in doc_patterns:
            if re.search(pattern, text1) or re.search(pattern, text2):
                return True
                
        return False
    
    def view_db(self, db_type: str = 'standard', output_path: str = None, figsize: tuple = (12, 8), seed: int = 42) -> str:
        """Generate a visual representation of the graph.
        
        Args:
            graph_type: Type of graph to visualize ('standard' or 'hypergraph')
            output_path: Path to save the visualization image. If None, will create
                         a graph_visualizations directory in the current path.
            figsize: Figure size as (width, height) in inches
            seed: Random seed for layout reproducibility
            
        Returns:
            Path to the saved visualization image
            
        Raises:
            ImportError: If matplotlib is not installed
            ValueError: If graph_type is invalid or graph has not been built
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logger.error("Matplotlib not installed. Please install with: pip install matplotlib")
            raise ImportError("Matplotlib is required for visualization. Install with: pip install matplotlib")
            
        # Validate graph type
        if graph_type not in ['standard', 'hypergraph']:
            raise ValueError("graph_type must be 'standard' or 'hypergraph'")
            
        # Build the graph if it hasn't been built yet
        if graph_type == 'standard':
            if self.graph is None:
                logger.info("Building standard graph first...")
                self.build_standard_graph()
            graph = self.graph
            if graph is None or len(graph.nodes) == 0:
                raise ValueError("Standard graph has not been built or has no nodes")
        else:  # hypergraph
            if self.hypergraph is None:
                logger.info("Building hypergraph first...")
                self.build_hypergraph()
            graph = self.hypergraph
            if graph is None or len(graph.nodes) == 0:
                raise ValueError("Hypergraph has not been built or has no nodes")
                
        # Set up output directory
        if output_path is None:
            viz_dir = os.path.join(os.getcwd(), "graph_visualizations")
            os.makedirs(viz_dir, exist_ok=True)
            output_path = os.path.join(viz_dir, f"{graph_type}_graph.png")
            
        # Create visualization
        logger.info(f"Generating {graph_type} graph visualization with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
        plt.figure(figsize=figsize)
        pos = self.nx.spring_layout(graph, seed=seed)  # Position nodes using spring layout
        
        try:
            if graph_type == 'standard':
                # Categorize nodes by type for standard graph
                content_nodes = [n for n in graph.nodes if str(n).startswith('content_')]
                reference_nodes = [n for n in graph.nodes if isinstance(n, str) and 'Para' in str(n)]
                hierarchy_nodes = [n for n in graph.nodes if n not in content_nodes and n not in reference_nodes]
                
                # Draw nodes with different colors
                self.nx.draw_networkx_nodes(graph, pos, nodelist=content_nodes, node_color='lightblue', 
                                      node_size=500, alpha=0.8, label="Content")
                self.nx.draw_networkx_nodes(graph, pos, nodelist=reference_nodes, node_color='lightgreen', 
                                      node_size=500, alpha=0.8, label="References")
                self.nx.draw_networkx_nodes(graph, pos, nodelist=hierarchy_nodes, node_color='salmon', 
                                      node_size=700, alpha=0.8, label="Hierarchy")
                
                plt.title("Standard Graph Structure")
                
            else:  # hypergraph
                # Categorize nodes by type for hypergraph
                he_nodes = [n for n in graph.nodes if isinstance(n, str) and str(n).startswith('he_')]
                reference_nodes = [n for n in graph.nodes if isinstance(n, str) and 'Para' in str(n)]
                other_nodes = [n for n in graph.nodes if n not in he_nodes and n not in reference_nodes]
                
                # Draw nodes with different colors
                self.nx.draw_networkx_nodes(graph, pos, nodelist=he_nodes, node_color='purple', 
                                      node_size=700, alpha=0.8, label="Hyperedges")
                self.nx.draw_networkx_nodes(graph, pos, nodelist=reference_nodes, node_color='lightgreen', 
                                      node_size=500, alpha=0.8, label="References")
                self.nx.draw_networkx_nodes(graph, pos, nodelist=other_nodes, node_color='orange', 
                                      node_size=500, alpha=0.8, label="Content")
                
                plt.title("Hypergraph Structure")
            
            # Draw edges and labels for both graph types
            self.nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5)
            
            # Draw labels with smaller font size to avoid overlap
            self.nx.draw_networkx_labels(graph, pos, font_size=8)
            
            # Add legend and finalize
            plt.legend(loc='upper right', scatterpoints=1)
            plt.axis('off')  # Turn off axis
            plt.tight_layout()
            
            # Save the visualization
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Graph visualization saved to: {output_path}")
            plt.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating graph visualization: {str(e)}")
            plt.close()
            raise


@dataclass
class ProcessingResult:
    """Results from processing a directory of documents."""
    vector_db_paths: List[str]
    graph_db_paths: List[str]
    memory_db_paths: List[str]
    partition_merged_paths: Dict[str, Dict[str, str]]
    statistics: Dict[str, Any]
    status: str = "completed"
    message: str = ""

@dataclass
class BatchResult:
    """Results from processing a batch of documents."""
    vector_db_paths: List[str]
    graph_db_paths: List[str]
    memory_db_paths: List[str]
    statistics: Dict[str, Any]

@dataclass
class ProcessingStatistics:
    """Centralized statistics collection."""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    total_documents: int = 0
    files_processed: int = 0
    pdfs_converted: int = 0
    chunks_created: int = 0
    vector_db_size: int = 0
    graph_nodes: int = 0
    graph_edges: int = 0
    episodic_memory_entries_created: int = 0
    personality_memory_entries_created: int = 0
    processing_time: float = 0
    
    def update(self, stat_name: str, value: Any, increment: bool = False):
        """
        Update a statistic by name.
        
        Args:
            stat_name: The name of the statistic to update
            value: The value to set or increment by
            increment: If True, add the value to the existing statistic; if False, replace the existing value
        """
        if hasattr(self, stat_name):
            if increment:
                current_value = getattr(self, stat_name)
                if isinstance(current_value, (int, float)) and isinstance(value, (int, float)):
                    setattr(self, stat_name, current_value + value)
                else:
                    logger.warning(f"Cannot increment non-numeric statistic {stat_name}")
            else:
                setattr(self, stat_name, value)
        else:
            logger.warning(f"Unknown statistic: {stat_name}")
    
    def finalize(self):
        """Calculate final statistics when processing is complete."""
        self.end_time = time.time()
        self.processing_time = self.end_time - self.start_time
        logger.info(f"Processing completed in {self.processing_time:.2f} seconds")
        
    def get_all(self) -> Dict[str, Any]:
        """Return all statistics as a dictionary."""
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_documents": self.total_documents,
            "files_processed": self.files_processed,
            "pdfs_converted": self.pdfs_converted,
            "chunks_created": self.chunks_created,
            "vector_db_size": self.vector_db_size,
            "graph_nodes": self.graph_nodes,
            "graph_edges": self.graph_edges,
            "episodic_memory_entries_created": self.episodic_memory_entries_created,
            "personality_memory_entries_created": self.personality_memory_entries_created,
            "processing_time": self.processing_time
        }


class PartitionManager:
    """Manages document partitions for database merging and organization."""
    
    def __init__(self):
        """Initialize the partition manager."""
        self.logger = get_logger(__name__)
    
    def extract_partition(self, file_path: Union[str, Path]) -> str:
        """Extract partition information from a file path.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Partition name (e.g., 'au-standard', 'eu-guidance')
        """
        path_str = str(file_path)
        
        # Determine document type from path
        if 'standard' in path_str:
            doc_type = 'standard'
        elif 'guidance' in path_str:
            doc_type = 'guidance'
        elif 'opinion' in path_str:
            doc_type = 'opinion'
        else:
            doc_type = 'general'

        # Determine region from path
        if '/au/' in path_str or '\\au\\' in path_str:
            region = 'au'
        elif '/eu/' in path_str or '\\eu\\' in path_str:
            region = 'eu'
        elif '/bs/' in path_str or '\\bs\\' in path_str:
            region = 'bs'
        else:
            region = 'ge'
        
        return f"{region}-{doc_type}"
    
    def extract_partition_from_db(self, db_path: Union[str, Path]) -> str:
        """Extract partition information from a database file.
        
        Args:
            db_path: Path to the database file
            
        Returns:
            Partition name
        """
        try:
            # Try to load the database and extract partition information
            if str(db_path).endswith('.parquet'):
                df = pd.read_parquet(db_path)
                if 'partition' in df.columns and not df['partition'].empty:
                    return df['partition'].iloc[0]
            
            # Fallback to path-based extraction
            file_path = Path(db_path)
            if 'APS' in file_path.stem or 'APG' in file_path.stem:
                return 'policy'
            elif 'CRE' in file_path.stem:
                return 'basel'
            elif re.search(r'risk.*opinion', file_path.stem, re.IGNORECASE):
                return 'opinion'
            else:
                return 'general'
        except Exception as e:
            self.logger.warning(f"Error extracting partition from {db_path}: {e}")
            return 'general'
    
    def group_by_partition(self, db_paths: List[str]) -> Dict[str, List[str]]:
        """Group database paths by partition.
        
        Args:
            db_paths: List of database file paths
            
        Returns:
            Dictionary mapping partition names to lists of file paths
        """
        partition_to_paths = {}
        
        for db_path in db_paths:
            partition = self.extract_partition_from_db(db_path)
            if partition not in partition_to_paths:
                partition_to_paths[partition] = []
            partition_to_paths[partition].append(db_path)
        
        return partition_to_paths
    
    def get_partition_name_from_metadata(self, region: str, doc_type: str) -> str:
        """Generate a partition name from region and document type.
        
        Args:
            region: Region code ('au', 'eu', 'bs', etc.)
            doc_type: Document type ('standard', 'guidance', 'opinion', etc.)
            
        Returns:
            Partition name
        """
        if not region:
            region = 'ge'
        if not doc_type:
            doc_type = 'general'
        
        return f"{region}-{doc_type}"


class HierarchyManager:
    """Manages document hierarchies for structured chunking."""
    
    def __init__(self, hierarchy_dir: Optional[Union[str, Path]] = None, 
                 hierarchy_mapping: Optional[Dict[str, Any]] = None, 
                 default_hierarchy_file: Optional[str] = None):
        """Initialize the hierarchy manager.
        
        Args:
            hierarchy_dir: Directory containing hierarchy CSV files
            hierarchy_mapping: Mapping of region/doc_type to hierarchy files
            default_hierarchy_file: Default hierarchy CSV file name
        """
        self.logger = get_logger(__name__)
        self.hierarchy_mapping = hierarchy_mapping if hierarchy_mapping is not None else {}
        self.default_hierarchy_file_name = default_hierarchy_file
        self.hierarchy_dir = Path(hierarchy_dir) if hierarchy_dir else Path.cwd() / "db" / "raw" / "hierarchy" # Adjusted default
        
        self.logger.info(f"HierarchyManager initialized with hierarchy_dir: {self.hierarchy_dir}")
        self.logger.debug(f"HierarchyManager received hierarchy_mapping: {self.hierarchy_mapping}")
        self.logger.info(f"HierarchyManager default_hierarchy_file_name set to: {self.default_hierarchy_file_name}")

        if not self.hierarchy_dir.exists():
            self.logger.warning(f"Hierarchy directory {self.hierarchy_dir} does not exist. Creating it.")
            try:
                self.hierarchy_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.logger.error(f"Failed to create hierarchy directory {self.hierarchy_dir}: {e}")
    
    def find_hierarchy_for_document(self, doc_info: Union[Dict[str, Any], DocumentInfo]) -> Optional[pd.DataFrame]:
        """Find an appropriate hierarchy CSV file for a document.

        Args:
            doc_info: Document information (dict or DocumentInfo)

        Returns:
            DataFrame with hierarchy data, or None if not found
        """
        self.logger.debug(f"Attempting to find hierarchy for doc_info: {doc_info}")

        if not self.hierarchy_dir.exists():
            self.logger.error(f"Hierarchy directory {self.hierarchy_dir} does not exist. Cannot find hierarchies.")
            return None

        if isinstance(doc_info, dict):
            region = doc_info.get('region', '').lower()
            doc_type = doc_info.get('doc_type', '').lower()
            file_path = doc_info.get('file_path', '')
            file_stem = Path(file_path).stem if file_path else ''
        else:  # DocumentInfo object
            region = doc_info.region.lower()
            doc_type = doc_info.doc_type.lower()
            file_stem = doc_info.base_name
        
        self.logger.info(f"Looking for hierarchy for document: region='{region}', doc_type='{doc_type}', stem='{file_stem}'")

        # 1. Try to match using the provided hierarchy_mapping (new structure)
        if self.hierarchy_mapping and region and doc_type:
            self.logger.debug(f"Using hierarchy_mapping: {self.hierarchy_mapping}")
            region_mappings = self.hierarchy_mapping.get(region)
            if region_mappings:
                self.logger.debug(f"Found mappings for region '{region}': {region_mappings}")
                for mapping_item in region_mappings:
                    if isinstance(mapping_item, dict) and doc_type in mapping_item:
                        mapped_filename = mapping_item[doc_type]
                        self.logger.info(f"Found mapped_filename '{mapped_filename}' for region '{region}' and doc_type '{doc_type}'")
                        mapped_file_path = self.hierarchy_dir / mapped_filename
                        if mapped_file_path.exists():
                            try:
                                df = pd.read_csv(mapped_file_path)
                                self.logger.info(f"Successfully loaded mapped hierarchy file: '{mapped_file_path}'")
                                return df
                            except Exception as e:
                                self.logger.warning(f"Error reading mapped hierarchy file '{mapped_file_path}': {e}")
                        else:
                            self.logger.warning(f"Mapped hierarchy file '{mapped_file_path}' not found at expected location.")
                        break # Found doc_type, no need to check further in this region's list
                else: # Loop finished, doc_type not found in region_mappings
                    self.logger.debug(f"Doc_type '{doc_type}' not found in any mapping_item for region '{region}'.")
            else:
                self.logger.debug(f"Region '{region}' not found as a key in hierarchy_mapping.")
        elif not self.hierarchy_mapping:
            self.logger.debug("Hierarchy mapping configuration (self.hierarchy_mapping) is not available or is empty.")
        elif not region:
            self.logger.debug(f"Region is missing for {file_stem}, cannot use mapping.")
        elif not doc_type:
            self.logger.debug(f"Doc_type is missing for {file_stem}, cannot use mapping.")

        # 2. Try to use the configured default_hierarchy_file_name
        if self.default_hierarchy_file_name:
            self.logger.info(f"Mapping lookup failed or did not yield a readable file. Attempting to use default hierarchy: {self.default_hierarchy_file_name}")
            default_file_path = self.hierarchy_dir / self.default_hierarchy_file_name
            if default_file_path.exists():
                try:
                    df = pd.read_csv(default_file_path)
                    self.logger.info(f"Successfully loaded default hierarchy file: '{default_file_path}'")
                    return df
                except Exception as e:
                    self.logger.warning(f"Error reading configured default hierarchy file '{default_file_path}': {e}")
            else:
                self.logger.warning(f"Configured default hierarchy file '{default_file_path}' not found.")
        else:
            self.logger.debug("No default_hierarchy_file_name configured.")

        # 3. Fallback to glob-based search if mapping and default file fail
        self.logger.info(f"Mapping and default file approaches failed. Proceeding with glob-based hierarchy search for document (stem: {file_stem}).")
        hierarchy_files = list(self.hierarchy_dir.glob("*.csv"))
        if not hierarchy_files:
            self.logger.warning(f"No hierarchy CSV files found in {self.hierarchy_dir} for glob-based fallback.")
            return None
        
        # Fallback strategies (simplified from original, as primary should be mapping/default)
        # Try to match by filename pattern in the stem (e.g., APS001_Hierarchy.csv for APS001.md)
        # More specific patterns like region/doc_type in filename could be added if necessary
        for h_file in hierarchy_files:
            h_stem_lower = h_file.stem.lower()
            # Attempt a more direct match: <file_stem>_hierarchy.csv or <file_stem>.csv
            if h_stem_lower == f"{file_stem.lower()}_hierarchy" or h_stem_lower == file_stem.lower():
                try:
                    df = pd.read_csv(h_file)
                    self.logger.info(f"Found matching hierarchy file by specific stem pattern: {h_file}")
                    return df
                except Exception as e:
                    self.logger.warning(f"Error reading hierarchy file {h_file} during glob fallback: {e}")
        
        # If no specific match, and if there's only ONE hierarchy file, use it as a last resort default.
        if len(hierarchy_files) == 1:
            self.logger.warning(f"No specific match found via globbing. Only one CSV found: {hierarchy_files[0]}. Using it as a last resort.")
            try:
                df = pd.read_csv(hierarchy_files[0])
                return df
            except Exception as e:
                self.logger.warning(f"Error reading the single available hierarchy file {hierarchy_files[0]}: {e}")
        elif hierarchy_files: # More than one, and no specific match
             self.logger.warning(f"Multiple CSVs found in {self.hierarchy_dir}, but no specific glob match for {file_stem}. Cannot determine fallback.")

        self.logger.error(f"No suitable hierarchy file found for document: region='{region}', doc_type='{doc_type}', stem='{file_stem}' after all attempts.")
        return None


class PipelineCoordinator:
    """Centralized coordinator for the document discovery and processing pipeline.
    
    This class coordinates all database operations (vector, graph, memory), document discovery,
    batch processing, and result management. It provides a centralized interface for the
    knowledge service to interact with all database builders and utilities.
    
    The coordinator implements the following responsibilities:
    1. Document discovery with file priority rules (.md over .pdf)
    2. Batch processing of documents to create vector, graph, and memory databases
    3. Database merging by partition (region and document type)
    4. Statistics tracking and result management
    
    This design centralizes coordination logic that was previously scattered across
    the KnowledgeService class, making the codebase more maintainable and modular.
    """
    
    def __init__(self, config: Dict[str, Any], hierarchy_mapping: Dict[str, Any], default_hierarchy_file: Optional[str]):
        """Initialize the PipelineCoordinator with necessary components.
        
        Args:
            config: Configuration dictionary for the pipeline
            hierarchy_mapping: Mapping of region/doc_type to hierarchy files
            default_hierarchy_file: Default hierarchy file name
        """
        logger.info("Initializing PipelineCoordinator")
        logger.debug(f"PipelineCoordinator received hierarchy_mapping: {hierarchy_mapping}")
        logger.debug(f"PipelineCoordinator received default_hierarchy_file: {default_hierarchy_file}")
        start_time = time.time()
        
        try:
            self.config = config
            
            # Initialize utilities
            self.data_utility = DataUtility()
            
            # Initialize processing components
            self.text_parser = TextParser()
            self.text_chunker = TextChunker()
            self.generator = Generator()
            
            # Initialize database builders
            self.vector_builder = VectorBuilder(
                parser=self.text_parser,
                chunker=self.text_chunker,
                generator=self.generator
            )
            
            # Initialize graph builder
            self.graph_builder = GraphBuilder()
            
            # Initialize memory builder
            self.memory_builder = MemoryBuilder()
            
            # Initialize document discoverer
            self.document_discoverer = DocumentDiscoverer()
            
            # Initialize statistics
            self.statistics = ProcessingStatistics()
            
            # Set default paths
            self.db_dir = Path(config.get('db_dir', Path.cwd() / "db"))
            self.raw_dir = Path(config.get('raw_dir', self.db_dir / "raw"))
            self.vector_dir = Path(config.get('vector_dir', self.db_dir / "vector"))
            self.graph_dir = Path(config.get('graph_dir', self.db_dir / "graph"))
            self.memory_dir = Path(config.get('memory_dir', self.db_dir / "memory"))
            self.hierarchy_dir = Path(config.get('hierarchy_dir', self.raw_dir / "hierarchy"))

            # Store hierarchy mapping and initialize manager
            self.hierarchy_manager = HierarchyManager(
                hierarchy_dir=self.hierarchy_dir, 
                hierarchy_mapping=hierarchy_mapping,
                default_hierarchy_file=default_hierarchy_file
            )
            
            # Sample personality traits for basic population (from config or default)
            self.personality_traits = config.get('personality_traits', [])
            
            # Get personality memory path from config or use default
            personality_path = config.get('system', {}).get('paths', {}).get('personality_memory')
            self.personality_memory_path = Path(personality_path) if personality_path else None
            
            logger.info(f"PipelineCoordinator initialized in {time.time() - start_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"PipelineCoordinator initialization failed: {str(e)}")
            logger.debug(f"Initialization error details: {traceback.format_exc()}")
            raise
    
    def process_directory(self, raw_dir: Path, output_dirs: Dict[str, Path], 
                         processing_options: Dict[str, Any]) -> ProcessingResult:
        """Main pipeline coordination method - processes all documents in a directory.
        
        This method orchestrates the complete pipeline:
        1. Discover documents using DocumentDiscoverer
        2. Process documents in batches
        3. Merge databases by partition
        4. Create personality memory from config
        5. Collect final statistics
        
        Args:
            raw_dir: Directory containing raw documents
            output_dirs: Dictionary mapping output types ('vector', 'graph', 'memory') to directories
            processing_options: Dictionary of processing options including:
                - process_subdirs: Whether to process subdirectories
                - chunking_method: Method for text chunking
                - embedding_model: Model to use for embeddings
                - pdf_conversion_method: Method for PDF conversion
                - force_rebuild: Whether to force rebuilding existing databases
                - merge_results: Whether to merge individual databases
                - memory_entries_per_vector: Number of memory entries to create per vector database
        
        Returns:
            ProcessingResult object containing all processing results and statistics
        """
        logger.info("Starting document processing pipeline")
        overall_start_time = time.time()
        
        try:
            # Extract processing options
            process_subdirs = processing_options.get('process_subdirs', True)
            chunking_method = processing_options.get('chunking_method', 'hierarchy')
            embedding_model = processing_options.get('embedding_model')
            pdf_conversion_method = processing_options.get('pdf_conversion_method', 'pymupdf')
            force_rebuild = processing_options.get('force_rebuild', False)
            merge_results = processing_options.get('merge_results', True)
            memory_entries_per_vector = processing_options.get('memory_entries_per_vector', 5)
            
            # Extract output directories
            vector_dir = output_dirs.get('vector', self.vector_dir)
            graph_dir = output_dirs.get('graph', self.graph_dir)
            memory_dir = output_dirs.get('memory', self.memory_dir)
            
            # Ensure output directories exist
            vector_dir.mkdir(exist_ok=True, parents=True)
            graph_dir.mkdir(exist_ok=True, parents=True)
            memory_dir.mkdir(exist_ok=True, parents=True)
            
            # Step 1: Discover documents
            documents = self.discover_documents(raw_dir, process_subdirs)
            logger.info(f"Discovered {len(documents)} documents")
            self.statistics.update('total_documents', len(documents))
            
            if not documents:
                logger.warning(f"No documents found in {raw_dir}")
                result = ProcessingResult(
                    vector_db_paths=[],
                    graph_db_paths=[],
                    memory_db_paths=[],
                    partition_merged_paths={},
                    statistics=self.statistics.get_all(),
                    status="completed",
                    message=f"No documents found in {raw_dir}"
                )
                return result
            
            # Step 2: Process documents in batches
            # For now, we process all documents in a single batch
            # In the future, this could be parallelized or split into smaller batches
            batch_result = self.process_documents_batch(
                documents=documents,
                output_vector_dir=vector_dir,
                output_graph_dir=graph_dir,
                output_memory_dir=memory_dir,
                memory_entries_per_vector=memory_entries_per_vector,
                chunking_method=chunking_method,
                embedding_model=embedding_model,
                pdf_conversion_method=pdf_conversion_method,
                force_rebuild=force_rebuild
            )
            
            vector_db_paths = batch_result.vector_db_paths
            graph_db_paths = batch_result.graph_db_paths
            memory_db_paths = batch_result.memory_db_paths
            
            # Update statistics from batch processing
            for key, value in batch_result.statistics.items():
                if isinstance(value, (int, float)):
                    self.statistics.update(key, value)
            
            # Step 3: Merge databases by partition if requested
            partition_merged_paths = {} # This will store paths to merged files, keyed by type then partition
            # merged_vector_db_path = None # Not storing a single path anymore, using partition_merged_paths
            # merged_graph_db_path = None  # Not storing a single path anymore
            # merged_episodic_memory_db_path = None # Not part of this specific subtask's merging focus
            # personality_memory_db_path = None # Not part of this specific subtask's merging focus
            
            if merge_results and vector_db_paths:
                logger.info("Processing option 'merge_results' is True. Merging vector databases by partition.")
                # The output directory for merged vector DBs is implicitly self.vector_builder.vector_dir
                merged_vector_db_paths_by_partition = self.merge_vector_databases_by_partition(
                    vector_db_paths=vector_db_paths
                )
                if merged_vector_db_paths_by_partition:
                    partition_merged_paths['vector'] = merged_vector_db_paths_by_partition
                else:
                    logger.warning("Merging vector databases by partition resulted in no paths.")

                if graph_db_paths:
                    logger.info("Processing option 'merge_results' is True. Merging graph databases by partition.")
                    # The output_dir for merged graph DBs is implicitly self.graph_builder.graph_dir
                    merged_graph_db_paths_by_partition = self.merge_graph_databases_by_partition(
                        graph_db_paths=graph_db_paths
                    )
                    if merged_graph_db_paths_by_partition:
                        partition_merged_paths['graph'] = merged_graph_db_paths_by_partition
                    else:
                        logger.warning("Merging graph databases by partition resulted in no paths.")

                # Episodic memory database merging (if needed by partition, implement similarly)
                # if memory_db_paths:
                #    logger.info("Merging episodic memory databases.")
                #    # This would require a merge_episodic_memory_databases_by_partition method
                #    # For now, the existing merge_episodic_memory_databases merges all into one.
                #    merged_episodic_memory_db_path = self.merge_episodic_memory_databases(
                #        memory_db_paths=memory_db_paths, # Contains individual m_{basename}.parquet files
                #        output_dir=memory_dir,
                #        output_filename="episodic_memory_merged.parquet" # Ensure a distinct name if needed
                #    )
                #    if merged_episodic_memory_db_path:
                #        # partition_merged_paths might not be the right place if it's a single merged file
                #        logger.info(f"Merged episodic memory database at: {merged_episodic_memory_db_path}")
                #    else:
                #        logger.warning("Merging episodic memory databases resulted in no path.")

            # Step 4: Create/setup personality memory DB (typically a global, not per-partition merged)
            # This is generally called once, not necessarily tied to merge_results of document processing.
            # personality_memory_db_path = self.setup_personality_memory(memory_dir)
            # logger.info(f"Personality memory setup complete. Path: {personality_memory_db_path}")
            
            # Step 5: Finalize statistics
            self.statistics.finalize()
            
            # Step 6: Create and return final result
            result = ProcessingResult(
                vector_db_paths=vector_db_paths,
                graph_db_paths=graph_db_paths,
                memory_db_paths=memory_db_paths,
                partition_merged_paths=partition_merged_paths,
                statistics=self.statistics.get_all(),
                status="completed",
                message=f"Successfully processed {len(documents)} documents"
            )
            
            logger.info(f"Pipeline completed in {time.time() - overall_start_time:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Error in document processing pipeline: {str(e)}")
            logger.debug(f"Pipeline error details: {traceback.format_exc()}")
            
            # Return partial result with error status
            return ProcessingResult(
                vector_db_paths=[],
                graph_db_paths=[],
                memory_db_paths=[],
                partition_merged_paths={},
                statistics=self.statistics.get_all(),
                status="error",
                message=f"Pipeline error: {str(e)}"
            )

    def discover_documents(self, raw_dir: Path, process_subdirs: bool = True) -> List[DocumentInfo]: # Changed return type
        """Discover documents in a directory, applying file priority rules and returning DocumentInfo objects.

        Uses DocumentDiscoverer to find all potential documents and then applies priority:
        1. When both .md and .pdf files with the same name (and in the same directory) exist, .md file is prioritized.
        2. When only a .md file exists, it is used directly.
        3. When only a .pdf file exists, it is used.

        Args:
            raw_dir: Directory containing raw documents.
            process_subdirs: Whether to process subdirectories (passed to DocumentDiscoverer).

        Returns:
            List of DocumentInfo objects that should be processed.
        """
        logger.info(f"Discovering documents in {raw_dir} using DocumentDiscoverer and applying priority rules.")

        if not raw_dir.exists():
            logger.warning(f"Raw directory {raw_dir} does not exist")
            return []

        # Step 1: Use DocumentDiscoverer to get all DocumentInfo objects.
        # DocumentDiscoverer.discover_documents handles process_subdirs and initial filtering,
        # and creates DocumentInfo objects with path-based metadata.
        all_document_infos: List[DocumentInfo] = self.document_discoverer.discover_documents(raw_dir, process_subdirs)
        
        logger.debug(f"DocumentDiscoverer found {len(all_document_infos)} potential documents with metadata.")

        # Step 2: Apply file priority rules (.md over .pdf for same basename in same directory).
        # Group DocumentInfo objects by their parent directory and base_name.
        file_groups: Dict[Tuple[Path, str], Dict[str, DocumentInfo]] = {}

        for doc_info in all_document_infos:
            # Use file_path.parent to ensure uniqueness for files with same name in different subdirs
            group_key = (doc_info.file_path.parent, doc_info.base_name) 
            if group_key not in file_groups:
                file_groups[group_key] = {}
            
            # doc_info.file_type is 'md' or 'pdf' (guaranteed lowercase by DocumentDiscoverer)
            file_groups[group_key][doc_info.file_type] = doc_info

        priority_documents: List[DocumentInfo] = []
        for group_key, files_in_group in file_groups.items():
            if 'md' in files_in_group:
                priority_documents.append(files_in_group['md'])  # Prioritize MD
            elif 'pdf' in files_in_group:
                priority_documents.append(files_in_group['pdf']) # Otherwise, take PDF
            # If neither (e.g. only .txt and it wasn't filtered by DocumentDiscoverer), it's ignored here.
            # DocumentDiscoverer is set to find only 'pdf', 'md' currently.

        logger.info(f"After applying file priority rules, {len(priority_documents)} DocumentInfo objects will be processed")
        return priority_documents
    
    def process_documents_batch(self, 
                       documents: List[DocumentInfo],
                       output_vector_dir: Path,
                       output_graph_dir: Path,
                       output_memory_dir: Path,
                       memory_entries_per_vector: int = 5,
                       chunking_method: str = 'hierarchy',
                       embedding_model: Optional[str] = None,
                       pdf_conversion_method: str = 'pymupdf',
                       force_rebuild: bool = False) -> BatchResult:
        """Process a batch of documents through the full pipeline.
        
        Args:
            documents: List of DocumentInfo objects to process
            output_vector_dir: Directory to save vector databases
            output_graph_dir: Directory to save graph databases
            output_memory_dir: Directory to save memory databases
            memory_entries_per_vector: Number of memory entries to create per vector database
            chunking_method: Method for text chunking
            embedding_model: Model to use for embeddings
            pdf_conversion_method: Method for PDF conversion
            force_rebuild: Whether to force rebuilding existing databases
            
        Returns:
            BatchResult object containing paths and statistics
        """
        logger.info(f"Processing batch of {len(documents)} documents")
        start_time = time.time()
        
        # Initialize results
        vector_db_paths = []
        graph_db_paths = []
        memory_db_paths = []
        batch_stats = {"documents_processed": 0, "errors": 0}
        
        # Ensure output directories exist
        output_vector_dir.mkdir(parents=True, exist_ok=True)
        output_graph_dir.mkdir(parents=True, exist_ok=True)
        output_memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Process each document
        for doc_info_obj in documents:
            doc_path = doc_info_obj.file_path
            try:
                logger.info(f"Processing document: {doc_path}")
                doc_stats = {}
                
                # Skip if files already exist and force_rebuild is False
                doc_basename = doc_path.stem
                vector_db_filename = f"v_{doc_basename}.parquet"
                graph_db_filename = f"g_{doc_basename}.pkl"
                memory_db_filename = f"m_{doc_basename}.parquet"
                
                vector_db_path = output_vector_dir / vector_db_filename
                graph_db_path = output_graph_dir / graph_db_filename
                memory_db_path = output_memory_dir / memory_db_filename
                
                if not force_rebuild and vector_db_path.exists() and graph_db_path.exists() and memory_db_path.exists():
                    logger.info(f"Skipping {doc_path} - all databases already exist")
                    vector_db_paths.append(str(vector_db_path))
                    graph_db_paths.append(str(graph_db_path))
                    memory_db_paths.append(str(memory_db_path))
                    batch_stats["documents_processed"] += 1
                    continue
                
                # Step 1: Load hierarchy for document (if chunking_method is 'hierarchy')
                df_headings = None
                if chunking_method == 'hierarchy':
                    # doc_info_obj (DocumentInfo instance) already contains region and doc_type
                    # from DocumentDiscoverer which uses path-based extraction.
                    # Pass it directly to load_hierarchy_for_document.
                    df_headings = self.load_hierarchy_for_document(doc_info_obj)
                
                # Step 2: Create vector database
                # Initialize with correct path but don't check existence yet
                vector_db_path = output_vector_dir / f"v_{doc_basename}.parquet"
                if force_rebuild or not vector_db_path.exists():
                    vector_db_path, vector_metadata = self.vector_builder.create_db(
                        input_file=str(doc_path),
                        df_headings=df_headings,
                        chunking_method=chunking_method,
                        model=embedding_model,
                        conversion_method=pdf_conversion_method
                    )
                    if vector_db_path:
                        # Update statistics
                        vector_db_paths.append(vector_db_path)
                        doc_stats.update(vector_metadata)
                        logger.info(f"Created vector database: {vector_db_path}")
                    else:
                        logger.warning(f"Failed to create vector database for {doc_path}")
                        batch_stats["errors"] += 1
                        continue
                else:
                    logger.info(f"Using existing vector database: {vector_db_path}")
                    vector_db_paths.append(str(vector_db_path))
                
                # Step 3: Create graph database based on the vector database
                # Initialize with correct path but don't check existence yet
                graph_db_path = output_graph_dir / f"g_{doc_basename}.pkl"
                if vector_db_path and (force_rebuild or not graph_db_path.exists()):
                    # Initialize the GraphBuilder with the vector database
                    self.graph_builder = GraphBuilder(vectordb_file=vector_db_path)
                    
                    # Create the graph database
                    graph = self.graph_builder.create_db(vector_db_file=vector_db_path)
                    
                    # Save the graph database
                    if graph:
                        graph_db_path = self.graph_builder.save_db()
                        graph_db_paths.append(graph_db_path)
                        
                        # Update statistics
                        doc_stats["graph_nodes"] = graph.number_of_nodes()
                        doc_stats["graph_edges"] = graph.number_of_edges()
                        logger.info(f"Created graph database: {graph_db_path}")
                    else:
                        logger.warning(f"Failed to create graph database for {doc_path}")
                else:
                    if graph_db_path.exists():
                        logger.info(f"Using existing graph database: {graph_db_path}")
                        graph_db_paths.append(str(graph_db_path))
                
                # Step 4: Create memory database based on the vector database
                # Initialize with correct path but don't check existence yet
                memory_db_path = output_memory_dir / f"m_{doc_basename}.parquet"
                if vector_db_path and (force_rebuild or not memory_db_path.exists()):
                    # Create the memory database
                    memory_db_path = self.memory_builder.create_episodic_db(
                        vector_db_file=vector_db_path,
                        num_entries=memory_entries_per_vector
                    )
                    
                    if memory_db_path:
                        memory_db_paths.append(memory_db_path)
                        
                        # Update statistics
                        try:
                            memory_df = pd.read_parquet(memory_db_path)
                            doc_stats["memory_entries"] = len(memory_df)
                        except Exception as e:
                            logger.warning(f"Error reading memory database: {str(e)}")
                        
                        logger.info(f"Created memory database: {memory_db_path}")
                    else:
                        logger.warning(f"Failed to create memory database for {doc_path}")
                else:
                    if memory_db_path.exists():
                        logger.info(f"Using existing memory database: {memory_db_path}")
                        memory_db_paths.append(str(memory_db_path))
                
                # Update batch statistics
                batch_stats["documents_processed"] += 1
                
                # Collect statistics from this operation
                self.collect_statistics_from_operation(doc_stats)
                
            except Exception as e:
                logger.error(f"Error processing document {doc_path}: {str(e)}")
                logger.debug(f"Document processing error details: {traceback.format_exc()}")
                batch_stats["errors"] += 1
        
        # Calculate processing time
        processing_time = time.time() - start_time
        batch_stats["processing_time"] = processing_time
        
        logger.info(f"Batch processing completed in {processing_time:.2f} seconds. Processed {batch_stats['documents_processed']} documents with {batch_stats['errors']} errors.")
        
        return BatchResult(
            vector_db_paths=vector_db_paths,
            graph_db_paths=graph_db_paths,
            memory_db_paths=memory_db_paths,
            statistics=batch_stats
        )
    
    def _extract_metadata_from_path(self, file_path: Path) -> Tuple[str, str]:
        """Extract region and document type from file path.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Tuple of (region, document_type)
        """
        # This is a simplified implementation - customize based on your file naming convention
        file_name = file_path.stem
        
        # Default values
        region = "default"
        doc_type = "standard"
        
        # Extract region (e.g., 'au', 'eu', 'bs') from first 2-3 characters
        region_match = re.match(r'^([a-z]{2,3})', file_name.lower())
        if region_match:
            region = region_match.group(1)
        
        # Extract document type from name patterns
        if 'standard' in file_name.lower():
            doc_type = 'standard'
        elif 'guidance' in file_name.lower():
            doc_type = 'guidance'
        elif 'opinion' in file_name.lower():
            doc_type = 'opinion'
        
        return region, doc_type

    def coordinate_cross_database_creation(self, 
                                      vector_db_path: str,
                                      output_graph_dir: Path,
                                      output_memory_dir: Path,
                                      memory_entries_per_vector: int = 5,
                                      force_rebuild: bool = False) -> Dict[str, str]:
        """Orchestrate the creation of graph and memory databases from a vector database.
        
        This method coordinates the pipeline from vector → graph → memory databases,
        ensuring all dependencies are properly managed.
        
        Args:
            vector_db_path: Path to the vector database file
            output_graph_dir: Directory to save the graph database
            output_memory_dir: Directory to save the memory database
            memory_entries_per_vector: Number of memory entries to create per vector
            force_rebuild: Whether to force rebuilding existing databases
            
        Returns:
            Dictionary with paths to created databases
        """
        logger.info(f"Coordinating cross-database creation from vector database: {vector_db_path}")
        start_time = time.time()
        
        result = {
            "vector_db": vector_db_path,
            "graph_db": None,
            "memory_db": None
        }
        
        try:
            # Ensure output directories exist
            output_graph_dir.mkdir(parents=True, exist_ok=True)
            output_memory_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract base name for output files
            vector_db_basename = Path(vector_db_path).stem
            if vector_db_basename.startswith('v_'):
                base_name = vector_db_basename[2:]  # Remove 'v_' prefix
            else:
                base_name = vector_db_basename
            
            graph_db_filename = f"g_{base_name}.pkl"
            memory_db_filename = f"m_{base_name}.parquet"
            
            graph_db_path = output_graph_dir / graph_db_filename
            memory_db_path = output_memory_dir / memory_db_filename
            
            # Step 1: Create graph database from vector database
            if force_rebuild or not graph_db_path.exists():
                logger.info(f"Creating graph database from vector database: {vector_db_path}")
                
                # Initialize the GraphBuilder with the vector database
                self.graph_builder = GraphBuilder(vectordb_file=vector_db_path)
                
                # Create the graph database
                graph = self.graph_builder.create_db(vector_db_file=vector_db_path)
                
                # Save the graph database
                if graph:
                    graph_db_path_str = self.graph_builder.save_db(custom_name=graph_db_filename)
                    result["graph_db"] = graph_db_path_str
                    
                    # Update statistics
                    stats = {
                        "graph_nodes": graph.number_of_nodes(),
                        "graph_edges": graph.number_of_edges()
                    }
                    self.collect_statistics_from_operation(stats)
                    
                    logger.info(f"Created graph database: {graph_db_path_str}")
                else:
                    logger.warning(f"Failed to create graph database from {vector_db_path}")
            else:
                logger.info(f"Using existing graph database: {graph_db_path}")
                result["graph_db"] = str(graph_db_path)
            
            # Step 2: Create memory database from vector database
            if force_rebuild or not memory_db_path.exists():
                logger.info(f"Creating memory database from vector database: {vector_db_path}")
                
                # Create the memory database
                memory_db_path_str = self.memory_builder.create_db(
                    vector_db_path=vector_db_path,
                    max_entries_per_chunk=memory_entries_per_vector,
                    output_file=str(memory_db_path)
                )
                
                if memory_db_path_str:
                    result["memory_db"] = memory_db_path_str
                    
                    # Update statistics
                    try:
                        memory_df = pd.read_parquet(memory_db_path_str)
                        stats = {"memory_entries": len(memory_df)}
                        self.collect_statistics_from_operation(stats)
                    except Exception as e:
                        logger.warning(f"Error reading memory database: {str(e)}")
                    
                    logger.info(f"Created memory database: {memory_db_path_str}")
                else:
                    logger.warning(f"Failed to create memory database from {vector_db_path}")
            else:
                logger.info(f"Using existing memory database: {memory_db_path}")
                result["memory_db"] = str(memory_db_path)
            
            # Log completion
            processing_time = time.time() - start_time
            logger.info(f"Cross-database creation completed in {processing_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in cross-database creation: {str(e)}")
            logger.debug(f"Cross-database creation error details: {traceback.format_exc()}")
            return result

    def merge_vector_databases_by_partition(self, 
                                       vector_db_paths: List[str]
                                       # output_dir is implicitly self.vector_builder.vector_dir
                                       # output_prefix is removed as naming is fixed to v_{partition_name}.parquet
                                       ) -> Dict[str, str]:
        """Merge vector databases by partition. Output files are named v_{partition_name}.parquet.
        
        Args:
            vector_db_paths: List of vector database paths to merge
            
        Returns:
            Dictionary mapping partition names to merged database paths (e.g., {"au-standard": "path/to/v_au-standard.parquet"})
        """
        logger.info(f"Merging {len(vector_db_paths)} vector databases by partition.")
        start_time = time.time()
        
        result = {}
        self.partition_manager = PartitionManager() # Ensure partition_manager is initialized

        try:
            # Group databases by partition
            partition_groups = self.partition_manager.group_by_partition(vector_db_paths)
            logger.info(f"Grouped vector databases into {len(partition_groups)} partitions: {list(partition_groups.keys())}")
            
            # Merge each partition
            for partition_name, partition_db_paths in partition_groups.items():
                if not partition_db_paths:
                    logger.warning(f"No vector databases found for partition '{partition_name}'")
                    continue
                    
                logger.info(f"Merging {len(partition_db_paths)} vector databases for partition '{partition_name}'")
                
                # VectorBuilder.merge_db will save it as v_{partition_name}.parquet in its self.vector_dir
                merged_db = self.vector_builder.merge_db(
                    parquet_files=partition_db_paths,
                    output_name=partition_name  # Pass partition_name as the stem
                )
                
                if merged_db is not None and not merged_db.empty:
                    # Construct the actual path where VectorBuilder.merge_db saved the file
                    actual_save_path = self.vector_builder.vector_dir / f"v_{partition_name}.parquet"
                    result[partition_name] = str(actual_save_path)
                    
                    # Update statistics
                    stats = {
                        "vector_db_size": len(merged_db), # This might be cumulative; consider per-partition if needed
                        # "partition_merged": True # This is too generic for overall stats; specific logging is better
                    }
                    self.collect_statistics_from_operation(stats) # Ensure this handles cumulative stats correctly
                    
                    logger.info(f"Merged vector database for partition '{partition_name}' saved to {actual_save_path}")
                else:
                    logger.warning(f"Failed to merge vector databases for partition '{partition_name}', or merged DB was empty.")
            
            processing_time = time.time() - start_time
            logger.info(f"Vector database merging by partition completed in {processing_time:.2f} seconds. Merged partitions: {list(result.keys())}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error merging vector databases by partition: {str(e)}")
            logger.debug(f"Vector database merging error details: {traceback.format_exc()}")
            return result # Return partial results or empty dict if error occurred early

    def merge_graph_databases_by_partition(self, 
                                      graph_db_paths: List[str]
                                      # output_dir is implicitly self.graph_builder.graph_dir
                                      # output_prefix is removed as naming is fixed to g_{partition_name}.pkl
                                      ) -> Dict[str, str]:
        """Merge graph databases by partition. Output files are named g_{partition_name}.pkl.
        
        Args:
            graph_db_paths: List of graph database paths to merge
            
        Returns:
            Dictionary mapping partition names to merged database paths (e.g., {"au-standard": "path/to/g_au-standard.pkl"})
        """
        logger.info(f"Merging {len(graph_db_paths)} graph databases by partition.")
        start_time = time.time()
        
        result = {}
        self.partition_manager = PartitionManager() # Ensure partition_manager is initialized
        # Ensure graph_builder is initialized (it might be initialized in process_directory or needs to be here)
        if not hasattr(self, 'graph_builder') or self.graph_builder is None:
            self.graph_builder = GraphBuilder()
            logger.info("Initialized GraphBuilder in merge_graph_databases_by_partition as it was not set.")

        try:
            # Group databases by partition
            partition_groups = self.partition_manager.group_by_partition(graph_db_paths)
            logger.info(f"Grouped graph databases into {len(partition_groups)} partitions: {list(partition_groups.keys())}")
            
            # Merge each partition
            for partition_name, partition_db_paths_for_group in partition_groups.items():
                if not partition_db_paths_for_group:
                    logger.warning(f"No graph databases found for partition '{partition_name}'")
                    continue
                    
                logger.info(f"Merging {len(partition_db_paths_for_group)} graph databases for partition '{partition_name}'")
                
                # GraphBuilder.merge_dbs will save it as g_{partition_name}.pkl in its self.graph_dir
                merged_graph = self.graph_builder.merge_dbs(
                    graph_files=partition_db_paths_for_group,
                    output_name=partition_name  # Pass partition_name as the stem
                )
                
                if merged_graph is not None and merged_graph.number_of_nodes() > 0 : # Check if graph is not empty
                    # Construct the actual path where GraphBuilder.merge_dbs saved the file
                    actual_save_path = self.graph_builder.graph_dir / f"g_{partition_name}.pkl"
                    result[partition_name] = str(actual_save_path)
                    
                    # Update statistics
                    stats = {
                        "graph_nodes": merged_graph.number_of_nodes(),
                        "graph_edges": merged_graph.number_of_edges(),
                        # "partition_merged": True # Generic, better to log specific merge event
                    }
                    self.collect_statistics_from_operation(stats)
                    
                    logger.info(f"Merged graph database for partition '{partition_name}' saved to {actual_save_path}")
                else:
                    logger.warning(f"Failed to merge graph databases for partition '{partition_name}', or merged graph was empty.")
            
            processing_time = time.time() - start_time
            logger.info(f"Graph database merging by partition completed in {processing_time:.2f} seconds. Merged partitions: {list(result.keys())}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error merging graph databases by partition: {str(e)}")
            logger.debug(f"Graph database merging error details: {traceback.format_exc()}")
            return result # Return partial results or empty dict if error occurred early


    def merge_all_databases_by_partition(self, db_paths: Dict[str, List[str]], output_name: str) -> Dict[str, Dict[str, str]]:
        """Merge all databases by partition.
        
        Args:
            db_paths: Dictionary mapping database types to lists of database paths
            output_name: Base name for merged output files
            
        Returns:
            Dictionary mapping partition names to dictionaries of merged database paths
        """
        logger.info(f"Merging databases by partition with base name: {output_name}")
        
        # TODO: Implement database merging by partition
        # This method should use the partition manager to:  
        # 1. Group databases by partition (region/document type)
        # 2. Merge vector databases within each partition
        # 3. Merge graph databases within each partition
        # 4. Return paths to all merged databases by partition
        
        # Placeholder - return empty dictionary for now
        return {}
    
    def merge_episodic_memory_databases(self, memory_db_paths: List[str], output_dir: Path, output_filename: str) -> str:
        """Merge episodic memory databases.
        
        Args:
            memory_db_paths: List of memory database paths to merge
            output_dir: Directory to save merged memory database
            output_filename: Filename for merged memory database
            
        Returns:
            Path to merged memory database
        """
        logger.info(f"Merging {len(memory_db_paths)} episodic memory databases")
        
        # TODO: Implement episodic memory database merging
        # This method should use the memory builder to merge all episodic memory databases
        # and return the path to the merged database
        
        # Placeholder - return empty string for now
        return ""
    
    def setup_personality_memory(self, output_dir: Path) -> str:
        """Create personality memory database from configuration.
        
        Args:
            output_dir: Directory to save personality memory database
            
        Returns:
            Path to personality memory database
        """
        logger.info("Setting up personality memory database")
        
        # TODO: Implement personality memory setup
        # This method should use the memory builder to create a personality memory database
        # from the personality traits in the configuration
        
        # Placeholder - return empty string for now
        return ""
    
    def load_hierarchy_for_document(self, doc_info: Union[Dict[str, Any], DocumentInfo]) -> Optional[pd.DataFrame]:
        """Load the appropriate hierarchy for a document.
        
        Args:
            doc_info: Document information (dict or DocumentInfo)
            
        Returns:
            DataFrame with hierarchy data, or None if not found
        """
        logger.debug(f"Loading hierarchy for document: {doc_info}")
        
        try:
            # HierarchyManager is now initialized in PipelineCoordinator.__init__
            
            # Find hierarchy for document
            hierarchy_df = self.hierarchy_manager.find_hierarchy_for_document(doc_info)
            
            if hierarchy_df is not None and not hierarchy_df.empty:
                logger.info(f"Found hierarchy for document with {len(hierarchy_df)} entries")
                return hierarchy_df
            else:
                logger.warning(f"No hierarchy found for document")
                return None
                
        except Exception as e:
            logger.error(f"Error loading hierarchy for document: {str(e)}")
            logger.debug(f"Hierarchy loading error details: {traceback.format_exc()}")
            return None

    def collect_statistics_from_operation(self, stats: Dict[str, Any]) -> None:
        """Update statistics from an operation.
        
        Args:
            stats: Dictionary of statistics to update
        """
        logger.debug(f"Collecting statistics: {stats}")
        
        try:
            # Map dictionary keys to ProcessingStatistics attributes
            mapping = {
                "documents_processed": "files_processed",
                "pdfs_converted": "pdfs_converted",
                "chunks": "chunks_created",
                "chunks_created": "chunks_created",
                "vector_db_size": "vector_db_size",
                "graph_nodes": "graph_nodes",
                "graph_edges": "graph_edges",
                "memory_entries": "episodic_memory_entries_created",
                "personality_entries": "personality_memory_entries_created"
            }
            
            # Update statistics
            for key, value in stats.items():
                if key in mapping and hasattr(self.statistics, mapping[key]):
                    self.statistics.update(mapping[key], value, increment=True)
                elif hasattr(self.statistics, key):
                    self.statistics.update(key, value, increment=True)
            
        except Exception as e:
            logger.error(f"Error collecting statistics: {str(e)}")
            logger.debug(f"Statistics collection error details: {traceback.format_exc()}")

    def get_final_statistics(self) -> Dict[str, Any]:
        """Get the final processing statistics.
        
        Returns:
            Dictionary with all processing statistics
        """
        logger.debug("Retrieving final statistics")
        
        try:
            # Finalize statistics
            self.statistics.finalize()
            
            # Get all statistics
            return self.statistics.get_all()
            
        except Exception as e:
            logger.error(f"Error retrieving statistics: {str(e)}")
            logger.debug(f"Statistics retrieval error details: {traceback.format_exc()}")
        return {"error": str(e)}