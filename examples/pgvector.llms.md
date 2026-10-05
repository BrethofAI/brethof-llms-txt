# pgvector

> An open-source Postgres extension for vector similarity search, supporting exact and approximate nearest neighbor search with multiple vector types and distance functions.

It is a Postgres extension supporting Postgres 13+, installable by compiling from source or via Docker, Homebrew, PGXN, APT, Yum, pkg, APK, or conda-forge. It supports single-precision, half-precision, binary, and sparse vectors with L2, inner product, cosine, L1, Hamming, and Jaccard distances. Indexing uses HNSW or IVFFlat for approximate nearest neighbor search, with quantization for scaling to many vectors.

## Docs

- [pgvector](https://raw.githubusercontent.com/pgvector/pgvector/master/README.md): Open-source vector similarity search for Postgres with exact and approximate nearest neighbor search, multiple vector types, and distance functions.
- [Installation](https://github.com/pgvector/pgvector/blob/master/README.md#installation): How to compile and install the extension on Linux, Mac, and Windows, plus Docker, Homebrew, PGXN, APT, and other options.
- [Getting Started](https://github.com/pgvector/pgvector/blob/master/README.md#getting-started): Enabling the extension, creating a vector column, inserting vectors, and getting nearest neighbors by distance.
- [Storing](https://github.com/pgvector/pgvector/blob/master/README.md#storing): Creating tables with vector columns, inserting, bulk loading with COPY, upserting, updating, and deleting vectors.
- [Querying](https://github.com/pgvector/pgvector/blob/master/README.md#querying): Getting nearest neighbors, supported distance functions, rows within a distance, distances, and vector aggregates.
- [Indexing](https://github.com/pgvector/pgvector/blob/master/README.md#indexing): Exact versus approximate nearest neighbor search, and the HNSW and IVFFlat index types.
- [HNSW](https://github.com/pgvector/pgvector/blob/master/README.md#hnsw): HNSW index creation for each distance function, supported types, index and query options, and build time tips.
- [IVFFlat](https://github.com/pgvector/pgvector/blob/master/README.md#ivfflat): IVFFlat index creation, keys to good recall, distance functions, supported types, and query options.
- [Filtering](https://github.com/pgvector/pgvector/blob/master/README.md#filtering): Indexing nearest neighbor queries with a WHERE clause using exact or approximate indexes, partial indexing, and partitioning.
- [Multitenancy](https://github.com/pgvector/pgvector/blob/master/README.md#multitenancy): Tenant isolation for approximate indexes using list partitioning or separate tables.
- [Iterative Index Scans](https://github.com/pgvector/pgvector/blob/master/README.md#iterative-index-scans): Enabling iterative index scans for filtered queries, strict versus relaxed ordering, and scan options for HNSW and IVFFlat.
- [Binary Vectors](https://github.com/pgvector/pgvector/blob/master/README.md#binary-vectors): Storing binary vectors with the bit type and querying by Hamming or Jaccard distance.
- [Binary Quantization](https://github.com/pgvector/pgvector/blob/master/README.md#binary-quantization): Using expression indexing for binary quantization, querying by Hamming distance, and re-ranking for better recall.
- [Sparse Vectors](https://github.com/pgvector/pgvector/blob/master/README.md#sparse-vectors): Storing sparse vectors with the sparsevec type, the index:value format, and nearest neighbors by L2 distance.
- [Hybrid Search](https://github.com/pgvector/pgvector/blob/master/README.md#hybrid-search): Combining pgvector with Postgres full-text search using Reciprocal Rank Fusion or a cross-encoder.
- [Indexing Subvectors](https://github.com/pgvector/pgvector/blob/master/README.md#indexing-subvectors): Indexing subvectors with expression indexing, cosine distance search, and re-ranking by full vectors.
- [Performance](https://github.com/pgvector/pgvector/blob/master/README.md#performance): Tuning Postgres parameters, using halfvec, bulk loading with COPY, indexing, querying, and vacuuming tips.
- [Scaling](https://github.com/pgvector/pgvector/blob/master/README.md#scaling): Reducing the working set with halfvec and binary quantization, plus vertical and horizontal scaling options.
- [Monitoring](https://github.com/pgvector/pgvector/blob/master/README.md#monitoring): Monitoring performance with pg_stat_statements or PgHero, and checking recall against exact search.
- [Languages](https://github.com/pgvector/pgvector/blob/master/README.md#languages): Client libraries and examples for using pgvector from many languages, including Ada, Python, Ruby, and Rust.
- [Frequently Asked Questions](https://github.com/pgvector/pgvector/blob/master/README.md#frequently-asked-questions): Answers on storage limits, replication, high-dimension indexing, mixed dimensions, extra precision, and index memory.
- [Troubleshooting](https://github.com/pgvector/pgvector/blob/master/README.md#troubleshooting): Fixes for queries not using indexes or parallel scans, and fewer results after adding HNSW or IVFFlat indexes.
- [Reference](https://github.com/pgvector/pgvector/blob/master/README.md#reference): Reference for vector, halfvec, bit, and sparsevec types, with operators, functions, and aggregate functions.
- [Installation Notes - Linux and Mac](https://github.com/pgvector/pgvector/blob/master/README.md#installation-notes---linux-and-mac): Solutions for multiple Postgres installs, missing headers, missing SDKs, and portable compilation on Linux and Mac.
- [Installation Notes - Windows](https://github.com/pgvector/pgvector/blob/master/README.md#installation-notes---windows): Fixes for Windows installation errors: missing header, mismatched architecture, missing symbol with Postgres 17.0-17.2, and permissions.
- [Additional Installation Methods](https://github.com/pgvector/pgvector/blob/master/README.md#additional-installation-methods): Installing via Docker, Homebrew, PGXN, APT, and Yum, with supported Docker tags and the --shm-size note.
- [Upgrading](https://github.com/pgvector/pgvector/blob/master/README.md#upgrading): How to upgrade pgvector by installing the latest version and running ALTER EXTENSION UPDATE in each database.

## Optional

- [Changelog](https://raw.githubusercontent.com/pgvector/pgvector/master/CHANGELOG.md): Version-by-version list of bug fixes and improvements, including iterative index scans and HNSW and IVFFlat fixes.
