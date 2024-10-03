import logging
import os
import pickle

import pandas as pd
from fastapi import APIRouter
from geopy.distance import great_circle

from real_estate_modeling_api.api import schemas
from real_estate_modeling_api.db import crud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Function to check eligibility
def check_eligibility(input_data: schemas.EligibilityRequest):
    eligible_categories = []
    for category, criteria in eligibility_criteria.items():
        if (criteria["min_area"] <= input_data.area <= criteria["max_area"] and
            input_data.floor in criteria["floor"]):
            eligible_categories.append(category)

    return eligible_categories


@router.post("/check_eligibility/")
def get_eligibility_check(input_data: schemas.EligibilityRequest):
    eligible_categories = check_eligibility(input_data)
    return {"eligible_categories": eligible_categories}