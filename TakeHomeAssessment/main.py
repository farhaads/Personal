import flask 
import json 
import numbers
app = flask.Flask(__name__)


#run with : "python ./main.py" in powershell terminal
#Postman test request JSON file: https://www.getpostman.com/collections/4ca9a175cbe3365aeda5

@app.errorhandler(404)
def page_not_found(error):
    return "Aborted with 404","404"


@app.route("/survivorCount/",methods=['GET','POST'])
def organiseSurvivors():
    payload = flask.request.data
    payload = json.loads(payload)
    
    #get the lower boundary of the bins
    minNumber = min(payload['binBoundaries'])
    #get the upper boundary of the bins
    maxNumber = max(payload['binBoundaries'])
    
    #initialised the bincounters to zero
    lower =  0
    middle = 0
    upper =  0

#iterating for each data object within the payload JSON array
    for datapoint in payload['data']:
        #checking if the specified binfield is an number
        if (isinstance(datapoint[payload['binField']], numbers.Number)) :
            #sorting the attributes into the specified bins
            if datapoint[payload['binField']] <= minNumber:
                lower = lower + 1 

            elif datapoint[payload['binField']] >= maxNumber:
                upper = upper + 1 

            elif datapoint[payload['binField']] > minNumber and datapoint[payload['binField']] < maxNumber:
                middle = middle + 1  
        else:
        #raise HTTPException(status_code=404, detail="not found") in event specified binfield is not a number
           flask.abort(404)
        #returns the desired output 
    return json.dumps(
        {"count": [
            lower,
            middle,
            upper
            ]
        })

if __name__ == '__main__':
    app.run(debug=True)