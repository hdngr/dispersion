Dispersion
==========
### Overview

The following is a python implementation of the dispersion algrotithm recently defined by 
Lars Backstrom and Jon Kleinberg here: http://arxiv.org/pdf/1310.6753v1.pdf.

In english, dispersion is a score for each indivdual (v) in a person's (u) network (G_u)
where the dispersion articulates how 'far apart' their mutual connections are.

Dispersion has the ability to predict the spouse of a facebook user with up to 60% accuracy.
*The implementation here is normalized with embededness (~50% accuracy)*

### Usage

I will be submitting a pull request to networkx to include 'disperion centrality' in the next
release.  In the meantime:

* Clone this repo
* in a python shell:
        `from dispersion import *`
* load the *network_json.json* file from the *data* directory
* `dispersion(network_json, 1)` will return a dictionary of the absolute and normalized dispersion score for all nodes in my network.

### Implementation
* Data: is a GraphAlchemist network json object.  More later on how you can create your ego network using facebook oauth.
* We used just 4 lines of cypher to query the data from neo4j *./cypher/

Feedback and tips on optimization welcome.

