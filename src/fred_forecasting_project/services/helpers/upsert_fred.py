import logging
import numpy as np

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import or_

from fred_forecasting_project.models.observations import Observation

logger = logging.getLogger(__name__)
def upsert_fred(session, df):
    if df.empty:
        logger.info("No observations to upsert.")
        return
    
    records = (
        df.reset_index(names="date")
        .assign(date=lambda x: x["date"].dt.date)
        .replace({np.nan: None})
        .to_dict(orient="records")
    )

    update_cols = [
        c.name
        for c in Observation.__table__.columns
        if c.name != "date"
    ]

    stmt = insert(Observation).values(records)
    
    stmt = stmt.on_conflict_do_update(
        index_elements=["date"],
        set_={
            col: getattr(stmt.excluded, col)
            for col in update_cols
        },
        where=or_(
            *[
                Observation.__table__.c[col].is_distinct_from(
                    stmt.excluded[col]
                )
                for col in update_cols
            ]
        ),
    )

    session.execute(stmt)
    logger.info("Upserted %d FRED observations.", len(records))