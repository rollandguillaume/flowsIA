
goParsing = True
goLearning = True

fileNameResult = "resources/FRERET_ROLLAND.txt"


# -----------DEV-ONLY----------------
# PARSER
index = "flows"
type = "flows"
tagIntType = ["destinationPort", "sourcePort", "totalDestinationBytes", "totalDestinationPackets", "totalSourceBytes", "totalSourcePackets"]
bulkSize = 50000

# VECTOR
indexVector = "vector"
indexVectorTest = "evaluationtest"
indexVectorType = "vector1"

flags = ["S","R","P","A","F","Illegal7","Illegal8"]
directions = ["L2R", "L2L", "R2L", "R2R"]
normalTag = "Normal"
maxPort = 65535