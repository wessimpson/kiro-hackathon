"""
Neo4j Database Client for Knowledge Graph Operations
"""
from neo4j import GraphDatabase, Driver
from typing import Optional, Dict, Any, List
import logging
from src.config.settings import settings

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Neo4j database client for knowledge graph operations"""
    
    def __init__(self):
        self.driver: Optional[Driver] = None
        self.uri = settings.neo4j_uri
        self.user = settings.neo4j_user
        self.password = settings.neo4j_password
    
    def connect(self) -> None:
        """Establish connection to Neo4j database"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("Successfully connected to Neo4j database")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self) -> None:
        """Close database connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query and return results"""
        if not self.driver:
            raise RuntimeError("Database connection not established")
        
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def create_node(self, node_type: str, properties: Dict[str, Any]) -> str:
        """Create a node in the knowledge graph"""
        query = f"""
        CREATE (n:{node_type} $properties)
        RETURN n.id as node_id
        """
        result = self.execute_query(query, {"properties": properties})
        return result[0]["node_id"] if result else None
    
    def create_relationship(self, from_node_id: str, to_node_id: str, 
                          relationship_type: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """Create a relationship between two nodes"""
        query = f"""
        MATCH (a), (b)
        WHERE a.id = $from_id AND b.id = $to_id
        CREATE (a)-[r:{relationship_type} $properties]->(b)
        RETURN r
        """
        self.execute_query(query, {
            "from_id": from_node_id,
            "to_id": to_node_id,
            "properties": properties or {}
        })
    
    def find_node(self, node_type: str, properties: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a node by type and properties"""
        where_clause = " AND ".join([f"n.{key} = ${key}" for key in properties.keys()])
        query = f"""
        MATCH (n:{node_type})
        WHERE {where_clause}
        RETURN n
        """
        result = self.execute_query(query, properties)
        return result[0]["n"] if result else None
    
    def get_user_knowledge_graph(self, user_id: str) -> Dict[str, Any]:
        """Retrieve complete knowledge graph for a user"""
        query = """
        MATCH (u:USER {user_id: $user_id})
        OPTIONAL MATCH (u)-[:HAS_SKILL]->(s:SKILL)
        OPTIONAL MATCH (u)-[:HAS_EXPERIENCE]->(e:EXPERIENCE)
        OPTIONAL MATCH (u)-[:CREATED_PROJECT]->(p:PROJECT)
        RETURN u as user,
               collect(DISTINCT s) as skills,
               collect(DISTINCT e) as experiences,
               collect(DISTINCT p) as projects
        """
        result = self.execute_query(query, {"user_id": user_id})
        return result[0] if result else {}
    
    def get_company_knowledge_graph(self, company_id: str) -> Dict[str, Any]:
        """Retrieve complete knowledge graph for a company"""
        query = """
        MATCH (c:COMPANY {id: $company_id})
        OPTIONAL MATCH (c)-[:OFFERS_JOB]->(j:JOB_POSTING)
        OPTIONAL MATCH (j)-[:REQUIRES_SKILL]->(r:REQUIREMENT)
        RETURN c as company,
               collect(DISTINCT j) as job_postings,
               collect(DISTINCT r) as requirements
        """
        result = self.execute_query(query, {"company_id": company_id})
        return result[0] if result else {}
    
    def calculate_job_match_score(self, user_id: str, job_id: str) -> float:
        """Calculate compatibility score between user and job"""
        query = """
        MATCH (u:USER {user_id: $user_id})-[:HAS_SKILL]->(us:SKILL)
        MATCH (j:JOB_POSTING {id: $job_id})-[:REQUIRES_SKILL]->(jr:REQUIREMENT)-[:RELATES_TO_SKILL]->(js:SKILL)
        WITH u, j, 
             count(DISTINCT us) as user_skills,
             count(DISTINCT js) as job_skills,
             count(DISTINCT CASE WHEN us.name = js.name THEN us END) as matching_skills
        RETURN CASE 
            WHEN job_skills = 0 THEN 0.0
            ELSE toFloat(matching_skills) / toFloat(job_skills)
        END as match_score
        """
        result = self.execute_query(query, {"user_id": user_id, "job_id": job_id})
        return result[0]["match_score"] if result else 0.0
    
    def setup_indexes(self) -> None:
        """Create database indexes for performance"""
        indexes = [
            "CREATE INDEX user_id_index IF NOT EXISTS FOR (u:USER) ON (u.user_id)",
            "CREATE INDEX skill_name_index IF NOT EXISTS FOR (s:SKILL) ON (s.name)",
            "CREATE INDEX company_name_index IF NOT EXISTS FOR (c:COMPANY) ON (c.name)",
            "CREATE INDEX job_title_index IF NOT EXISTS FOR (j:JOB_POSTING) ON (j.title)",
            "CREATE INDEX node_id_index IF NOT EXISTS FOR (n) ON (n.id)"
        ]
        
        for index_query in indexes:
            try:
                self.execute_query(index_query)
                logger.info(f"Created index: {index_query}")
            except Exception as e:
                logger.warning(f"Index creation failed or already exists: {e}")


# Global Neo4j client instance
neo4j_client = Neo4jClient()