import logging
import os
import pickle
import yaml
import pandas as pd
from fastapi import APIRouter
from geopy.distance import great_circle

from real_estate_modeling_api.api import schemas
from real_estate_modeling_api.db import crud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def load_yaml_to_list(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        # Load the YAML content
        yaml_data = yaml.safe_load(file)
        
        # Extract the 'items' list
        items = yaml_data['service']['eligibility']['items']
        return items


yaml_file_path = './src/real_estate_modeling_api/conf/config.yaml'
eligibility_criteria = load_yaml_to_list(yaml_file_path)

# Function to check eligibility
def check_eligibility(input_data: schemas.EligibilityRequest):
    eligible_categories = []
    for item in eligibility_criteria:
        if not item["min_area"]:
            item["min_area"] = 0
        if not item["max_area"]:
            item["max_area"] = 999999
        if (item["min_area"] <= input_data.area <= item["max_area"]):
            if not item["floors"]:
                eligible_categories.append(item["name"])
            else:    
                if isinstance(item["floors"], int):
                    item["floors"] = [item["floors"]]
                if input_data.floor in item["floors"]:
                    eligible_categories.append(item["name"])
            

    return eligible_categories


@router.get("/criteria")
def get_eligibility_check():
    return {"eligibility_criteria": eligibility_criteria}


@router.post("/check")
def get_eligibility_check(input_data: schemas.EligibilityRequest):
    eligible_categories = check_eligibility(input_data)
    return {"eligible_categories": eligible_categories}
