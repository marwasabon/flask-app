from flask import Blueprint, request, jsonify
from ..models.claim import Claim
from ..models.item import Item 
from ..models.match import Match
from app import db
from app.models.db_storage import DBStorage
storage = DBStorage(db)

def find_potential_matches(new_claim):
    items = Item.query.filter_by(status='Found').all()
    print(f"Items found with status 'Found': {[item.id for item in items]}")
    potential_matches = []
    
    for item in items:
        print(f"Checking item: {item.id}")
        if (item.category == new_claim.item.category and
            item.description == new_claim.item.description and
            new_claim.additional_information in item.description):
            print(f"Item {item.id} matches the claim {new_claim.id}")
            potential_matches.append(item)
        else:
            print(f"Item {item.id} does not match the claim {new_claim.id}") 
    
    for item in potential_matches:
        match = Match(
            claim_id=new_claim.id,
            item_id=item.id,
            potential_owner_user_id=item.user_id,# this part 
            status='pending'
        )
        storage.new(match)
    
    storage.save()
    
    return potential_matches

def find_potential_matches_for_lost_item(lost_item):
    found_items = Item.query.filter_by(status='Found').all()
    print(f"Found items with status 'Found': {[item.id for item in found_items]}")
    potential_matches = []
    
    for found_item in found_items:
        print(f"Checking found item: {found_item.id}")
        if (found_item.item_name == lost_item.item_name and
            found_item.item_color == lost_item.item_color and
            found_item.item_brand == lost_item.item_brand and
            lost_item.description in found_item.description):
            print(f"Found item {found_item.id} matches the lost item {lost_item.id}")
            potential_matches.append(found_item)
        else:
            print(f"Found item {found_item.id} does not match the lost item {lost_item.id}") 
    for match_item in potential_matches:
        # Create a new claim
        claim = Claim(
            item_id=lost_item.id,  # Reference to the lost item
            user_id=lost_item.user_id,
            status='direct'
        )
        storage.new(claim)
        storage.save()  # Save the claim to get the claim_id
    for match_item in potential_matches:
        match = Match(
            claim_id=claim.id,  # No claim yet, only matching lost and found items
            item_id=match_item.id,# aka found item id
            #lost_item_id=lost_item.id,  # Reference to the lost item
            potential_owner_user_id=lost_item.user_id,
            status='potential'
        )
        storage.new(match)
    
    storage.save()
    
    return potential_matches
