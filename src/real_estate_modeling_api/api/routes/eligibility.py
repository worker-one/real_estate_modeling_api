import logging
import yaml
from fastapi import APIRouter
from real_estate_modeling_api.api import schemas
from real_estate_modeling_api.core.eligibility import (
    check_eligibility_facility,
    check_eligibility_land,
    facility_eligibility_table,
    land_eligibility_table
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def load_yaml_to_list(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        # Load the YAML content
        yaml_data = yaml.safe_load(file)

        # Extract the 'items' list
        items = yaml_data['service']['eligibility']
        return items


yaml_file_path = './src/real_estate_modeling_api/conf/config.yaml'
eligibility_criteria = load_yaml_to_list(yaml_file_path)

@router.get("/criteria/facility")
def get_eligibility_check():
    return {"eligibility_criteria": facility_eligibility_table.to_dict()}

@router.get("/criteria/land")
def get_eligibility_check():
    return {"eligibility_criteria": land_eligibility_table.to_dict()}


@router.post("/check/facility")
def get_eligibility_check(input_data: schemas.FacilityEligibilityRequest):
    eligible_categories = check_eligibility_facility(input_data)
    return {"eligible_categories": eligible_categories}

@router.post("/check/land")
def get_eligibility_check(input_data: schemas.LandEligibilityRequest):
    eligible_categories = check_eligibility_land(input_data)
    return {"eligible_categories": eligible_categories}
