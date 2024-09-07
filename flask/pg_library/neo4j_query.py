#!/usr/bin/env python3
# Ben Payne
# Physics Derivation Graph
# https://allofphysics.com

# Creative Commons Attribution 4.0 International License
# https://creativecommons.org/licenses/by/4.0/

"""
queries for Neo4j, written in Cypher


TODO: view current schema
https://neo4j.com/docs/getting-started/current/cypher-intro/schema/
https://neo4j.com/developer/kb/viewing-schema-data-with-apoc/



# CYPHER help
* <https://neo4j.com/docs/cypher-manual/current>
* <https://neo4j.com/docs/cypher-refcard/current/>
* https://gist.github.com/DaniSancas/1d5265fc159a95ff457b940fc5046887

In Cypher queries
- parenthesis indicate a node
- in `p:Person` the `p` is a variable and node label is `Person`
- {} brackets to add properties (key-value pairs) to the node

"""

import neo4j  # needed for exception handling
import random  # for trace IDs
from typing import Dict, List

import list_of_valid


def list_IDs(tx, node_type: str) -> List[str]:
    """
    for a specific node type (e.g., derivation XOR step XOR symbol, etc)
    return a list of all PDG IDs for the nodes

    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/list_IDs start " + trace_id)

    print("neo4j_query/list_IDs: node_type=", node_type)
    assert node_type in list_of_valid.node_types

    list_of_IDs = []  # type:List[str]
    for result in tx.run("MATCH (n:" + node_type + ") RETURN n.id"):
        # print(result.data())
        list_of_IDs.append(result.data()["n.id"])

    print("[TRACE] func: neo4j_query/list_IDs end " + trace_id)
    return list_of_IDs


def apoc_export_json(tx, output_filename: str):
    """
    https://neo4j.com/labs/apoc/4.4/overview/apoc.export/apoc.export.json.all/

    The output file is written to disk within the neo4j container.
    For the PDG, docker-compose has a shared folder on the host accessible both Neo4j and Flask.
    The file from neo4j can then be accessed by Flask for providing to the user via the web interface.

    >>> apoc_export_json(tx)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/apoc_export_json start " + trace_id)

    for result in tx.run(
        "CALL apoc.export.json.all('" + output_filename + "',{useTypes:true})"
    ):
        pass

    print("[TRACE] func: neo4j_query/apoc_export_json end " + trace_id)
    return result


def apoc_export_cypher(tx, output_filename: str):
    """
    https://neo4j.com/labs/apoc/4.4/export/cypher/


    The output file is written to disk within the neo4j container.
    For the PDG, docker-compose has a shared folder on the host accessible both Neo4j and Flask.
    The file from neo4j can then be accessed by Flask for providing to the user via the web interface.

    >>> apoc_export_cypher(tx)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/apoc_export_cypher start " + trace_id)

    # "cypher.all" produces 1 file with constraints
    # https://neo4j.com/labs/apoc/4.4/overview/apoc.export/apoc.export.cypher.all/
    # TODO: possibly switch to
    # https://neo4j.com/labs/apoc/4.4/overview/apoc.export/apoc.export.cypher.query/
    # which produces separate files for relationships and nodes

    for result in tx.run(
        "CALL apoc.export.cypher.all('" + output_filename + "', {"
        "format: 'cypher-shell',"
        "useOptimizations: {type: 'UNWIND_BATCH', unwindBatchSize: 20}"
        "}) "
        "YIELD file, batches, source, format, nodes, relationships, properties, time, rows, batchSize "
        "RETURN file, batches, source, format, nodes, relationships, properties, time, rows, batchSize;"
    ):
        pass

    print("[TRACE] func: neo4j_query/apoc_export_cypher end " + trace_id)
    return result


def constrain_unique_id(tx) -> None:
    """
    https://neo4j.com/docs/getting-started/current/cypher-intro/schema/#cypher-intro-constraints

    >>> constrain_unique_id()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/constrain_unique_id start " + trace_id)

    for node_type in list_of_valid.node_types:
        # try:
        tx.run(
            "CREATE CONSTRAINT constrain_"
            + node_type
            + "_id FOR (n:"
            + node_type
            + ") REQUIRE n.id IS UNIQUE"
        )
        # except Exception as err:
        #     print("neo4j/constrain_unique_id: WARNING:", err)

    print("[TRACE] func: neo4j_query/constrain_unique_id end " + trace_id)
    return


def get_scalar_id_that_has_value_and_units_id(tx, value_and_units_id: str):
    """
    >>>
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/get_scalar_id_that_has_value_and_units_id start "
        + trace_id
    )
    result = tx.run(
        "MATCH (s:scalar)-[]->(v:value_with_units) WHERE v.id='"
        + value_and_units_id
        + "' RETURN s.id"
    )

    scalar_id = result.data()
    print("neo4j_query/get_scalar_id_that_has_value_and_units_id: scalar_id", scalar_id)

    print(
        "[TRACE] func: neo4j_query/get_scalar_id_that_has_value_and_units_id end "
        + trace_id
    )
    return scalar_id


def get_list_of_symbol_IDs_per_category_in_expression_or_feed(
    tx, expression_or_feed: str, expression_or_feed_id: str, symbol_category: str
) -> List[str]:
    """
    an expression has one or more sybmols
    This read query returns which symbol IDs are used for the provided expression ID

    this is the opposite query of `expressions_that_use_symbol`

    >>> get_list_of_symbol_IDs_in_expression_or_feed()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/get_list_of_symbol_IDs_in_expression_or_feed start "
        + trace_id
    )

    print(
        "neo4j_query/get_list_of_symbol_IDs_in_expression_or_feed: symbol_category=",
        symbol_category,
    )

    print("neo4j_query/list_IDs: expression_or_feed=", expression_or_feed)
    assert expression_or_feed in ["expression", "feed"]
    print("neo4j_query/list_IDs: symbol_category=", symbol_category)
    assert symbol_category in list_of_valid.symbol_categories

    symbol_list = []  # type:List[str]
    for result in tx.run(
        "MATCH (e:"
        + expression_or_feed
        + ")-[:HAS_SYMBOL]->(s:"
        + symbol_category
        + ") WHERE e.id='"
        + expression_or_feed_id
        + "' RETURN s.id"
    ):
        symbol_list.append(result.data()["s.id"])
    print("expression_or_feed_id=", expression_or_feed_id, "symbol_list=", symbol_list)

    print(
        "[TRACE] func: neo4j_query/get_list_of_symbol_IDs_in_expression_or_feed end "
        + trace_id
    )
    return symbol_list


