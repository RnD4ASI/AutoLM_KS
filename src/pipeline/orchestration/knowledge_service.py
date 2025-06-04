import os
import argparse
import json
import time
import traceback
from pathlib import Path
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))
from typing import Dict, List, Any, Optional, Union

# Import necessary modules
from src.pipeline.shared.logging import get_logger
from src.pipeline.processing.dbbuilder import PipelineCoordinator
from src.pipeline.shared.utility import DataUtility

logger = get_logger(__name__)


class KnowledgeService:
    """
    Simplified orchestration layer for knowledge base creation.
    
    This service provides a thin interface that delegates all database operations
    to the PipelineCoordinator in dbbuilder.py. It handles configuration loading,
    parameter validation, and result formatting while maintaining backward
    compatibility with the original API.
    """
    
    def __init__(self, config_file_path: Optional[Union[str, Path]] = None):
        """
        Initialize the KnowledgeService with configuration.
        
        Args:
            config_file_path: Path to configuration file. If None, uses default path.
        """
        logger.info("Initializing KnowledgeService")
        start_time = time.time()
        
        try:
            # Load configuration
            self.config_path = Path(config_file_path) if config_file_path else Path.cwd() / "config" / "main_config.json"
            self.config = self._load_config()
            
            # Load hierarchy configuration
            self.hierarchy_config_path = Path.cwd() / "config" / "hierarchy_config.json"
            try:
                hierarchy_config = DataUtility.text_operation(
                    operation='load', 
                    file_path=self.hierarchy_config_path, 
                    file_type='json'
                )
                if hierarchy_config is None: # DataUtility.text_operation load returns None if file not found, but we catch FileNotFoundError
                    hierarchy_config = {}
                    logger.warning(f"Loading {self.hierarchy_config_path} with DataUtility returned None, using empty dict.")
            except FileNotFoundError:
                logger.warning(f"Hierarchy config file not found at {self.hierarchy_config_path} (handled by DataUtility), using empty dict.")
                hierarchy_config = {}
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from {self.hierarchy_config_path}: {e}, using empty dict.")
                hierarchy_config = {}
            except Exception as e:
                logger.error(f"An unexpected error occurred while loading {self.hierarchy_config_path}: {e}, using empty dict.")
                hierarchy_config = {}
            hierarchy_mapping = hierarchy_config.get("hierarchy_mapping", {})
            default_hierarchy_file = hierarchy_config.get("default_hierarchy_file", None)
            logger.info(f"Loaded hierarchy_mapping: {hierarchy_mapping}")
            logger.info(f"Loaded default_hierarchy_file: {default_hierarchy_file}")
            
            # Initialize the pipeline coordinator (main workhorse)
            self.coordinator = PipelineCoordinator(
                config=self.config,
                hierarchy_mapping=hierarchy_mapping,
                default_hierarchy_file=default_hierarchy_file
            )
            
            logger.info(f"KnowledgeService initialized in {time.time() - start_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"KnowledgeService initialization failed: {str(e)}")
            logger.debug(f"Initialization error details: {traceback.format_exc()}")
            raise
    
    def run(self, 
           raw_dir: Optional[Union[str, Path]] = None,
           vector_dir: Optional[Union[str, Path]] = None,
           graph_dir: Optional[Union[str, Path]] = None,
           memory_dir: Optional[Union[str, Path]] = None,
           memory_entries_per_vector: int = 5,
           chunking_method: str = 'hierarchy',
           embedding_model: Optional[str] = None,
           pdf_conversion_method: str = 'pymupdf',
           force_rebuild: bool = False,
           merge_results: bool = True,
           process_subdirs: bool = True) -> Dict[str, Any]:
        """
        Run the complete knowledge service pipeline.
        
        This method maintains the same interface as the original implementation
        but delegates all operations to the PipelineCoordinator.
        
        Args:
            raw_dir: Directory containing raw documents
            vector_dir: Directory to save vector databases
            graph_dir: Directory to save graph databases
            memory_dir: Directory to save memory databases
            memory_entries_per_vector: Number of memory entries to create per vector database
            chunking_method: Method to use for text chunking ('hierarchy' or 'length')
            embedding_model: Model to use for generating embeddings
            pdf_conversion_method: Method to use for PDF conversion
            force_rebuild: Whether to force rebuilding existing databases
            merge_results: Whether to merge individual databases
            process_subdirs: Whether to process files from all subdirectories
            
        Returns:
            Dictionary with processing results and statistics (backward compatible format)
        """
        logger.info("Starting knowledge service pipeline")
        overall_start_time = time.time()
        
        try:
            # Validate parameters
            if not self._validate_parameters(
                chunking_method=chunking_method,
                pdf_conversion_method=pdf_conversion_method,
                memory_entries_per_vector=memory_entries_per_vector
            ):
                raise ValueError("Invalid parameters provided")
            
            # Setup output directories
            output_dirs = self._setup_output_directories(
                vector_dir=vector_dir,
                graph_dir=graph_dir,
                memory_dir=memory_dir
            )
            
            # Prepare processing options
            processing_options = {
                'chunking_method': chunking_method,
                'embedding_model': embedding_model or self.config.get('knowledge_base', {}).get('vector_store', {}).get('embedding_model', 'all-MiniLM-L6-v2'),
                'pdf_conversion_method': pdf_conversion_method,
                'force_rebuild': force_rebuild,
                'merge_results': merge_results,
                'process_subdirs': process_subdirs,
                'memory_entries_per_vector': memory_entries_per_vector
            }
            
            # Delegate everything to the pipeline coordinator
            result = self.coordinator.process_directory(
                raw_dir=Path(raw_dir) if raw_dir else Path.cwd() / "db" / "raw",
                output_dirs=output_dirs,
                processing_options=processing_options
            )
            
            # Add total processing time
            total_time = time.time() - overall_start_time
            result.statistics['total_time'] = total_time
            
            logger.info(f"Knowledge service pipeline completed in {total_time:.2f} seconds")
            
            # Return in backward-compatible dictionary format as a dict
            return {
                'status': result.status,
                'message': result.message,
                'stats': result.statistics,
                'individual_vector_db_paths': result.vector_db_paths,
                'individual_graph_db_paths': result.graph_db_paths,
                'individual_episodic_memory_db_paths': result.memory_db_paths,
                'individual_personality_memory_db_paths': result.memory_db_paths, # Corrected from result.personality_memory_paths if it was a typo and should be same as episodic for individual files. Or specific if distinct. Assuming it refers to the same list of individual memory files generated before any merge.
                'partition_merged_db_paths': result.partition_merged_paths # Added to expose paths of merged DBs by partition
            }
            
        except Exception as e:
            logger.error(f"Knowledge service failed: {str(e)}")
            logger.debug(f"Error details: {traceback.format_exc()}")
            raise
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file with fallback to defaults.
        
        Returns:
            Configuration dictionary
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                logger.debug(f"Loaded configuration from {self.config_path}")
                return config
            else:
                logger.warning(f"Config file not found at {self.config_path}, using defaults")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Return default configuration if file not found.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "system": {
                "paths": {
                    "knowledge_base": "db",
                    "source": "data"
                },
                "supported_file_types": ["pdf", "md", "txt"]
            },
            "knowledge_base": {
                "chunking": {
                    "method": "hierarchy",
                    "other_config": {
                        "chunk_size": 1000,
                        "chunk_overlap": 100
                    }
                },
                "vector_store": {
                    "embedding_model": "all-MiniLM-L6-v2",
                    "similarity_threshold": 0.7,
                    "top_k": 5
                }
            }
        }
    

    def _validate_parameters(self, **kwargs) -> bool:
        """
        Validate input parameters.
        
        Args:
            **kwargs: Parameters to validate
            
        Returns:
            True if all parameters are valid
            
        Raises:
            ValueError: If any parameter is invalid
        """
        # Validate chunking method
        chunking_method = kwargs.get('chunking_method')
        if chunking_method not in ['hierarchy', 'length']:
            raise ValueError(f"Invalid chunking_method: {chunking_method}. Must be 'hierarchy' or 'length'")
        
        # Validate PDF conversion method
        pdf_conversion_method = kwargs.get('pdf_conversion_method')
        valid_pdf_methods = ['pymupdf', 'markitdown', 'openleaf', 'llamaindex', 'textract']
        if pdf_conversion_method not in valid_pdf_methods:
            raise ValueError(f"Invalid pdf_conversion_method: {pdf_conversion_method}. Must be one of {valid_pdf_methods}")
        
        # Validate memory entries per vector
        memory_entries_per_vector = kwargs.get('memory_entries_per_vector')
        if not isinstance(memory_entries_per_vector, int) or memory_entries_per_vector < 1:
            raise ValueError(f"Invalid memory_entries_per_vector: {memory_entries_per_vector}. Must be a positive integer")
        
        return True
    
    def _setup_output_directories(self, **kwargs) -> Dict[str, Path]:
        """
        Setup and validate output directories.
        
        Args:
            **kwargs: Directory paths from arguments
            
        Returns:
            Dictionary mapping directory type to Path objects
        """
        db_dir = Path.cwd() / "db"
        
        output_dirs = {
            'vector': Path(kwargs.get('vector_dir')) if kwargs.get('vector_dir') else db_dir / "vector",
            'graph': Path(kwargs.get('graph_dir')) if kwargs.get('graph_dir') else db_dir / "graph", 
            'memory': Path(kwargs.get('memory_dir')) if kwargs.get('memory_dir') else db_dir / "memory"
        }
        
        # Create directories if they don't exist
        for dir_type, dir_path in output_dirs.items():
            try:
                dir_path.mkdir(exist_ok=True, parents=True)
                logger.debug(f"Created {dir_type} directory: {dir_path}")
            except Exception as e:
                raise ValueError(f"Cannot create {dir_type} directory {dir_path}: {str(e)}")
        
        return output_dirs


