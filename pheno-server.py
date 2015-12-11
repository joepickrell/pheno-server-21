#!/usr/bin/env python3
import re, os, sys, gzip
import json
import random

from flask import Flask, render_template, jsonify, abort, make_response
from flask import request, url_for
from flask import send_from_directory


# import from the 21 Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)

#Wallet
wallet = Wallet()
payment = Payment(app, wallet)

# path to the prediction files to use
vcf_path = os.path.dirname(os.path.realpath(__file__)) + '/json'


# simple content model: dictionary of phenotypes
phenos = {}

# get a list of the files in the directory
file_list = os.listdir(vcf_path)

for f in file_list:
	tmp = f.split("/")
	tmp = tmp[len(tmp)-1]
	tmp = tmp.split(".")[0]
	infile = open(vcf_path+"/"+f)
	phenos[tmp] = json.load(infile)

# endpoint to look up VCF files to buy
@app.route('/phenos', methods=['GET'])
def file_lookup():
    return json.dumps({"phenolist": list(phenos)})


@app.route('/phenos/<pheno>', methods=['GET'])
@payment.required(1000)
def get_model(pheno):
	if pheno in list(phenos):
    		return json.dumps(phenos[pheno])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