# def symbols_in_feed(tx, feed_id: str, symbol_category: str) -> list:
#     """
#     a feed has one or more sybmols
#     This read query returns which symbol IDs are used for the provided feed ID

#     this is the opposite query of `feeds_that_use_symbol`

#     """
#     trace_id = str(random.randint(1000000, 9999999))
#     print("[TRACE] func: neo4j_query/symbols_in_feed start " + trace_id)

#     print("neo4j_query/symbols_in_feed: symbol_category=", symbol_category)

#     assert symbol_category in list_of_valid.symbol_categories

#     symbol_list = []
#     for result in tx.run(
#         "MATCH (e:feed)-[:HAS_SYMBOL]->(s:'"
#         + symbol_category
#         + "') WHERE e.id='"
#         + feed_id
#         + "' RETURN s.id"
#     ):
#         symbol_list.append(result.data()["s.id"])
#     print("feed_id=", feed_id, "symbol_list=", symbol_list)

#     print("[TRACE] func: neo4j_query/symbols_in_feed end " + trace_id)
#     return symbol_list


def get_list_node_dicts_of_type(tx, node_type: str) -> list:
    """
    for a specific node type (e.g., derivation XOR step XOR symbol, etc)
    return a list of all nodes

    >>> list_nodes_of_type(tx)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/get_list_node_dicts_of_type start " + trace_id)

    # must be one of these node types. See also 'schema.log' file
    print("neo4j_query/get_list_node_dicts_of_type:  node type:", node_type)
    assert node_type in list_of_valid.node_types

    node_list = []  # type:List[dict]
    for result in tx.run("MATCH (n:" + node_type + ") RETURN n"):
        # print(result.data()["n"])
        node_list.append(result.data()["n"])

    print("[TRACE] func: neo4j_query/get_list_node_dicts_of_type end " + trace_id)
    return node_list


def get_derivation_dicts_that_use_feed(tx, feed_id: str) -> list:
    """ """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/get_derivation_dicts_that_use_feed start " + trace_id
    )
    print("neo4j_query/get_derivation_dicts_that_use_feed: feed_id=", feed_id)

    # TODO: this should be derivation->step->feed
    list_of_derivation_dicts = []  # type:List[dict]
    for result in tx.run(
        'MATCH (d:derivation)-[]->(s:step)-[]->(f:feed) WHERE f.id = "'
        + str(feed_id)
        + '" RETURN d'
    ):
        list_of_derivation_dicts.append(result.data()["d"])

    print(
        "[TRACE] func: neo4j_query/get_derivation_dicts_that_use_feed end " + trace_id
    )
    return list_of_derivation_dicts


def derivations_that_use_inference_rule(tx, inference_rule_id: str) -> list:
    """
    which derivations contain this inference rule?

    >>> derivations_that_use_inference_rule()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/derivations_that_use_inference_rule start "
        + trace_id
    )

    print(
        "neo4j_query/derivations_that_use_inference_rule: inference_rule_id=",
        inference_rule_id,
    )

    list_of_derivation_dicts = []  # type:List[dict]
    for result in tx.run(
        'MATCH (d:derivation)-[]->(s:step)-[]->(i:inference_rule) WHERE i.id = "'
        + str(inference_rule_id)
        + '" RETURN d'
    ):
        list_of_derivation_dicts.append(result.data()["d"])
        # print("list_of_derivations=", list_of_derivations)

    # print(
    #     "inference_rule_id=",
    #     inference_rule_id,
    #     "list_of_derivations=",
    #     list_of_derivation_dicts,
    # )

    print(
        "[TRACE] func: neo4j_query/derivations_that_use_inference_rule end " + trace_id
    )
    return list_of_derivation_dicts


def get_list_of_expression_dicts_that_use_symbol_id_by_category(
    tx, symbol_id: str, symbol_category: str
) -> list:
    """
    which expressions contain this symbol?

    >>> expressions_that_use_symbol()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/get_list_of_expression_dicts_that_use_symbol_id_by_category start "
        + trace_id
    )

    print(
        "neo4j_query/get_list_of_expression_dicts_that_use_symbol_id_by_category: symbol_category=",
        symbol_category,
    )

    assert symbol_category in list_of_valid.symbol_categories

    list_of_expression_dicts = []  # type: List[dict]

    for result in tx.run(
        "MATCH (e:expression)-[r]->(s:"
        + symbol_category
        + ") WHERE s.id = '"
        + str(symbol_id)
        + "' RETURN e"
    ):
        list_of_expression_dicts.append(result.data()["e"])

    print(
        "neo4j_query/get_list_of_expression_dicts_that_use_symbol_id_by_category: symbol_id=",
        symbol_id,
        "list_of_expressions=",
        list_of_expression_dicts,
    )

    print(
        "[TRACE] func: neo4j_query/get_list_of_expression_dicts_that_use_symbol_id_by_category end "
        + trace_id
    )
    return list_of_expression_dicts


def get_list_of_derivation_dicts_that_use_symbol_id_by_category(
    tx, symbol_id: str, symbol_category: str
) -> list:
    """
    which derivations contain this symbol?

    >>> derivations_that_use_symbol()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/get_list_of_derivation_dicts_that_use_symbol_id_by_category start "
        + trace_id
    )

    print(
        "neo4j_query/get_list_of_derivation_dicts_that_use_symbol_id_by_category: symbol_category=",
        symbol_category,
    )
    assert symbol_category in list_of_valid.symbol_categories

    list_of_derivation_dicts = []  # type: List[dict]

    # TODO: should be derivation->step->expression->symbol
    for result in tx.run(
        "MATCH (d:derivation)-[]->(:step)-[]->(:expression)-[]->(s:"
        + symbol_category
        + ") WHERE s.id = '"
        + str(symbol_id)
        + "' RETURN d"
    ):
        list_of_derivation_dicts.append(result.data()["d"])

    #    print("symbol_id=", symbol_id, "list_of_derivations=", list_of_derivation_dicts)

    print(
        "[TRACE] func: neo4j_query/get_list_of_derivation_dicts_that_use_symbol_id_by_category end "
        + trace_id
    )
    return list_of_derivation_dicts


