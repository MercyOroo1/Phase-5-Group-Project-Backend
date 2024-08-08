from flask import Blueprint
from flask_restful import Api,Resource,reqparse


listingfee_bp=Blueprint('listingfee',__name__,url_prefix='/listingfee')
listingfee_api=Api(listingfee_bp)
