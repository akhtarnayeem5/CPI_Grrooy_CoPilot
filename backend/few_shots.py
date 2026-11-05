#backend/few_shots.py

FEW_SHOTS = [
    {
        "input": "Write a Groovy script to read a CSV file and print the contents.",
        "output": """import groovy.csv.CsvParser
def csvFile = new File('data.csv')
def parser = new CsvParser()
csvFile.withReader { reader ->
    def rows = parser.parse(reader)
    rows.each { row ->
        println row
    }
}"""
    },
    {
        "input": "Read an incoming JSON payload, extract the customer ID, and save it in a message property.",
        "output": """import groovy.json.JsonSlurper
def jsonPayload = '{"customerId": "12345", "name": "John Doe"}
def slurper = new JsonSlurper()
def parsedJson = slurper.parseText(jsonPayload)
def customerId = parsedJson.customerId
def message = new Message()
message.setProperty("customerId", customerId)"""    
}
]