def get_list_of_value_dicts_for_constant_id(tx, scalar_id: str) -> list:
    """
    >>>
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/get_list_of_value_dicts_for_constant_id start "
        + trace_id
    )
    print("neo4j_query/get_list_of_value_dicts_for_constant_id: scalar_id=", scalar_id)

    list_of_value_dicts = []  # type: List[dict]
    for result in tx.run(
        'MATCH (s:scalar {id:"' + scalar_id + '"})-[]->(v:value_with_units) RETURN v',
    ):
        list_of_value_dicts.append(result.data()["v"])
    print(
        "[TRACE] func: neo4j_query/get_list_of_value_dicts_for_constant_id start "
        + trace_id
    )
    return list_of_value_dicts


def get_list_of_step_dicts_in_this_derivation(tx, derivation_id: str) -> list:
    """
    For a given derivation, what are all the associated step IDs?

    >>> get_list_of_step_dicts_in_this_derivation(tx)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/get_list_of_step_dicts_in_this_derivation start "
        + trace_id
    )

    list_of_step_dicts = []  # type: List[dict]
    for result in tx.run(
        'MATCH (d:derivation {id:"'
        + derivation_id
        + '"})-[r:HAS_STEP]->(s:step) RETURN r.sequence_index,s',
    ):
        res = result.data()

        print("neo4j_query/get_list_of_step_dicts_in_this_derivation: res=", res)
        # res= {'r.sequence_index': 0, 's': {'note_after_step_latex': '', 'author_name_latex': 'ben', 'id': '4022988', 'created_datetime': '2024-06-02_21-40-52-881678', 'note_before_step_latex': ''}}

        this_step_dict = res["s"]
        # print(
        #     "neo4j_query/get_list_of_step_dicts_in_this_derivation: this_step_dict=",
        #     this_step_dict,
        # )

        this_step_index = res["r.sequence_index"]
        print(
            "neo4j_query/get_list_of_step_dicts_in_this_derivation: this_step_index_dict=",
            this_step_index,
        )

        # add sequence_index property value to dict
        this_step_dict["sequence_index"] = this_step_index

        list_of_step_dicts.append(this_step_dict)

    print(
        "[TRACE] func: neo4j_query/get_list_of_step_dicts_in_this_derivation end "
        + trace_id
    )
    return list_of_step_dicts


def step_has_sequence_index(tx, step_id: str) -> int:
    """
    >>> step_has_sequence_index()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/step_has_sequence_index start " + trace_id)
    sequence_index = 0
    result = tx.run(
        'MATCH ()-[r:HAS_STEP]->(n:step {id:"' + step_id + '"}) RETURN r.sequence_index'
    )
    # print(type(result)) # don't access the `result` variable more than once, as mentioned on https://neo4j.com/docs/python-manual/current/transformers/
    sequence_index = result.data()[0]["r.sequence_index"]
    print("neo4j_query/step_has_sequence_index: sequence_index=", sequence_index)

    print("[TRACE] func: neo4j_query/step_has_sequence_index end " + trace_id)
    return sequence_index


def step_has_inference_rule(tx, step_id: str):
    """
    use case: when displaying a derivation, user wants to see inference rule per step

    >>> step_has_inference_rule()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/step_has_inference_rule start " + trace_id)

    result = tx.run(
        'MATCH (n:step {id:"'
        + step_id
        + '"})-[r:HAS_INFERENCE_RULE]->(m:inference_rule) RETURN m'
    )
    # print(type(result)) # don't access the `result` variable more than once, as mentioned on https://neo4j.com/docs/python-manual/current/transformers/
    inf_rule_list_of_dicts = result.data()
    # print(type(inf_rule_result))  # <class 'list'>
    # print(len(inf_rule_result))  # 0
    # print(inf_rule_result)
    # [{'m': {'name_latex': 'add x to both sides', 'number_of_outputs': 1, 'number_of_inputs': 1, 'author_name_latex': 'ben', 'number_of_feeds': 1, 'id': '8818915', 'latex': 'add $1 to both sides of Eq $2 to get Eq $3'}}]

    print("[TRACE] func: neo4j_query/step_has_inference_rule end " + trace_id)
    return inf_rule_list_of_dicts[0]["m"]


def get_derivation_id_from_step_id(tx, step_id: str) -> str:
    """
    >>>
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/get_derivation_id_from_step_id start " + trace_id)

    print("neo4j_query/get_derivation_id_from_step_id: step_id=", step_id)

    result = tx.run(
        'MATCH (d:derivation)-[r:"HAS_STEP"]->(:step {"id":"'
        + step_id
        + "}) RETURN d.id"
    )

    derivation_id = result.data()

    print("neo4j_query/get_derivation_id_from_step_id: derivation_id=", derivation_id)

    print("[TRACE] func: neo4j_query/get_derivation_id_from_step_id end " + trace_id)
    return derivation_id


def get_list_of_expression_dicts_from_step_id_and_expr_type(
    tx, step_id: str, expression_type: str
) -> list:
    """
    use case: when displaying a derivation,
    for each step the user wants to know the inputs, feeds, and outputs.

    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/get_list_of_expression_dicts_from_step_id_and_expr_type start "
        + trace_id
    )

    print(
        "neo4j_query/step_has_expressions: step_id=",
        step_id,
        "; expression_type=",
        expression_type,
    )
    assert (
        expression_type == "HAS_INPUT"
        or expression_type == "HAS_FEED"
        or expression_type == "HAS_OUTPUT"
    )

    # print("TODO: figure out how to get the sequence_index for this expression")
    # print(
    #     'MATCH (n:step {id:"'
    #     + step_id
    #     + '"})-[r:'
    #     + expression_type
    #     + "]->(m:expression) RETURN m"
    # )

    list_of_expression_dicts = []  # type:List[dict]

    if expression_type == "HAS_FEED":
        destination_node_type = "feed"
    else:
        destination_node_type = "expression"

    print(
        'MATCH (:step {id:"'
        + step_id
        + '"})-[r:'
        + expression_type
        + "]->(m:"
        + destination_node_type
        + ") RETURN m"
    )

    for result in tx.run(
        'MATCH (:step {id:"'
        + step_id
        + '"})-[r:'
        + expression_type
        + "]->(m:"
        + destination_node_type
        + ") RETURN m"
    ):
        # print(result.data())
        list_of_expression_dicts.append(result.data())

    print("list_of_expression_dicts=", list_of_expression_dicts)

    print(
        "[TRACE] func: neo4j_query/get_list_of_expression_dicts_from_step_id_and_expr_type end "
        + trace_id
    )
    return list_of_expression_dicts


