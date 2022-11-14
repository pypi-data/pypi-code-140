# -*- coding: utf-8 -*-
"""
Module containing the implementation of Geofile operations using a sql statement.
"""

from concurrent import futures
from dataclasses import dataclass
from datetime import datetime
import logging
import logging.config
import math
import multiprocessing
from pathlib import Path
import shutil
from typing import Iterable, List, Optional

import pandas as pd

import geofileops as gfo
from geofileops import GeofileType, GeometryType, PrimitiveType
from geofileops import fileops
from geofileops.fileops import _append_to_nolock
from . import _io_util
from . import _ogr_util
from . import _sqlite_util
from . import _general_util

################################################################################
# Some init
################################################################################

logger = logging.getLogger(__name__)

################################################################################
# Operations on one layer
################################################################################


def buffer(
    input_path: Path,
    output_path: Path,
    distance: float,
    quadrantsegments: int = 5,
    input_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    columns: Optional[List[str]] = None,
    explodecollections: bool = False,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    if distance < 0:
        # For a double sided buffer, aA negative buffer is only relevant
        # for polygon types, so only keep polygon results
        # Negative buffer creates invalid stuff, so use collectionextract
        # to keep only polygons
        sql_template = f"""
            SELECT ST_CollectionExtract(
                       ST_buffer({{geometrycolumn}}, {distance}, {quadrantsegments}),
                       3
                   ) AS geom
                  {{columns_to_select_str}}
              FROM "{{input_layer}}" layer
             WHERE 1=1
                  {{batch_filter}}
        """
    else:
        sql_template = f"""
            SELECT ST_Buffer({{geometrycolumn}}, {distance}, {quadrantsegments}) AS geom
                  {{columns_to_select_str}}
              FROM "{{input_layer}}" layer
             WHERE 1=1
                  {{batch_filter}}
        """

    # Buffer operation always results in polygons...
    force_output_geometrytype = GeometryType.MULTIPOLYGON

    return _single_layer_vector_operation(
        input_path=input_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="buffer",
        input_layer=input_layer,
        output_layer=output_layer,
        columns=columns,
        explodecollections=explodecollections,
        force_output_geometrytype=force_output_geometrytype,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def convexhull(
    input_path: Path,
    output_path: Path,
    input_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    columns: Optional[List[str]] = None,
    explodecollections: bool = False,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Prepare sql template for this operation
    sql_template = """
            SELECT ST_ConvexHull({geometrycolumn}) AS geom
                  {columns_to_select_str}
              FROM "{input_layer}" layer
             WHERE 1=1
               {batch_filter}"""

    # Output geometry type same as input geometry type
    input_layer_info = gfo.get_layerinfo(input_path, input_layer)
    return _single_layer_vector_operation(
        input_path=input_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="convexhull",
        input_layer=input_layer,
        output_layer=output_layer,
        columns=columns,
        explodecollections=explodecollections,
        force_output_geometrytype=input_layer_info.geometrytype,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def delete_duplicate_geometries(
    input_path: Path,
    output_path: Path,
    input_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    columns: Optional[List[str]] = None,
    explodecollections: bool = False,
    force: bool = False,
):

    # The query as written doesn't give correct results when parallellized,
    # but it isn't useful to do it for this operation.
    sql_template = """
            SELECT {geometrycolumn} AS geom
                  {columns_to_select_str}
              FROM "{input_layer}" layer
             WHERE layer.rowid IN (
                    SELECT MIN(layer_sub.rowid) AS rowid_to_keep
                      FROM "{input_layer}" layer_sub
                     GROUP BY layer_sub.{geometrycolumn}
                )
            """

    # Go!
    input_layer_info = gfo.get_layerinfo(input_path, input_layer)
    return _single_layer_vector_operation(
        input_path=input_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="delete_duplicate_geometries",
        input_layer=input_layer,
        output_layer=output_layer,
        columns=columns,
        explodecollections=explodecollections,
        force_output_geometrytype=input_layer_info.geometrytype,
        filter_null_geoms=True,
        nb_parallel=1,
        force=force,
    )


def isvalid(
    input_path: Path,
    output_path: Path,
    input_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
) -> bool:

    # Prepare sql template for this operation
    sql_template = """
            SELECT ST_IsValidDetail({geometrycolumn}) AS geom
                  ,ST_IsValid({geometrycolumn}) AS isvalid
                  ,ST_IsValidReason({geometrycolumn}) AS isvalidreason
                  {columns_to_select_str}
              FROM "{input_layer}" layer
             WHERE ST_IsValid({geometrycolumn}) <> 1
               {batch_filter}"""

    _single_layer_vector_operation(
        input_path=input_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="isvalid",
        input_layer=input_layer,
        output_layer=output_layer,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )

    # If no invalid geoms are found, there won't be an output file
    if not output_path.exists():
        # If output is a geopackage, check if all data can be read
        try:
            input_geofiletype = GeofileType(input_path)
            if input_geofiletype.is_spatialite_based:
                _sqlite_util.test_data_integrity(path=input_path)
                logger.debug("test_data_integrity was succesfull")
        except Exception:
            logger.exception(
                "No invalid geometries found, but some attributes could not be read"
            )
            return False

        return True
    else:
        layerinfo = gfo.get_layerinfo(output_path)
        logger.info(
            f"Found {layerinfo.featurecount} invalid geometries in {output_path}"
        )
        return False


def makevalid(
    input_path: Path,
    output_path: Path,
    input_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    columns: Optional[List[str]] = None,
    explodecollections: bool = False,
    force_output_geometrytype: Optional[GeometryType] = None,
    precision: Optional[float] = None,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Specify output_geomatrytype, because otherwise makevalid results in
    # column type 'GEOMETRY'/'UNKNOWN(ANY)'
    layerinfo = gfo.get_layerinfo(input_path, input_layer)
    if force_output_geometrytype is None:
        force_output_geometrytype = layerinfo.geometrytype

    # First compose the operation to be done on the geometries
    # If the number of decimals of coordinates should be limited
    if precision is not None:
        operation = f"SnapToGrid({{geometrycolumn}}, {precision})"
    else:
        operation = "{geometrycolumn}"

    # Prepare sql template for this operation
    operation = f"ST_MakeValid({operation})"

    # If we want a specific geometrytype as result, extract it
    if force_output_geometrytype is not GeometryType.GEOMETRYCOLLECTION:
        primitivetypeid = force_output_geometrytype.to_primitivetype.value
        operation = f"ST_CollectionExtract({operation}, {primitivetypeid})"

    # Now we can prepare the entire statement
    sql_template = f"""
            SELECT {operation} AS geom
                {{columns_to_select_str}}
            FROM "{{input_layer}}" layer
            WHERE 1=1
                {{batch_filter}}"""

    _single_layer_vector_operation(
        input_path=input_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="makevalid",
        input_layer=input_layer,
        output_layer=output_layer,
        columns=columns,
        explodecollections=explodecollections,
        force_output_geometrytype=force_output_geometrytype,
        # filter_null_geoms=False,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )

    # If output is a geopackage, check if all data can be read
    output_geofiletype = GeofileType(input_path)
    if output_geofiletype.is_spatialite_based:
        _sqlite_util.test_data_integrity(path=input_path)


def select(
    input_path: Path,
    output_path: Path,
    sql_stmt: str,
    sql_dialect: Optional[str] = "SQLITE",
    input_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    columns: Optional[List[str]] = None,
    explodecollections: bool = False,
    force_output_geometrytype: Optional[GeometryType] = None,
    nb_parallel: int = 1,
    batchsize: int = -1,
    force: bool = False,
):

    # Check if output exists already here, to evade to much logging to be written
    if output_path.exists():
        if force is False:
            logger.info(f"Stop select: output exists already {output_path}")
            return
    logger.debug(f"  -> select to execute:\n{sql_stmt}")

    # If no output geometrytype is specified, use the geometrytype of the input layer
    if force_output_geometrytype is None:
        force_output_geometrytype = gfo.get_layerinfo(
            input_path, input_layer
        ).geometrytype
        logger.info(
            "No force_output_geometrytype specified, so defaults to input layer "
            f"geometrytype: {force_output_geometrytype}"
        )

    # Go!
    return _single_layer_vector_operation(
        input_path=input_path,
        output_path=output_path,
        sql_template=sql_stmt,
        operation_name="select",
        input_layer=input_layer,
        output_layer=output_layer,
        columns=columns,
        explodecollections=explodecollections,
        force_output_geometrytype=force_output_geometrytype,
        sql_dialect=sql_dialect,
        filter_null_geoms=False,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def simplify(
    input_path: Path,
    output_path: Path,
    tolerance: float,
    input_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    columns: Optional[List[str]] = None,
    explodecollections: bool = False,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Prepare sql template for this operation
    sql_template = f"""
            SELECT ST_SimplifyPreserveTopology({{geometrycolumn}}, {tolerance}) AS geom
                  {{columns_to_select_str}}
              FROM "{{input_layer}}" layer
             WHERE 1=1
               {{batch_filter}}"""

    # Output geometry type same as input geometry type
    input_layer_info = gfo.get_layerinfo(input_path, input_layer)
    return _single_layer_vector_operation(
        input_path=input_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="simplify",
        input_layer=input_layer,
        output_layer=output_layer,
        columns=columns,
        explodecollections=explodecollections,
        force_output_geometrytype=input_layer_info.geometrytype,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def _single_layer_vector_operation(
    input_path: Path,
    output_path: Path,
    sql_template: str,
    operation_name: str,
    input_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    columns: Optional[List[str]] = None,
    explodecollections: bool = False,
    force_output_geometrytype: Optional[GeometryType] = None,
    sql_dialect: Optional[str] = "SQLITE",
    filter_null_geoms: bool = True,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Init
    start_time = datetime.now()

    # Check input parameters...
    if not input_path.exists():
        raise Exception(
            f"Error {operation_name}: input_path doesn't exist: {input_path}"
        )

    # Check/get layer names
    if input_layer is None:
        input_layer = gfo.get_only_layer(input_path)
    if output_layer is None:
        output_layer = gfo.get_default_layer(output_path)

    # If output file exists already, either clean up or return...
    if output_path.exists():
        if force is False:
            logger.info(f"Stop {operation_name}: output exists already {output_path}")
            return
        else:
            gfo.remove(output_path)

    # Get layer info of the input layer
    input_layerinfo = gfo.get_layerinfo(input_path, input_layer)

    # Calculate
    tempdir = _io_util.create_tempdir(f"geofileops/{operation_name.replace(' ', '_')}")
    try:
        processing_params = _prepare_processing_params(
            input1_path=input_path,
            input1_layer=input_layer,
            input1_layer_alias="layer",
            tempdir=tempdir,
            nb_parallel=nb_parallel,
            batchsize=batchsize,
            convert_to_spatialite_based=False,
        )
        # If None is returned, just stop.
        if processing_params is None or processing_params.batches is None:
            return

        # If there are multiple batches, there needs to be a {batch_filter}
        # placeholder in the sql template!
        if len(processing_params.batches) > 1:
            if "{batch_filter}" not in sql_template:
                raise ValueError(
                    "Error: nb_batches > 1 but no {batch_filter} "
                    f"placeholder in sql_template\n{sql_template}"
                )

        # Format column string for use in select
        formatted_column_strings = format_column_strings(
            columns_specified=columns, columns_available=input_layerinfo.columns
        )

        # Prepare output filename
        tmp_output_path = tempdir / output_path.name
        nb_done = 0

        # Processing in threads is 2x faster for small datasets (on Windows)
        calculate_in_threads = True if input_layerinfo.featurecount <= 100 else False
        with _general_util.PooledExecutorFactory(
            threadpool=calculate_in_threads,
            max_workers=processing_params.nb_parallel,
            initializer=_general_util.initialize_worker(),
        ) as calculate_pool:

            batches = {}
            future_to_batch_id = {}
            for batch_id in processing_params.batches:

                batches[batch_id] = {}
                batches[batch_id]["layer"] = output_layer

                tmp_partial_output_path = (
                    tempdir / f"{output_path.stem}_{batch_id}{output_path.suffix}"
                )
                batches[batch_id]["tmp_partial_output_path"] = tmp_partial_output_path

                # Now we have everything to format sql statement
                sql_stmt = sql_template.format(
                    geometrycolumn=input_layerinfo.geometrycolumn,
                    columns_to_select_str=formatted_column_strings.columns,
                    input_layer=processing_params.batches[batch_id]["layer"],
                    batch_filter=processing_params.batches[batch_id]["batch_filter"],
                )

                # Make sure no NULL geoms are outputted...
                if filter_null_geoms is True:
                    sql_stmt = f"""
                            SELECT sub.*
                            FROM
                                ( {sql_stmt}
                                ) sub
                            WHERE sub.geom IS NOT NULL"""

                batches[batch_id]["sql_stmt"] = sql_stmt

                # Remark: this temp file doesn't need spatial index
                translate_info = _ogr_util.VectorTranslateInfo(
                    input_path=processing_params.batches[batch_id]["path"],
                    output_path=tmp_partial_output_path,
                    output_layer=output_layer,
                    sql_stmt=sql_stmt,
                    sql_dialect=sql_dialect,
                    explodecollections=explodecollections,
                    force_output_geometrytype=force_output_geometrytype,
                    options={"LAYER_CREATION.SPATIAL_INDEX": False},
                )
                future = calculate_pool.submit(
                    _ogr_util.vector_translate_by_info, info=translate_info
                )
                future_to_batch_id[future] = batch_id

            # Loop till all parallel processes are ready, but process each one
            # that is ready already
            # Calculating can be done in parallel, but only one process can write to
            # the same file at the time
            for future in futures.as_completed(future_to_batch_id):
                try:
                    _ = future.result()
                except Exception as ex:
                    batch_id = future_to_batch_id[future]
                    logger.exception(f"Error executing {batches[batch_id]}")
                    raise Exception(f"Error executing {batches[batch_id]}") from ex

                # Start copy of the result to a common file
                # Remark: give higher priority, because this is the slowest factor
                batch_id = future_to_batch_id[future]
                tmp_partial_output_path = batches[batch_id]["tmp_partial_output_path"]

                if tmp_partial_output_path.exists():
                    gfo.append_to(
                        src=tmp_partial_output_path,
                        dst=tmp_output_path,
                        dst_layer=output_layer,
                        create_spatial_index=False,
                    )
                    gfo.remove(tmp_partial_output_path)
                else:
                    logger.debug(f"Result file {tmp_partial_output_path} was empty")

                # Log the progress and prediction speed
                nb_done += 1
                _general_util.report_progress(
                    start_time,
                    nb_done,
                    len(batches),
                    operation_name,
                    nb_parallel=nb_parallel,
                )

        # Round up and clean up
        # Now create spatial index and move to output location
        if tmp_output_path.exists():
            gfo.create_spatial_index(path=tmp_output_path, layer=output_layer)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            gfo.move(tmp_output_path, output_path)
        else:
            logger.debug(f"Result of {operation_name} was empty!")

    finally:
        # Clean tmp dir
        shutil.rmtree(tempdir)
        logger.info(f"Processing ready, took {datetime.now()-start_time}!")


################################################################################
# Operations on two layers
################################################################################


def clip(
    input_path: Path,
    clip_path: Path,
    output_path: Path,
    input_layer: Optional[str] = None,
    input_columns: Optional[List[str]] = None,
    input_columns_prefix: str = "",
    clip_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    explodecollections: bool = False,
    output_with_spatial_index: bool = True,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Init
    # In the query, important to only extract the geometry types that are expected
    input_layer_info = gfo.get_layerinfo(input_path, input_layer)
    primitivetypeid = input_layer_info.geometrytype.to_primitivetype.value

    # If the input type is not point, force the output type to multi,
    # because erase clip cause eg. polygons to be split to multipolygons...
    force_output_geometrytype = input_layer_info.geometrytype
    if force_output_geometrytype is not GeometryType.POINT:
        force_output_geometrytype = input_layer_info.geometrytype.to_multitype

    # Prepare sql template for this operation
    # Remarks:
    #   - ST_intersection(geometry , NULL) gives NULL as result! -> hence the CASE
    #   - use of the with instead of an inline view is a lot faster
    #   - WHERE geom IS NOT NULL to evade rows with a NULL geom, they give issues in
    #     later operations
    input1_layer_rtree = "rtree_{input1_layer}_{input1_geometrycolumn}"
    input2_layer_rtree = "rtree_{input2_layer}_{input2_geometrycolumn}"
    sql_template = f"""
          SELECT * FROM (
            WITH layer2_unioned AS (
              SELECT layer1.rowid AS layer1_rowid
                    ,ST_union(layer2.{{input2_geometrycolumn}}) AS geom
                FROM {{input1_databasename}}."{{input1_layer}}" layer1
                JOIN {{input1_databasename}}."{input1_layer_rtree}" layer1tree
                  ON layer1.fid = layer1tree.id
                JOIN {{input2_databasename}}."{{input2_layer}}" layer2
                JOIN {{input2_databasename}}."{input2_layer_rtree}" layer2tree
                  ON layer2.fid = layer2tree.id
               WHERE 1=1
                 {{batch_filter}}
                 AND layer1tree.minx <= layer2tree.maxx
                 AND layer1tree.maxx >= layer2tree.minx
                 AND layer1tree.miny <= layer2tree.maxy
                 AND layer1tree.maxy >= layer2tree.miny
                 AND ST_Intersects(
                        layer1.{{input1_geometrycolumn}},
                        layer2.{{input2_geometrycolumn}}) = 1
                 AND ST_Touches(
                        layer1.{{input1_geometrycolumn}},
                        layer2.{{input2_geometrycolumn}}) = 0
               GROUP BY layer1.rowid
            )
            SELECT CASE WHEN layer2_unioned.geom IS NULL THEN NULL
                        ELSE ST_CollectionExtract(
                               ST_intersection(layer1.{{input1_geometrycolumn}},
                                               layer2_unioned.geom), {primitivetypeid})
                   END as geom
                  {{layer1_columns_prefix_alias_str}}
              FROM {{input1_databasename}}."{{input1_layer}}" layer1
              JOIN layer2_unioned ON layer1.rowid = layer2_unioned.layer1_rowid
             WHERE 1=1
               {{batch_filter}}
          )
          WHERE geom IS NOT NULL
            AND ST_NPoints(geom) > 0
            -- ST_CollectionExtract outputs empty, but not NULL geoms in spatialite 4.3
            """

    # Go!
    return _two_layer_vector_operation(
        input1_path=input_path,
        input2_path=clip_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="clip",
        input1_layer=input_layer,
        input1_columns=input_columns,
        input1_columns_prefix=input_columns_prefix,
        input2_layer=clip_layer,
        input2_columns=None,
        output_layer=output_layer,
        explodecollections=explodecollections,
        force_output_geometrytype=force_output_geometrytype,
        output_with_spatial_index=output_with_spatial_index,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def erase(
    input_path: Path,
    erase_path: Path,
    output_path: Path,
    input_layer: Optional[str] = None,
    input_columns: Optional[List[str]] = None,
    input_columns_prefix: str = "",
    erase_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    explodecollections: bool = False,
    output_with_spatial_index: bool = True,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Init
    # In the query, important to only extract the geometry types that are expected
    input_layer_info = gfo.get_layerinfo(input_path, input_layer)
    primitivetypeid = input_layer_info.geometrytype.to_primitivetype.value

    # If the input type is not point, force the output type to multi,
    # because erase can cause eg. polygons to be split to multipolygons...
    force_output_geometrytype = input_layer_info.geometrytype
    if force_output_geometrytype is not GeometryType.POINT:
        force_output_geometrytype = input_layer_info.geometrytype.to_multitype

    # Prepare sql template for this operation
    # Remarks:
    #   - ST_difference(geometry , NULL) gives NULL as result! -> hence the CASE
    #   - use of the with instead of an inline view is a lot faster
    #   - WHERE geom IS NOT NULL to evade rows with a NULL geom, they give issues in
    #     later operations
    input1_layer_rtree = "rtree_{input1_layer}_{input1_geometrycolumn}"
    input2_layer_rtree = "rtree_{input2_layer}_{input2_geometrycolumn}"
    sql_template = f"""
          SELECT * FROM (
            WITH layer2_unioned AS (
              SELECT layer1.rowid AS layer1_rowid
                    ,ST_union(layer2.{{input2_geometrycolumn}}) AS geom
                FROM {{input1_databasename}}."{{input1_layer}}" layer1
                JOIN {{input1_databasename}}."{input1_layer_rtree}" layer1tree
                  ON layer1.fid = layer1tree.id
                JOIN {{input2_databasename}}."{{input2_layer}}" layer2
                JOIN {{input2_databasename}}."{input2_layer_rtree}" layer2tree
                  ON layer2.fid = layer2tree.id
               WHERE 1=1
                 {{batch_filter}}
                 AND layer1tree.minx <= layer2tree.maxx
                 AND layer1tree.maxx >= layer2tree.minx
                 AND layer1tree.miny <= layer2tree.maxy
                 AND layer1tree.maxy >= layer2tree.miny
                 AND ST_Intersects(
                        layer1.{{input1_geometrycolumn}},
                        layer2.{{input2_geometrycolumn}}) = 1
                 AND ST_Touches(
                        layer1.{{input1_geometrycolumn}},
                        layer2.{{input2_geometrycolumn}}) = 0
               GROUP BY layer1.rowid
            )
            SELECT CASE WHEN layer2_unioned.geom IS NULL
                        THEN layer1.{{input1_geometrycolumn}}
                        ELSE ST_CollectionExtract(
                                ST_difference(
                                    layer1.{{input1_geometrycolumn}},
                                    layer2_unioned.geom),
                                    {primitivetypeid})
                   END as geom
                  {{layer1_columns_prefix_alias_str}}
              FROM {{input1_databasename}}."{{input1_layer}}" layer1
              LEFT JOIN layer2_unioned ON layer1.rowid = layer2_unioned.layer1_rowid
             WHERE 1=1
               {{batch_filter}}
          )
          WHERE geom IS NOT NULL
            AND ST_NPoints(geom) > 0
            -- ST_CollectionExtract outputs empty, but not NULL geoms in spatialite 4.3
            """

    # Go!
    return _two_layer_vector_operation(
        input1_path=input_path,
        input2_path=erase_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="erase",
        input1_layer=input_layer,
        input1_columns=input_columns,
        input1_columns_prefix=input_columns_prefix,
        input2_layer=erase_layer,
        output_layer=output_layer,
        explodecollections=explodecollections,
        force_output_geometrytype=force_output_geometrytype,
        output_with_spatial_index=output_with_spatial_index,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def export_by_location(
    input_to_select_from_path: Path,
    input_to_compare_with_path: Path,
    output_path: Path,
    min_area_intersect: Optional[float] = None,
    area_inters_column_name: Optional[str] = "area_inters",
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input2_layer: Optional[str] = None,
    input2_columns: Optional[List[str]] = None,
    output_layer: Optional[str] = None,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Prepare sql template for this operation
    # TODO: test performance difference between the following two queries
    input1_layer_rtree = "rtree_{input1_layer}_{input1_geometrycolumn}"
    input2_layer_rtree = "rtree_{input2_layer}_{input2_geometrycolumn}"
    sql_template = f"""
            SELECT layer1.{{input1_geometrycolumn}} AS geom
                  {{layer1_columns_prefix_alias_str}}
              FROM {{input1_databasename}}."{{input1_layer}}" layer1
              JOIN {{input1_databasename}}."{input1_layer_rtree}" layer1tree
                ON layer1.fid = layer1tree.id
             WHERE 1=1
               {{batch_filter}}
               AND EXISTS (
                  SELECT 1
                    FROM {{input2_databasename}}."{{input2_layer}}" layer2
                    JOIN {{input2_databasename}}."{input2_layer_rtree}" layer2tree
                      ON layer2.fid = layer2tree.id
                   WHERE layer1tree.minx <= layer2tree.maxx
                     AND layer1tree.maxx >= layer2tree.minx
                     AND layer1tree.miny <= layer2tree.maxy
                     AND layer1tree.maxy >= layer2tree.miny
                     AND ST_intersects(layer1.{{input1_geometrycolumn}},
                                       layer2.{{input2_geometrycolumn}}) = 1
                     AND ST_touches(layer1.{{input1_geometrycolumn}},
                                    layer2.{{input2_geometrycolumn}}) = 0)
            """
    # Calculate intersect area if necessary
    area_inters_column_expression = ""
    if area_inters_column_name is not None or min_area_intersect is not None:
        if area_inters_column_name is None:
            area_inters_column_name = "area_inters"
        area_inters_column_expression = f""",ST_area(ST_intersection(ST_union(layer1.{{input1_geometrycolumn}}),
                    ST_union(layer2.{{input2_geometrycolumn}}))
                 ) as {area_inters_column_name}"""

    # Prepare sql template for this operation
    sql_template = f"""
            SELECT ST_union(layer1.{{input1_geometrycolumn}}) as geom
                  {{layer1_columns_prefix_str}}
                  {area_inters_column_expression}
              FROM {{input1_databasename}}."{{input1_layer}}" layer1
              JOIN {{input1_databasename}}."{input1_layer_rtree}" layer1tree
                ON layer1.fid = layer1tree.id
              JOIN {{input2_databasename}}."{{input2_layer}}" layer2
              JOIN {{input2_databasename}}."{input2_layer_rtree}" layer2tree
                ON layer2.fid = layer2tree.id
             WHERE 1=1
               {{batch_filter}}
               AND layer1tree.minx <= layer2tree.maxx
               AND layer1tree.maxx >= layer2tree.minx
               AND layer1tree.miny <= layer2tree.maxy
               AND layer1tree.maxy >= layer2tree.miny
               AND ST_Intersects(layer1.{{input1_geometrycolumn}},
                                 layer2.{{input2_geometrycolumn}}) = 1
               AND ST_Touches(layer1.{{input1_geometrycolumn}},
                              layer2.{{input2_geometrycolumn}}) = 0
             GROUP BY layer1.rowid {{layer1_columns_prefix_str}}
            """

    # Filter on intersect area if necessary
    if min_area_intersect is not None:
        sql_template = f"""
                SELECT sub.*
                  FROM
                    ( {sql_template}
                    ) sub
                 WHERE sub.{area_inters_column_name} >= {min_area_intersect}"""

    # Go!
    input_layer_info = gfo.get_layerinfo(input_to_select_from_path, input1_layer)
    return _two_layer_vector_operation(
        input1_path=input_to_select_from_path,
        input2_path=input_to_compare_with_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="export_by_location",
        input1_layer=input1_layer,
        input1_columns=input1_columns,
        input2_layer=input2_layer,
        input2_columns=input2_columns,
        output_layer=output_layer,
        force_output_geometrytype=input_layer_info.geometrytype,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def export_by_distance(
    input_to_select_from_path: Path,
    input_to_compare_with_path: Path,
    output_path: Path,
    max_distance: float,
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input2_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Prepare sql template for this operation
    input1_layer_rtree = "rtree_{input1_layer}_{input1_geometrycolumn}"
    input2_layer_rtree = "rtree_{input2_layer}_{input2_geometrycolumn}"
    sql_template = f"""
        SELECT geom
              {{layer1_columns_prefix_alias_str}}
          FROM {{input1_databasename}}."{{input1_layer}}" layer1
          JOIN {{input1_databasename}}."{input1_layer_rtree}" layer1tree
            ON layer1.fid = layer1tree.id
         WHERE 1=1
               {{batch_filter}}
               AND EXISTS (
                    SELECT 1
                      FROM {{input2_databasename}}."{{input2_layer}}" layer2
                      JOIN {{input2_databasename}}."{input2_layer_rtree}" layer2tree
                        ON layer2.fid = layer2tree.id
                     WHERE (layer1tree.minx-{max_distance}) <= layer2tree.maxx
                       AND (layer1tree.maxx+{max_distance}) >= layer2tree.minx
                       AND (layer1tree.miny-{max_distance}) <= layer2tree.maxy
                       AND (layer1tree.maxy+{max_distance}) >= layer2tree.miny
                       AND ST_distance(
                            layer1.{{input1_geometrycolumn}},
                            layer2.{{input2_geometrycolumn}}) <= {max_distance})
    """

    input_layer_info = gfo.get_layerinfo(input_to_select_from_path, input1_layer)

    # Go!
    return _two_layer_vector_operation(
        input1_path=input_to_select_from_path,
        input2_path=input_to_compare_with_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="export_by_distance",
        input1_layer=input1_layer,
        input1_columns=input1_columns,
        input2_layer=input2_layer,
        output_layer=output_layer,
        force_output_geometrytype=input_layer_info.geometrytype,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def intersection(
    input1_path: Path,
    input2_path: Path,
    output_path: Path,
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input1_columns_prefix: str = "l1_",
    input2_layer: Optional[str] = None,
    input2_columns: Optional[List[str]] = None,
    input2_columns_prefix: str = "l2_",
    output_layer: Optional[str] = None,
    explodecollections: bool = False,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # In the query, important to only extract the geometry types that are expected
    # TODO: test for geometrycollection, line, point,...
    input1_layer_info = gfo.get_layerinfo(input1_path, input1_layer)
    input2_layer_info = gfo.get_layerinfo(input2_path, input2_layer)
    primitivetype_to_extract = PrimitiveType(
        min(
            input1_layer_info.geometrytype.to_primitivetype.value,
            input2_layer_info.geometrytype.to_primitivetype.value,
        )
    )

    # For the output file, if output is going to be polygon or linestring, force
    # MULTI variant to evade ugly warnings
    force_output_geometrytype = primitivetype_to_extract.to_multitype

    # Prepare sql template for this operation
    input1_layer_rtree = "rtree_{input1_layer}_{input1_geometrycolumn}"
    input2_layer_rtree = "rtree_{input2_layer}_{input2_geometrycolumn}"
    sql_template = f"""
        SELECT sub.geom
             {{layer1_columns_from_subselect_str}}
             {{layer2_columns_from_subselect_str}}
          FROM
            ( SELECT ST_CollectionExtract(
                       ST_Intersection(
                            layer1.{{input1_geometrycolumn}},
                            layer2.{{input2_geometrycolumn}}),
                            {primitivetype_to_extract.value}) as geom
                    {{layer1_columns_prefix_alias_str}}
                    {{layer2_columns_prefix_alias_str}}
                FROM {{input1_databasename}}."{{input1_layer}}" layer1
                JOIN {{input1_databasename}}."{input1_layer_rtree}" layer1tree
                  ON layer1.fid = layer1tree.id
                JOIN {{input2_databasename}}."{{input2_layer}}" layer2
                JOIN {{input2_databasename}}."{input2_layer_rtree}" layer2tree
                  ON layer2.fid = layer2tree.id
               WHERE 1=1
                 {{batch_filter}}
                 AND layer1tree.minx <= layer2tree.maxx
                 AND layer1tree.maxx >= layer2tree.minx
                 AND layer1tree.miny <= layer2tree.maxy
                 AND layer1tree.maxy >= layer2tree.miny
                 AND ST_Intersects(
                        layer1.{{input1_geometrycolumn}},
                        layer2.{{input2_geometrycolumn}}) = 1
                 AND ST_Touches(
                        layer1.{{input1_geometrycolumn}},
                        layer2.{{input2_geometrycolumn}}) = 0
            ) sub
         WHERE sub.geom IS NOT NULL
    """

    # Go!
    return _two_layer_vector_operation(
        input1_path=input1_path,
        input2_path=input2_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="intersection",
        input1_layer=input1_layer,
        input1_columns=input1_columns,
        input1_columns_prefix=input1_columns_prefix,
        input2_layer=input2_layer,
        input2_columns=input2_columns,
        input2_columns_prefix=input2_columns_prefix,
        output_layer=output_layer,
        explodecollections=explodecollections,
        force_output_geometrytype=force_output_geometrytype,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def join_by_location(
    input1_path: Path,
    input2_path: Path,
    output_path: Path,
    spatial_relations_query: str = "intersects is True",
    discard_nonmatching: bool = True,
    min_area_intersect: Optional[float] = None,
    area_inters_column_name: Optional[str] = None,
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input1_columns_prefix: str = "l1_",
    input2_layer: Optional[str] = None,
    input2_columns: Optional[List[str]] = None,
    input2_columns_prefix: str = "l2_",
    output_layer: Optional[str] = None,
    explodecollections: bool = False,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Prepare sql template for this operation
    # Prepare intersection area columns/filter
    area_inters_column_expression = ""
    area_inters_column_in_output = ""
    area_inters_column_0_in_output = ""
    area_inters_filter = ""
    if area_inters_column_name is not None or min_area_intersect is not None:
        if area_inters_column_name is not None:
            area_inters_column_name_touse = area_inters_column_name
            area_inters_column_in_output = f',"{area_inters_column_name}"'
            area_inters_column_0_in_output = f',0 AS "{area_inters_column_name}"'
        else:
            area_inters_column_name_touse = "area_inters"
        area_inters_column_expression = (
            ",ST_area(ST_intersection(sub_filter.geom, sub_filter.l2_geom)) "
            f'as "{area_inters_column_name_touse}"'
        )
        if min_area_intersect is not None:
            area_inters_filter = (
                f'WHERE sub_area."{area_inters_column_name_touse}" '
                f">= {min_area_intersect}"
            )

    # Prepare spatial relations filter
    if spatial_relations_query != "intersects is True":
        # joining should only be possible on features that at least have an
        # interaction! So, add "intersects is True" to query to evade errors!
        spatial_relations_query = f"({spatial_relations_query}) and intersects is True"
    spatial_relations_filter = _prepare_spatial_relations_filter(
        spatial_relations_query
    )

    # Prepare sql template
    #
    # Remark: use "LIMIT -1 OFFSET 0" to evade that the sqlite query optimizer
    #     "flattens" the subquery, as that makes checking the spatial
    #     relations (using ST_RelateMatch) very slow!
    input1_layer_rtree = "rtree_{input1_layer}_{input1_geometrycolumn}"
    input2_layer_rtree = "rtree_{input2_layer}_{input2_geometrycolumn}"
    sql_template = f"""
        WITH layer1_relations_filtered AS (
          SELECT sub_area.*
            FROM (
              SELECT sub_filter.*
                    {area_inters_column_expression}
                FROM (
                  SELECT layer1.{{input1_geometrycolumn}} as geom
                        ,layer1.fid l1_fid
                        ,layer2.{{input2_geometrycolumn}} as l2_geom
                        {{layer1_columns_prefix_alias_str}}
                        {{layer2_columns_prefix_alias_str}}
                        ,ST_relate(layer1.{{input1_geometrycolumn}},
                                   layer2.{{input2_geometrycolumn}}) as spatial_relation
                    FROM {{input1_databasename}}."{{input1_layer}}" layer1
                    JOIN {{input1_databasename}}."{input1_layer_rtree}" layer1tree
                      ON layer1.fid = layer1tree.id
                    JOIN {{input2_databasename}}."{{input2_layer}}" layer2
                    JOIN {{input2_databasename}}."{input2_layer_rtree}" layer2tree
                      ON layer2.fid = layer2tree.id
                   WHERE 1=1
                     {{batch_filter}}
                     AND layer1tree.minx <= layer2tree.maxx
                     AND layer1tree.maxx >= layer2tree.minx
                     AND layer1tree.miny <= layer2tree.maxy
                     AND layer1tree.maxy >= layer2tree.miny
                   LIMIT -1 OFFSET 0
                  ) sub_filter
               WHERE {spatial_relations_filter.format(
                    spatial_relation="sub_filter.spatial_relation")}
               LIMIT -1 OFFSET 0
              ) sub_area
           {area_inters_filter}
          )
        SELECT sub.geom
              {{layer1_columns_from_subselect_str}}
              {{layer2_columns_from_subselect_str}}
              ,sub.spatial_relation
              {area_inters_column_in_output}
          FROM layer1_relations_filtered sub
    """

    # If a left join is asked, add all features from layer1 that weren't
    # matched.
    if discard_nonmatching is False:
        sql_template = f"""
            {sql_template}
            UNION ALL
            SELECT layer1.{{input1_geometrycolumn}} as geom
                  {{layer1_columns_prefix_alias_str}}
                  {{layer2_columns_prefix_alias_null_str}}
                  ,NULL as spatial_relation
                  {area_inters_column_0_in_output}
              FROM {{input1_databasename}}."{{input1_layer}}" layer1
             WHERE 1=1
               {{batch_filter}}
               AND layer1.fid NOT IN (
                   SELECT l1_fid FROM layer1_relations_filtered)
        """

    # Go!
    input1_layer_info = gfo.get_layerinfo(input1_path, input1_layer)
    return _two_layer_vector_operation(
        input1_path=input1_path,
        input2_path=input2_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="join_by_location",
        input1_layer=input1_layer,
        input1_columns=input1_columns,
        input1_columns_prefix=input1_columns_prefix,
        input2_layer=input2_layer,
        input2_columns=input2_columns,
        input2_columns_prefix=input2_columns_prefix,
        output_layer=output_layer,
        force_output_geometrytype=input1_layer_info.geometrytype,
        explodecollections=explodecollections,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def _prepare_spatial_relations_filter(query: str) -> str:

    named_spatial_relations = {
        # "disjoint": ["FF*FF****"],
        "equals": ["TFFF*FFF*"],
        "touches": ["FT*******", "F**T*****", "F***T****"],
        "within": ["T*F**F***"],
        "overlaps": ["T*T***T**", "1*T***T**"],
        "crosses": ["T*T******", "T*****T**", "0********"],
        "intersects": ["T********", "*T*******", "***T*****", "****T****"],
        "contains": ["T*****FF*"],
        "covers": ["T*****FF*", "*T****FF*", "***T**FF*", "****T*FF*"],
        "coveredby": ["T*F**F***", "*TF**F***", "**FT*F***", "**F*TF***"],
    }

    # Parse query and replace things that need to be replaced
    import re

    query_tokens = re.split("([ =()])", query)

    query_tokens_prepared = []
    nb_unclosed_brackets = 0
    for token in query_tokens:
        if token == "":
            continue
        elif token in [" ", "\n", "\t", "and", "or"]:
            query_tokens_prepared.append(token)
        elif token == "(":
            nb_unclosed_brackets += 1
            query_tokens_prepared.append(token)
        elif token == ")":
            nb_unclosed_brackets -= 1
            query_tokens_prepared.append(token)
        elif token == "is":
            query_tokens_prepared.append("=")
        elif token == "True":
            query_tokens_prepared.append("1")
        elif token == "False":
            query_tokens_prepared.append("0")
        elif token in named_spatial_relations:
            match_list = []
            for spatial_relation in named_spatial_relations[token]:
                match = (
                    f"ST_RelateMatch({{spatial_relation}}, '{spatial_relation}') = 1"
                )
                match_list.append(match)
            query_tokens_prepared.append(f"({' or '.join(match_list)})")
        elif len(token) == 9 and re.fullmatch("^[FT012*]+$", token) is not None:
            token_prepared = f"ST_RelateMatch({{spatial_relation}}, '{token}')"
            query_tokens_prepared.append(token_prepared)
        else:
            raise ValueError(
                f"Unexpected token in query (query is case sensitive!): {token}"
            )

    # If there are unclosed brackets, raise
    if nb_unclosed_brackets > 0:
        raise ValueError(f"not all brackets are closed in query {query}")
    elif nb_unclosed_brackets < 0:
        raise ValueError(f"more closing brackets than opening ones in query {query}")

    result = f"({''.join(query_tokens_prepared)})"
    return result


def join_nearest(
    input1_path: Path,
    input2_path: Path,
    output_path: Path,
    nb_nearest: int,
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input1_columns_prefix: str = "l1_",
    input2_layer: Optional[str] = None,
    input2_columns: Optional[List[str]] = None,
    input2_columns_prefix: str = "l2_",
    output_layer: Optional[str] = None,
    explodecollections: bool = False,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # Init some things...
    # Because there is preprocessing done in this function, check output path
    # here already
    if output_path.exists() and force is False:
        logger.info(f"Stop join_nearest: output exists already {output_path}")
        return
    if input1_layer is None:
        input1_layer = gfo.get_only_layer(input1_path)
    if input2_layer is None:
        input2_layer = gfo.get_only_layer(input2_path)

    # Prepare input files
    # To use knn index, the input layers need to be in sqlite file format
    # (not a .gpkg!), so prepare this
    if input1_path == input2_path and GeofileType(input1_path) == GeofileType.SQLite:
        # Input files already ok...
        input1_tmp_path = input1_path
        input1_tmp_layer = input1_layer
        input2_tmp_path = input2_path
        input2_tmp_layer = input2_layer
    else:
        # Put input2 layer in sqlite gfo...
        tempdir = _io_util.create_tempdir("geofileops/join_nearest")
        input1_tmp_path = tempdir / "both_input_layers.sqlite"
        input1_tmp_layer = "input1_layer"
        gfo.convert(
            src=input1_path,
            src_layer=input1_layer,
            dst=input1_tmp_path,
            dst_layer=input1_tmp_layer,
        )

        # Add input2 layer to sqlite gfo...
        input2_tmp_path = input1_tmp_path
        input2_tmp_layer = "input2_layer"
        gfo.append_to(
            src=input2_path,
            src_layer=input2_layer,
            dst=input2_tmp_path,
            dst_layer=input2_tmp_layer,
        )

    # Remark: the 2 input layers need to be in one file!
    sql_template = f"""
            SELECT layer1.{{input1_geometrycolumn}} as geom
                  {{layer1_columns_prefix_alias_str}}
                  {{layer2_columns_prefix_alias_str}}
                  ,k.pos, k.distance
              FROM {{input1_databasename}}."{{input1_layer}}" layer1
              JOIN {{input2_databasename}}.knn k
              JOIN {{input2_databasename}}."{{input2_layer}}" layer2
                ON layer2.rowid = k.fid
             WHERE k.f_table_name = '{{input2_layer}}'
                AND k.f_geometry_column = '{{input2_geometrycolumn}}'
                AND k.ref_geometry = layer1.{{input1_geometrycolumn}}
                AND k.max_items = {nb_nearest}
                {{batch_filter}}
            """

    input1_layer_info = gfo.get_layerinfo(input1_path, input1_layer)

    # Go!
    return _two_layer_vector_operation(
        input1_path=input1_tmp_path,
        input2_path=input2_tmp_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="join_nearest",
        input1_layer=input1_tmp_layer,
        input1_columns=input1_columns,
        input1_columns_prefix=input1_columns_prefix,
        input2_layer=input2_tmp_layer,
        input2_columns=input2_columns,
        input2_columns_prefix=input2_columns_prefix,
        output_layer=output_layer,
        force_output_geometrytype=input1_layer_info.geometrytype,
        explodecollections=explodecollections,
        use_ogr=True,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def select_two_layers(
    input1_path: Path,
    input2_path: Path,
    output_path: Path,
    sql_stmt: str,
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input1_columns_prefix: str = "l1_",
    input2_layer: Optional[str] = None,
    input2_columns: Optional[List[str]] = None,
    input2_columns_prefix: str = "l2_",
    output_layer: Optional[str] = None,
    force_output_geometrytype: Optional[GeometryType] = None,
    explodecollections: bool = False,
    nb_parallel: int = 1,
    batchsize: int = -1,
    force: bool = False,
):

    # Go!
    return _two_layer_vector_operation(
        input1_path=input1_path,
        input2_path=input2_path,
        output_path=output_path,
        sql_template=sql_stmt,
        operation_name="select_two_layers",
        input1_layer=input1_layer,
        input1_columns=input1_columns,
        input1_columns_prefix=input1_columns_prefix,
        input2_layer=input2_layer,
        input2_columns=input2_columns,
        input2_columns_prefix=input2_columns_prefix,
        output_layer=output_layer,
        force_output_geometrytype=force_output_geometrytype,
        explodecollections=explodecollections,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def split(
    input1_path: Path,
    input2_path: Path,
    output_path: Path,
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input1_columns_prefix: str = "l1_",
    input2_layer: Optional[str] = None,
    input2_columns: Optional[List[str]] = None,
    input2_columns_prefix: str = "l2_",
    output_layer: Optional[str] = None,
    explodecollections: bool = False,
    output_with_spatial_index: bool = True,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # In the query, important to only extract the geometry types that are
    # expected, so the primitive type of input1_layer
    # TODO: test for geometrycollection, line, point,...
    input1_layer_info = gfo.get_layerinfo(input1_path, input1_layer)
    primitivetype_to_extract = input1_layer_info.geometrytype.to_primitivetype

    # For the output file, force MULTI variant to evade ugly warnings
    force_output_geometrytype = primitivetype_to_extract.to_multitype

    # Prepare sql template for this operation
    input1_layer_rtree = "rtree_{input1_layer}_{input1_geometrycolumn}"
    input2_layer_rtree = "rtree_{input2_layer}_{input2_geometrycolumn}"
    sql_template = f"""
        SELECT * FROM
          ( WITH layer2_unioned AS (
              SELECT layer1.rowid AS layer1_rowid
                    ,ST_union(layer2.{{input2_geometrycolumn}}) AS geom
                FROM {{input1_databasename}}."{{input1_layer}}" layer1
                JOIN {{input1_databasename}}."{input1_layer_rtree}" layer1tree
                  ON layer1.fid = layer1tree.id
                JOIN {{input2_databasename}}."{{input2_layer}}" layer2
                JOIN {{input2_databasename}}."{input2_layer_rtree}" layer2tree
                  ON layer2.fid = layer2tree.id
               WHERE 1=1
                 {{batch_filter}}
                 AND layer1tree.minx <= layer2tree.maxx
                 AND layer1tree.maxx >= layer2tree.minx
                 AND layer1tree.miny <= layer2tree.maxy
                 AND layer1tree.maxy >= layer2tree.miny
                 AND ST_Intersects(layer1.{{input1_geometrycolumn}},
                                   layer2.{{input2_geometrycolumn}}) = 1
                 AND ST_Touches(layer1.{{input1_geometrycolumn}},
                                layer2.{{input2_geometrycolumn}}) = 0
               GROUP BY layer1.rowid
            )
            SELECT ST_CollectionExtract(
                        ST_intersection(layer1.{{input1_geometrycolumn}},
                                        layer2.{{input2_geometrycolumn}}),
                        {primitivetype_to_extract.value}) as geom
                  {{layer1_columns_prefix_alias_str}}
                  {{layer2_columns_prefix_alias_str}}
              FROM {{input1_databasename}}."{{input1_layer}}" layer1
              JOIN {{input1_databasename}}."{input1_layer_rtree}" layer1tree
                ON layer1.fid = layer1tree.id
              JOIN {{input2_databasename}}."{{input2_layer}}" layer2
              JOIN {{input2_databasename}}."{input2_layer_rtree}" layer2tree
                ON layer2.fid = layer2tree.id
             WHERE 1=1
               {{batch_filter}}
               AND layer1tree.minx <= layer2tree.maxx
               AND layer1tree.maxx >= layer2tree.minx
               AND layer1tree.miny <= layer2tree.maxy
               AND layer1tree.maxy >= layer2tree.miny
               AND ST_Intersects(layer1.{{input1_geometrycolumn}},
                                 layer2.{{input2_geometrycolumn}}) = 1
               AND ST_Touches(layer1.{{input1_geometrycolumn}},
                              layer2.{{input2_geometrycolumn}}) = 0
            UNION ALL
            SELECT CASE WHEN layer2_unioned.geom IS NULL
                        THEN layer1.{{input1_geometrycolumn}}
                        ELSE ST_CollectionExtract(
                                ST_difference(layer1.{{input1_geometrycolumn}},
                                              layer2_unioned.geom),
                                {primitivetype_to_extract.value})
                   END as geom
                  {{layer1_columns_prefix_alias_str}}
                  {{layer2_columns_prefix_alias_null_str}}
              FROM {{input1_databasename}}."{{input1_layer}}" layer1
              LEFT JOIN layer2_unioned ON layer1.rowid = layer2_unioned.layer1_rowid
             WHERE 1=1
               {{batch_filter}}
           )
         WHERE geom IS NOT NULL
           AND ST_NPoints(geom) > 0
    """

    # Go!
    return _two_layer_vector_operation(
        input1_path=input1_path,
        input2_path=input2_path,
        output_path=output_path,
        sql_template=sql_template,
        operation_name="split",
        input1_layer=input1_layer,
        input1_columns=input1_columns,
        input1_columns_prefix=input1_columns_prefix,
        input2_layer=input2_layer,
        input2_columns=input2_columns,
        input2_columns_prefix=input2_columns_prefix,
        output_layer=output_layer,
        force_output_geometrytype=force_output_geometrytype,
        explodecollections=explodecollections,
        output_with_spatial_index=output_with_spatial_index,
        nb_parallel=nb_parallel,
        batchsize=batchsize,
        force=force,
    )


def symmetric_difference(
    input1_path: Path,
    input2_path: Path,
    output_path: Path,
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input1_columns_prefix: str = "l1_",
    input2_layer: Optional[str] = None,
    input2_columns: Optional[List[str]] = None,
    input2_columns_prefix: str = "l2_",
    output_layer: Optional[str] = None,
    explodecollections: bool = False,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # A symmetric difference can be simulated by doing an "erase" of input1
    # and input2 and then append the result of an erase of input2 with
    # input1...

    # Because both erase calculations will be towards temp files,
    # we need to do some additional init + checks here...
    if force is False and output_path.exists():
        return
    if output_layer is None:
        output_layer = gfo.get_default_layer(output_path)

    tempdir = _io_util.create_tempdir("geofileops/symmdiff")
    try:
        # First erase input2 from input1 to a temporary output file
        erase1_output_path = tempdir / "layer1_erase_layer2_output.gpkg"
        erase(
            input_path=input1_path,
            erase_path=input2_path,
            output_path=erase1_output_path,
            input_layer=input1_layer,
            input_columns=input1_columns,
            input_columns_prefix=input1_columns_prefix,
            erase_layer=input2_layer,
            output_layer=output_layer,
            explodecollections=explodecollections,
            output_with_spatial_index=False,
            nb_parallel=nb_parallel,
            batchsize=batchsize,
            force=force,
        )

        if input2_columns is None or len(input2_columns) > 0:
            input2_info = gfo.get_layerinfo(input2_path)
            columns_to_add = (
                input2_columns if input2_columns is not None else input2_info.columns
            )
            for column in columns_to_add:
                gfo.add_column(
                    erase1_output_path,
                    name=f"{input2_columns_prefix}{column}",
                    type=input2_info.columns[column].gdal_type,
                )

        # Now erase input1 from input2 to another temporary output file
        erase2_output_path = tempdir / "layer2_erase_layer1_output.gpkg"
        erase(
            input_path=input2_path,
            erase_path=input1_path,
            output_path=erase2_output_path,
            input_layer=input2_layer,
            input_columns=input2_columns,
            input_columns_prefix=input2_columns_prefix,
            erase_layer=input1_layer,
            output_layer=output_layer,
            explodecollections=explodecollections,
            output_with_spatial_index=False,
            nb_parallel=nb_parallel,
            batchsize=batchsize,
            force=force,
        )

        # Now append
        _append_to_nolock(
            src=erase2_output_path,
            dst=erase1_output_path,
            src_layer=output_layer,
            dst_layer=output_layer,
        )

        # Create spatial index
        gfo.create_spatial_index(path=erase1_output_path, layer=output_layer)

        # Now we are ready to move the result to the final spot...
        if output_path.exists():
            gfo.remove(output_path)
        gfo.move(erase1_output_path, output_path)

    finally:
        shutil.rmtree(tempdir)


def union(
    input1_path: Path,
    input2_path: Path,
    output_path: Path,
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input1_columns_prefix: str = "l1_",
    input2_layer: Optional[str] = None,
    input2_columns: Optional[List[str]] = None,
    input2_columns_prefix: str = "l2_",
    output_layer: Optional[str] = None,
    explodecollections: bool = False,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):

    # A union can be simulated by doing a "split" of input1 and input2 and
    # then append the result of an erase of input2 with input1...

    # Because the calculations in split and erase will be towards temp files,
    # we need to do some additional init + checks here...
    if force is False and output_path.exists():
        return
    if output_layer is None:
        output_layer = gfo.get_default_layer(output_path)

    tempdir = _io_util.create_tempdir("geofileops/union")
    try:
        # First split input1 with input2 to a temporary output gfo...
        split_output_path = tempdir / "split_output.gpkg"
        split(
            input1_path=input1_path,
            input2_path=input2_path,
            output_path=split_output_path,
            input1_layer=input1_layer,
            input1_columns=input1_columns,
            input1_columns_prefix=input1_columns_prefix,
            input2_layer=input2_layer,
            input2_columns=input2_columns,
            input2_columns_prefix=input2_columns_prefix,
            output_layer=output_layer,
            explodecollections=explodecollections,
            output_with_spatial_index=False,
            nb_parallel=nb_parallel,
            batchsize=batchsize,
            force=force,
        )

        # Now erase input1 from input2 to another temporary output gfo...
        erase_output_path = tempdir / "erase_output.gpkg"
        erase(
            input_path=input2_path,
            erase_path=input1_path,
            output_path=erase_output_path,
            input_layer=input2_layer,
            input_columns=input2_columns,
            input_columns_prefix=input2_columns_prefix,
            erase_layer=input1_layer,
            output_layer=output_layer,
            explodecollections=explodecollections,
            output_with_spatial_index=False,
            nb_parallel=nb_parallel,
            batchsize=batchsize,
            force=force,
        )

        # Now append
        _append_to_nolock(
            src=erase_output_path,
            dst=split_output_path,
            src_layer=output_layer,
            dst_layer=output_layer,
        )

        # Create spatial index
        gfo.create_spatial_index(path=split_output_path, layer=output_layer)

        # Now we are ready to move the result to the final spot...
        if output_path.exists():
            gfo.remove(output_path)
        gfo.move(split_output_path, output_path)

    finally:
        shutil.rmtree(tempdir)


def _two_layer_vector_operation(
    input1_path: Path,
    input2_path: Path,
    output_path: Path,
    sql_template: str,
    operation_name: str,
    input1_layer: Optional[str] = None,
    input1_columns: Optional[List[str]] = None,
    input1_columns_prefix: str = "l1_",
    input2_layer: Optional[str] = None,
    input2_columns: Optional[List[str]] = None,
    input2_columns_prefix: str = "l2_",
    output_layer: Optional[str] = None,
    explodecollections: bool = False,
    force_output_geometrytype: Optional[GeometryType] = None,
    output_with_spatial_index: bool = True,
    use_ogr: bool = False,
    nb_parallel: int = -1,
    batchsize: int = -1,
    force: bool = False,
):
    """
    Executes an operation that needs 2 input files.

    Args:
        input1_path (str): the file to export features from
        input2_path (str): the file to check intersections with
        output_path (str): output file
        input1_layer (str, optional): [description]. Defaults to None.
        input1_columns
        input1_columns_prefix
        input2_layer (str, optional): [description]. Defaults to None.
        input2_columns
        input2_columns_prefix
        output_layer (str, optional): [description]. Defaults to None.
        explodecollections (bool, optional): Explode collecions in output.
            Defaults to False.
        force_output_geometrytype (GeometryType, optional): Defaults to None.
        use_ogr (bool, optional): If True, ogr is used to do the processing,
            In this case different input files (input1_path, input2_path) are
            NOT supported. If False, sqlite3 is used directly.
            Defaults to False.
        nb_parallel (int, optional): [description]. Defaults to -1.
        batchsize (int, optional): indicative number of rows to process per
            batch. A smaller batch size, possibly in combination with a
            smaller nb_parallel, will reduce the memory usage.
            Defaults to -1: (try to) determine optimal size automatically.
        force (bool, optional): [description]. Defaults to False.

    Raises:
        Exception: [description]
    """
    # Init
    if not input1_path.exists():
        raise Exception(
            f"Error {operation_name}: input1_path doesn't exist: {input1_path}"
        )
    if not input2_path.exists():
        raise Exception(
            f"Error {operation_name}: input2_path doesn't exist: {input2_path}"
        )
    if use_ogr is True and input1_path != input2_path:
        raise Exception(
            f"Error {operation_name}: if use_ogr True, input1_path == input2_path!"
        )
    if output_path.exists():
        if force is False:
            logger.info(f"Stop {operation_name}: output exists already {output_path}")
            return
        else:
            gfo.remove(output_path)

    # Check if spatialite is properly installed to execute this query
    _sqlite_util.check_runtimedependencies()

    # Init layer info
    start_time = datetime.now()
    if input1_layer is None:
        input1_layer = gfo.get_only_layer(input1_path)
    if input2_layer is None:
        input2_layer = gfo.get_only_layer(input2_path)
    if output_layer is None:
        output_layer = gfo.get_default_layer(output_path)
    tempdir = _io_util.create_tempdir(f"geofileops/{operation_name}")

    # Use get_layerinfo to check if the input files are valid
    gfo.get_layerinfo(input1_path, input1_layer)
    gfo.get_layerinfo(input2_path, input2_layer)

    # Prepare output filename
    tmp_output_path = tempdir / output_path.name
    tmp_output_path.parent.mkdir(exist_ok=True, parents=True)
    gfo.remove(tmp_output_path)

    try:
        # Prepare tmp files/batches
        logger.info(
            f"Prepare input (params) for {operation_name} with tempdir: {tempdir}"
        )
        processing_params = _prepare_processing_params(
            input1_path=input1_path,
            input1_layer=input1_layer,
            input1_layer_alias="layer1",
            input2_path=input2_path,
            input2_layer=input2_layer,
            tempdir=tempdir,
            nb_parallel=nb_parallel,
            batchsize=batchsize,
            convert_to_spatialite_based=True,
        )
        if processing_params is None or processing_params.batches is None:
            return

        # Prepare column names,... to format the select
        # Format column strings for use in select
        assert processing_params.input1_path is not None
        input1_tmp_layerinfo = gfo.get_layerinfo(
            processing_params.input1_path, processing_params.input1_layer
        )
        input1_strs = format_column_strings(
            columns_specified=input1_columns,
            columns_available=input1_tmp_layerinfo.columns,
            table_alias="layer1",
            columnname_prefix=input1_columns_prefix,
        )
        assert processing_params.input2_path is not None
        input2_tmp_layerinfo = gfo.get_layerinfo(
            processing_params.input2_path, processing_params.input2_layer
        )
        input2_strs = format_column_strings(
            columns_specified=input2_columns,
            columns_available=input2_tmp_layerinfo.columns,
            table_alias="layer2",
            columnname_prefix=input2_columns_prefix,
        )

        # Check input crs'es
        if input1_tmp_layerinfo.crs != input2_tmp_layerinfo.crs:
            logger.warning(
                "input1 has a different crs than input2: \n\tinput1: "
                f"{input1_tmp_layerinfo.crs} \n\tinput2: {input2_tmp_layerinfo.crs}"
            )

        # Calculate
        # Processing in threads is 2x faster for small datasets (on Windows)
        calculate_in_threads = (
            True if input1_tmp_layerinfo.featurecount <= 100 else False
        )
        logger.info(
            f"Start {operation_name} ({processing_params.nb_parallel} parallel workers)"
        )
        with _general_util.PooledExecutorFactory(
            threadpool=calculate_in_threads,
            max_workers=processing_params.nb_parallel,
            initializer=_general_util.initialize_worker(),
        ) as calculate_pool:

            # Start looping
            batches = {}
            future_to_batch_id = {}
            for batch_id in processing_params.batches:

                batches[batch_id] = {}
                batches[batch_id]["layer"] = output_layer

                tmp_partial_output_path = (
                    tempdir / f"{output_path.stem}_{batch_id}.gpkg"
                )
                batches[batch_id]["tmp_partial_output_path"] = tmp_partial_output_path

                # Keep input1_tmp_layer and input2_tmp_layer for backwards
                # compatibility
                sql_stmt = sql_template.format(
                    input1_databasename="{input1_databasename}",
                    input2_databasename="{input2_databasename}",
                    layer1_columns_from_subselect_str=input1_strs.columns_subselect,
                    layer1_columns_prefix_alias_str=input1_strs.columns_prefix_alias,
                    layer1_columns_prefix_str=input1_strs.columns_prefix,
                    input1_layer=processing_params.batches[batch_id]["layer"],
                    input1_tmp_layer=processing_params.batches[batch_id]["layer"],
                    input1_geometrycolumn=input1_tmp_layerinfo.geometrycolumn,
                    layer2_columns_from_subselect_str=input2_strs.columns_subselect,
                    layer2_columns_prefix_alias_str=input2_strs.columns_prefix_alias,
                    layer2_columns_prefix_str=input2_strs.columns_prefix,
                    layer2_columns_prefix_alias_null_str=input2_strs.columns_prefix_alias_null,  # noqa: E501
                    input2_layer=processing_params.input2_layer,
                    input2_tmp_layer=processing_params.input2_layer,
                    input2_geometrycolumn=input2_tmp_layerinfo.geometrycolumn,
                    batch_filter=processing_params.batches[batch_id]["batch_filter"],
                )

                batches[batch_id]["sqlite_stmt"] = sql_stmt

                # Remark: this temp file doesn't need spatial index
                if use_ogr is False:
                    # Use an aggressive speedy sqlite profile
                    future = calculate_pool.submit(
                        _sqlite_util.create_table_as_sql,
                        input1_path=processing_params.batches[batch_id]["path"],
                        input1_layer=processing_params.batches[batch_id]["layer"],
                        input2_path=processing_params.input2_path,
                        output_path=tmp_partial_output_path,
                        sql_stmt=sql_stmt,
                        output_layer=output_layer,
                        output_geometrytype=force_output_geometrytype,
                        create_spatial_index=False,
                        profile=_sqlite_util.SqliteProfile.SPEED,
                    )
                    future_to_batch_id[future] = batch_id
                else:
                    # Use ogr to run the query
                    #   * input2 path (= using attach) doesn't seem to work
                    #   * ogr doesn't fill out database names, so do it now
                    sql_stmt = sql_stmt.format(
                        input1_databasename=processing_params.input1_databasename,
                        input2_databasename=processing_params.input2_databasename,
                    )

                    future = calculate_pool.submit(
                        _ogr_util.vector_translate,
                        input_path=processing_params.batches[batch_id]["path"],
                        output_path=tmp_partial_output_path,
                        sql_stmt=sql_stmt,
                        output_layer=output_layer,
                        explodecollections=explodecollections,
                        force_output_geometrytype=force_output_geometrytype,
                        options={"LAYER_CREATION.SPATIAL_INDEX": False},
                    )
                future_to_batch_id[future] = batch_id

            # Loop till all parallel processes are ready, but process each one
            # that is ready already
            nb_done = 0
            _general_util.report_progress(
                start_time,
                nb_done,
                len(processing_params.batches),
                operation_name,
                processing_params.nb_parallel,
            )
            for future in futures.as_completed(future_to_batch_id):
                try:
                    # Get the result
                    result = future.result()
                    if result is not None:
                        logger.debug(result)

                    # Start copy of the result to a common file
                    batch_id = future_to_batch_id[future]

                    # If the calculate gave results, copy to output
                    tmp_partial_output_path = batches[batch_id][
                        "tmp_partial_output_path"
                    ]
                    if (
                        tmp_partial_output_path.exists()
                        and tmp_partial_output_path.stat().st_size > 0
                    ):
                        fileops._append_to_nolock(
                            src=tmp_partial_output_path,
                            dst=tmp_output_path,
                            explodecollections=explodecollections,
                            force_output_geometrytype=force_output_geometrytype,
                            create_spatial_index=False,
                        )
                    else:
                        logger.debug(f"Result file {tmp_partial_output_path} was empty")

                    # Cleanup tmp partial file
                    gfo.remove(tmp_partial_output_path, missing_ok=True)

                except Exception as ex:
                    batch_id = future_to_batch_id[future]
                    raise Exception(f"Error executing {batches[batch_id]}") from ex

                # Log the progress and prediction speed
                nb_done += 1
                _general_util.report_progress(
                    start_time=start_time,
                    nb_done=nb_done,
                    nb_todo=len(processing_params.batches),
                    operation=operation_name,
                    nb_parallel=processing_params.nb_parallel,
                )

        # Round up and clean up
        # Now create spatial index and move to output location
        if tmp_output_path.exists():
            if output_with_spatial_index is True:
                gfo.create_spatial_index(path=tmp_output_path, layer=output_layer)
            if tmp_output_path != output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                gfo.move(tmp_output_path, output_path)
        else:
            logger.debug(f"Result of {operation_name} was empty!")

        logger.info(f"{operation_name} ready, took {datetime.now()-start_time}!")
    except Exception:
        gfo.remove(output_path)
        gfo.remove(tmp_output_path)
        raise
    finally:
        shutil.rmtree(tempdir)


class ProcessingParams:
    def __init__(
        self,
        input1_path: Optional[Path] = None,
        input1_layer: Optional[str] = None,
        input1_databasename: Optional[str] = None,
        input2_path: Optional[Path] = None,
        input2_layer: Optional[str] = None,
        input2_databasename: Optional[str] = None,
        nb_parallel: int = -1,
        batches: Optional[dict] = None,
    ):
        self.input1_path = input1_path
        self.input1_layer = input1_layer
        self.input1_databasename = input1_databasename
        self.input2_path = input2_path
        self.input2_layer = input2_layer
        self.input2_databasename = input2_databasename
        self.nb_parallel = nb_parallel
        self.batches = batches


def _prepare_processing_params(
    input1_path: Path,
    input1_layer: str,
    tempdir: Path,
    convert_to_spatialite_based: bool,
    nb_parallel: int,
    batchsize: int = -1,
    input1_layer_alias: Optional[str] = None,
    input2_path: Optional[Path] = None,
    input2_layer: Optional[str] = None,
) -> Optional[ProcessingParams]:

    # Init
    returnvalue = ProcessingParams(nb_parallel=nb_parallel)
    input1_layerinfo = gfo.get_layerinfo(input1_path, input1_layer)

    if input1_layerinfo.featurecount == 0:
        logger.info(
            f"input1 layer contains 0 rows, file: {input1_path}, layer: {input1_layer}"
        )
        return None

    # Determine the optimal number of parallel processes + batches
    if returnvalue.nb_parallel == -1:
        # If no batch size specified, put at least 100 rows in a batch
        if batchsize <= 0:
            min_rows_per_batch = 100
        else:
            # If batchsize is specified, use the batch size
            min_rows_per_batch = batchsize

        max_parallel = max(int(input1_layerinfo.featurecount / min_rows_per_batch), 1)
        returnvalue.nb_parallel = min(multiprocessing.cpu_count(), max_parallel)

    # Determine optimal number of batches
    # Remark: especially for 'select' operation, if nb_parallel is 1
    #         nb_batches should be 1 (select might give wrong results)
    if returnvalue.nb_parallel > 1:
        # Limit number of rows processed in parallel to limit memory use
        if batchsize > 0:
            max_rows_parallel = batchsize * returnvalue.nb_parallel
        else:
            max_rows_parallel = 200000

        # Adapt number of batches to max_rows_parallel
        if input1_layerinfo.featurecount > max_rows_parallel:
            # If more rows than can be handled simultanously in parallel
            nb_batches = int(
                input1_layerinfo.featurecount
                / (max_rows_parallel / returnvalue.nb_parallel)
            )
        elif batchsize > 0:
            # If a batchsize is specified, try to honer it
            nb_batches = returnvalue.nb_parallel
        else:
            # If no batchsize specified, add some batches to reduce impact of possible
            # "unbalanced" batches regarding needed processing time.
            nb_batches = returnvalue.nb_parallel * 2

    elif batchsize > 0:
        nb_batches = math.ceil(input1_layerinfo.featurecount / batchsize)
    else:
        nb_batches = 1

    # Prepare input files for the calculation
    returnvalue.input1_layer = input1_layer
    returnvalue.input2_layer = input2_layer

    if convert_to_spatialite_based is False:
        returnvalue.input1_path = input1_path
        returnvalue.input2_path = input2_path
    else:
        # Check if the input files are of the correct geofiletype
        input1_geofiletype = GeofileType(input1_path)
        input2_geofiletype = None
        if input2_path is not None:
            input2_geofiletype = GeofileType(input2_path)

        # If input files are of the same format + are spatialite compatible,
        # just use them
        if input1_geofiletype.is_spatialite_based and (
            input2_geofiletype is None or input1_geofiletype == input2_geofiletype
        ):
            returnvalue.input1_path = input1_path
        else:
            # If not ok, copy the input layer to gpkg
            returnvalue.input1_path = tempdir / f"{input1_path.stem}.gpkg"
            gfo.convert(
                src=input1_path,
                src_layer=input1_layer,
                dst=returnvalue.input1_path,
                dst_layer=returnvalue.input1_layer,
            )

        if input2_path is not None and input2_geofiletype is not None:
            if (
                input2_geofiletype == input1_geofiletype
                and input2_geofiletype.is_spatialite_based
            ):
                returnvalue.input2_path = input2_path
            else:
                # If not spatialite compatible, copy the input layer to gpkg
                returnvalue.input2_path = tempdir / f"{input2_path.stem}.gpkg"
                gfo.convert(
                    src=input2_path,
                    src_layer=input2_layer,
                    dst=returnvalue.input2_path,
                    dst_layer=returnvalue.input2_layer,
                )

    # Fill out the database names to use in the sql statements
    returnvalue.input1_databasename = "main"
    if input2_path is None or input1_path == input2_path:
        returnvalue.input2_databasename = returnvalue.input1_databasename
    else:
        returnvalue.input2_databasename = "input2"

    # Prepare batches to process
    # Get column names and info
    layer1_info = gfo.get_layerinfo(returnvalue.input1_path, returnvalue.input1_layer)

    # Check number of batches + appoint nb rows to batches
    nb_rows_input_layer = layer1_info.featurecount
    if nb_batches > int(nb_rows_input_layer / 10):
        nb_batches = max(int(nb_rows_input_layer / 10), 1)

    batches = {}
    if nb_batches == 1:
        # If only one batch, no filtering is needed
        batches[0] = {}
        batches[0]["layer"] = returnvalue.input1_layer
        batches[0]["path"] = returnvalue.input1_path
        batches[0]["batch_filter"] = ""
    else:
        # Determine the min_rowid and max_rowid
        sql_stmt = f'''SELECT MIN(rowid) as min_rowid, MAX(rowid) as max_rowid
                         FROM "{layer1_info.name}"'''
        batch_info_df = gfo.read_file_sql(
            path=returnvalue.input1_path, sql_stmt=sql_stmt
        )
        min_rowid = pd.to_numeric(batch_info_df["min_rowid"][0])
        max_rowid = pd.to_numeric(batch_info_df["max_rowid"][0])

        # Determine the exact batches to use
        if ((max_rowid - min_rowid) / nb_rows_input_layer) < 1.1:
            # If the rowid's are quite consecutive, use an imperfect, but
            # fast distribution in batches
            batch_info_list = []
            nb_rows_per_batch = round(nb_rows_input_layer / nb_batches)
            offset = 0
            offset_per_batch = round((max_rowid - min_rowid) / nb_batches)
            for batch_id in range(nb_batches):
                start_rowid = offset
                if batch_id < (nb_batches - 1):
                    # End rowid for this batch is the next start_rowid - 1
                    end_rowid = offset + offset_per_batch - 1
                else:
                    # For the last batch, take the max_rowid so no rowid's are
                    # 'lost' due to rounding errors
                    end_rowid = max_rowid
                batch_info_list.append(
                    (batch_id, nb_rows_per_batch, start_rowid, end_rowid)
                )
                offset += offset_per_batch
            batch_info_df = pd.DataFrame(
                batch_info_list, columns=["id", "nb_rows", "start_rowid", "end_rowid"]
            )
        else:
            # The rowids are not consecutive, so determine the optimal rowid
            # ranges for each batch so each batch has same number of elements
            # Remark: this might take some seconds for larger datasets!
            sql_stmt = f"""
                    SELECT batch_id AS id
                        ,COUNT(*) AS nb_rows
                        ,MIN(rowid) AS start_rowid
                        ,MAX(rowid) AS end_rowid
                    FROM (SELECT rowid
                                ,NTILE({nb_batches}) OVER (ORDER BY rowid) batch_id
                            FROM "{layer1_info.name}"
                        )
                    GROUP BY batch_id;
                    """
            batch_info_df = gfo.read_file_sql(
                path=returnvalue.input1_path, sql_stmt=sql_stmt
            )

        # Prepare the layer alias to use in the batch filter
        layer_alias_d = ""
        if input1_layer_alias is not None:
            layer_alias_d = f"{input1_layer_alias}."

        # Now loop over all batch ranges to build up the necessary filters
        for batch_info in batch_info_df.itertuples():
            # Fill out the batch properties
            batches[batch_info.id] = {}
            batches[batch_info.id]["layer"] = returnvalue.input1_layer
            batches[batch_info.id]["path"] = returnvalue.input1_path

            # The batch filter
            if batch_info.id < nb_batches:
                batches[batch_info.id]["batch_filter"] = (
                    f"AND ({layer_alias_d}rowid >= {batch_info.start_rowid} "
                    f"AND {layer_alias_d}rowid <= {batch_info.end_rowid}) "
                )
            else:
                batches[batch_info.id][
                    "batch_filter"
                ] = f"AND {layer_alias_d}rowid >= {batch_info.start_rowid} "

    # No use starting more processes than the number of batches...
    if len(batches) < returnvalue.nb_parallel:
        returnvalue.nb_parallel = len(batches)

    returnvalue.batches = batches
    return returnvalue


@dataclass
class FormattedColumnStrings:
    columns: str
    columns_prefix: str
    columns_prefix_alias: str
    columns_prefix_alias_null: str
    columns_subselect: str


def format_column_strings(
    columns_specified: Optional[List[str]],
    columns_available: Iterable[str],
    table_alias: str = "",
    columnname_prefix: str = "",
) -> FormattedColumnStrings:

    # First prepare the actual column list to use
    if columns_specified is not None:
        # Case-insensitive check if input1_columns contains columns not in layer...
        columns_available_upper = [column.upper() for column in columns_available]
        missing_columns = [
            col
            for col in columns_specified
            if (col.upper() not in columns_available_upper)
        ]
        if len(missing_columns) > 0:
            raise Exception(
                "Error, columns_specified contains columns not in "
                f"columns_available: {missing_columns}. Available: {columns_available}"
            )

        # Create column list to keep in the casing of the original columns
        columns_specified_upper = [column.upper() for column in columns_specified]
        columns = [
            col for col in columns_available if (col.upper() in columns_specified_upper)
        ]
    else:
        columns = list(columns_available)

    # Now format the column strings
    columns_quoted_str = ""
    columns_prefix_alias_null_str = ""
    columns_prefix_str = ""
    columns_prefix_alias_str = ""
    columns_from_subselect_str = ""
    if len(columns) > 0:
        if table_alias is not None and table_alias != "":
            table_alias_d = f"{table_alias}."
        else:
            table_alias_d = ""
        columns_quoted = [f'"{column}"' for column in columns]
        columns_quoted_str = "," + ", ".join(columns_quoted)
        columns_prefix_alias_null = [
            f'NULL "{columnname_prefix}{column}"' for column in columns
        ]
        columns_prefix_alias_null_str = "," + ", ".join(columns_prefix_alias_null)
        columns_prefix = [f'{table_alias_d}"{column}"' for column in columns]
        columns_prefix_str = "," + ", ".join(columns_prefix)
        columns_table_aliased_column_aliased = [
            f'{table_alias_d}"{column}" "{columnname_prefix}{column}"'
            for column in columns
        ]
        columns_prefix_alias_str = "," + ", ".join(columns_table_aliased_column_aliased)
        columns_from_subselect = [
            f'sub."{columnname_prefix}{column}"' for column in columns
        ]
        columns_from_subselect_str = "," + ", ".join(columns_from_subselect)

    return FormattedColumnStrings(
        columns=columns_quoted_str,
        columns_prefix=columns_prefix_str,
        columns_prefix_alias=columns_prefix_alias_str,
        columns_prefix_alias_null=columns_prefix_alias_null_str,
        columns_subselect=columns_from_subselect_str,
    )


def dissolve_singlethread(
    input_path: Path,
    output_path: Path,
    groupby_columns: Optional[Iterable[str]] = None,
    agg_columns: Optional[dict] = None,
    explodecollections: bool = False,
    input_layer: Optional[str] = None,
    output_layer: Optional[str] = None,
    force: bool = False,
):
    """
    Remark: this is not a parallelized version!!!
    """
    # Init
    start_time = datetime.now()
    if output_path.exists():
        if force is False:
            logger.info(f"Stop dissolve: Output exists already {output_path}")
            return
        else:
            gfo.remove(output_path)

    # Check layer names
    if input_layer is None:
        input_layer = gfo.get_only_layer(input_path)
    if output_layer is None:
        output_layer = gfo.get_default_layer(output_path)

    # Use get_layerinfo to check if the layer definition is OK
    layerinfo = gfo.get_layerinfo(input_path, input_layer)

    # Prepare the strings regarding groupby_columns to use in the select statement.
    if groupby_columns is not None:
        # Because the query uses a subselect, the groupby columns need to be prefixed.
        columns_with_prefix = [f'layer."{column}"' for column in groupby_columns]
        groupby_columns_str = ", ".join(columns_with_prefix)
        groupby_columns_for_groupby_str = groupby_columns_str
        groupby_columns_for_select_str = ", " + groupby_columns_str
    else:
        # Even if no groupby is provided, we still need to use a groupby clause,
        # otherwise ST_union doesn't seem to work.
        groupby_columns_for_groupby_str = "'1'"
        groupby_columns_for_select_str = ""

    # Prepare the strings regarding agg_columns to use in the select statement.
    agg_columns_str = ""
    if agg_columns is not None:
        # Prepare some lists for later use
        columns_upper_dict = {col.upper(): col for col in layerinfo.columns}
        groupby_columns_upper_dict = {}
        if groupby_columns is not None:
            groupby_columns_upper_dict = {col.upper(): col for col in groupby_columns}

        # Start preparation of agg_columns_str
        if "json" in agg_columns:
            agg_columns_str = ""
            # If the columns specified are None, take all columns that are not in
            # groupby_columns
            if agg_columns["json"] is None:
                for column in layerinfo.columns:
                    if column.upper() not in groupby_columns_upper_dict:
                        agg_columns_str += f"'{column}', layer.{column}"
            else:
                for column in agg_columns["json"]:
                    agg_columns_str += f"'{column}', layer.{column}"
            agg_columns_str = f", json_object({agg_columns_str}) as json"
        elif "columns" in agg_columns:
            for agg_column in agg_columns["columns"]:
                # Init
                distinct_str = ""
                extra_param_str = ""

                # Prepare aggregation keyword.
                if agg_column["agg"].lower() in [
                    "count",
                    "sum",
                    "min",
                    "max",
                    "median",
                ]:
                    aggregation_str = agg_column["agg"]
                elif agg_column["agg"].lower() in ["mean", "avg"]:
                    aggregation_str = "avg"
                elif agg_column["agg"].lower() == "concat":
                    aggregation_str = "group_concat"
                    if "sep" in agg_column:
                        extra_param_str = f", '{agg_column['sep']}'"
                else:
                    raise ValueError(
                        f"Error: aggregation {agg_column['agg']} is not supported!"
                    )

                # If distinct is specified, add the distinct keyword
                if "distinct" in agg_column and agg_column["distinct"] is True:
                    distinct_str = "DISTINCT "

                # Prepare column name string.
                # Make sure the columns name casing is same as input file
                column_str = (
                    f'layer."{columns_upper_dict[agg_column["column"].upper()]}"'
                )

                # Now put everything togethers
                agg_columns_str += (
                    f", {aggregation_str}({distinct_str}{column_str}{extra_param_str}) "
                    f'AS "{agg_column["as"]}"'
                )

    # Now prepare the sql statement
    # Remark: calculating the area in the enclosing selects halves the
    # processing time

    # The operation to run on the geometry
    operation = f"ST_union(layer.{layerinfo.geometrycolumn})"
    force_output_geometrytype = None

    # If the input is a linestring, also apply st_linemerge().
    # If not, the individual lines are just concatenated together8 and common
    # points are not removed, resulting in the original seperate lines again
    # if explodecollections is True.
    if layerinfo.geometrytype.to_primitivetype == PrimitiveType.LINESTRING:
        operation = f"ST_LineMerge({operation})"
        if explodecollections is True:
            force_output_geometrytype = GeometryType.LINESTRING

    sql_stmt = f"""
            SELECT {operation} AS geom
                  {groupby_columns_for_select_str}
                  {agg_columns_str}
              FROM "{input_layer}" layer
             GROUP BY {groupby_columns_for_groupby_str}"""

    _ogr_util.vector_translate(
        input_path=input_path,
        output_path=output_path,
        output_layer=output_layer,
        sql_stmt=sql_stmt,
        sql_dialect="SQLITE",
        force_output_geometrytype=force_output_geometrytype,
        explodecollections=explodecollections,
    )

    logger.info(f"Processing ready, took {datetime.now()-start_time}!")
