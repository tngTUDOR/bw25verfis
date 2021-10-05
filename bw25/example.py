"""Example code to do LCA with bw2."""
import random

import bw2calc as bc

# import bw2analyzer as ba
import bw2data as bd
import bw2io as bi
import bw_processing as bp
import matrix_utils as mu

# Start a new project
bd.projects.set_current("product project")
# Create biosphere3 database
bi.bw2setup()
# Gather some random flows from a method
# to use as inputs of a fake Activity
a_method = bd.Method(random.choice(sorted(bd.methods)))
cfs = a_method.load()
some_cfs = random.choices(cfs, k=10)
expected_score = sum([cf[1] for cf in some_cfs])
product_db = bd.Database("products")
product_data = {
    "name": "Fake product A",
    "unit": "kilogram",
    "exchanges": [
        {"amount": 1, "type": "biosphere", "input": flow[0]} for flow in some_cfs
    ],
}
product_db.write({("products", "productA"): product_data})

product_a = product_db.get("productA")

product_lca = bc.LCA({product_a: 1}, a_method.name)
product_lca.lci()
product_lca.lcia()

assert expected_score == product_lca.score