def get_node_properties(tx, node_type: str, node_id: str) -> dict:
    """
    metadata associated with the node_id

    >>> node_properties()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/node_properties start " + trace_id)

    print("neo4j_query/node_properties: node_type=", node_type)
    assert node_type in list_of_valid.node_types
    print("neo4j_query/node_properties: node_id:", node_id)

    result = tx.run(
        "MATCH (n: " + str(node_type) + ') WHERE n.id = "' + str(node_id) + '" RETURN n'
    )
    # node_data = result.data()['n']
    node_data = result.data()[0]["n"]
    print("neo4j_query/node_properties: node_data=", node_data)

    print("[TRACE] func: neo4j_query/node_properties end " + trace_id)
    return node_data


def add_derivation(
    tx,
    derivation_id: str,
    now_str: str,
    derivation_name_latex: str,
    derivation_abstract_latex: str,
    derivation_reference_latex: str,
    author_name_latex: str,
) -> None:
    """
    Create a new derivation node

    >>> add_derivation(tx)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_derivation start " + trace_id)

    print(
        derivation_id,
        now_str,
        derivation_name_latex,
        derivation_abstract_latex,
        author_name_latex,
    )

    result = tx.run(
        "merge (:derivation "
        '{name_latex:"' + derivation_name_latex + '",'
        ' abstract_latex:"' + derivation_abstract_latex + '",'
        ' created_datetime:"' + now_str + '",'
        ' reference_latex:"' + derivation_reference_latex + '",'
        ' author_name_latex:"' + author_name_latex + '",'
        ' id:"' + derivation_id + '"})'
    )

    print("[TRACE] func: neo4j_query/add_derivation end " + trace_id)
    return


def add_inference_rule(
    tx,
    inference_rule_id: str,
    inference_rule_name: str,
    inference_rule_latex: str,
    author_name_latex: str,
    number_of_inputs: int,
    number_of_feeds: int,
    number_of_outputs: int,
):
    """
    the "number_of_" are passed in as integers,
    but when writing the query string they are
    cast to integers to enable concatenation, but
    Neo4j sees the query as containing integers.

    >>> add_inference_rule(tx,)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_inference_rule start " + trace_id)

    assert (
        (int(number_of_inputs) > 0)
        or (int(number_of_feeds) > 0)
        or (int(number_of_outputs) > 0)
    )
    assert int(number_of_inputs) >= 0
    assert int(number_of_feeds) >= 0
    assert int(number_of_outputs) >= 0

    result = tx.run(
        "merge (:inference_rule "
        '{name_latex:"' + inference_rule_name + '", '
        ' latex:"' + inference_rule_latex + '", '
        ' author_name_latex:"' + author_name_latex + '", '
        ' id:"' + inference_rule_id + '", '
        " number_of_inputs:" + str(number_of_inputs) + ", "
        " number_of_feeds:" + str(number_of_feeds) + ", "
        " number_of_outputs:" + str(number_of_outputs) + "})"
    )

    print("[TRACE] func: neo4j_query/add_inference_rule end " + trace_id)
    return


def edit_step_notes(
    tx, step_id: str, note_before_step_latex: str, note_after_step_latex: str
) -> None:
    """
    TODO: deprecate this in favor of edit_node_properties
    see https://gist.github.com/DaniSancas/1d5265fc159a95ff457b940fc5046887#update-node-properties-add-new-or-modify

    >>> edit_step_notes()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/edit_step_notes start " + trace_id)

    result = tx.run(
        'MERGE (s:step {id:"' + str(step_id) + '", '
        'SET s ={id:"' + str(step_id) + '", '
        'note_before_step_latex: "' + str(note_before_step_latex) + '", '
        'note_before_step_latex: "' + str(note_after_step_latex) + '"}'
    )

    print("[TRACE] func: neo4j_query/edit_step_notes end " + trace_id)
    return


def edit_expression(
    tx,
    expression_id: str,
    expression_latex_lhs: str,
    expression_latex_relation: str,
    expression_latex_rhs: str,
    expression_latex_condition: str,
    expression_name_latex: str,
    expression_description_latex: str,
    expression_reference_latex: str,
    now_str: str,
    author_name_latex: str,
) -> None:
    """
    see https://gist.github.com/DaniSancas/1d5265fc159a95ff457b940fc5046887#update-node-properties-add-new-or-modify

    >>> edit_expression()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/edit_expression start " + trace_id)

    result = tx.run(
        'MERGE (e:expression {id:"' + str(expression_id) + '"})'
        'SET e = {id: "' + str(expression_id) + '",'
        'name_latex: "' + str(expression_name_latex) + '",'
        'description_latex: "' + str(expression_description_latex) + '",'
        'reference_latex: "' + str(expression_reference_latex) + '",'
        'created_datetime:"' + now_str + '",'
        'author_name_latex:"' + author_name_latex + '",'
        'latex_lhs: "' + str(expression_latex_lhs) + '",'
        'latex_relation: "' + str(expression_latex_relation) + '",'
        'latex_rhs: "' + str(expression_latex_rhs) + '",'
        'latex_condition: "' + str(expression_latex_condition) + '"}'
    )

    print("[TRACE] func: neo4j_query/edit_expression end " + trace_id)
    return


# def edit_feed(
#     tx,
#     feed_id: str,
#     feed_latex: str,
#     feed_name: str,
#     feed_description: str,
#     now_str: str,
#     author_name_latex: str,
# ) -> None:
#     """
#     >>> edit_feed()
#     """
#     trace_id = str(random.randint(1000000, 9999999))
#     print("[TRACE] func: neo4j_query/edit_feed start " + trace_id)

#     result = tx.run(
#         'MERGE (e:feed {id:"' + str(feed_id) + '"})'
#         'SET e = {id: "' + str(feed_id) + '",'
#         'name_latex: "' + str(feed_name) + '",'
#         'description_latex: "' + str(feed_description) + '",'
#         'created_datetime:"' + now_str + '",'
#         'author_name_latex:"' + author_name_latex + '",'
#         'latex: "' + str(feed_latex) + '"}'
#     )

#     print("[TRACE] func: neo4j_query/edit_feed end " + trace_id)
#     return


