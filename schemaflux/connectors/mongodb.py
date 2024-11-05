import os
from typing import Any, List, Tuple
from pymongo import MongoClient
from .base import BaseConnector

class MongoDBConnector(BaseConnector):
    def __init__(self):
        super().__init__()
        self.client = None
        self.db = None

    def connect(self):
        """Establish MongoDB connection using environment variables."""
        try:
            mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
            db_name = os.environ.get('MONGODB_DATABASE', 'migrations')
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
        except Exception as e:
            raise Exception(f"MongoDB connection failed: {str(e)}")

    def execute(self, operation: str, params: Any = None) -> Any:
        """Execute single MongoDB operation."""
        try:
            # Parse and execute MongoDB operation
            op_type, collection, query = self._parse_operation(operation)
            query = self._replace_params(query, params)
            
            coll = self.db[collection]
            result = getattr(coll, op_type)(**query)
            
            self._query_count += 1
            if hasattr(result, 'modified_count'):
                self._operations_count += result.modified_count
            elif hasattr(result, 'inserted_ids'):
                self._operations_count += len(result.inserted_ids)
            return result
        except Exception as e:
            raise Exception(f"MongoDB operation failed: {str(e)}")

    def execute_batch(self, operations: List[Tuple[str, Any]]) -> None:
        """Execute multiple MongoDB operations in a batch."""
        try:
            for operation, params in operations:
                self.execute(operation, params)
        except Exception as e:
            raise Exception(f"MongoDB batch operation failed: {str(e)}")

    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()

    def _parse_operation(self, operation: str) -> Tuple[str, str, dict]:
        """Parse MongoDB operation string into components."""
        try:
            # Example format: "insert_many:users:{'documents': []}"
            op_type, collection, query = operation.split(':', 2)
            query = eval(query)  # Convert string representation to dict
            return op_type, collection, query
        except Exception as e:
            raise Exception(f"Invalid MongoDB operation format: {str(e)}")

    def _replace_params(self, query: dict, params: Any) -> dict:
        """Replace parameters in the query with actual values."""
        if not params:
            return query
        
        # If params is a dict, update the query with it
        if isinstance(params, dict):
            query.update(params)
        return query
