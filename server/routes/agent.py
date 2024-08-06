from flask_restful import Resource,Api,reqparse
from flask import Flask,Blueprint
from flask_cors import CORS
from models import db ,Agent, AgentApplication,User
from flask_jwt_extended import jwt_required, get_jwt_identity


agent_bp=Blueprint('agent',__name__,url_prefix='/agents')
agent_api=Api(agent_bp)
CORS(agent_bp)
agent_parser=reqparse.RequestParser()
agent_parser.add_argument('license_number',type=str,required=True, help='License number cannot be blank')
agent_parser.add_argument('full_name',type=str,required=True, help='Full name cannot be blank')
agent_parser.add_argument('email',type=str,required=True, help='Email cannot be blank')
agent_parser.add_argument('experience',type=str,required=True, help='Experience cannot be blank')
agent_parser.add_argument('phone_number',type=str,required=True, help='Phone number cannot be blank')
agent_parser.add_argument('for_sale',type=int,required=True, help='For sale cannot be blank')
agent_parser.add_argument('sold',type=int,required=True, help='Sold cannot be blank')
agent_parser.add_argument('languages',type=str,required=True, help='Languages cannot be blank')
agent_parser.add_argument('agency_name',type=str,required=True, help='Agency name cannot be blank')
agent_parser.add_argument('listed_properties',type=str,required=True, help='Listed properties cannot be blank')
agent_parser.add_argument('photo_url',type=str, help='photo url is optional')



class AgentResource(Resource):
    # get all agents by the user
    def get(self, id):
        agent=Agent.query.get_or_404(id)
        return {'id':agent.id, 'licence_number':agent.license_number,'full_name':agent.full_name,'email':agent.email,'experience':agent.experience,'phone_number':agent.phone_number,'for_sale':agent.for_sale,'sold':agent.sold,'languages':agent.languages,'agency_name':agent.agency_name,'listed_properties':agent.listed_properties,'photo_url':agent.photo_url}
    # an agent can edit his or her info
    def put(self, id):
        agent=Agent.query.get_or_404(id)
        data=agent_parser.parse_args()
        agent.license_number=data['license_number']
        agent.full_name=data['full_name']
        agent.email=data['email']
        agent.experience=data['experience']
        agent.phone_number=data['phone_number']
        agent.for_sale=data['for_sale']
        agent.sold=data['sold']
        agent.languages=data['languages']
        agent.agency_name=data['agency_name']
        agent.listed_properties=data['listed_properties']
        if 'photo_url' in data:
            agent.photo_url=data['photo_url']
        db.session.commit()
        return {'id':agent.id, 'license_number':agent.license_number,'full_name':agent.full_name,'email':agent.email,'experience':agent.experience,'phone_number':agent.phone_number,'for_sale':agent.for_sale,'sold':agent.sold,"languages":agent.languages,'listed_properties':agent.listed_properties,'photo_url':agent.photo_url}
    # an agent can delete his own account
    def delete(self,id):
      agent=Agent.query.get_or_404(id)
      db.session.delete(agent)
      db.session.commit()
      return {'message':'Agent deleted'}

agent_api.add_resource(AgentResource,'<int:id>')

class AgentResourceList(Resource):
    def get(self):
        agents=Agent.query.all()
        return [{'id':agent.id, 'license_number':agent.license_number,'full_name':agent.full_name,'email':agent.email,'experience':agent.experience,'phone_number':agent.phone_number,'for_sale':agent.for_sale,'sold':agent.sold,'languages':agent.languages,'agency_name':agent.agency_name,'listed_properties':agent.listed_properties,'photo_url':agent.photo_url} for agent in agents]
    # agent application 
    def post(self):
        data=agent_parser.parse_args()
        agent=Agent(license_number=data['license_number'],full_name=data['full_name'],email=data['email'],experience=data['experience'],phone_number=data['phone_number'],for_sale=data['for_sale'],sold=data['sold'],languages=data['languages'],agency_name=data['agency_name'],listed_properties=data['listed_properties'],photo_url=data['photo_url'])
        db.session.add(agent)
        db.session.commit()
        return {"message": "agent added successfully"}
    





agent_api.add_resource(AgentResourceList,'/list')

class PropertiesAgentResource(Resource):
    def get(self, id):
        agent=Agent.query.get_or_404(id)
        properties=agent.properties
        return [{'id': property.id, 'property': property.address,'city':property.city ,'square_footage':property.square_footage,'price':property.price,'property_type': property.property_type,'listing_status':property.listing_status,'rooms':property.rooms}for property in properties]
        
    


agent_api.add_resource(PropertiesAgentResource,'/<int:id>/properties')