def edit_node_property(
    tx, node_type: str, node_id: str, property_key: str, property_value
) -> None:
    """
    property_value can be either str or int

    see https://gist.github.com/DaniSancas/1d5265fc159a95ff457b940fc5046887#update-node-properties-add-new-or-modify
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/edit_node_property start " + trace_id)

    print(
        "node_type=",
        node_type,
        ", node_id=",
        node_id,
        ",property_key=",
        property_key,
        ", property_value=",
        property_value,
    )
    assert node_type in list_of_valid.node_types

    # https://neo4j.com/docs/getting-started/cypher-intro/updating/

    # https://stackoverflow.com/a/15019884/1164295 says "bool is a subclass of int."
    if isinstance(property_value, int):
        result = tx.run(
            "MERGE (n:" + str(node_type) + ' {id:"' + str(node_id) + '"})'
            "SET n." + str(property_key) + " = " + str(property_value)
        )
    elif isinstance(property_value, str):  # string needs quotes
        result = tx.run(
            "MERGE (n:" + str(node_type) + ' {id:"' + str(node_id) + '"})'
            "SET n." + str(property_key) + ' = "' + str(property_value) + '"'
        )

    print("[TRACE] func: neo4j_query/edit_node_property end" + trace_id)
    return


def edit_derivation_metadata(
    tx,
    derivation_id: str,
    derivation_name_latex: str,
    abstract_latex: str,
    now_str: str,
    author_name_latex: str,
) -> None:
    """
    TODO: deprecate this in favor of modify node properties

    >>> edit_derivation_metadata()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/edit_derivation_metadata start " + trace_id)

    result = tx.run(
        'MERGE (d:derivation {id:"' + str(derivation_id) + '"})'
        'SET d = {id: "' + str(derivation_id) + '",'
        'name_latex: "' + str(derivation_name_latex) + '",'
        'created_datetime:"' + now_str + '",'
        'author_name_latex:"' + author_name_latex + '",'
        'abstract_latex: "' + str(abstract_latex) + '"}'
    )
    #'SET d.derivation_name_latex = "'+ str(derivation_name_latex) +'", '
    #'SET d.abstract_latex = "'+ str(abstract_latex) +'"})'

    print("[TRACE] func: neo4j_query/edit_derivation_metadata end " + trace_id)
    return


def disconnect_step_from_inference_rule(tx, step_id: str) -> None:
    """
    called by "delete derivation"

    https://stackoverflow.com/questions/57553886/neo4j-what-happens-to-a-directional-relationship-when-one-node-is-deleted

    as part of this sequence:
     1) for each step,
           * disconnect step from inference rule (remove edge)
           * disconnect step from expressions (remove edge)
           * disconnect step from derivation (remove edge)
           * delete step node
     2) delete derivation node
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/disconnect_step_from_inference_rule start "
        + trace_id
    )
    # TODO
    print("not doing anything yet")
    print(
        "[TRACE] func: neo4j_query/disconnect_step_from_inference_rule end " + trace_id
    )
    return


def delete_node(tx, node_id: str, node_type) -> None:
    """
    called by "delete derivation"

    https://stackoverflow.com/questions/57553886/neo4j-what-happens-to-a-directional-relationship-when-one-node-is-deleted

    as part of this sequence:
     1) for each step, delete step node. All associated edges disappear automatically
     2) delete derivation node

    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/delete_node start " + trace_id)

    # must be one of these node types. See also 'schema.log' file
    print("neo4j_query/delete_node: node_type=", node_type)
    assert node_type in list_of_valid.node_types

    result = tx.run(
        "MATCH (d:" + node_type + ' {id:"' + node_id + '"}) DETACH DELETE d'
    )
    print("result.data=", result.data())

    print("[TRACE] func: neo4j_query/delete_node end " + trace_id)
    return


def disconnect_symbol_from_expression(
    tx, symbol_id: str, expression_id: str, symbol_category: str
) -> None:
    """
    called by "edit expression"

    https://neo4j.com/docs/cypher-manual/current/clauses/delete/
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/disconnect_symbol_from_expression start " + trace_id
    )

    print(
        "neo4j_query/disconnect_symbol_from_expression: symbol_category=",
        symbol_category,
    )
    assert symbol_category in list_of_valid.symbol_categories

    result = tx.run(
        "MATCH (e:expression)-[r:HAS_SYMBOL]->(s:"
        + symbol_category
        + ")"
        + 'WHERE e.id="'
        + str(expression_id)
        + '" AND s.id="'
        + str(symbol_id)
        + '"  DELETE r'
    )
    print("result.data=", result.data())

    print("[TRACE] func: neo4j_query/disconnect_symbol_from_expression end " + trace_id)
    return


def disconnect_symbol_from_feed(
    tx, symbol_id: str, feed_id: str, symbol_category: str
) -> None:
    """
    called by "edit feed"

    https://neo4j.com/docs/cypher-manual/current/clauses/delete/
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/disconnect_symbol_from_feed start " + trace_id)

    print("neo4j_query/disconnect_symbol_from_feed: symbol_category=", symbol_category)
    assert symbol_category in list_of_valid.symbol_categories

    result = tx.run(
        "MATCH (e:feed)-[r:HAS_SYMBOL]->(s:"
        + symbol_category
        + ")"
        + 'WHERE e.id="'
        + str(feed_id)
        + '" AND s.id="'
        + str(symbol_id)
        + '"  DELETE r'
    )
    print("result.data=", result.data())

    print("[TRACE] func: neo4j_query/disconnect_symbol_from_feed end " + trace_id)
    return


def add_symbol_to_expression_or_feed(
    tx,
    expression_or_feed: str,
    symbol_id: str,
    expression_or_feed_id: str,
    symbol_category: str,
) -> None:
    """ """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_symbol_to_expression start " + trace_id)
    print("symbol_id=", symbol_id, "expression_or_feed_id=", expression_or_feed_id)

    print(
        "neo4j_query/add_symbol_to_expression_or_feed: expression_or_feed=",
        expression_or_feed,
    )
    assert expression_or_feed in ["expression", "feed"]
    print(
        "neo4j_query/add_symbol_to_expression_or_feed: symbol_category=",
        symbol_category,
    )
    assert symbol_category in list_of_valid.symbol_categories

    result = tx.run(
        "MATCH (e:"
        + expression_or_feed
        + "),(s:"
        + symbol_category
        + ") "
        + 'WHERE e.id="'
        + str(expression_or_feed_id)
        + '" AND s.id="'
        + str(symbol_id)
        + '" '
        + "MERGE (e)-[r:HAS_SYMBOL]->(s)"
    )

    print("[TRACE] func: neo4j_query/add_symbol_to_expression end " + trace_id)
    return


