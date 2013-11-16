// A sample cypher query for returning a user's ego network
// TODO: optimize
MATCH p = (n)-[r:FRIEND]-(nn), pp = (nn)-[rr:FRIEND]-(nnn)-[:FRIEND]-(n)
WHERE ID(n) = {some_internal_id}
WITH (NODES(p) + NODES(pp)) as nodes, 
     (RELATIONSHIPS(p) + RELATIONSHIPS(pp)) as rels     
RETURN DISTINCT nodes, rels;
                
