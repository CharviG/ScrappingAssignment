# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 10:23:04 2021

@author: Charvi.Gaur
"""

import scrapData as sd
from flask import Flask, abort
from flask_restplus import Resource, Api, fields

with open('VERSION') as f:
    __version__ = f.read()

app = Flask(__name__)
api = Api(
    app, version=__version__, title='',
    description='An interface to scrap data',
)

model_scrapdata = api.model('Scrap data from drt.gov.in', {
    'drt': fields.String(required=True),
    'party': fields.String(required=True)
})

ns_ld = api.namespace('drtdrat', description='DRT/DRAT Case Status Report')

@ns_ld.route('/scrap_data')
class ScrapData(Resource):
    @ns_ld.expect(model_scrapdata, validate=True)
    def post(self):
        drt = api.payload['drt']
        party = api.payload['party']
        obj = sd.DRTData(drt, party)
        return obj.scrapData()
    
if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        threaded=True)