def get_list_of_sequence_values_for_derivation_id(tx, derivation_id: str) -> list:
    """
    sequence value is a positive integer for ordering the steps of a derivation
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/list_sequence_values start " + trace_id)

    list_of_sequence_values = []  # type:List[int]

    print("derivation_id=", derivation_id)
    print(
        'MATCH (d:derivation {id:"'
        + derivation_id
        + '"})-[r]->(s:step) RETURN r.sequence_index'
    )
    for result in tx.run(
        'MATCH (d:derivation {id:"'
        + derivation_id
        + '"})-[r]->(s:step) RETURN r.sequence_index'
    ):
        record = result.data()
        # record= {'r.sequence_index': '1'}
        print("record=", record)

        list_of_sequence_values.append(int(record["r.sequence_index"]))

    list_of_sequence_values.sort()
    print("list_of_sequence_values=", list_of_sequence_values)

    print("[TRACE] func: neo4j_query/list_sequence_values end " + trace_id)
    return list_of_sequence_values


def add_step_to_derivation(
    tx,
    step_id: str,
    derivation_id: str,
    inference_rule_id: str,
    new_sequence_value: int,
    now_str: str,
    note_before_step_latex: str,
    note_after_step_latex: str,
    author_name_latex: str,
) -> None:
    """
    can't add inference rules in same query because step needs to exist first

    >>> add_step_to_derivation()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_step_to_derivation start " + trace_id)

    # # https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.Result
    # print("result=",result.single())

    print("insert step with id; this works")
    result = tx.run(
        'MERGE (:step {id:"' + step_id + '", '
        'author_name_latex:"' + author_name_latex + '", '
        'note_before_step_latex:"' + note_before_step_latex + '", '
        'created_datetime:"' + now_str + '", '
        'note_after_step_latex:"' + note_after_step_latex + '"})'
    )
    # print(result.data()) # this just shows "[]"

    print("step with edge", derivation_id)
    result = tx.run(
        "MATCH (a:derivation),(b:step) "
        'WHERE a.id="' + str(derivation_id) + '" AND b.id="' + str(step_id) + '" '
        "MERGE (a)-[r:HAS_STEP {sequence_index: "
        + str(new_sequence_value)
        + "}]->(b) RETURN r"
    )

    print("inference_rule_id", inference_rule_id)
    result = tx.run(
        "MATCH (a:step),(b:inference_rule) "
        'WHERE a.id="' + str(step_id) + '" AND b.id="' + str(inference_rule_id) + '"'
        "MERGE (a)-[:HAS_INFERENCE_RULE]->(b)"
    )
    # print(result.data()) # this just shows "[]"

    print("[TRACE] func: neo4j_query/add_step_to_derivation end " + trace_id)
    return


def connect_expressions_to_step(
    tx,
    step_id: str,
    now_str: str,
    list_of_input_expression_IDs: list,
    list_of_feed_expression_IDs: list,
    list_of_output_expression_IDs: list,
    author_name_latex: str,
) -> None:
    """
    adding expressions to step can only be done once step exists

    >>> connect_expressions_to_step()
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/connect_expressions_to_step start " + trace_id)

    assert (
        (len(list_of_input_expression_IDs) > 0)
        or (len(list_of_feed_expression_IDs) > 0)
        or (len(list_of_output_expression_IDs) > 0)
    )

    print("list_of_input_expression_IDs", list_of_input_expression_IDs)
    print("list_of_feed_expression_IDs", list_of_feed_expression_IDs)
    print("list_of_output_expression_IDs", list_of_output_expression_IDs)

    # input expressions
    for input_index, input_id in enumerate(list_of_input_expression_IDs):
        print("input_id=", input_id, "; input_index=", input_index)
        print("step_id=", step_id)
        result = tx.run(
            "MATCH (a:step),(b:expression) "
            'WHERE a.id="' + str(step_id) + '" AND b.id="' + str(input_id) + '" '
            'MERGE (a)-[:HAS_INPUT {sequence_index: "' + str(input_index) + '"}]->(b)'
        )
        # print(result.data()) # this just shows "[]"

    # feed expressions
    for feed_index, feed_id in enumerate(list_of_feed_expression_IDs):
        print("feed_id=", feed_id, "; feed_index=", feed_index)
        result = tx.run(
            "MATCH (a:step),(b:feed) "
            'WHERE a.id="' + str(step_id) + '" AND b.id="' + str(feed_id) + '" '
            'MERGE (a)-[:HAS_FEED {sequence_index: "' + str(feed_index) + '"}]->(b)'
        )
        # print(result.data()) # this just shows "[]"

    # output expressions
    for output_index, output_id in enumerate(list_of_output_expression_IDs):
        print("output_id=", output_id, "; output_index=", output_index)
        result = tx.run(
            "MATCH (a:step),(b:expression) "
            'WHERE a.id="' + str(step_id) + '" AND b.id="' + str(output_id) + '" '
            'MERGE (a)-[:HAS_OUTPUT {sequence_index: "' + str(output_index) + '"}]->(b)'
        )
        # print(result.data()) # this just shows "[]"

    print("[TRACE] func: neo4j_query/connect_expressions_to_step end " + trace_id)
    return


def add_expression(
    tx,
    expression_id: str,
    expression_name_latex: str,
    expression_latex_lhs: str,
    expression_latex_relation: str,
    expression_latex_rhs: str,
    expression_latex_condition: str,
    expression_description_latex: str,
    expression_reference_latex: str,
    author_name_latex: str,
) -> None:
    """
    nothing returned by function because action is to write change to Neo4j database

    >>> add_expression(tx,)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_expression start " + trace_id)

    result = tx.run(
        "MERGE (:expression "
        '{name_latex:"' + str(expression_name_latex) + '", '
        ' latex_lhs:"' + str(expression_latex_lhs) + '", '
        ' latex_relation:"' + str(expression_latex_relation) + '", '
        ' latex_rhs:"' + str(expression_latex_rhs) + '", '
        ' latex_condition: "' + str(expression_latex_condition) + '", '
        #' lean:"' + str(expression_lean) + '", '
        #' sympy:"' + str(expression_sympy) + '", '
        ' description_latex:"' + str(expression_description_latex) + '", '
        ' reference_latex:"' + str(expression_reference_latex) + '", '
        ' author_name_latex:"' + str(author_name_latex) + '", '
        ' id:"' + str(expression_id) + '"})'
    )

    print("[TRACE] func: neo4j_query/add_expression end " + trace_id)
    return


