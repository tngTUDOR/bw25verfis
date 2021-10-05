##########
bw25verfis
##########

A repository with some tools to test brightway25.

This repository holds containerfiles describing a reproducible environment
to test brightway25.

+ ``bw25`` . To test brightway25 with a Linux-based continuumio/miniconda3 image

*************
Docker images
*************

bw25
====

Use
---

Build the container images, and then create a container to run the tests.

1. Building images 

   1.a with Buildah 

          .. code-block:: bash

                buildah bud -t bw25:latest -f bw25/Containerfile bw25/

2. Run code inside the container

   2.a with Podman

          .. code-block:: bash

                podman run -it bw25:latest

        Once inside the container, try:

        .. code-block:: python

                import bw2analyzer as ba
                import bw2data as bd
                import bw2calc as bc
                import bw2io as bi
                import matrix_utils as mu
                import bw_processing as bp
                import random

                # Create biosphere3 database
                bi.bw2setup()
                # Gather some random flows from a method
                # to use as inputs of a fake Activity
                a_method = bd.Method(random.choice(sorted(bd.methods)))
                cfs = a_method.load()
                some_cfs = random.choices(cfs, k=10)
                expected_score = sum([cf[1] for cf in some_cfs])
                product_db = bd.Database("products")
                product_data = {"name": "Fake product A", 
                        "unit":"kilogram", 
                        "exchanges":[
                            {"amount":1,"type":"biosphere","input":flow[0]} for flow in some_cfs ]
                        }
                product_db.write({("products", "productA"): product_data})

                product_a = product_db.get("productA")

                product_lca = bc.LCA({product_a:1}, a_method.name)
                product_lca.lci()
                product_lca.lcia()

                assert expected_score == product_lca.score


Base image
----------

``continuumio/miniconda3``

Requirements
------------

+ ``brightway25``
+ ``bw2ui``