def main():
    """Main entry point for the knowledge service."""
    parser = argparse.ArgumentParser(description="AutoLM Knowledge Service")
    
    parser.add_argument("--raw_dir", type=str, default="db/raw",
                        help="Directory containing raw documents")
    parser.add_argument("--vector_dir", type=str, default="db/vector",
                        help="Directory to save vector databases")
    parser.add_argument("--graph_dir", type=str, default="db/graph",
                        help="Directory to save graph databases")
    parser.add_argument("--memory_dir", type=str, default="db/memory",
                        help="Directory to save memory databases")
    parser.add_argument("--config", type=str, default="config/main_config.json",
                        help="Path to configuration file")
    parser.add_argument("--chunking_method", type=str, default="hierarchy",
                        choices=["hierarchy", "length"],
                        help="Method to use for text chunking")
    parser.add_argument("--embedding_model", type=str,
                        help="Model to use for generating embeddings")
    parser.add_argument("--pdf_conversion", type=str, default="pymupdf",
                        choices=["pymupdf", "markitdown", "openleaf", "llamaindex", "textract"],
                        help="Method to use for PDF conversion")
    parser.add_argument("--force_rebuild", action="store_true",
                        help="Force rebuilding existing databases")
    parser.add_argument("--no_merge", action="store_true",
                        help="Do not merge individual databases")
    parser.add_argument("--process_subdirs", action="store_true", default=True,
                        help="Process files from all subdirectories (default: True)")
    parser.add_argument("--memory_entries_per_vector", type=int, default=5,
                        help="Number of memory entries to create per vector database")
    
    args = parser.parse_args()
    
    try:
        # Initialize the knowledge service
        service = KnowledgeService(config_file_path=args.config)
        
        # Run the pipeline
        result = service.run(
            raw_dir=args.raw_dir,
            vector_dir=args.vector_dir,
            graph_dir=args.graph_dir,
            memory_dir=args.memory_dir,
            chunking_method=args.chunking_method,
            embedding_model=args.embedding_model,
            pdf_conversion_method=args.pdf_conversion,
            force_rebuild=args.force_rebuild,
            merge_results=not args.no_merge,
            process_subdirs=args.process_subdirs,
            memory_entries_per_vector=args.memory_entries_per_vector
        )
        
        # Print summary using the result's format_summary method if available
        # Otherwise, format manually for backward compatibility
        print("\nKnowledge Service Summary:")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        print(f"\nStatistics:")
        stats = result['stats']
        print(f"  Files processed: {stats.get('files_processed', 0)}")
        print(f"  PDFs converted: {stats.get('pdfs_converted', 0)}")
        print(f"  Chunks created: {stats.get('chunks_created', 0)}")
        print(f"  Vector DB size: {stats.get('vector_db_size', 0) / (1024*1024):.2f} MB")
        print(f"  Graph nodes: {stats.get('graph_nodes', 0)}")
        print(f"  Graph edges: {stats.get('graph_edges', 0)}")
        print(f"  Episodic Memory Entries: {stats.get('episodic_memory_entries_created', 0)}")
        print(f"  Personality Memory Entries: {stats.get('personality_memory_entries_created', 0)}")
        print(f"  Total Processing time: {stats.get('total_time', 0):.2f} seconds")
        
        print(f"\nDatabase Files Created:")
        if result.get('individual_vector_db_paths'):
            print(f"  Individual Vector DBs: {len(result['individual_vector_db_paths'])} files")
        if result.get('individual_graph_db_paths'):
            print(f"  Individual Graph DBs: {len(result['individual_graph_db_paths'])} files")
        if result.get('individual_episodic_memory_db_paths'):
            print(f"  Individual Memory DBs: {len(result['individual_episodic_memory_db_paths'])} files")

        print(f"\nConsolidated Databases:")
        if result.get('partition_merged_db_paths'):
            print(f"  Partition-merged DBs: {json.dumps(result['partition_merged_db_paths'], indent=2)}")
        # The following keys like 'merged_vector_db_parquet' might be deprecated if partition_merged_db_paths is comprehensive
        # else: # Fallback to old keys if new one is not there, for smoother transition (optional)
            if result.get('merged_vector_db_parquet'):
                print(f"  Merged Vector DB (legacy key): {result['merged_vector_db_parquet']}")
            if result.get('merged_graph_db_pickle'):
                print(f"  Merged Graph DB (legacy key): {result['merged_graph_db_pickle']}")
            if result.get('merged_episodic_memory_db_parquet'):
                print(f"  Merged Episodic Memory DB (legacy key): {result['merged_episodic_memory_db_parquet']}")
        
        # Personality memory is usually a single file, not typically merged by document partition
        if result.get('personality_memory_db_paths'): # Assuming this key exists if personality DB is processed
             personality_db_path = result['personality_memory_db_paths'] # Adjust if it's a list or single string
             if isinstance(personality_db_path, list) and len(personality_db_path) > 0:
                 print(f"  Personality Memory DB: {personality_db_path[0]}") # Print first if it's a list
             elif isinstance(personality_db_path, str):
                 print(f"  Personality Memory DB: {personality_db_path}")


        return 0
        
    except Exception as e:
        logger.error(f"Knowledge service failed: {str(e)}")
        logger.debug(f"Error details: {traceback.format_exc()}")
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())