def add_feed(
    tx,
    feed_id: str,
    feed_latex: str,
    feed_sympy: str,
    feed_lean: str,
    author_name_latex: str,
) -> None:
    """
    nothing returned by function because action is to write change to Neo4j database

    >>> add_feed(tx,)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_feed start " + trace_id)

    result = tx.run(
        "merge (:feed "
        '{latex:"' + str(feed_latex) + '", '
        ' author_name_latex:"' + str(author_name_latex) + '", '
        ' sympy:"' + str(feed_sympy) + '", '
        ' lean:"' + str(feed_lean) + '", '
        ' id:"' + str(feed_id) + '"})'
    )

    print("[TRACE] func: neo4j_query/add_feed end " + trace_id)
    return


def add_quantum_operator_symbol(
    tx,
    symbol_id: str,
    symbol_name: str,
    symbol_latex: str,
    symbol_description: str,
    symbol_requires_arguments: bool,
    symbol_reference: str,
    author_name_latex: str,
) -> None:
    """
    nothing returned by function because action is to write change to Neo4j database

    >>> add_symbol(tx,)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_quantum_operator_symbol start " + trace_id)

    result = tx.run(
        "merge (:quantum_operator "
        '{name_latex:"' + str(symbol_name) + '", '
        ' latex:"' + str(symbol_latex) + '", '
        ' description_latex:"' + str(symbol_description) + '", '
        ' author_name_latex:"' + str(author_name_latex) + '", '
        " requires_arguments:" + str(symbol_requires_arguments) + ", "
        ' reference_latex:"' + str(symbol_reference) + '", '
        ' id:"' + str(symbol_id) + '"})'
    )

    print("[TRACE] func: neo4j_query/add_quantum_operator_symbol end " + trace_id)
    return


def add_constant_value_with_units(
    tx,
    scalar_id: str,
    value_with_units_id: str,
    number_decimal: float,
    number_power: float,
    dict_of_units: dict,
    author_name_latex: str,
) -> None:
    """
    >>>
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_constant_value_with_units start " + trace_id)

    str_to_add = ""
    for property_key, property_value in dict_of_units.items():
        str_to_add += property_key + ':"' + str(property_value) + '", '

    print("neo4j_query/add_constant_value_with_units: str_to_add=", str_to_add)

    # create new node for value
    result = tx.run(
        "merge (:value_with_units "
        "{number_decimal:" + str(number_decimal) + ", "
        " number_power: " + str(number_power) + ", "
        ' id:"'
        + str(value_with_units_id)
        + '", '
        + str_to_add
        + ' author_name_latex:"'
        + str(author_name_latex)
        + '"})'
    )

    # create edge between scalar and value
    result = tx.run(
        "MATCH (s:scalar),(v:value_with_units) "
        'WHERE s.id="'
        + str(scalar_id)
        + '" AND v.id="'
        + str(value_with_units_id)
        + '" '
        "MERGE (s)-[:HAS_VALUE]->(v)"
    )

    print("[TRACE] func: neo4j_query/add_constant_value_with_units end " + trace_id)
    return


def add_scalar_symbol(
    tx,
    symbol_id: str,
    symbol_name: str,
    symbol_latex: str,
    symbol_description: str,
    symbol_reference: str,
    symbol_scope: str,
    symbol_variable_or_constant: str,
    symbol_domain: str,
    dimension_length: int,
    dimension_time: int,
    dimension_mass: int,
    dimension_temperature: int,
    dimension_electric_charge: int,
    dimension_amount_of_substance: int,
    dimension_luminous_intensity: int,
    author_name_latex: str,
):
    """
    >>>
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_scalar_symbol start " + trace_id)

    # corresponds to SpecifyNewSymbolDIRECTScalarForm
    assert len(symbol_latex) > 0
    assert len(symbol_scope) > 0
    assert len(symbol_variable_or_constant) > 0

    result = tx.run(
        "merge (:symbol:scalar "
        '{name_latex:"' + str(symbol_name) + '", '
        ' latex:"' + str(symbol_latex) + '", '
        ' description_latex:"' + str(symbol_description) + '", '
        ' reference_latex:"' + str(symbol_reference) + '",'
        ' scope:"' + str(symbol_scope) + '",'
        ' variable_or_constant:"' + str(symbol_variable_or_constant) + '",'
        ' domain:"' + str(symbol_domain) + '",'
        " dimension_length: " + str(dimension_length) + ", "
        " dimension_time: " + str(dimension_time) + ", "
        " dimension_mass: " + str(dimension_mass) + ", "
        " dimension_temperature: " + str(dimension_temperature) + ", "
        " dimension_electric_charge: " + str(dimension_electric_charge) + ", "
        " dimension_amount_of_substance: " + str(dimension_amount_of_substance) + ", "
        " dimension_luminous_intensity: " + str(dimension_luminous_intensity) + ", "
        ' author_name_latex:"' + str(author_name_latex) + '", '
        ' id:"' + str(symbol_id) + '"})'
    )

    print("[TRACE] func: neo4j_query/add_scalar_symbol end " + trace_id)
    return


