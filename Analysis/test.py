import sys
sys.path.append('../')

import env

import Transfer.connectDB as connectDB
import Transfer.getData as getData

logs = connectDB.connectToCollection('logs2')
getData.getItem(logs, "SWITCH", 7,['STATE'])