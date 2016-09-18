from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def make_response_from_dictionary(result):
    response = HttpResponse(json.dumps(result),content_type = 'application/jsn')
    response["Access-Control-Allow-Headers"] = "*"
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    return response

def get_symbol(company):
	from googleapiclient.discovery import build
	service = build("customsearch", "v1", developerKey = "AIzaSyDmyOuXLX02ywm93Sz2mlDIwhedbNwv8Ao")
	res = service.cse().list(q='google stock', cx='000909054054179336272:z2tjtgdflws').execute()
	for item in res["items"]:
		if "pagemap" in item:
			if "financialquote" in item["pagemap"]:
				symbol = item["pagemap"]["financialquote"][0]["tickersymbol"]
				print symbol
				return symbol
	return ""

@csrf_exempt
def generate(request):
	print "got request"
	json_data = request.body
	print json_data
	data = json.loads(json_data)
	company = data["company"]
	start = ""
	end = ""
	if "start" in data:
		start = data["start"]
	if "end" in data:
		end = data["end"]
	symbol = get_symbol(company)
	if not symbol:
		return make_response_from_dictionary({"result" : "failure"})
	result = {}
	#result["end_of_day_data"] = generate_end_of_day_data(symbol=symbol, start=start, end=end)
	#result["vwap"] = generate_vwap(symbol=symbol, start=start, end=end)
	#result["twap"] = generate_twap(symbol=symbol, start=start, end=end)
	#result["market_spread"] = generate_market_spread(symbol=symbol, start=start, end=end)
	#result["result"] = "success"
	return make_response_from_dictionary(result)	

def generate_end_of_day_data(symbol, start, end):
	filein = "end_of_day_data.py"
	if not start:
		now = datetime.now()
		prev = now - timedelta(days=1)
		start = "%d/%d/%d" % (prev.month, prev.day, prev.year)
		end  = "%d/%d/%d" % (now.month, now.day, now.year)
	f = open(filein,'r')
	filedata = f.read()
	f.close()
	newdata = filedata.replace("insert_symbol_here", symbol)
	newdata = filedata.replace("insert_start_here", start)
	newdata = filedata.replace("insert_end_here", end)
	f = open(fileout,'w')
	f.write(newdata)
	f.close()
	return filein

def generate_vwap(symbol, start, end):
	filein = "vwap.py"
	if not start:
		now = datetime.now()
		prev = now - timedelta(days=1)
		start = "%d/%d/%d 00:00:00.000" % (prev.month, prev.day, prev.year)
		end  = "%d/%d/%d 23:59:59.999" % (now.month, now.day, now.year)
	f = open(filein,'r')
	filedata = f.read()
	f.close()
	newdata = filedata.replace("insert_symbol_here", symbol)
	newdata = filedata.replace("insert_start_here", start)
	newdata = filedata.replace("insert_end_here", end)
	f = open(fileout,'w')
	f.write(newdata)
	f.close()
	return filein