def add_vector_symbol(
    tx,
    symbol_id: str,
    symbol_name: str,
    symbol_latex: str,
    symbol_description: str,
    symbol_reference: str,
    symbol_is_composite: bool,
    symbol_size: str,
    symbol_orientation: str,
    symbol_number_of_entries: str,
    author_name_latex: str,
):
    """
    >>>
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_vector_symbol start " + trace_id)

    # corresponds to SpecifyNewSymbolDIRECTVectorForm
    assert len(symbol_latex) > 0

    if symbol_size == "arbitrary":
        result = tx.run(
            "merge (:symbol:vector "
            '{name_latex:"' + str(symbol_name) + '", '
            ' latex:"' + str(symbol_latex) + '", '
            ' description_latex:"' + str(symbol_description) + '", '
            ' reference_latex:"' + str(symbol_reference) + '", '
            'orientation:"' + str(symbol_orientation) + '", '
            " size: '" + str(symbol_size) + "',"
            "is_composite:" + str(symbol_is_composite) + ","
            ' author_name_latex:"' + str(author_name_latex) + '", '
            ' id:"' + str(symbol_id) + '"})'
        )
    else:  # fixed size
        result = tx.run(
            "merge (:symbol:vector "
            '{name_latex:"' + str(symbol_name) + '", '
            ' latex:"' + str(symbol_latex) + '", '
            ' description_latex:"' + str(symbol_description) + '", '
            ' reference_latex:"' + str(symbol_reference) + '", '
            'orientation:"' + str(symbol_orientation) + '", '
            " size: '" + str(symbol_size) + "',"
            'number_of_entries:"' + str(symbol_number_of_entries) + '", '
            "is_composite:" + str(symbol_is_composite) + ","
            ' author_name_latex:"' + str(author_name_latex) + '", '
            ' id:"' + str(symbol_id) + '"})'
        )

    print("[TRACE] func: neo4j_query/add_vector_symbol end " + trace_id)
    return


def add_matrix_symbol(
    tx,
    symbol_id: str,
    symbol_name: str,
    symbol_latex: str,
    symbol_description: str,
    symbol_reference: str,
    symbol_is_composite: bool,
    symbol_size: str,
    symbol_number_of_rows: str,
    symbol_number_of_columns: str,
    author_name_latex: str,
):
    """
    >>>
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_matrix_symbol start " + trace_id)

    # corresponds to SpecifyNewSymbolDIRECTMatrixForm
    assert len(symbol_latex) > 0

    if symbol_size == "arbitrary":
        result = tx.run(
            "merge (:symbol:matrix "
            '{name_latex:"' + str(symbol_name) + '", '
            ' latex:"' + str(symbol_latex) + '", '
            ' description_latex:"' + str(symbol_description) + '", '
            ' reference_latex:"' + str(symbol_reference) + '", '
            " size: '" + str(symbol_size) + "',"
            "is_composite:" + str(symbol_is_composite) + ","
            ' author_name_latex:"' + str(author_name_latex) + '", '
            ' id:"' + str(symbol_id) + '"})'
        )
    else:  # fixed size
        result = tx.run(
            "merge (:matrix "
            '{name_latex:"' + str(symbol_name) + '", '
            ' latex:"' + str(symbol_latex) + '", '
            ' description_latex:"' + str(symbol_description) + '", '
            ' reference_latex:"' + str(symbol_reference) + '", '
            " size: '" + str(symbol_size) + "',"
            'number_of_rows:"' + str(symbol_number_of_rows) + '", '
            'number_of_columns:"' + str(symbol_number_of_columns) + '", '
            "is_composite:" + str(symbol_is_composite) + ","
            ' author_name_latex:"' + str(author_name_latex) + '", '
            ' id:"' + str(symbol_id) + '"})'
        )

    print("[TRACE] func: neo4j_query/add_matrix_symbol end " + trace_id)
    return


def add_operation_symbol(
    tx,
    operation_id: str,
    operation_name: str,
    operation_latex: str,
    operation_description_latex: str,
    operation_reference_latex: str,
    operation_argument_count: int,
    author_name_latex: str,
) -> None:
    """
    nothing returned by function because action is to write change to Neo4j database

    >>> add_operation(tx,)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_operation_symbol start " + trace_id)

    # corresponds to SpecifyNewSymbolDIRECTOperationForm
    assert len(operation_name) > 0
    assert len(operation_latex) > 0
    assert int(operation_argument_count) > 0

    result = tx.run(
        "merge (:operation "
        '{name_latex:"' + str(operation_name) + '", '
        ' latex:"' + str(operation_latex) + '", '
        ' description_latex:"' + str(operation_description_latex) + '", '
        ' reference_latex:"' + str(operation_reference_latex) + '", '
        " argument_count:" + str(operation_argument_count) + ", "
        ' author_name_latex:"' + str(author_name_latex) + '", '
        ' id:"' + str(operation_id) + '"})'
    )

    print("[TRACE] func: neo4j_query/add_operation_symbol end " + trace_id)
    return


def add_relation_symbol(
    tx,
    relation_id: str,
    relation_name_latex: str,
    relation_latex: str,
    relation_description_latex: str,
    relation_reference_latex: str,
    author_name_latex: str,
) -> None:
    """
    nothing returned by function because action is to write change to Neo4j database

    >>> add_operation(tx,)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/add_relation_symbol start " + trace_id)

    # corresponds to SpecifyNewSymbolDIRECTOperationForm
    assert len(relation_name_latex) > 0
    assert len(relation_latex) > 0

    result = tx.run(
        "merge (:relation "
        '{name_latex:"' + str(relation_name_latex) + '", '
        ' latex:"' + str(relation_latex) + '", '
        ' description_latex:"' + str(relation_description_latex) + '", '
        ' reference_latex:"' + str(relation_reference_latex) + '", '
        ' author_name_latex:"' + str(author_name_latex) + '", '
        ' id:"' + str(relation_id) + '"})'
    )

    print("[TRACE] func: neo4j_query/add_relation_symbol end " + trace_id)
    return


def list_of_all_node_IDs_and_labels(tx) -> list:
    """
    >>> list_of_all_nodes()
    """
    result = tx.run("MATCH (n) RETURN n.id, labels(n)")
    record = result.data()
    # print("neo4j_query/list_of_all_nodes: record=", record)
    return record


def delete_all_nodes_and_relationships(tx) -> None:
    """
    Delete all nodes and relationships from Neo4j database

    This requires write access to Neo4j database

    nothing returned by function because action is to write change to Neo4j database

    >>> delete_all_nodes_and_relationships(tx)
    """
    trace_id = str(random.randint(1000000, 9999999))
    print(
        "[TRACE] func: neo4j_query/delete_all_nodes_and_relationships start " + trace_id
    )

    tx.run("MATCH (n) DETACH DELETE n")

    print(
        "[TRACE] func: neo4j_query/delete_all_nodes_and_relationships end " + trace_id
    )
    return


def user_query(tx, query: str) -> list:
    """
    User-submitted Cypher query for Neo4j database

    Read-only for Neo4j database

    >>> user_query(tx, "test")
    """
    trace_id = str(random.randint(1000000, 9999999))
    print("[TRACE] func: neo4j_query/user_query start " + trace_id)

    list_of_results = []
    try:
        for result in tx.run(query):
            list_of_results.append(str(result))
    except neo4j.exceptions.ClientError:
        list_of_results = ["WRITE OPERATIONS NOT ALLOWED (1)"]
    except neo4j.exceptions.TransactionError:
        list_of_results = ["WRITE OPERATIONS NOT ALLOWED (2)"]

    print("[TRACE] func: neo4j_query/user_query end " + trace_id)
    return list_of_results

