import os
import json
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import logging
from google.cloud import bigquery
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """BigQuery database connection manager for e-commerce database"""
    
    def __init__(self, service_account_path: str = None, project_id: str = None, dataset_id: str = None):
        # Default paths and IDs
        if service_account_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            service_account_path = os.path.join(project_root, "config", "bq-key.json")
        
        self.service_account_path = service_account_path
        
        # Get project_id from service account file if not provided
        if project_id is None or dataset_id is None:
            try:
                with open(service_account_path, 'r') as f:
                    service_account_info = json.load(f)
                    if project_id is None:
                        project_id = service_account_info.get('project_id')
            except Exception as e:
                logger.error(f"Error reading service account file: {e}")
                raise
        
        self.project_id = project_id
        self.dataset_id = dataset_id or "ecommerce_data"
        
        # Initialize BigQuery client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize BigQuery client with service account credentials"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            self.client = bigquery.Client(credentials=credentials, project=self.project_id)
            logger.info(f"BigQuery client initialized for project: {self.project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize BigQuery client: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager for BigQuery client (for compatibility)"""
        try:
            yield self.client
        except Exception as e:
            logger.error(f"BigQuery error: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries"""
        try:
            # Handle parameterized queries for BigQuery
            if params:
                # Use proper BigQuery parameterized queries
                job_config = bigquery.QueryJobConfig()
                
                # Convert ? placeholders to named parameters
                formatted_query = query
                query_params = []
                
                for i, param in enumerate(params):
                    param_name = f"param_{i}"
                    formatted_query = formatted_query.replace('?', f"@{param_name}", 1)
                    
                    # Determine parameter type
                    if isinstance(param, str):
                        query_params.append(bigquery.ScalarQueryParameter(param_name, "STRING", param))
                    elif isinstance(param, int):
                        query_params.append(bigquery.ScalarQueryParameter(param_name, "INT64", param))
                    elif isinstance(param, float):
                        query_params.append(bigquery.ScalarQueryParameter(param_name, "FLOAT64", param))
                    else:
                        # Default to string
                        query_params.append(bigquery.ScalarQueryParameter(param_name, "STRING", str(param)))
                
                job_config.query_parameters = query_params
                query = formatted_query
                query_job = self.client.query(query, job_config=job_config)
            else:
                query_job = self.client.query(query)
            
            results = query_job.result()
            
            # Convert to list of dictionaries
            rows = []
            for row in results:
                rows.append(dict(row))
            
            return rows
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            logger.error(f"Query: {query}")
            if params:
                logger.error(f"Parameters: {params}")
            raise
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        try:
            # Handle parameterized queries
            if params:
                # Use proper BigQuery parameterized queries
                job_config = bigquery.QueryJobConfig()
                
                # Convert ? placeholders to named parameters
                formatted_query = query
                query_params = []
                
                for i, param in enumerate(params):
                    param_name = f"param_{i}"
                    formatted_query = formatted_query.replace('?', f"@{param_name}", 1)
                    
                    # Determine parameter type
                    if isinstance(param, str):
                        query_params.append(bigquery.ScalarQueryParameter(param_name, "STRING", param))
                    elif isinstance(param, int):
                        query_params.append(bigquery.ScalarQueryParameter(param_name, "INT64", param))
                    elif isinstance(param, float):
                        query_params.append(bigquery.ScalarQueryParameter(param_name, "FLOAT64", param))
                    else:
                        # Default to string
                        query_params.append(bigquery.ScalarQueryParameter(param_name, "STRING", str(param)))
                
                job_config.query_parameters = query_params
                query = formatted_query
                query_job = self.client.query(query, job_config=job_config)
            else:
                query_job = self.client.query(query)
            
            result = query_job.result()
            
            # BigQuery doesn't return affected rows the same way as SQLite
            # Return 1 for successful execution, 0 for no changes
            return 1 if query_job.state == 'DONE' else 0
        except Exception as e:
            logger.error(f"Update execution failed: {e}")
            logger.error(f"Query: {query}")
            if params:
                logger.error(f"Parameters: {params}")
            raise

    # Test helper methods (for test scripts only)
    def get_customer_info(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer information by ID (for testing)"""
        query = f"""
        SELECT _id, username, password, email, name, phone, address, created_date
        FROM `{self.project_id}.{self.dataset_id}.customers` 
        WHERE _id = ?
        """
        results = self.execute_query(query, (customer_id,))
        return results[0] if results else None
    
    def get_customer_orders(self, customer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get customer's orders (for testing)"""
        query = f"""
        SELECT _id, customer_id, product, sku, price, quantity, order_date, 
               status, status_detail, tracking_number, eta, updated_at
        FROM `{self.project_id}.{self.dataset_id}.orders`
        WHERE customer_id = ?
        ORDER BY order_date DESC
        LIMIT {limit}
        """
        return self.execute_query(query, (customer_id,))
    
    def get_customer_latest_order(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer's most recent order (for testing)"""
        query = f"""
        SELECT _id, customer_id, product, sku, price, quantity, order_date, 
               status, status_detail, tracking_number, eta, updated_at
        FROM `{self.project_id}.{self.dataset_id}.orders`
        WHERE customer_id = ?
        ORDER BY order_date DESC
        LIMIT 1
        """
        results = self.execute_query(query, (customer_id,))
        return results[0] if results else None
    
    def search_orders_by_status(self, customer_id: str, status: str) -> List[Dict[str, Any]]:
        """Search customer orders by status (for testing)"""
        query = f"""
        SELECT _id, customer_id, product, sku, price, quantity, order_date, 
               status, status_detail, tracking_number, eta, updated_at
        FROM `{self.project_id}.{self.dataset_id}.orders`
        WHERE customer_id = ? AND status = ?
        ORDER BY order_date DESC
        """
        return self.execute_query(query, (customer_id, status))
    
    def get_all_customers(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all customers (for testing)"""
        query = f"""
        SELECT _id, username, email, name, phone, created_date
        FROM `{self.project_id}.{self.dataset_id}.customers` 
        ORDER BY created_date DESC
        LIMIT {limit}
        """
        return self.execute_query(query, ())
    
    def get_sample_customers_for_ui(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get sample customers for UI (for testing)"""
        query = f"""
        SELECT _id, username, email, name, phone, created_date
        FROM `{self.project_id}.{self.dataset_id}.customers` 
        ORDER BY _id
        LIMIT {limit}
        """
        return self.execute_query(query, ())

# Global database instance for test scripts
db = DatabaseConnection() 