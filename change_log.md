# Change Log

## Recent Updates

This log details significant changes and bug fixes applied to the pipeline.

### 1. Fixed HuggingFace EmbeddingError in `src/pipeline/processing/generator.py`
- **File Changed**: `src/pipeline/processing/generator.py`
- **Method Affected**: `_get_hf_embeddings`
- **Change**: Modified the method to correctly load local SentenceTransformer models. Implemented robust error handling to return zero vectors if the model fails to load or produce embeddings. This involved fetching embedding dimensions after a successful model load and using these dimensions to create zero vectors in various exception scenarios, including batch processing failures and individual text encoding failures.
- **Reason**: To prevent crashes when HuggingFace models are unavailable or fail, ensuring the pipeline can continue or gracefully handle embedding issues.

### 2. Fixed Missing `chunk_content` Key in `src/pipeline/processing/dbbuilder.py`
- **File Changed**: `src/pipeline/processing/dbbuilder.py`
- **Method Affected**: `GraphBuilder._find_cross_references`
- **Change**: Updated the call to `self.metagenerator.get_meta_generation` to pass the text content of a chunk using the keyword argument `chunk_content` instead of `content`.
- **Reason**: To align with the expected parameter name in the `MetaGenerator`'s prompt template for cross-reference extraction, ensuring correct functionality.

### 3. Handled `ValueError` in `hierarchy_based_chunking` in `src/pipeline/processing/dbbuilder.py`
- **File Changed**: `src/pipeline/processing/dbbuilder.py`
- **Method Affected**: `TextChunker.hierarchy_based_chunking`
- **Change**: Modified the method to log a warning and return an empty DataFrame with the correct schema if no matching headings are found for a document in the `df_headings` input. Previously, this situation would raise a `ValueError`.
- **Reason**: To make the chunking process more resilient to missing heading information for individual documents, allowing the pipeline to continue processing other documents.

### 4. Fixed Zero Division Error in `src/pipeline/processing/dbbuilder.py`
- **File Changed**: `src/pipeline/processing/dbbuilder.py`
- **Method Affected**: `GraphBuilder._find_similar_chunks` (called by `_create_standard_graph` and `_create_hypergraph`)
- **Change**: Added checks for zero norm vectors before attempting vector normalization. If a `query_vector` has a zero norm, similarity calculation for that chunk is skipped. If a `other_vector` (comparison vector) has a zero norm, that specific comparison is skipped.
- **Reason**: To prevent `RuntimeWarning` or `ZeroDivisionError` during cosine similarity calculation if any text chunk results in a zero-magnitude embedding vector.

### 5. Implemented Personality Memory DB Creation from JSON in `src/pipeline/processing/dbbuilder.py`
- **File Changed**: `src/pipeline/processing/dbbuilder.py`
- **Method Affected**: `MemoryBuilder.create_personality_db`
- **Change**:
    - The method now loads personality traits data directly from a fixed JSON file: `db/memory/personality_memory_full.json`.
    - The output Parquet file is now fixed to `db/memory/personality_memory.parquet`.
    - Parameters `personality_traits` and `output_file` were removed from the method signature.
    - Added error handling for JSON file reading (e.g., `FileNotFoundError`, `json.JSONDecodeError`).
    - Retained existing logic for schema conformance, duplicate handling, and Parquet serialization.
- **Reason**: To centralize the source of personality traits and standardize the creation process of the personality memory database.

### 6. Updated Episodic Memory DB Creation in `src/pipeline/processing/dbbuilder.py`
- **File Changed**: `src/pipeline/processing/dbbuilder.py`
- **Method Affected**: `MemoryBuilder.create_episodic_db`
- **Change**:
    - If `db/memory/episodic_memory.parquet` doesn't exist, it's created with 3 predefined dummy entries (each with unique `entity` and `context.chunk_id`).
    - If the file exists, it's loaded, and new entries from a `vector_db_file` (if provided) are appended.
    - Implemented stricter duplicate prevention: new entries are skipped if their `entity` OR `context.chunk_id` already exists in the memory database (either from dummy entries or previously loaded/added entries).
    - Corrected population of `existing_context_chunk_ids` from the nested `context` dictionary.
- **Reason**: To provide default content for the episodic memory DB when it's first created and to ensure data integrity by preventing duplicate entries based on specified key fields.

### 7. Implemented Vector DB Aggregation by Partition in `src/pipeline/orchestration/knowledge_service.py` and `src/pipeline/processing/dbbuilder.py`
- **Files Changed**: `src/pipeline/orchestration/knowledge_service.py`, `src/pipeline/processing/dbbuilder.py`
- **Methods Affected**:
    - `PipelineCoordinator.merge_vector_databases_by_partition` (in `dbbuilder.py`): Refined to use `partition_name` as the output stem. Its `output_dir` and `output_prefix` parameters were removed as `VectorBuilder` now handles its own output directory.
    - `PipelineCoordinator.process_directory` (in `dbbuilder.py`): Updated to call the refined `merge_vector_databases_by_partition` and store results in `partition_merged_paths['vector']`.
    - `KnowledgeService.run` (in `knowledge_service.py`): Updated to correctly expose the `partition_merged_paths` (now including vector merge results) in its final return dictionary. The `merge_results` flag already controlled this flow.
- **Change**: Added functionality to merge individual vector databases (e.g., `v_documentA.parquet`, `v_documentB.parquet`) into partition-specific databases (e.g., `v_au-standard.parquet`). The merging is triggered by the `merge_results` flag in `KnowledgeService`.
- **Reason**: To consolidate vector data by predefined partitions (REGION_DOCTYPE) for more organized storage and potentially more efficient querying across related documents.

### 8. Implemented Graph DB Aggregation by Partition in `src/pipeline/orchestration/knowledge_service.py` and `src/pipeline/processing/dbbuilder.py`
- **Files Changed**: `src/pipeline/orchestration/knowledge_service.py`, `src/pipeline/processing/dbbuilder.py`
- **Methods Affected**:
    - `PipelineCoordinator.merge_graph_databases_by_partition` (in `dbbuilder.py`): Refined to use `partition_name` as the output stem for `GraphBuilder.merge_dbs`. Its `output_dir` and `output_prefix` parameters were removed. Ensured `GraphBuilder` is initialized if needed.
    - `PipelineCoordinator.process_directory` (in `dbbuilder.py`): Updated to call the refined `merge_graph_databases_by_partition` when `merge_results` is true and `graph_db_paths` exist, storing results in `partition_merged_paths['graph']`.
    - `KnowledgeService.run` (in `knowledge_service.py`): No direct changes needed in this step as the previous modifications to return `partition_merged_paths` already cover exposing graph merge results.
- **Change**: Added functionality to merge individual graph databases (e.g., `g_documentA.pkl`, `g_documentB.pkl`) into partition-specific databases (e.g., `g_au-standard.pkl`). Merging is controlled by the `merge_results` flag.
- **Reason**: To consolidate graph data by predefined partitions, similar to vector DBs, for better organization and potentially more efficient graph-based analyses on related document sets.
